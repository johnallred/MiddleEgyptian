"""
Unify entry identifier schema in Entries2.json.

44,658 entries use the MongoDB extended-JSON _id form:
    "_id": {"$oid": "628573728383418c993ae446"}

834 entries (the Faulkner per-page scrapes that became new entries
during the medium-effort merge) instead carry:
    "Id": {"Timestamp": 1613535769, "Machine": 16648859,
           "Pid": 19577, "Increment": 8112726,
           "CreationTime": "/Date(1613535769000)/"}

The Faulkner field names match the legacy MongoDB ObjectId byte layout
exactly:
    timestamp  4 bytes  (seconds since epoch)
    machine    3 bytes  (max 0xFFFFFF)
    pid        2 bytes  (max 0xFFFF)
    increment  3 bytes  (max 0xFFFFFF)
    --------
    total     12 bytes  ->  24 hex chars

So we can losslessly reconstruct an ObjectId from each Faulkner Id and
replace it with an _id: {$oid: "..."} object. CreationTime is redundant
with Timestamp; it gets dropped.

The script is idempotent: re-running on a file that's already unified
is a no-op.
"""

import json
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


def faulkner_id_to_oid(faulkner_id: dict) -> str:
    """
    Encode {Timestamp, Machine, Pid, Increment} as a 24-char hex ObjectId.
    """
    ts = int(faulkner_id["Timestamp"])
    machine = int(faulkner_id["Machine"])
    pid = int(faulkner_id["Pid"])
    inc = int(faulkner_id["Increment"])

    # Sanity-check the byte budgets
    if not (0 <= ts < 2**32):
        raise ValueError(f"Timestamp out of range: {ts}")
    if not (0 <= machine < 2**24):
        raise ValueError(f"Machine out of range: {machine}")
    if not (0 <= pid < 2**16):
        raise ValueError(f"Pid out of range: {pid}")
    if not (0 <= inc < 2**24):
        raise ValueError(f"Increment out of range: {inc}")

    raw = (
        ts.to_bytes(4, "big")
        + machine.to_bytes(3, "big")
        + pid.to_bytes(2, "big")
        + inc.to_bytes(3, "big")
    )
    return raw.hex()


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    converted = 0
    skipped = 0
    samples = []

    for e in entries:
        has_id = "_id" in e and e["_id"] is not None
        has_faulkner = "Id" in e and isinstance(e["Id"], dict)
        if has_id and not has_faulkner:
            continue                            # already unified
        if has_faulkner:
            try:
                oid = faulkner_id_to_oid(e["Id"])
            except (KeyError, ValueError, TypeError) as exc:
                skipped += 1
                print(f"  skipped (bad Faulkner Id): {exc}")
                continue
            new_id = {"$oid": oid}
            if not has_id:
                e["_id"] = new_id
            # In the very rare case where BOTH exist, leave _id alone
            # (the Mongo one is authoritative) and just drop Id.
            old_id = e.pop("Id")
            converted += 1
            if len(samples) < 4:
                samples.append((old_id, new_id))

    # Verify final state
    no_id = sum(1 for e in entries if "_id" not in e or e["_id"] is None)
    has_faulkner_leftover = sum(1 for e in entries if "Id" in e)

    print(f"\nConverted Faulkner Id -> _id : {converted:,}")
    print(f"Skipped (bad data)            : {skipped}")
    print(f"Entries still missing _id     : {no_id}  (should be 0)")
    print(f"Entries still carrying Id     : {has_faulkner_leftover}  (should be 0)")

    print("\nSample conversions:")
    for old, new in samples:
        print(f"  Faulkner Id: {old}")
        print(f"  -> _id     : {new}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
