"""
Generate RES (Revised Encoding Scheme) strings from Manuel de Codage.

Port of MiddleEgyptianDataset/MiddleEgyptianDictionary/Services/
ManuelDeCodageToRESConverter.cs into Python.

The C# converter is a substring-replacement table plus a small regex post-
processor; there is no actual parser. We replicate it faithfully:

  1. Iterate SUBSTITUTIONS in their original order (Python dict iteration
     is insertion-ordered, matching C#'s Dictionary behavior).
  2. For each (key, value) pair, do str.replace(key, value) on the
     accumulating result.
  3. Replace '&' (MdC compound joiner) with ':' (RES vertical stack).
  4. Lowercase trailing letter suffixes: Y1A -> Y1a, Aa15B -> Aa15b.

Then for every entry in Entries2.json:

  * Add `ResAuto` with the converter output (so curated vs auto can be
    compared).
  * Add `ResSource = "curated"` if Res was already non-null, otherwise
    `"auto"` and copy ResAuto into Res so the field is populated.

Validation: before writing, we run the converter on every entry that
already has a curated Res value and report the exact-match rate. If the
port is faithful, this should be very high; mismatches are dumped in
groups so any bug in the port jumps out.
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# Substitution table — ported VERBATIM from
# ManuelDeCodageToRESConverter.cs, preserving insertion order so that the
# substring-replacement semantics match the C# implementation exactly.
# ---------------------------------------------------------------------------

SUBSTITUTIONS: dict[str, str] = {
    # --- Manuel de Codage tokens needing direct translation ---
    "D153": "D26",
    "O38A": "O38[mirror]",
    "R8A": "R8*[sep=0,fix]R8*[sep=0,fix]R8",
    "S56": "S7",
    "S14B": "S14b",
    "U6A": "U6a",
    "U6B": "U6b",
    "V30A": "V30a",
    "V40A": "V40a",
    "W3A": "W3a",
    "W14A": "W14a",
    "W24A": "W24a",
    "T26F": "T26",
    "T26H": "T26",
    "A51&X1": "insert[b,sep=0.2](A51,X1)",
    "Y1V": "Y1a",

    # --- Vygus errors (undisplayable Vygus characters) ---
    "A33B": "A33",
    "A95": "A15",
    "A21A": "A21",
    "A34A": "A34",
    "A36C": "A37",
    "A4B": "A4",
    "A4C": "A4",
    "A43B": "A41",
    "A299B": "A41",
    "A40B": "A42",
    "A59B": "A59",
    "A133A": "A6",
    "N90": "D12",
    "Y24": "D12",
    "D26A": "D26",
    "D210": "D36",
    "D46D": "D46",
    "E102B": "E4",
    "F16A": "F16[mirror]",
    "F37D": "F37a",
    "F37E": "F37a",
    "F37AA": "F37a",
    "F37B": "F37a",
    "F37F": "F37a",
    "F37J": "F37a",
    "F39A": "F39",
    "F51D": "F51",
    "F51F": "F51",
    "G22A": "G22",
    "G29A": "G29",
    "G49E": "G49",
    "G237": "G49",
    "G167": "G50",
    "G7C": "G7",
    "H6B": "H6[rotate=330]",
    "I14A": "I14",
    "I14B": "I14",
    "I14C": "I14",
    "O202": "M13",
    "O353": "M13",
    "M4B": "M4",
    "M7A": "M7",
    "N11A": "N11[rotate=90]",
    "N62A": "N12[rotate=180]",
    "N21A": "N21[mirror]",
    "N24E": "N24",
    "S106": "N37",
    "N8A": "N8",
    "O29V": "O29[rotate=90]",
    "O30U": "O30[rotate=180]",
    "O40A": "O40",
    "O48A": "O48",
    "P4A": "P4",
    "P30": "P4",
    "P34": "P4",
    "P36": "P4",
    "Q12A": "Q2",
    "R1E": "R1",
    "R10B": "R10",
    "R15A": "R15",
    "R3C": "R3",
    "R3P": "R3",
    "S15A": "S15",
    "S116": "S27:S27",
    "G56": "stack(A,a)",
    "G57": "stack(A,f)",
    "V71": "stack(a,H)",
    "G58": "stack(Aa15,A)",
    "M145": "stack(Aa15,i)",
    "I34": "stack(b,D)",
    "D170A": "stack(D28,D52)",
    "D189": "stack(D32, W24)",
    "V41": "stack(D37,Z7)",
    "G225": "stack(G29,U7)",
    "V81": "stack(k,H)",
    "V90": "stack(k,V29)",
    "G87": "stack(m,D40)",
    "M159": "stack(M23, a)",
    "O91": "stack(O6, a)",
    "O90": "stack(O6, O29)",
    "R78": "stack(R15, a)",
    "T69": "stack(T14, a)",
    "T29C": "stack(T28, T30)",
    "U1A": "stack(U1,i)",
    "T14C": "T14[mirror]",
    "T19B": "T19",
    "T79": "T19",
    "T21V": "T21[rotate=270]",
    "T24E": "T24[mirror]",
    "T30A": "T30",
    "T30B": "T30A",
    "S123": "T32A",
    "S126": "T32A",
    "T9C": "T9",
    "U19A": "U19",
    "U32B": "U32",
    "U39Q": "U39",
    "U39L": "U40",
    "U7A": "U8",
    "S89": "V1",
    "V36G": "V36",
    "V5A": "V5[rotate=330]",
    "W15B": "W15",
    "W21A": "W21",
    "X3A": "X3",
    "Y2V": "Y1A",
    "Y8A": "Y8",
    "Z11A": "Z11",

    # --- Number expansions ---
    "Z15A": "Z1*Z1",
    "Z15B": "Z1*Z1*Z1",
    "Z15C": "Z1*Z1*Z1*Z1",
    "Z15I": ".*[sep=0]Z1*Z1*[sep=0].:Z1*Z1*Z1",
    "Z15": "Z1",
    "V20I": "V20*V20",
    "V20J": "V20*V20*V20",
    "V20K": "V20*V20*V20*V20",
    "V20L": ".*[sep=0]V20*V20*[sep=0].:V20*V20*V20",
    "100": "V1",
    "V1A": "V1*V1",
    "V1B": "V1*V1*V1",
    "V1C": "V1*V1*V1*V1",
    "V1I": ".*[sep = 0]V1*V1*[sep=0].:V1*V1*V1",
    "1000": "M12",
    "D50A": "D50*[fix,sep=0.2]D50",
    "D50B": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50",
    "D50C": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50",
    "D50D": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50:[fix,sep=0.2].*[sep=0]D50*[fix,sep=0.2]D50*[sep=0].",
    "D50E": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50:[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50",
    "D50F": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50:[fix,sep=0.2,size=inf].*[sep=0.2] D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[sep=0.2].",
    "D50G": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50:[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50",
    "D50H": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50:[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50:[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50",
    "D50I": "D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50*[fix,sep=0.2]D50",
    "D67A": "D67:[fix,sep=0.3]D67",
    "D67B": "D67*[fix,sep=0.3]D67:[fit,fix,sep=0.3]D67",
    "D67C": "D67*[fix,sep=0.3]D67:[fix,sep=0.3]D67*[fix,sep=0.3]D67",
    "D67D": "D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67:[fit,fix,sep=0.3]D67*[fix,sep=0.3]D67",
    "D67E": "D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67:[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67",
    "D67F": "D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67:[fit,fix,sep=0.3,size=inf]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67",
    "D67G": "D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67:[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67",
    "D67H": "D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67:[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67:[fix,sep=0.3]D67*[fix,sep=0.3]D67*[fix,sep=0.3]D67",
    "F51A": "F51*[fit,fix,sep=0.2]F51*[fit,fix,sep=0.2]F51",
    "F51B": "F51:[fit,fix,sep=0.2]F51:[fit,fix,sep=0.2]F51",
    "M12A": "M12:[fix,sep=0.3]M12",
    "M12B": "M12*[fix,sep=0.3]M12:[fit,fix,sep=0.3]M12",
    "M12C": "M12*[fix,sep=0.3]M12:[fix,sep=0.3]M12*[fix,sep=0.3]M12",
    "M12D": "M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12:[fit,fix,sep=0.3]M12*[fix,sep=0.3]M12",
    "M12E": "M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12:[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12",
    "M12F": "M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12:[fit,fix,sep=0.3,size=inf]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12",
    "M12G": "M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12:[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12",
    "M12H": "M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12:[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12:[fix,sep=0.3]M12*[fix,sep=0.3]M12*[fix,sep=0.3]M12",
    "N33A": "N33*[sep=0.5]N33*[sep=0.5] N33",
    "A14&Z2": "insert[bs,sep=0.5](A14,Z1*[sep=1.5]Z1*[sep=1.5]Z1)",
    "A17&Z2": "insert[be](A17*[sep=0.0]empty[width=0.2,height=0.0],Z1*Z1*Z1)",
    "A24&Z2D": "insert[te,sep=0.5](A24*[sep=0.0]empty[width=0.3],Z1*[sep=0.5]Z1*[sep=0.5]Z1)",
    "Z2A": "Z1*Z1*Z1",
    "Z2B": "D67*[sep=0.5]D67*[sep=0.5]D67",
    "Z2C": "Z1:[fix,sep=0.3]Z1*[sep=2.0]Z1",
    "Z2D": "Z1*[sep=2.0]Z1:[fix,sep=0.3]Z1",
    "Z2": "Z1*[sep=2.0]Z1*[sep=2.0]Z1",
    "Z3A": "Z1[rotate=90]:Z1[rotate=90]:Z1[rotate=90]",
    "Z3B": "D67:D67:D67",
    "Z3": "Z1:[sep=0.3]Z1:[sep=0.3]Z1",
    "Z4A": "Z1*[sep=2]Z1",
    "Z4B": "Z1[rotate=90]:Z1[rotate=90]",
}


# ---------------------------------------------------------------------------
# Converter
# ---------------------------------------------------------------------------

_POSTFIX_RX = re.compile(r"((?:[A-Z]|Aa|AA)[0-9]+)([A-Za-z]+)")


def _postfix_lowercase(s: str) -> str:
    """Y1A -> Y1a, Aa15B -> Aa15b (match C# PostFixLetterToLower)."""
    return _POSTFIX_RX.sub(lambda m: m.group(1) + m.group(2).lower(), s)


def mdc_to_res(mdc: str) -> str:
    """Convert a Manuel de Codage string to a RES string."""
    if not mdc:
        return mdc
    result = mdc
    for key, value in SUBSTITUTIONS.items():
        if key in result:
            result = result.replace(key, value)
    result = result.replace("&", ":")
    return _postfix_lowercase(result)


# ---------------------------------------------------------------------------
# Main: validate + fill
# ---------------------------------------------------------------------------

def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # ===== Validation pass: compare converter output to existing curated Res =====
    total_with_curated = 0
    exact_matches = 0
    mismatches: list[tuple[str, str, str]] = []  # (mdc, curated, auto)
    for e in entries:
        mdc = e.get("ManuelDeCodage")
        res = e.get("Res")
        if not mdc or not res:
            continue
        total_with_curated += 1
        auto = mdc_to_res(mdc)
        if auto == res:
            exact_matches += 1
        else:
            mismatches.append((mdc, res, auto))

    print("\n=== Validation against existing curated Res ===")
    print(f"Entries with curated Res         : {total_with_curated:,}")
    print(f"Exact matches with converter     : {exact_matches:,}  "
          f"({100*exact_matches/total_with_curated:.1f}%)")
    print(f"Mismatches                       : {len(mismatches):,}")

    # Classify mismatches: where does the converter disagree?
    diff_kinds = Counter()
    for mdc, cur, auto in mismatches[:1000]:
        # Some structured signals: did one have brackets the other lacked?
        if "[" in auto and "[" not in cur:
            diff_kinds["converter_adds_brackets"] += 1
        elif "[" in cur and "[" not in auto:
            diff_kinds["curated_has_brackets"] += 1
        elif "stack(" in auto and "stack(" not in cur:
            diff_kinds["converter_uses_stack"] += 1
        elif "stack(" in cur and "stack(" not in auto:
            diff_kinds["curated_uses_stack"] += 1
        elif "*" in auto and "*" not in cur:
            diff_kinds["converter_adds_star"] += 1
        elif "*" in cur and "*" not in auto:
            diff_kinds["curated_uses_star"] += 1
        else:
            diff_kinds["other"] += 1
    print("\nMismatch breakdown (first 1000):")
    for kind, n in diff_kinds.most_common():
        print(f"  {n:5}  {kind}")

    print("\nSample mismatches (10):")
    for mdc, cur, auto in mismatches[:10]:
        print(f"  MdC    : {mdc!r}")
        print(f"  Curated: {cur!r}")
        print(f"  Auto   : {auto!r}\n")

    # ===== Fill pass =====
    print("=== Filling pass ===")
    filled = 0
    res_auto_added = 0
    for e in entries:
        mdc = e.get("ManuelDeCodage")
        if not mdc:
            continue
        auto = mdc_to_res(mdc)
        e["ResAuto"] = auto
        res_auto_added += 1
        if not e.get("Res"):
            e["Res"] = auto
            e["ResSource"] = "auto"
            filled += 1
        else:
            e["ResSource"] = "curated"

    print(f"ResAuto added to                 : {res_auto_added:,} entries")
    print(f"Res filled from null              : {filled:,}")
    res_curated = sum(1 for e in entries if e.get("ResSource") == "curated")
    res_auto = sum(1 for e in entries if e.get("ResSource") == "auto")
    print(f"Final ResSource = curated         : {res_curated:,}")
    print(f"Final ResSource = auto            : {res_auto:,}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
