﻿$(document).ready(function () {
    $('.select2').hide();
    $('.select2').children().hide();
    var outData = getOutData();
    $('.js-example-basic-multiple').select2({

        data: outData,
        placeholder: "Id, [translit.], [narrow], [broad], [tall]",
        width: "60%",
        multiple: true,
        escapeMarkup: function (markup) {
            return markup;
        },
        templateResult: function (data) {
            return data.html;
        },
        templateSelection: function (data) {
            return data.display;
        },
        allowDuplicates: true,
        sortSelectedBySelectionTime: true
    });
    $('.select2').hide();
    $('.select2').children().hide();
});

function SelectClick1() {
    $('.js-example-basic-multiple').on('change', function (e) {
        var data = e;
        console.log(e);
    });
}

function SelectClick() {
    $(".js-example-basic-multiple").on('select2:select select2:unselect', function (e) {
        var data = $('.js-example-basic-multiple').select2('data');
        data = data.sort((a, b) => a.timeStamp - b.timeStamp);
        var signQuery = [];
        data.forEach(function (item) {
            signQuery.push(item.display);
        });
        var text = signQuery.join(' ');
        $("#SignQuery").val(text);
    });
}

function ChangeTextbox(x) {
    switch (x) {
        // Switch to the Gardiner Ids tab, swap out textbox for tagged one
        case 1:
            $("#regular-input").hide();
            $('.select2').show();
            $('.select2').children().show();
            break;
        // Switch to another tab, use regular input box.
        case 0:
            $('.select2').hide();
            $('.select2').children().hide();
            $("#regular-input").show();
            break;
    }
}

function UpdateValues() {
    if ($("#exactmatchcheck").is(':checked')) {
        $("#exactmatch").prop("checked", true);
        $("#exactmatch").val(true);
        $("#exactmatch").prop("active", true)
    } else {
        $("#exactmatch").prop("checked", false);
        $("#exactmatch").val(false);
        $("#exactmatch").prop("active", false)
    }

    if ($("#formattingcheck").is(':checked')) {
        $("#formatting").prop("checked", true);
        $("#formatting").prop("active", true);
        $("#formatting").val(true);
    } else {
        $("#formatting").prop("checked", false);
        $("#formatting").prop("active", false);
        $("#formatting").val(false);
    }
}

function getOutData() {
    return [
        {
            "id": "A1",
            "text": "A1: seated man",
            "html": "<span class=\"uni\">&#x13000;</span> A1: seated man",
            "display": "A1"
        },
        {
            "id": "A10",
            "text": "A10: seated man holding oar",
            "html": "<span class=\"uni\">&#x1300C;</span> A10: seated man holding oar",
            "display": "A10"
        },
        {
            "id": "A100",
            "text": "A100",
            "html": "<img src=\"/Search/Image?key=A100\" alt=\"A100\" style=\"max-height:24px; max-width: 28px;\" /> A100",
            "display": "A100"
        },
        {
            "id": "A103",
            "text": "A103",
            "html": "<img src=\"/Search/Image?key=A103\" alt=\"A103\" style=\"max-height:24px; max-width: 28px;\" /> A103",
            "display": "A103"
        },
        {
            "id": "A104",
            "text": "A104",
            "html": "<img src=\"/Search/Image?key=A104\" alt=\"A104\" style=\"max-height:24px; max-width: 28px;\" /> A104",
            "display": "A104"
        },
        {
            "id": "A108",
            "text": "A108",
            "html": "<img src=\"/Search/Image?key=A108\" alt=\"A108\" style=\"max-height:24px; max-width: 28px;\" /> A108",
            "display": "A108"
        },
        {
            "id": "A10a",
            "text": "A10A: seated man holding oar",
            "html": "<img src=\"/Search/Image?key=A10A\" alt=\"A10A\" style=\"max-height:24px; max-width: 28px;\" /> A10A: seated man holding oar",
            "display": "A10a"
        },
        {
            "id": "A113",
            "text": "A113",
            "html": "<img src=\"/Search/Image?key=A113\" alt=\"A113\" style=\"max-height:24px; max-width: 28px;\" /> A113",
            "display": "A113"
        },
        {
            "id": "A115",
            "text": "A115",
            "html": "<img src=\"/Search/Image?key=A115\" alt=\"A115\" style=\"max-height:24px; max-width: 28px;\" /> A115",
            "display": "A115"
        },
        {
            "id": "A116",
            "text": "A116",
            "html": "<img src=\"/Search/Image?key=A116\" alt=\"A116\" style=\"max-height:24px; max-width: 28px;\" /> A116",
            "display": "A116"
        },
        {
            "id": "A116b",
            "text": "A116B",
            "html": "<img src=\"/Search/Image?key=A116B\" alt=\"A116B\" style=\"max-height:24px; max-width: 28px;\" /> A116B",
            "display": "A116b"
        },
        {
            "id": "A117a",
            "text": "A117A",
            "html": "<img src=\"/Search/Image?key=A117A\" alt=\"A117A\" style=\"max-height:24px; max-width: 28px;\" /> A117A",
            "display": "A117a"
        },
        {
            "id": "A119",
            "text": "A119",
            "html": "<img src=\"/Search/Image?key=A119\" alt=\"A119\" style=\"max-height:24px; max-width: 28px;\" /> A119",
            "display": "A119"
        },
        {
            "id": "A12",
            "text": "A12: soldier with bow and quiver [mSa]",
            "html": "<span class=\"uni\">&#x1300E;</span> A12: soldier with bow and quiver",
            "display": "A12"
        },
        {
            "id": "A121",
            "text": "A121",
            "html": "<img src=\"/Search/Image?key=A121\" alt=\"A121\" style=\"max-height:24px; max-width: 28px;\" /> A121",
            "display": "A121"
        },
        {
            "id": "A121c",
            "text": "A121C",
            "html": "<img src=\"/Search/Image?key=A121C\" alt=\"A121C\" style=\"max-height:24px; max-width: 28px;\" /> A121C",
            "display": "A121c"
        },
        {
            "id": "A125",
            "text": "A125",
            "html": "<img src=\"/Search/Image?key=A125\" alt=\"A125\" style=\"max-height:24px; max-width: 28px;\" /> A125",
            "display": "A125"
        },
        {
            "id": "A13",
            "text": "A13: man with arms tied behind his back",
            "html": "<span class=\"uni\">&#x1300F;</span> A13: man with arms tied behind his back",
            "display": "A13"
        },
        {
            "id": "A131a",
            "text": "A131A",
            "html": "<img src=\"/Search/Image?key=A131A\" alt=\"A131A\" style=\"max-height:24px; max-width: 28px;\" /> A131A",
            "display": "A131a"
        },
        {
            "id": "A133a",
            "text": "A133A",
            "html": "<img src=\"/Search/Image?key=A133A\" alt=\"A133A\" style=\"max-height:24px; max-width: 28px;\" /> A133A",
            "display": "A133a"
        },
        {
            "id": "A135",
            "text": "A135",
            "html": "<img src=\"/Search/Image?key=A135\" alt=\"A135\" style=\"max-height:24px; max-width: 28px;\" /> A135",
            "display": "A135"
        },
        {
            "id": "A135c",
            "text": "A135C",
            "html": "<img src=\"/Search/Image?key=A135C\" alt=\"A135C\" style=\"max-height:24px; max-width: 28px;\" /> A135C",
            "display": "A135c"
        },
        {
            "id": "A137",
            "text": "A137",
            "html": "<img src=\"/Search/Image?key=A137\" alt=\"A137\" style=\"max-height:24px; max-width: 28px;\" /> A137",
            "display": "A137"
        },
        {
            "id": "A139a",
            "text": "A139A",
            "html": "<img src=\"/Search/Image?key=A139A\" alt=\"A139A\" style=\"max-height:24px; max-width: 28px;\" /> A139A",
            "display": "A139a"
        },
        {
            "id": "A13a",
            "text": "A13A: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13A\" alt=\"A13A\" style=\"max-height:24px; max-width: 28px;\" /> A13A: man with arms tied behind his back",
            "display": "A13a"
        },
        {
            "id": "A13b",
            "text": "A13B: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13B\" alt=\"A13B\" style=\"max-height:24px; max-width: 28px;\" /> A13B: man with arms tied behind his back",
            "display": "A13b"
        },
        {
            "id": "A13c",
            "text": "A13C: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13C\" alt=\"A13C\" style=\"max-height:24px; max-width: 28px;\" /> A13C: man with arms tied behind his back",
            "display": "A13c"
        },
        {
            "id": "A13d",
            "text": "A13D: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13D\" alt=\"A13D\" style=\"max-height:24px; max-width: 28px;\" /> A13D: man with arms tied behind his back",
            "display": "A13d"
        },
        {
            "id": "A13e",
            "text": "A13E: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13E\" alt=\"A13E\" style=\"max-height:24px; max-width: 28px;\" /> A13E: man with arms tied behind his back",
            "display": "A13e"
        },
        {
            "id": "A13g",
            "text": "A13G: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13G\" alt=\"A13G\" style=\"max-height:24px; max-width: 28px;\" /> A13G: man with arms tied behind his back",
            "display": "A13g"
        },
        {
            "id": "A13n",
            "text": "A13N: man with arms tied behind his back",
            "html": "<img src=\"/Search/Image?key=A13N\" alt=\"A13N\" style=\"max-height:24px; max-width: 28px;\" /> A13N: man with arms tied behind his back",
            "display": "A13n"
        },
        {
            "id": "A14",
            "text": "A14: falling man with blood streaming from his head",
            "html": "<span class=\"uni\">&#x13010;</span> A14: falling man with blood streaming from his head",
            "display": "A14"
        },
        {
            "id": "A141",
            "text": "A141",
            "html": "<img src=\"/Search/Image?key=A141\" alt=\"A141\" style=\"max-height:24px; max-width: 28px;\" /> A141",
            "display": "A141"
        },
        {
            "id": "A143a",
            "text": "A143A",
            "html": "<img src=\"/Search/Image?key=A143A\" alt=\"A143A\" style=\"max-height:24px; max-width: 28px;\" /> A143A",
            "display": "A143a"
        },
        {
            "id": "A148",
            "text": "A148",
            "html": "<img src=\"/Search/Image?key=A148\" alt=\"A148\" style=\"max-height:24px; max-width: 28px;\" /> A148",
            "display": "A148"
        },
        {
            "id": "A14a",
            "text": "A14A: man whose head is hit with an axe",
            "html": "<span class=\"uni\">&#x13011;</span> A14A: man whose head is hit with an axe",
            "display": "A14a"
        },
        {
            "id": "A14b",
            "text": "A14B: falling man with blood streaming from his head",
            "html": "<img src=\"/Search/Image?key=A14B\" alt=\"A14B\" style=\"max-height:24px; max-width: 28px;\" /> A14B: falling man with blood streaming from his head",
            "display": "A14b"
        },
        {
            "id": "A14c",
            "text": "A14C: falling man with blood streaming from his head",
            "html": "<img src=\"/Search/Image?key=A14C\" alt=\"A14C\" style=\"max-height:24px; max-width: 28px;\" /> A14C: falling man with blood streaming from his head",
            "display": "A14c"
        },
        {
            "id": "A14d",
            "text": "A14D: falling man with blood streaming from his head",
            "html": "<img src=\"/Search/Image?key=A14D\" alt=\"A14D\" style=\"max-height:24px; max-width: 28px;\" /> A14D: falling man with blood streaming from his head",
            "display": "A14d"
        },
        {
            "id": "A14e",
            "text": "A14E: falling man with blood streaming from his head",
            "html": "<img src=\"/Search/Image?key=A14E\" alt=\"A14E\" style=\"max-height:24px; max-width: 28px;\" /> A14E: falling man with blood streaming from his head",
            "display": "A14e"
        },
        {
            "id": "A14g",
            "text": "A14G: falling man with blood streaming from his head",
            "html": "<img src=\"/Search/Image?key=A14G\" alt=\"A14G\" style=\"max-height:24px; max-width: 28px;\" /> A14G: falling man with blood streaming from his head",
            "display": "A14g"
        },
        {
            "id": "A15",
            "text": "A15: man falling [xr]",
            "html": "<span class=\"uni\">&#x13012;</span> A15: man falling",
            "display": "A15"
        },
        {
            "id": "A150",
            "text": "A150",
            "html": "<img src=\"/Search/Image?key=A150\" alt=\"A150\" style=\"max-height:24px; max-width: 28px;\" /> A150",
            "display": "A150"
        },
        {
            "id": "A153",
            "text": "A153",
            "html": "<img src=\"/Search/Image?key=A153\" alt=\"A153\" style=\"max-height:24px; max-width: 28px;\" /> A153",
            "display": "A153"
        },
        {
            "id": "A158",
            "text": "A158",
            "html": "<img src=\"/Search/Image?key=A158\" alt=\"A158\" style=\"max-height:24px; max-width: 28px;\" /> A158",
            "display": "A158"
        },
        {
            "id": "A15a",
            "text": "A15A: man falling",
            "html": "<img src=\"/Search/Image?key=A15A\" alt=\"A15A\" style=\"max-height:24px; max-width: 28px;\" /> A15A: man falling",
            "display": "A15a"
        },
        {
            "id": "A16",
            "text": "A16: man bowing down",
            "html": "<span class=\"uni\">&#x13013;</span> A16: man bowing down",
            "display": "A16"
        },
        {
            "id": "A166",
            "text": "A166",
            "html": "<img src=\"/Search/Image?key=A166\" alt=\"A166\" style=\"max-height:24px; max-width: 28px;\" /> A166",
            "display": "A166"
        },
        {
            "id": "A16a",
            "text": "A16A: man bowing down",
            "html": "<img src=\"/Search/Image?key=A16A\" alt=\"A16A\" style=\"max-height:24px; max-width: 28px;\" /> A16A: man bowing down",
            "display": "A16a"
        },
        {
            "id": "A17",
            "text": "A17: child sitting with hand to mouth [Xrd]",
            "html": "<span class=\"uni\">&#x13014;</span> A17: child sitting with hand to mouth",
            "display": "A17"
        },
        {
            "id": "A17a",
            "text": "A17A: child sitting with arms hanging down",
            "html": "<span class=\"uni\">&#x13015;</span> A17A: child sitting with arms hanging down",
            "display": "A17a"
        },
        {
            "id": "A17b",
            "text": "A17B: child sitting with hand to mouth",
            "html": "<img src=\"/Search/Image?key=A17B\" alt=\"A17B\" style=\"max-height:24px; max-width: 28px;\" /> A17B: child sitting with hand to mouth",
            "display": "A17b"
        },
        {
            "id": "A17d",
            "text": "A17D: child sitting with hand to mouth",
            "html": "<img src=\"/Search/Image?key=A17D\" alt=\"A17D\" style=\"max-height:24px; max-width: 28px;\" /> A17D: child sitting with hand to mouth",
            "display": "A17d"
        },
        {
            "id": "A18",
            "text": "A18: child wearing S3",
            "html": "<span class=\"uni\">&#x13016;</span> A18: child wearing S3",
            "display": "A18"
        },
        {
            "id": "A184",
            "text": "A184",
            "html": "<img src=\"/Search/Image?key=A184\" alt=\"A184\" style=\"max-height:24px; max-width: 28px;\" /> A184",
            "display": "A184"
        },
        {
            "id": "A189",
            "text": "A189",
            "html": "<img src=\"/Search/Image?key=A189\" alt=\"A189\" style=\"max-height:24px; max-width: 28px;\" /> A189",
            "display": "A189"
        },
        {
            "id": "A19",
            "text": "A19: bent man leaning on staff",
            "html": "<span class=\"uni\">&#x13017;</span> A19: bent man leaning on staff",
            "display": "A19"
        },
        {
            "id": "A190a",
            "text": "A190A",
            "html": "<img src=\"/Search/Image?key=A190A\" alt=\"A190A\" style=\"max-height:24px; max-width: 28px;\" /> A190A",
            "display": "A190a"
        },
        {
            "id": "A193",
            "text": "A193",
            "html": "<img src=\"/Search/Image?key=A193\" alt=\"A193\" style=\"max-height:24px; max-width: 28px;\" /> A193",
            "display": "A193"
        },
        {
            "id": "A199",
            "text": "A199",
            "html": "<img src=\"/Search/Image?key=A199\" alt=\"A199\" style=\"max-height:24px; max-width: 28px;\" /> A199",
            "display": "A199"
        },
        {
            "id": "A199a",
            "text": "A199A",
            "html": "<img src=\"/Search/Image?key=A199A\" alt=\"A199A\" style=\"max-height:24px; max-width: 28px;\" /> A199A",
            "display": "A199a"
        },
        {
            "id": "A2",
            "text": "A2: seated man with hand to mouth",
            "html": "<span class=\"uni\">&#x13001;</span> A2: seated man with hand to mouth",
            "display": "A2"
        },
        {
            "id": "A20",
            "text": "A20: man leaning on forked staff",
            "html": "<span class=\"uni\">&#x13018;</span> A20: man leaning on forked staff",
            "display": "A20"
        },
        {
            "id": "A200",
            "text": "A200",
            "html": "<img src=\"/Search/Image?key=A200\" alt=\"A200\" style=\"max-height:24px; max-width: 28px;\" /> A200",
            "display": "A200"
        },
        {
            "id": "A201",
            "text": "A201",
            "html": "<img src=\"/Search/Image?key=A201\" alt=\"A201\" style=\"max-height:24px; max-width: 28px;\" /> A201",
            "display": "A201"
        },
        {
            "id": "A202",
            "text": "A202",
            "html": "<img src=\"/Search/Image?key=A202\" alt=\"A202\" style=\"max-height:24px; max-width: 28px;\" /> A202",
            "display": "A202"
        },
        {
            "id": "A207a",
            "text": "A207A",
            "html": "<img src=\"/Search/Image?key=A207A\" alt=\"A207A\" style=\"max-height:24px; max-width: 28px;\" /> A207A",
            "display": "A207a"
        },
        {
            "id": "A21",
            "text": "A21: man holding staff with handkerchief [sr]",
            "html": "<span class=\"uni\">&#x13019;</span> A21: man holding staff with handkerchief",
            "display": "A21"
        },
        {
            "id": "A211",
            "text": "A211",
            "html": "<img src=\"/Search/Image?key=A211\" alt=\"A211\" style=\"max-height:24px; max-width: 28px;\" /> A211",
            "display": "A211"
        },
        {
            "id": "A211a",
            "text": "A211A",
            "html": "<img src=\"/Search/Image?key=A211A\" alt=\"A211A\" style=\"max-height:24px; max-width: 28px;\" /> A211A",
            "display": "A211a"
        },
        {
            "id": "A216b",
            "text": "A216B",
            "html": "<img src=\"/Search/Image?key=A216B\" alt=\"A216B\" style=\"max-height:24px; max-width: 28px;\" /> A216B",
            "display": "A216b"
        },
        {
            "id": "A216c",
            "text": "A216C",
            "html": "<img src=\"/Search/Image?key=A216C\" alt=\"A216C\" style=\"max-height:24px; max-width: 28px;\" /> A216C",
            "display": "A216c"
        },
        {
            "id": "A219a",
            "text": "A219A",
            "html": "<img src=\"/Search/Image?key=A219A\" alt=\"A219A\" style=\"max-height:24px; max-width: 28px;\" /> A219A",
            "display": "A219a"
        },
        {
            "id": "A21a",
            "text": "A21A: man holding staff with handkerchief",
            "html": "<img src=\"/Search/Image?key=A21A\" alt=\"A21A\" style=\"max-height:24px; max-width: 28px;\" /> A21A: man holding staff with handkerchief",
            "display": "A21a"
        },
        {
            "id": "A22",
            "text": "A22: statue of man with staff and S42",
            "html": "<span class=\"uni\">&#x1301A;</span> A22: statue of man with staff and S42",
            "display": "A22"
        },
        {
            "id": "A223",
            "text": "A223",
            "html": "<img src=\"/Search/Image?key=A223\" alt=\"A223\" style=\"max-height:24px; max-width: 28px;\" /> A223",
            "display": "A223"
        },
        {
            "id": "A23",
            "text": "A23: king with staff and T3",
            "html": "<span class=\"uni\">&#x1301B;</span> A23: king with staff and T3",
            "display": "A23"
        },
        {
            "id": "A233",
            "text": "A233",
            "html": "<img src=\"/Search/Image?key=A233\" alt=\"A233\" style=\"max-height:24px; max-width: 28px;\" /> A233",
            "display": "A233"
        },
        {
            "id": "A239",
            "text": "A239",
            "html": "<img src=\"/Search/Image?key=A239\" alt=\"A239\" style=\"max-height:24px; max-width: 28px;\" /> A239",
            "display": "A239"
        },
        {
            "id": "A239a",
            "text": "A239A",
            "html": "<img src=\"/Search/Image?key=A239A\" alt=\"A239A\" style=\"max-height:24px; max-width: 28px;\" /> A239A",
            "display": "A239a"
        },
        {
            "id": "A23h",
            "text": "A23H: king with staff and T3",
            "html": "<img src=\"/Search/Image?key=A23H\" alt=\"A23H\" style=\"max-height:24px; max-width: 28px;\" /> A23H: king with staff and T3",
            "display": "A23h"
        },
        {
            "id": "A24",
            "text": "A24: man striking with both hands",
            "html": "<span class=\"uni\">&#x1301C;</span> A24: man striking with both hands",
            "display": "A24"
        },
        {
            "id": "A244",
            "text": "A244",
            "html": "<img src=\"/Search/Image?key=A244\" alt=\"A244\" style=\"max-height:24px; max-width: 28px;\" /> A244",
            "display": "A244"
        },
        {
            "id": "A244a",
            "text": "A244A",
            "html": "<img src=\"/Search/Image?key=A244A\" alt=\"A244A\" style=\"max-height:24px; max-width: 28px;\" /> A244A",
            "display": "A244a"
        },
        {
            "id": "A245",
            "text": "A245",
            "html": "<img src=\"/Search/Image?key=A245\" alt=\"A245\" style=\"max-height:24px; max-width: 28px;\" /> A245",
            "display": "A245"
        },
        {
            "id": "A245a",
            "text": "A245A",
            "html": "<img src=\"/Search/Image?key=A245A\" alt=\"A245A\" style=\"max-height:24px; max-width: 28px;\" /> A245A",
            "display": "A245a"
        },
        {
            "id": "A245b",
            "text": "A245B",
            "html": "<img src=\"/Search/Image?key=A245B\" alt=\"A245B\" style=\"max-height:24px; max-width: 28px;\" /> A245B",
            "display": "A245b"
        },
        {
            "id": "A248",
            "text": "A248",
            "html": "<img src=\"/Search/Image?key=A248\" alt=\"A248\" style=\"max-height:24px; max-width: 28px;\" /> A248",
            "display": "A248"
        },
        {
            "id": "A248b",
            "text": "A248B",
            "html": "<img src=\"/Search/Image?key=A248B\" alt=\"A248B\" style=\"max-height:24px; max-width: 28px;\" /> A248B",
            "display": "A248b"
        },
        {
            "id": "A25",
            "text": "A25: man striking, with left arm hanging behind back",
            "html": "<span class=\"uni\">&#x1301D;</span> A25: man striking, with left arm hanging behind back",
            "display": "A25"
        },
        {
            "id": "A25a",
            "text": "A25A: man striking, with left arm hanging behind back",
            "html": "<img src=\"/Search/Image?key=A25A\" alt=\"A25A\" style=\"max-height:24px; max-width: 28px;\" /> A25A: man striking, with left arm hanging behind back",
            "display": "A25a"
        },
        {
            "id": "A26",
            "text": "A26: man with one arm pointing forward",
            "html": "<span class=\"uni\">&#x1301E;</span> A26: man with one arm pointing forward",
            "display": "A26"
        },
        {
            "id": "A261",
            "text": "A261",
            "html": "<img src=\"/Search/Image?key=A261\" alt=\"A261\" style=\"max-height:24px; max-width: 28px;\" /> A261",
            "display": "A261"
        },
        {
            "id": "A27",
            "text": "A27: hastening man",
            "html": "<span class=\"uni\">&#x1301F;</span> A27: hastening man",
            "display": "A27"
        },
        {
            "id": "A275",
            "text": "A275",
            "html": "<img src=\"/Search/Image?key=A275\" alt=\"A275\" style=\"max-height:24px; max-width: 28px;\" /> A275",
            "display": "A275"
        },
        {
            "id": "A276",
            "text": "A276",
            "html": "<img src=\"/Search/Image?key=A276\" alt=\"A276\" style=\"max-height:24px; max-width: 28px;\" /> A276",
            "display": "A276"
        },
        {
            "id": "A278",
            "text": "A278",
            "html": "<img src=\"/Search/Image?key=A278\" alt=\"A278\" style=\"max-height:24px; max-width: 28px;\" /> A278",
            "display": "A278"
        },
        {
            "id": "A27a",
            "text": "A27A: hastening man",
            "html": "<img src=\"/Search/Image?key=A27A\" alt=\"A27A\" style=\"max-height:24px; max-width: 28px;\" /> A27A: hastening man",
            "display": "A27a"
        },
        {
            "id": "A28",
            "text": "A28: man with hands raised on either side",
            "html": "<span class=\"uni\">&#x13020;</span> A28: man with hands raised on either side",
            "display": "A28"
        },
        {
            "id": "A280",
            "text": "A280",
            "html": "<img src=\"/Search/Image?key=A280\" alt=\"A280\" style=\"max-height:24px; max-width: 28px;\" /> A280",
            "display": "A280"
        },
        {
            "id": "A282",
            "text": "A282",
            "html": "<img src=\"/Search/Image?key=A282\" alt=\"A282\" style=\"max-height:24px; max-width: 28px;\" /> A282",
            "display": "A282"
        },
        {
            "id": "A285",
            "text": "A285",
            "html": "<img src=\"/Search/Image?key=A285\" alt=\"A285\" style=\"max-height:24px; max-width: 28px;\" /> A285",
            "display": "A285"
        },
        {
            "id": "A29",
            "text": "A29: man upside down",
            "html": "<span class=\"uni\">&#x13021;</span> A29: man upside down",
            "display": "A29"
        },
        {
            "id": "A298",
            "text": "A298",
            "html": "<img src=\"/Search/Image?key=A298\" alt=\"A298\" style=\"max-height:24px; max-width: 28px;\" /> A298",
            "display": "A298"
        },
        {
            "id": "A299b",
            "text": "A299B",
            "html": "<img src=\"/Search/Image?key=A299B\" alt=\"A299B\" style=\"max-height:24px; max-width: 28px;\" /> A299B",
            "display": "A299b"
        },
        {
            "id": "A3",
            "text": "A3: man sitting on heel",
            "html": "<span class=\"uni\">&#x13002;</span> A3: man sitting on heel",
            "display": "A3"
        },
        {
            "id": "A30",
            "text": "A30: man with hands raised in front",
            "html": "<span class=\"uni\">&#x13022;</span> A30: man with hands raised in front",
            "display": "A30"
        },
        {
            "id": "A301",
            "text": "A301",
            "html": "<img src=\"/Search/Image?key=A301\" alt=\"A301\" style=\"max-height:24px; max-width: 28px;\" /> A301",
            "display": "A301"
        },
        {
            "id": "A304",
            "text": "A304",
            "html": "<img src=\"/Search/Image?key=A304\" alt=\"A304\" style=\"max-height:24px; max-width: 28px;\" /> A304",
            "display": "A304"
        },
        {
            "id": "A304c",
            "text": "A304C",
            "html": "<img src=\"/Search/Image?key=A304C\" alt=\"A304C\" style=\"max-height:24px; max-width: 28px;\" /> A304C",
            "display": "A304c"
        },
        {
            "id": "A304e",
            "text": "A304E",
            "html": "<img src=\"/Search/Image?key=A304E\" alt=\"A304E\" style=\"max-height:24px; max-width: 28px;\" /> A304E",
            "display": "A304e"
        },
        {
            "id": "A31",
            "text": "A31: man with hands raised behind him",
            "html": "<span class=\"uni\">&#x13023;</span> A31: man with hands raised behind him",
            "display": "A31"
        },
        {
            "id": "A310",
            "text": "A310",
            "html": "<img src=\"/Search/Image?key=A310\" alt=\"A310\" style=\"max-height:24px; max-width: 28px;\" /> A310",
            "display": "A310"
        },
        {
            "id": "A311",
            "text": "A311",
            "html": "<img src=\"/Search/Image?key=A311\" alt=\"A311\" style=\"max-height:24px; max-width: 28px;\" /> A311",
            "display": "A311"
        },
        {
            "id": "A313",
            "text": "A313",
            "html": "<img src=\"/Search/Image?key=A313\" alt=\"A313\" style=\"max-height:24px; max-width: 28px;\" /> A313",
            "display": "A313"
        },
        {
            "id": "A316",
            "text": "A316",
            "html": "<img src=\"/Search/Image?key=A316\" alt=\"A316\" style=\"max-height:24px; max-width: 28px;\" /> A316",
            "display": "A316"
        },
        {
            "id": "A31b",
            "text": "A31B: man with hands raised behind him",
            "html": "<img src=\"/Search/Image?key=A31B\" alt=\"A31B\" style=\"max-height:24px; max-width: 28px;\" /> A31B: man with hands raised behind him",
            "display": "A31b"
        },
        {
            "id": "A31c",
            "text": "A31C: man with hands raised behind him",
            "html": "<img src=\"/Search/Image?key=A31C\" alt=\"A31C\" style=\"max-height:24px; max-width: 28px;\" /> A31C: man with hands raised behind him",
            "display": "A31c"
        },
        {
            "id": "A32",
            "text": "A32: man dancing with arms to the back",
            "html": "<span class=\"uni\">&#x13024;</span> A32: man dancing with arms to the back",
            "display": "A32"
        },
        {
            "id": "A322",
            "text": "A322",
            "html": "<img src=\"/Search/Image?key=A322\" alt=\"A322\" style=\"max-height:24px; max-width: 28px;\" /> A322",
            "display": "A322"
        },
        {
            "id": "A323",
            "text": "A323",
            "html": "<img src=\"/Search/Image?key=A323\" alt=\"A323\" style=\"max-height:24px; max-width: 28px;\" /> A323",
            "display": "A323"
        },
        {
            "id": "A32a",
            "text": "A32A: man dancing with arms to the front",
            "html": "<span class=\"uni\">&#x13025;</span> A32A: man dancing with arms to the front",
            "display": "A32a"
        },
        {
            "id": "A32b",
            "text": "A32B: man dancing with arms to the back",
            "html": "<img src=\"/Search/Image?key=A32B\" alt=\"A32B\" style=\"max-height:24px; max-width: 28px;\" /> A32B: man dancing with arms to the back",
            "display": "A32b"
        },
        {
            "id": "A32d",
            "text": "A32D: man dancing with arms to the back",
            "html": "<img src=\"/Search/Image?key=A32D\" alt=\"A32D\" style=\"max-height:24px; max-width: 28px;\" /> A32D: man dancing with arms to the back",
            "display": "A32d"
        },
        {
            "id": "A32f",
            "text": "A32F: man dancing with arms to the back",
            "html": "<img src=\"/Search/Image?key=A32F\" alt=\"A32F\" style=\"max-height:24px; max-width: 28px;\" /> A32F: man dancing with arms to the back",
            "display": "A32f"
        },
        {
            "id": "A32h",
            "text": "A32H: man dancing with arms to the back",
            "html": "<img src=\"/Search/Image?key=A32H\" alt=\"A32H\" style=\"max-height:24px; max-width: 28px;\" /> A32H: man dancing with arms to the back",
            "display": "A32h"
        },
        {
            "id": "A33",
            "text": "A33: man with stick and bundle on shoulder [mniw]",
            "html": "<span class=\"uni\">&#x13026;</span> A33: man with stick and bundle on shoulder",
            "display": "A33"
        },
        {
            "id": "A330",
            "text": "A330",
            "html": "<img src=\"/Search/Image?key=A330\" alt=\"A330\" style=\"max-height:24px; max-width: 28px;\" /> A330",
            "display": "A330"
        },
        {
            "id": "A338",
            "text": "A338",
            "html": "<img src=\"/Search/Image?key=A338\" alt=\"A338\" style=\"max-height:24px; max-width: 28px;\" /> A338",
            "display": "A338"
        },
        {
            "id": "A33b",
            "text": "A33B: man with stick and bundle on shoulder",
            "html": "<img src=\"/Search/Image?key=A33B\" alt=\"A33B\" style=\"max-height:24px; max-width: 28px;\" /> A33B: man with stick and bundle on shoulder",
            "display": "A33b"
        },
        {
            "id": "A34",
            "text": "A34: man pounding in a mortar",
            "html": "<span class=\"uni\">&#x13027;</span> A34: man pounding in a mortar",
            "display": "A34"
        },
        {
            "id": "A346",
            "text": "A346",
            "html": "<img src=\"/Search/Image?key=A346\" alt=\"A346\" style=\"max-height:24px; max-width: 28px;\" /> A346",
            "display": "A346"
        },
        {
            "id": "A349",
            "text": "A349",
            "html": "<img src=\"/Search/Image?key=A349\" alt=\"A349\" style=\"max-height:24px; max-width: 28px;\" /> A349",
            "display": "A349"
        },
        {
            "id": "A34a",
            "text": "A34A: man pounding in a mortar",
            "html": "<img src=\"/Search/Image?key=A34A\" alt=\"A34A\" style=\"max-height:24px; max-width: 28px;\" /> A34A: man pounding in a mortar",
            "display": "A34a"
        },
        {
            "id": "A35",
            "text": "A35: man building wall",
            "html": "<span class=\"uni\">&#x13028;</span> A35: man building wall",
            "display": "A35"
        },
        {
            "id": "A351",
            "text": "A351",
            "html": "<img src=\"/Search/Image?key=A351\" alt=\"A351\" style=\"max-height:24px; max-width: 28px;\" /> A351",
            "display": "A351"
        },
        {
            "id": "A352",
            "text": "A352",
            "html": "<img src=\"/Search/Image?key=A352\" alt=\"A352\" style=\"max-height:24px; max-width: 28px;\" /> A352",
            "display": "A352"
        },
        {
            "id": "A359",
            "text": "A359",
            "html": "<img src=\"/Search/Image?key=A359\" alt=\"A359\" style=\"max-height:24px; max-width: 28px;\" /> A359",
            "display": "A359"
        },
        {
            "id": "A35e",
            "text": "A35E: man building wall",
            "html": "<img src=\"/Search/Image?key=A35E\" alt=\"A35E\" style=\"max-height:24px; max-width: 28px;\" /> A35E: man building wall",
            "display": "A35e"
        },
        {
            "id": "A36",
            "text": "A36: man kneading into vessel",
            "html": "<span class=\"uni\">&#x13029;</span> A36: man kneading into vessel",
            "display": "A36"
        },
        {
            "id": "A361",
            "text": "A361",
            "html": "<img src=\"/Search/Image?key=A361\" alt=\"A361\" style=\"max-height:24px; max-width: 28px;\" /> A361",
            "display": "A361"
        },
        {
            "id": "A363",
            "text": "A363",
            "html": "<img src=\"/Search/Image?key=A363\" alt=\"A363\" style=\"max-height:24px; max-width: 28px;\" /> A363",
            "display": "A363"
        },
        {
            "id": "A366",
            "text": "A366",
            "html": "<img src=\"/Search/Image?key=A366\" alt=\"A366\" style=\"max-height:24px; max-width: 28px;\" /> A366",
            "display": "A366"
        },
        {
            "id": "A36a",
            "text": "A36A: man kneading into vessel",
            "html": "<img src=\"/Search/Image?key=A36A\" alt=\"A36A\" style=\"max-height:24px; max-width: 28px;\" /> A36A: man kneading into vessel",
            "display": "A36a"
        },
        {
            "id": "A36c",
            "text": "A36C: man kneading into vessel",
            "html": "<img src=\"/Search/Image?key=A36C\" alt=\"A36C\" style=\"max-height:24px; max-width: 28px;\" /> A36C: man kneading into vessel",
            "display": "A36c"
        },
        {
            "id": "A37",
            "text": "A37: man in vessel",
            "html": "<span class=\"uni\">&#x1302A;</span> A37: man in vessel",
            "display": "A37"
        },
        {
            "id": "A375",
            "text": "A375",
            "html": "<img src=\"/Search/Image?key=A375\" alt=\"A375\" style=\"max-height:24px; max-width: 28px;\" /> A375",
            "display": "A375"
        },
        {
            "id": "A376a",
            "text": "A376A",
            "html": "<img src=\"/Search/Image?key=A376A\" alt=\"A376A\" style=\"max-height:24px; max-width: 28px;\" /> A376A",
            "display": "A376a"
        },
        {
            "id": "A38",
            "text": "A38: man holding necks of two emblematic animals with panther heads [qiz]",
            "html": "<span class=\"uni\">&#x1302B;</span> A38: man holding necks of two emblematic animals with panther heads",
            "display": "A38"
        },
        {
            "id": "A388",
            "text": "A388",
            "html": "<img src=\"/Search/Image?key=A388\" alt=\"A388\" style=\"max-height:24px; max-width: 28px;\" /> A388",
            "display": "A388"
        },
        {
            "id": "A39",
            "text": "A39: man on two giraffes",
            "html": "<span class=\"uni\">&#x1302C;</span> A39: man on two giraffes",
            "display": "A39"
        },
        {
            "id": "A4",
            "text": "A4: seated man with hands raised",
            "html": "<span class=\"uni\">&#x13003;</span> A4: seated man with hands raised",
            "display": "A4"
        },
        {
            "id": "A40",
            "text": "A40: seated god",
            "html": "<span class=\"uni\">&#x1302D;</span> A40: seated god",
            "display": "A40"
        },
        {
            "id": "A405",
            "text": "A405",
            "html": "<img src=\"/Search/Image?key=A405\" alt=\"A405\" style=\"max-height:24px; max-width: 28px;\" /> A405",
            "display": "A405"
        },
        {
            "id": "A406",
            "text": "A406",
            "html": "<img src=\"/Search/Image?key=A406\" alt=\"A406\" style=\"max-height:24px; max-width: 28px;\" /> A406",
            "display": "A406"
        },
        {
            "id": "A409",
            "text": "A409",
            "html": "<img src=\"/Search/Image?key=A409\" alt=\"A409\" style=\"max-height:24px; max-width: 28px;\" /> A409",
            "display": "A409"
        },
        {
            "id": "A40a",
            "text": "A40A: seated god with S40",
            "html": "<span class=\"uni\">&#x1302E;</span> A40A: seated god with S40",
            "display": "A40a"
        },
        {
            "id": "A40b",
            "text": "A40B: seated god",
            "html": "<img src=\"/Search/Image?key=A40B\" alt=\"A40B\" style=\"max-height:24px; max-width: 28px;\" /> A40B: seated god",
            "display": "A40b"
        },
        {
            "id": "A40d",
            "text": "A40D: seated god",
            "html": "<img src=\"/Search/Image?key=A40D\" alt=\"A40D\" style=\"max-height:24px; max-width: 28px;\" /> A40D: seated god",
            "display": "A40d"
        },
        {
            "id": "A41",
            "text": "A41: king with uraeus",
            "html": "<span class=\"uni\">&#x1302F;</span> A41: king with uraeus",
            "display": "A41"
        },
        {
            "id": "A410",
            "text": "A410",
            "html": "<img src=\"/Search/Image?key=A410\" alt=\"A410\" style=\"max-height:24px; max-width: 28px;\" /> A410",
            "display": "A410"
        },
        {
            "id": "A413",
            "text": "A413",
            "html": "<img src=\"/Search/Image?key=A413\" alt=\"A413\" style=\"max-height:24px; max-width: 28px;\" /> A413",
            "display": "A413"
        },
        {
            "id": "A414",
            "text": "A414",
            "html": "<img src=\"/Search/Image?key=A414\" alt=\"A414\" style=\"max-height:24px; max-width: 28px;\" /> A414",
            "display": "A414"
        },
        {
            "id": "A415",
            "text": "A415",
            "html": "<img src=\"/Search/Image?key=A415\" alt=\"A415\" style=\"max-height:24px; max-width: 28px;\" /> A415",
            "display": "A415"
        },
        {
            "id": "A417",
            "text": "A417",
            "html": "<img src=\"/Search/Image?key=A417\" alt=\"A417\" style=\"max-height:24px; max-width: 28px;\" /> A417",
            "display": "A417"
        },
        {
            "id": "A42",
            "text": "A42: king with uraeus and S45",
            "html": "<span class=\"uni\">&#x13030;</span> A42: king with uraeus and S45",
            "display": "A42"
        },
        {
            "id": "A424",
            "text": "A424",
            "html": "<img src=\"/Search/Image?key=A424\" alt=\"A424\" style=\"max-height:24px; max-width: 28px;\" /> A424",
            "display": "A424"
        },
        {
            "id": "A425",
            "text": "A425",
            "html": "<img src=\"/Search/Image?key=A425\" alt=\"A425\" style=\"max-height:24px; max-width: 28px;\" /> A425",
            "display": "A425"
        },
        {
            "id": "A42a",
            "text": "A42A: king with uraeus and S45",
            "html": "<span class=\"uni\">&#x13031;</span> A42A: king with uraeus and S45",
            "display": "A42a"
        },
        {
            "id": "A42c",
            "text": "A42C: king with uraeus and S45",
            "html": "<img src=\"/Search/Image?key=A42C\" alt=\"A42C\" style=\"max-height:24px; max-width: 28px;\" /> A42C: king with uraeus and S45",
            "display": "A42c"
        },
        {
            "id": "A43",
            "text": "A43: king wearing S1",
            "html": "<span class=\"uni\">&#x13032;</span> A43: king wearing S1",
            "display": "A43"
        },
        {
            "id": "A43b",
            "text": "A43B: king wearing S1",
            "html": "<img src=\"/Search/Image?key=A43B\" alt=\"A43B\" style=\"max-height:24px; max-width: 28px;\" /> A43B: king wearing S1",
            "display": "A43b"
        },
        {
            "id": "A43e",
            "text": "A43E: king wearing S1",
            "html": "<img src=\"/Search/Image?key=A43E\" alt=\"A43E\" style=\"max-height:24px; max-width: 28px;\" /> A43E: king wearing S1",
            "display": "A43e"
        },
        {
            "id": "A44",
            "text": "A44: king wearing S1 with S45",
            "html": "<span class=\"uni\">&#x13034;</span> A44: king wearing S1 with S45",
            "display": "A44"
        },
        {
            "id": "A45",
            "text": "A45: king wearing S3",
            "html": "<span class=\"uni\">&#x13035;</span> A45: king wearing S3",
            "display": "A45"
        },
        {
            "id": "A450",
            "text": "A450",
            "html": "<img src=\"/Search/Image?key=A450\" alt=\"A450\" style=\"max-height:24px; max-width: 28px;\" /> A450",
            "display": "A450"
        },
        {
            "id": "A459",
            "text": "A459",
            "html": "<img src=\"/Search/Image?key=A459\" alt=\"A459\" style=\"max-height:24px; max-width: 28px;\" /> A459",
            "display": "A459"
        },
        {
            "id": "A45a",
            "text": "A45A: king wearing S3 with S40",
            "html": "<span class=\"uni\">&#x13036;</span> A45A: king wearing S3 with S40",
            "display": "A45a"
        },
        {
            "id": "A462",
            "text": "A462",
            "html": "<img src=\"/Search/Image?key=A462\" alt=\"A462\" style=\"max-height:24px; max-width: 28px;\" /> A462",
            "display": "A462"
        },
        {
            "id": "A463a",
            "text": "A463A",
            "html": "<img src=\"/Search/Image?key=A463A\" alt=\"A463A\" style=\"max-height:24px; max-width: 28px;\" /> A463A",
            "display": "A463a"
        },
        {
            "id": "A466",
            "text": "A466",
            "html": "<img src=\"/Search/Image?key=A466\" alt=\"A466\" style=\"max-height:24px; max-width: 28px;\" /> A466",
            "display": "A466"
        },
        {
            "id": "A47",
            "text": "A47: shepherd seated and wrapped in mantle, holding stick [iry]",
            "html": "<span class=\"uni\">&#x13038;</span> A47: shepherd seated and wrapped in mantle, holding stick",
            "display": "A47"
        },
        {
            "id": "A473",
            "text": "A473",
            "html": "<img src=\"/Search/Image?key=A473\" alt=\"A473\" style=\"max-height:24px; max-width: 28px;\" /> A473",
            "display": "A473"
        },
        {
            "id": "A478a",
            "text": "A478A",
            "html": "<img src=\"/Search/Image?key=A478A\" alt=\"A478A\" style=\"max-height:24px; max-width: 28px;\" /> A478A",
            "display": "A478a"
        },
        {
            "id": "A48",
            "text": "A48: beardless man seated and holding knife",
            "html": "<span class=\"uni\">&#x13039;</span> A48: beardless man seated and holding knife",
            "display": "A48"
        },
        {
            "id": "A482",
            "text": "A482",
            "html": "<img src=\"/Search/Image?key=A482\" alt=\"A482\" style=\"max-height:24px; max-width: 28px;\" /> A482",
            "display": "A482"
        },
        {
            "id": "A487",
            "text": "A487",
            "html": "<img src=\"/Search/Image?key=A487\" alt=\"A487\" style=\"max-height:24px; max-width: 28px;\" /> A487",
            "display": "A487"
        },
        {
            "id": "A49",
            "text": "A49: seated Syrian holding stick",
            "html": "<span class=\"uni\">&#x1303A;</span> A49: seated Syrian holding stick",
            "display": "A49"
        },
        {
            "id": "A4a",
            "text": "A4A: seated man with hands raised",
            "html": "<img src=\"/Search/Image?key=A4A\" alt=\"A4A\" style=\"max-height:24px; max-width: 28px;\" /> A4A: seated man with hands raised",
            "display": "A4a"
        },
        {
            "id": "A4b",
            "text": "A4B: seated man with hands raised",
            "html": "<img src=\"/Search/Image?key=A4B\" alt=\"A4B\" style=\"max-height:24px; max-width: 28px;\" /> A4B: seated man with hands raised",
            "display": "A4b"
        },
        {
            "id": "A4c",
            "text": "A4C: seated man with hands raised",
            "html": "<img src=\"/Search/Image?key=A4C\" alt=\"A4C\" style=\"max-height:24px; max-width: 28px;\" /> A4C: seated man with hands raised",
            "display": "A4c"
        },
        {
            "id": "A5",
            "text": "A5: crouching man hiding behind wall",
            "html": "<span class=\"uni\">&#x13004;</span> A5: crouching man hiding behind wall",
            "display": "A5"
        },
        {
            "id": "A50",
            "text": "A50: noble on chair [Sps]",
            "html": "<span class=\"uni\">&#x1303B;</span> A50: noble on chair",
            "display": "A50"
        },
        {
            "id": "A51",
            "text": "A51: noble on chair with S45 [Spsi]",
            "html": "<span class=\"uni\">&#x1303C;</span> A51: noble on chair with S45",
            "display": "A51"
        },
        {
            "id": "A51a",
            "text": "A51A: noble on chair with S45",
            "html": "<img src=\"/Search/Image?key=A51A\" alt=\"A51A\" style=\"max-height:24px; max-width: 28px;\" /> A51A: noble on chair with S45",
            "display": "A51a"
        },
        {
            "id": "A51f",
            "text": "A51F: noble on chair with S45",
            "html": "<img src=\"/Search/Image?key=A51F\" alt=\"A51F\" style=\"max-height:24px; max-width: 28px;\" /> A51F: noble on chair with S45",
            "display": "A51f"
        },
        {
            "id": "A52",
            "text": "A52: noble squatting with S45",
            "html": "<span class=\"uni\">&#x1303D;</span> A52: noble squatting with S45",
            "display": "A52"
        },
        {
            "id": "A52aa",
            "text": "A52AA: noble squatting with S45",
            "html": "<img src=\"/Search/Image?key=A52J\" alt=\"A52J\" style=\"max-height:24px; max-width: 28px;\" /> A52AA: noble squatting with S45",
            "display": "A52aa"
        },
        {
            "id": "A53",
            "text": "A53: standing mummy",
            "html": "<span class=\"uni\">&#x1303E;</span> A53: standing mummy",
            "display": "A53"
        },
        {
            "id": "A54",
            "text": "A54: lying mummy",
            "html": "<span class=\"uni\">&#x1303F;</span> A54: lying mummy",
            "display": "A54"
        },
        {
            "id": "A55",
            "text": "A55: mummy on bed",
            "html": "<span class=\"uni\">&#x13040;</span> A55: mummy on bed",
            "display": "A55"
        },
        {
            "id": "A55a",
            "text": "A55A: mummy on bed",
            "html": "<img src=\"/Search/Image?key=A55A\" alt=\"A55A\" style=\"max-height:24px; max-width: 28px;\" /> A55A: mummy on bed",
            "display": "A55a"
        },
        {
            "id": "A56",
            "text": "A56: seated man holding stick",
            "html": "<span class=\"uni\">&#x13041;</span> A56: seated man holding stick",
            "display": "A56"
        },
        {
            "id": "A57",
            "text": "A57: man holding R4",
            "html": "<span class=\"uni\">&#x13042;</span> A57: man holding R4",
            "display": "A57"
        },
        {
            "id": "A58",
            "text": "A58: man applying hoe to ground",
            "html": "<span class=\"uni\">&#x13043;</span> A58: man applying hoe to ground",
            "display": "A58"
        },
        {
            "id": "A58a",
            "text": "A58A: man applying hoe to ground",
            "html": "<img src=\"/Search/Image?key=A58A\" alt=\"A58A\" style=\"max-height:24px; max-width: 28px;\" /> A58A: man applying hoe to ground",
            "display": "A58a"
        },
        {
            "id": "A58b",
            "text": "A58B: man applying hoe to ground",
            "html": "<img src=\"/Search/Image?key=A58B\" alt=\"A58B\" style=\"max-height:24px; max-width: 28px;\" /> A58B: man applying hoe to ground",
            "display": "A58b"
        },
        {
            "id": "A59",
            "text": "A59: man threatening with stick",
            "html": "<span class=\"uni\">&#x13044;</span> A59: man threatening with stick",
            "display": "A59"
        },
        {
            "id": "A59a",
            "text": "A59A: man threatening with stick",
            "html": "<img src=\"/Search/Image?key=A59A\" alt=\"A59A\" style=\"max-height:24px; max-width: 28px;\" /> A59A: man threatening with stick",
            "display": "A59a"
        },
        {
            "id": "A59b",
            "text": "A59B: man threatening with stick",
            "html": "<img src=\"/Search/Image?key=A59B\" alt=\"A59B\" style=\"max-height:24px; max-width: 28px;\" /> A59B: man threatening with stick",
            "display": "A59b"
        },
        {
            "id": "A5a",
            "text": "A5A: seated man hiding behind wall",
            "html": "<span class=\"uni\">&#x13005;</span> A5A: seated man hiding behind wall",
            "display": "A5a"
        },
        {
            "id": "A6",
            "text": "A6: seated man under vase from which water flows",
            "html": "<span class=\"uni\">&#x13006;</span> A6: seated man under vase from which water flows",
            "display": "A6"
        },
        {
            "id": "A60",
            "text": "A60: man sowing seeds",
            "html": "<span class=\"uni\">&#x13045;</span> A60: man sowing seeds",
            "display": "A60"
        },
        {
            "id": "A61",
            "text": "A61: man looking over his shoulder",
            "html": "<span class=\"uni\">&#x13046;</span> A61: man looking over his shoulder",
            "display": "A61"
        },
        {
            "id": "A6a",
            "text": "A6A: seated man reaching for libation stone, under vase from which water flows",
            "html": "<span class=\"uni\">&#x13007;</span> A6A: seated man reaching for libation stone, under vase from which water flows",
            "display": "A6a"
        },
        {
            "id": "A6k",
            "text": "A6K: seated man under vase from which water flows",
            "html": "<img src=\"/Search/Image?key=A6K\" alt=\"A6K\" style=\"max-height:24px; max-width: 28px;\" /> A6K: seated man under vase from which water flows",
            "display": "A6k"
        },
        {
            "id": "A7",
            "text": "A7: fatigued man",
            "html": "<span class=\"uni\">&#x13009;</span> A7: fatigued man",
            "display": "A7"
        },
        {
            "id": "A71",
            "text": "A71",
            "html": "<img src=\"/Search/Image?key=A71\" alt=\"A71\" style=\"max-height:24px; max-width: 28px;\" /> A71",
            "display": "A71"
        },
        {
            "id": "A73",
            "text": "A73",
            "html": "<img src=\"/Search/Image?key=A73\" alt=\"A73\" style=\"max-height:24px; max-width: 28px;\" /> A73",
            "display": "A73"
        },
        {
            "id": "A75",
            "text": "A75",
            "html": "<img src=\"/Search/Image?key=A75\" alt=\"A75\" style=\"max-height:24px; max-width: 28px;\" /> A75",
            "display": "A75"
        },
        {
            "id": "A76c",
            "text": "A76C",
            "html": "<img src=\"/Search/Image?key=A76C\" alt=\"A76C\" style=\"max-height:24px; max-width: 28px;\" /> A76C",
            "display": "A76c"
        },
        {
            "id": "A78",
            "text": "A78",
            "html": "<img src=\"/Search/Image?key=A78\" alt=\"A78\" style=\"max-height:24px; max-width: 28px;\" /> A78",
            "display": "A78"
        },
        {
            "id": "A7a",
            "text": "A7A: fatigued man",
            "html": "<img src=\"/Search/Image?key=A7A\" alt=\"A7A\" style=\"max-height:24px; max-width: 28px;\" /> A7A: fatigued man",
            "display": "A7a"
        },
        {
            "id": "A8",
            "text": "A8: man performing <span class=\"egytransl\">hnw</span>-rite",
            "html": "<span class=\"uni\">&#x1300A;</span> A8: man performing <span class=\"egytransl\">hnw</span>-rite",
            "display": "A8"
        },
        {
            "id": "A80",
            "text": "A80",
            "html": "<img src=\"/Search/Image?key=A80\" alt=\"A80\" style=\"max-height:24px; max-width: 28px;\" /> A80",
            "display": "A80"
        },
        {
            "id": "A81",
            "text": "A81",
            "html": "<img src=\"/Search/Image?key=A81\" alt=\"A81\" style=\"max-height:24px; max-width: 28px;\" /> A81",
            "display": "A81"
        },
        {
            "id": "A82",
            "text": "A82",
            "html": "<img src=\"/Search/Image?key=A82\" alt=\"A82\" style=\"max-height:24px; max-width: 28px;\" /> A82",
            "display": "A82"
        },
        {
            "id": "A84",
            "text": "A84",
            "html": "<img src=\"/Search/Image?key=A84\" alt=\"A84\" style=\"max-height:24px; max-width: 28px;\" /> A84",
            "display": "A84"
        },
        {
            "id": "A85",
            "text": "A85",
            "html": "<img src=\"/Search/Image?key=A85\" alt=\"A85\" style=\"max-height:24px; max-width: 28px;\" /> A85",
            "display": "A85"
        },
        {
            "id": "A87",
            "text": "A87",
            "html": "<img src=\"/Search/Image?key=A87\" alt=\"A87\" style=\"max-height:24px; max-width: 28px;\" /> A87",
            "display": "A87"
        },
        {
            "id": "A88",
            "text": "A88",
            "html": "<img src=\"/Search/Image?key=A88\" alt=\"A88\" style=\"max-height:24px; max-width: 28px;\" /> A88",
            "display": "A88"
        },
        {
            "id": "A9",
            "text": "A9: seated man with W10 on head",
            "html": "<span class=\"uni\">&#x1300B;</span> A9: seated man with W10 on head",
            "display": "A9"
        },
        {
            "id": "A90",
            "text": "A90",
            "html": "<img src=\"/Search/Image?key=A90\" alt=\"A90\" style=\"max-height:24px; max-width: 28px;\" /> A90",
            "display": "A90"
        },
        {
            "id": "A90c",
            "text": "A90C",
            "html": "<img src=\"/Search/Image?key=A90C\" alt=\"A90C\" style=\"max-height:24px; max-width: 28px;\" /> A90C",
            "display": "A90c"
        },
        {
            "id": "A90d",
            "text": "A90D",
            "html": "<img src=\"/Search/Image?key=A90D\" alt=\"A90D\" style=\"max-height:24px; max-width: 28px;\" /> A90D",
            "display": "A90d"
        },
        {
            "id": "A95",
            "text": "A95",
            "html": "<img src=\"/Search/Image?key=A95\" alt=\"A95\" style=\"max-height:24px; max-width: 28px;\" /> A95",
            "display": "A95"
        },
        {
            "id": "A96",
            "text": "A96",
            "html": "<img src=\"/Search/Image?key=A96\" alt=\"A96\" style=\"max-height:24px; max-width: 28px;\" /> A96",
            "display": "A96"
        },
        {
            "id": "A97",
            "text": "A97",
            "html": "<img src=\"/Search/Image?key=A97\" alt=\"A97\" style=\"max-height:24px; max-width: 28px;\" /> A97",
            "display": "A97"
        },
        {
            "id": "A98",
            "text": "A98",
            "html": "<img src=\"/Search/Image?key=A98\" alt=\"A98\" style=\"max-height:24px; max-width: 28px;\" /> A98",
            "display": "A98"
        },
        {
            "id": "B1",
            "text": "B1: seated woman",
            "html": "<span class=\"uni\">&#x13050;</span> B1: seated woman",
            "display": "B1"
        },
        {
            "id": "B12",
            "text": "B12",
            "html": "<img src=\"/Search/Image?key=B12\" alt=\"B12\" style=\"max-height:24px; max-width: 28px;\" /> B12",
            "display": "B12"
        },
        {
            "id": "B13a",
            "text": "B13A",
            "html": "<img src=\"/Search/Image?key=B13A\" alt=\"B13A\" style=\"max-height:24px; max-width: 28px;\" /> B13A",
            "display": "B13a"
        },
        {
            "id": "B18",
            "text": "B18",
            "html": "<img src=\"/Search/Image?key=B18\" alt=\"B18\" style=\"max-height:24px; max-width: 28px;\" /> B18",
            "display": "B18"
        },
        {
            "id": "B18a",
            "text": "B18A",
            "html": "<img src=\"/Search/Image?key=B18A\" alt=\"B18A\" style=\"max-height:24px; max-width: 28px;\" /> B18A",
            "display": "B18a"
        },
        {
            "id": "B19",
            "text": "B19",
            "html": "<img src=\"/Search/Image?key=B19\" alt=\"B19\" style=\"max-height:24px; max-width: 28px;\" /> B19",
            "display": "B19"
        },
        {
            "id": "B1a",
            "text": "B1A: seated woman",
            "html": "<img src=\"/Search/Image?key=B1A\" alt=\"B1A\" style=\"max-height:24px; max-width: 28px;\" /> B1A: seated woman",
            "display": "B1a"
        },
        {
            "id": "B1g",
            "text": "B1G: seated woman",
            "html": "<img src=\"/Search/Image?key=B1G\" alt=\"B1G\" style=\"max-height:24px; max-width: 28px;\" /> B1G: seated woman",
            "display": "B1g"
        },
        {
            "id": "B1h",
            "text": "B1H: seated woman",
            "html": "<img src=\"/Search/Image?key=B1H\" alt=\"B1H\" style=\"max-height:24px; max-width: 28px;\" /> B1H: seated woman",
            "display": "B1h"
        },
        {
            "id": "B2",
            "text": "B2: pregnant woman",
            "html": "<span class=\"uni\">&#x13051;</span> B2: pregnant woman",
            "display": "B2"
        },
        {
            "id": "B21b",
            "text": "B21B",
            "html": "<img src=\"/Search/Image?key=B21B\" alt=\"B21B\" style=\"max-height:24px; max-width: 28px;\" /> B21B",
            "display": "B21b"
        },
        {
            "id": "B24",
            "text": "B24",
            "html": "<img src=\"/Search/Image?key=B24\" alt=\"B24\" style=\"max-height:24px; max-width: 28px;\" /> B24",
            "display": "B24"
        },
        {
            "id": "B28",
            "text": "B28",
            "html": "<img src=\"/Search/Image?key=B28\" alt=\"B28\" style=\"max-height:24px; max-width: 28px;\" /> B28",
            "display": "B28"
        },
        {
            "id": "B2a",
            "text": "B2A: pregnant woman",
            "html": "<img src=\"/Search/Image?key=B2A\" alt=\"B2A\" style=\"max-height:24px; max-width: 28px;\" /> B2A: pregnant woman",
            "display": "B2a"
        },
        {
            "id": "B3",
            "text": "B3: woman giving birth [msi]",
            "html": "<span class=\"uni\">&#x13052;</span> B3: woman giving birth",
            "display": "B3"
        },
        {
            "id": "B37",
            "text": "B37",
            "html": "<img src=\"/Search/Image?key=B37\" alt=\"B37\" style=\"max-height:24px; max-width: 28px;\" /> B37",
            "display": "B37"
        },
        {
            "id": "B39a",
            "text": "B39A",
            "html": "<img src=\"/Search/Image?key=B39A\" alt=\"B39A\" style=\"max-height:24px; max-width: 28px;\" /> B39A",
            "display": "B39a"
        },
        {
            "id": "B4",
            "text": "B4: combination of B3 and F31",
            "html": "<span class=\"uni\">&#x13053;</span> B4: combination of B3 and F31",
            "display": "B4"
        },
        {
            "id": "B45a",
            "text": "B45A",
            "html": "<img src=\"/Search/Image?key=B45A\" alt=\"B45A\" style=\"max-height:24px; max-width: 28px;\" /> B45A",
            "display": "B45a"
        },
        {
            "id": "B47",
            "text": "B47",
            "html": "<img src=\"/Search/Image?key=B47\" alt=\"B47\" style=\"max-height:24px; max-width: 28px;\" /> B47",
            "display": "B47"
        },
        {
            "id": "B5",
            "text": "B5: woman suckling child",
            "html": "<span class=\"uni\">&#x13054;</span> B5: woman suckling child",
            "display": "B5"
        },
        {
            "id": "B53",
            "text": "B53",
            "html": "<img src=\"/Search/Image?key=B53\" alt=\"B53\" style=\"max-height:24px; max-width: 28px;\" /> B53",
            "display": "B53"
        },
        {
            "id": "B59",
            "text": "B59",
            "html": "<img src=\"/Search/Image?key=B59\" alt=\"B59\" style=\"max-height:24px; max-width: 28px;\" /> B59",
            "display": "B59"
        },
        {
            "id": "B5d",
            "text": "B5D: woman suckling child",
            "html": "<img src=\"/Search/Image?key=B5D\" alt=\"B5D\" style=\"max-height:24px; max-width: 28px;\" /> B5D: woman suckling child",
            "display": "B5d"
        },
        {
            "id": "B6",
            "text": "B6: woman on chair with child on lap",
            "html": "<span class=\"uni\">&#x13056;</span> B6: woman on chair with child on lap",
            "display": "B6"
        },
        {
            "id": "B64",
            "text": "B64",
            "html": "<img src=\"/Search/Image?key=B64\" alt=\"B64\" style=\"max-height:24px; max-width: 28px;\" /> B64",
            "display": "B64"
        },
        {
            "id": "B73",
            "text": "B73",
            "html": "<img src=\"/Search/Image?key=B73\" alt=\"B73\" style=\"max-height:24px; max-width: 28px;\" /> B73",
            "display": "B73"
        },
        {
            "id": "B76",
            "text": "B76",
            "html": "<img src=\"/Search/Image?key=B76\" alt=\"B76\" style=\"max-height:24px; max-width: 28px;\" /> B76",
            "display": "B76"
        },
        {
            "id": "B77",
            "text": "B77",
            "html": "<img src=\"/Search/Image?key=B77\" alt=\"B77\" style=\"max-height:24px; max-width: 28px;\" /> B77",
            "display": "B77"
        },
        {
            "id": "B77a",
            "text": "B77A",
            "html": "<img src=\"/Search/Image?key=B77A\" alt=\"B77A\" style=\"max-height:24px; max-width: 28px;\" /> B77A",
            "display": "B77a"
        },
        {
            "id": "B7a",
            "text": "B7A: queen wearing diadem and holding flower",
            "html": "<img src=\"/Search/Image?key=B7A\" alt=\"B7A\" style=\"max-height:24px; max-width: 28px;\" /> B7A: queen wearing diadem and holding flower",
            "display": "B7a"
        },
        {
            "id": "B7c",
            "text": "B7C: queen wearing diadem and holding flower",
            "html": "<img src=\"/Search/Image?key=B7C\" alt=\"B7C\" style=\"max-height:24px; max-width: 28px;\" /> B7C: queen wearing diadem and holding flower",
            "display": "B7c"
        },
        {
            "id": "B7e",
            "text": "B7E: queen wearing diadem and holding flower",
            "html": "<img src=\"/Search/Image?key=B7E\" alt=\"B7E\" style=\"max-height:24px; max-width: 28px;\" /> B7E: queen wearing diadem and holding flower",
            "display": "B7e"
        },
        {
            "id": "B8f",
            "text": "B8F: woman holding M9",
            "html": "<img src=\"/Search/Image?key=B8F\" alt=\"B8F\" style=\"max-height:24px; max-width: 28px;\" /> B8F: woman holding M9",
            "display": "B8f"
        },
        {
            "id": "B8g",
            "text": "B8G: woman holding M9",
            "html": "<img src=\"/Search/Image?key=B8G\" alt=\"B8G\" style=\"max-height:24px; max-width: 28px;\" /> B8G: woman holding M9",
            "display": "B8g"
        },
        {
            "id": "C1",
            "text": "C1: god with N6",
            "html": "<span class=\"uni\">&#x1305A;</span> C1: god with N6",
            "display": "C1"
        },
        {
            "id": "C10",
            "text": "C10: goddess with feather on head [mAat]",
            "html": "<span class=\"uni\">&#x13066;</span> C10: goddess with feather on head",
            "display": "C10"
        },
        {
            "id": "C104",
            "text": "C104",
            "html": "<img src=\"/Search/Image?key=C104\" alt=\"C104\" style=\"max-height:24px; max-width: 28px;\" /> C104",
            "display": "C104"
        },
        {
            "id": "C10a",
            "text": "C10A: goddess with feather on head holding S34",
            "html": "<span class=\"uni\">&#x13067;</span> C10A: goddess with feather on head holding S34",
            "display": "C10a"
        },
        {
            "id": "C11",
            "text": "C11: god with arms supporting (the sky) and M4 on head [HH]",
            "html": "<span class=\"uni\">&#x13068;</span> C11: god with arms supporting (the sky) and M4 on head",
            "display": "C11"
        },
        {
            "id": "C111c",
            "text": "C111C",
            "html": "<img src=\"/Search/Image?key=C111C\" alt=\"C111C\" style=\"max-height:24px; max-width: 28px;\" /> C111C",
            "display": "C111c"
        },
        {
            "id": "C114a",
            "text": "C114A",
            "html": "<img src=\"/Search/Image?key=C114A\" alt=\"C114A\" style=\"max-height:24px; max-width: 28px;\" /> C114A",
            "display": "C114a"
        },
        {
            "id": "C118",
            "text": "C118",
            "html": "<img src=\"/Search/Image?key=C118\" alt=\"C118\" style=\"max-height:24px; max-width: 28px;\" /> C118",
            "display": "C118"
        },
        {
            "id": "C12a",
            "text": "C12A: god with S9 and S40",
            "html": "<img src=\"/Search/Image?key=C12A\" alt=\"C12A\" style=\"max-height:24px; max-width: 28px;\" /> C12A: god with S9 and S40",
            "display": "C12a"
        },
        {
            "id": "C12k",
            "text": "C12K: god with S9 and S40",
            "html": "<img src=\"/Search/Image?key=C12K\" alt=\"C12K\" style=\"max-height:24px; max-width: 28px;\" /> C12K: god with S9 and S40",
            "display": "C12k"
        },
        {
            "id": "C138",
            "text": "C138",
            "html": "<img src=\"/Search/Image?key=C138\" alt=\"C138\" style=\"max-height:24px; max-width: 28px;\" /> C138",
            "display": "C138"
        },
        {
            "id": "C159",
            "text": "C159",
            "html": "<img src=\"/Search/Image?key=C159\" alt=\"C159\" style=\"max-height:24px; max-width: 28px;\" /> C159",
            "display": "C159"
        },
        {
            "id": "C164",
            "text": "C164",
            "html": "<img src=\"/Search/Image?key=C164\" alt=\"C164\" style=\"max-height:24px; max-width: 28px;\" /> C164",
            "display": "C164"
        },
        {
            "id": "C17",
            "text": "C17: god with head of falcon and S9",
            "html": "<span class=\"uni\">&#x1306E;</span> C17: god with head of falcon and S9",
            "display": "C17"
        },
        {
            "id": "C190",
            "text": "C190",
            "html": "<img src=\"/Search/Image?key=C190\" alt=\"C190\" style=\"max-height:24px; max-width: 28px;\" /> C190",
            "display": "C190"
        },
        {
            "id": "C195a",
            "text": "C195A",
            "html": "<img src=\"/Search/Image?key=C195A\" alt=\"C195A\" style=\"max-height:24px; max-width: 28px;\" /> C195A",
            "display": "C195a"
        },
        {
            "id": "C19c",
            "text": "C19C: mummy-shaped god",
            "html": "<img src=\"/Search/Image?key=C19C\" alt=\"C19C\" style=\"max-height:24px; max-width: 28px;\" /> C19C: mummy-shaped god",
            "display": "C19c"
        },
        {
            "id": "C2",
            "text": "C2: god with head of falcon with sun on head and holding S34",
            "html": "<span class=\"uni\">&#x1305B;</span> C2: god with head of falcon with sun on head and holding S34",
            "display": "C2"
        },
        {
            "id": "C20",
            "text": "C20: mummy-shaped god in shrine",
            "html": "<span class=\"uni\">&#x13071;</span> C20: mummy-shaped god in shrine",
            "display": "C20"
        },
        {
            "id": "C219",
            "text": "C219",
            "html": "<img src=\"/Search/Image?key=C219\" alt=\"C219\" style=\"max-height:24px; max-width: 28px;\" /> C219",
            "display": "C219"
        },
        {
            "id": "C229",
            "text": "C229",
            "html": "<img src=\"/Search/Image?key=C229\" alt=\"C229\" style=\"max-height:24px; max-width: 28px;\" /> C229",
            "display": "C229"
        },
        {
            "id": "C232",
            "text": "C232",
            "html": "<img src=\"/Search/Image?key=C232\" alt=\"C232\" style=\"max-height:24px; max-width: 28px;\" /> C232",
            "display": "C232"
        },
        {
            "id": "C248",
            "text": "C248",
            "html": "<img src=\"/Search/Image?key=C248\" alt=\"C248\" style=\"max-height:24px; max-width: 28px;\" /> C248",
            "display": "C248"
        },
        {
            "id": "C2a",
            "text": "C2A: god with head of falcon with sun on head",
            "html": "<span class=\"uni\">&#x1305C;</span> C2A: god with head of falcon with sun on head",
            "display": "C2a"
        },
        {
            "id": "C3",
            "text": "C3: god with head of ibis [DHwty]",
            "html": "<span class=\"uni\">&#x1305F;</span> C3: god with head of ibis",
            "display": "C3"
        },
        {
            "id": "C35",
            "text": "C35",
            "html": "<img src=\"/Search/Image?key=C35\" alt=\"C35\" style=\"max-height:24px; max-width: 28px;\" /> C35",
            "display": "C35"
        },
        {
            "id": "C4",
            "text": "C4: god with head of ram [Xnmw]",
            "html": "<span class=\"uni\">&#x13060;</span> C4: god with head of ram",
            "display": "C4"
        },
        {
            "id": "C6",
            "text": "C6: god with head of jackal [inpw]",
            "html": "<span class=\"uni\">&#x13062;</span> C6: god with head of jackal",
            "display": "C6"
        },
        {
            "id": "C7",
            "text": "C7: god with head of Seth-animal [stX]",
            "html": "<span class=\"uni\">&#x13063;</span> C7: god with head of Seth-animal",
            "display": "C7"
        },
        {
            "id": "C8a",
            "text": "C8A: ithyphallic god with S9, uplifted arm and S45",
            "html": "<img src=\"/Search/Image?key=C8A\" alt=\"C8A\" style=\"max-height:24px; max-width: 28px;\" /> C8A: ithyphallic god with S9, uplifted arm and S45",
            "display": "C8a"
        },
        {
            "id": "C9",
            "text": "C9: goddess with sun and horns",
            "html": "<span class=\"uni\">&#x13065;</span> C9: goddess with sun and horns",
            "display": "C9"
        },
        {
            "id": "C98a",
            "text": "C98A",
            "html": "<img src=\"/Search/Image?key=C98A\" alt=\"C98A\" style=\"max-height:24px; max-width: 28px;\" /> C98A",
            "display": "C98a"
        },
        {
            "id": "C98b",
            "text": "C98B",
            "html": "<img src=\"/Search/Image?key=C98B\" alt=\"C98B\" style=\"max-height:24px; max-width: 28px;\" /> C98B",
            "display": "C98b"
        },
        {
            "id": "C99b",
            "text": "C99B",
            "html": "<img src=\"/Search/Image?key=C99B\" alt=\"C99B\" style=\"max-height:24px; max-width: 28px;\" /> C99B",
            "display": "C99b"
        },
        {
            "id": "C9a",
            "text": "C9A: goddess with sun and horns",
            "html": "<img src=\"/Search/Image?key=C9A\" alt=\"C9A\" style=\"max-height:24px; max-width: 28px;\" /> C9A: goddess with sun and horns",
            "display": "C9a"
        },
        {
            "id": "C9i",
            "text": "C9I: goddess with sun and horns",
            "html": "<img src=\"/Search/Image?key=C9I\" alt=\"C9I\" style=\"max-height:24px; max-width: 28px;\" /> C9I: goddess with sun and horns",
            "display": "C9i"
        },
        {
            "id": "D1",
            "text": "D1: head in profile [tp]",
            "html": "<span class=\"uni\">&#x13076;</span> D1: head in profile",
            "display": "D1"
        },
        {
            "id": "D10",
            "text": "D10: <span class=\"egytransl\">wDAt</span>-eye [wDAt]",
            "html": "<span class=\"uni\">&#x13080;</span> D10: <span class=\"egytransl\">wDAt</span>-eye",
            "display": "D10"
        },
        {
            "id": "D100",
            "text": "D100",
            "html": "<img src=\"/Search/Image?key=D100\" alt=\"D100\" style=\"max-height:24px; max-width: 28px;\" /> D100",
            "display": "D100"
        },
        {
            "id": "D101",
            "text": "D101",
            "html": "<img src=\"/Search/Image?key=D101\" alt=\"D101\" style=\"max-height:24px; max-width: 28px;\" /> D101",
            "display": "D101"
        },
        {
            "id": "D105",
            "text": "D105",
            "html": "<img src=\"/Search/Image?key=D105\" alt=\"D105\" style=\"max-height:24px; max-width: 28px;\" /> D105",
            "display": "D105"
        },
        {
            "id": "D106",
            "text": "D106",
            "html": "<img src=\"/Search/Image?key=D106\" alt=\"D106\" style=\"max-height:24px; max-width: 28px;\" /> D106",
            "display": "D106"
        },
        {
            "id": "D108",
            "text": "D108",
            "html": "<img src=\"/Search/Image?key=D108\" alt=\"D108\" style=\"max-height:24px; max-width: 28px;\" /> D108",
            "display": "D108"
        },
        {
            "id": "D109",
            "text": "D109",
            "html": "<img src=\"/Search/Image?key=D109\" alt=\"D109\" style=\"max-height:24px; max-width: 28px;\" /> D109",
            "display": "D109"
        },
        {
            "id": "D10c",
            "text": "D10C: <span class=\"egytransl\">wDAt</span>-eye",
            "html": "<img src=\"/Search/Image?key=D10C\" alt=\"D10C\" style=\"max-height:24px; max-width: 28px;\" /> D10C: <span class=\"egytransl\">wDAt</span>-eye",
            "display": "D10c"
        },
        {
            "id": "D11",
            "text": "D11: left part of white of D10 [narrow]",
            "html": "<span class=\"uni\">&#x13081;</span> D11: left part of white of D10",
            "display": "D11"
        },
        {
            "id": "D113",
            "text": "D113",
            "html": "<img src=\"/Search/Image?key=D113\" alt=\"D113\" style=\"max-height:24px; max-width: 28px;\" /> D113",
            "display": "D113"
        },
        {
            "id": "D115",
            "text": "D115",
            "html": "<img src=\"/Search/Image?key=D115\" alt=\"D115\" style=\"max-height:24px; max-width: 28px;\" /> D115",
            "display": "D115"
        },
        {
            "id": "D117",
            "text": "D117",
            "html": "<img src=\"/Search/Image?key=D117\" alt=\"D117\" style=\"max-height:24px; max-width: 28px;\" /> D117",
            "display": "D117"
        },
        {
            "id": "D118",
            "text": "D118",
            "html": "<img src=\"/Search/Image?key=D118\" alt=\"D118\" style=\"max-height:24px; max-width: 28px;\" /> D118",
            "display": "D118"
        },
        {
            "id": "D12",
            "text": "D12: pupil of eye [narrow]",
            "html": "<span class=\"uni\">&#x13082;</span> D12: pupil of eye",
            "display": "D12"
        },
        {
            "id": "D120",
            "text": "D120",
            "html": "<img src=\"/Search/Image?key=D120\" alt=\"D120\" style=\"max-height:24px; max-width: 28px;\" /> D120",
            "display": "D120"
        },
        {
            "id": "D126",
            "text": "D126",
            "html": "<img src=\"/Search/Image?key=D126\" alt=\"D126\" style=\"max-height:24px; max-width: 28px;\" /> D126",
            "display": "D126"
        },
        {
            "id": "D128",
            "text": "D128",
            "html": "<img src=\"/Search/Image?key=D128\" alt=\"D128\" style=\"max-height:24px; max-width: 28px;\" /> D128",
            "display": "D128"
        },
        {
            "id": "D13",
            "text": "D13: eye-brow [broad]",
            "html": "<span class=\"uni\">&#x13083;</span> D13: eye-brow",
            "display": "D13"
        },
        {
            "id": "D130",
            "text": "D130",
            "html": "<img src=\"/Search/Image?key=D130\" alt=\"D130\" style=\"max-height:24px; max-width: 28px;\" /> D130",
            "display": "D130"
        },
        {
            "id": "D131",
            "text": "D131",
            "html": "<img src=\"/Search/Image?key=D131\" alt=\"D131\" style=\"max-height:24px; max-width: 28px;\" /> D131",
            "display": "D131"
        },
        {
            "id": "D132",
            "text": "D132",
            "html": "<img src=\"/Search/Image?key=D132\" alt=\"D132\" style=\"max-height:24px; max-width: 28px;\" /> D132",
            "display": "D132"
        },
        {
            "id": "D133",
            "text": "D133",
            "html": "<img src=\"/Search/Image?key=D133\" alt=\"D133\" style=\"max-height:24px; max-width: 28px;\" /> D133",
            "display": "D133"
        },
        {
            "id": "D134",
            "text": "D134",
            "html": "<img src=\"/Search/Image?key=D134\" alt=\"D134\" style=\"max-height:24px; max-width: 28px;\" /> D134",
            "display": "D134"
        },
        {
            "id": "D14",
            "text": "D14: right part of white of D10 [broad]",
            "html": "<span class=\"uni\">&#x13084;</span> D14: right part of white of D10",
            "display": "D14"
        },
        {
            "id": "D141",
            "text": "D141",
            "html": "<img src=\"/Search/Image?key=D141\" alt=\"D141\" style=\"max-height:24px; max-width: 28px;\" /> D141",
            "display": "D141"
        },
        {
            "id": "D143",
            "text": "D143",
            "html": "<img src=\"/Search/Image?key=D143\" alt=\"D143\" style=\"max-height:24px; max-width: 28px;\" /> D143",
            "display": "D143"
        },
        {
            "id": "D143b",
            "text": "D143B",
            "html": "<img src=\"/Search/Image?key=D143B\" alt=\"D143B\" style=\"max-height:24px; max-width: 28px;\" /> D143B",
            "display": "D143b"
        },
        {
            "id": "D146",
            "text": "D146",
            "html": "<img src=\"/Search/Image?key=D146\" alt=\"D146\" style=\"max-height:24px; max-width: 28px;\" /> D146",
            "display": "D146"
        },
        {
            "id": "D147",
            "text": "D147",
            "html": "<img src=\"/Search/Image?key=D147\" alt=\"D147\" style=\"max-height:24px; max-width: 28px;\" /> D147",
            "display": "D147"
        },
        {
            "id": "D15",
            "text": "D15: diagonal marking of D10 [broad]",
            "html": "<span class=\"uni\">&#x13085;</span> D15: diagonal marking of D10",
            "display": "D15"
        },
        {
            "id": "D152",
            "text": "D152",
            "html": "<img src=\"/Search/Image?key=D152\" alt=\"D152\" style=\"max-height:24px; max-width: 28px;\" /> D152",
            "display": "D152"
        },
        {
            "id": "D153",
            "text": "D153",
            "html": "<img src=\"/Search/Image?key=D153\" alt=\"D153\" style=\"max-height:24px; max-width: 28px;\" /> D153",
            "display": "D153"
        },
        {
            "id": "D154",
            "text": "D154",
            "html": "<img src=\"/Search/Image?key=D154\" alt=\"D154\" style=\"max-height:24px; max-width: 28px;\" /> D154",
            "display": "D154"
        },
        {
            "id": "D154a",
            "text": "D154A",
            "html": "<img src=\"/Search/Image?key=D154A\" alt=\"D154A\" style=\"max-height:24px; max-width: 28px;\" /> D154A",
            "display": "D154a"
        },
        {
            "id": "D156",
            "text": "D156",
            "html": "<img src=\"/Search/Image?key=D156\" alt=\"D156\" style=\"max-height:24px; max-width: 28px;\" /> D156",
            "display": "D156"
        },
        {
            "id": "D159",
            "text": "D159",
            "html": "<img src=\"/Search/Image?key=D159\" alt=\"D159\" style=\"max-height:24px; max-width: 28px;\" /> D159",
            "display": "D159"
        },
        {
            "id": "D16",
            "text": "D16: vertical marking of D10 [tall]",
            "html": "<span class=\"uni\">&#x13086;</span> D16: vertical marking of D10",
            "display": "D16"
        },
        {
            "id": "D17",
            "text": "D17: combination of D16 and D15 [broad]",
            "html": "<span class=\"uni\">&#x13087;</span> D17: combination of D16 and D15",
            "display": "D17"
        },
        {
            "id": "D170a",
            "text": "D170A",
            "html": "<img src=\"/Search/Image?key=D170A\" alt=\"D170A\" style=\"max-height:24px; max-width: 28px;\" /> D170A",
            "display": "D170a"
        },
        {
            "id": "D18",
            "text": "D18: ear",
            "html": "<span class=\"uni\">&#x13088;</span> D18: ear",
            "display": "D18"
        },
        {
            "id": "D189",
            "text": "D189",
            "html": "<img src=\"/Search/Image?key=D189\" alt=\"D189\" style=\"max-height:24px; max-width: 28px;\" /> D189",
            "display": "D189"
        },
        {
            "id": "D19",
            "text": "D19: nose, eye and cheek [fnD]",
            "html": "<span class=\"uni\">&#x13089;</span> D19: nose, eye and cheek",
            "display": "D19"
        },
        {
            "id": "D190",
            "text": "D190",
            "html": "<img src=\"/Search/Image?key=D190\" alt=\"D190\" style=\"max-height:24px; max-width: 28px;\" /> D190",
            "display": "D190"
        },
        {
            "id": "D191",
            "text": "D191",
            "html": "<img src=\"/Search/Image?key=D191\" alt=\"D191\" style=\"max-height:24px; max-width: 28px;\" /> D191",
            "display": "D191"
        },
        {
            "id": "D193",
            "text": "D193",
            "html": "<img src=\"/Search/Image?key=D193\" alt=\"D193\" style=\"max-height:24px; max-width: 28px;\" /> D193",
            "display": "D193"
        },
        {
            "id": "D2",
            "text": "D2: face [Hr]",
            "html": "<span class=\"uni\">&#x13077;</span> D2: face",
            "display": "D2"
        },
        {
            "id": "D20",
            "text": "D20: nose, eye and cheek in semi-cursive form",
            "html": "<span class=\"uni\">&#x1308A;</span> D20: nose, eye and cheek in semi-cursive form",
            "display": "D20"
        },
        {
            "id": "D200",
            "text": "D200",
            "html": "<img src=\"/Search/Image?key=D200\" alt=\"D200\" style=\"max-height:24px; max-width: 28px;\" /> D200",
            "display": "D200"
        },
        {
            "id": "D206",
            "text": "D206",
            "html": "<img src=\"/Search/Image?key=D206\" alt=\"D206\" style=\"max-height:24px; max-width: 28px;\" /> D206",
            "display": "D206"
        },
        {
            "id": "D207",
            "text": "D207",
            "html": "<img src=\"/Search/Image?key=D207\" alt=\"D207\" style=\"max-height:24px; max-width: 28px;\" /> D207",
            "display": "D207"
        },
        {
            "id": "D21",
            "text": "D21: mouth [broad] [r]",
            "html": "<span class=\"uni\">&#x1308B;</span> D21: mouth",
            "display": "D21"
        },
        {
            "id": "D210",
            "text": "D210",
            "html": "<img src=\"/Search/Image?key=D210\" alt=\"D210\" style=\"max-height:24px; max-width: 28px;\" /> D210",
            "display": "D210"
        },
        {
            "id": "D212a",
            "text": "D212A",
            "html": "<img src=\"/Search/Image?key=D212A\" alt=\"D212A\" style=\"max-height:24px; max-width: 28px;\" /> D212A",
            "display": "D212a"
        },
        {
            "id": "D217",
            "text": "D217",
            "html": "<img src=\"/Search/Image?key=D217\" alt=\"D217\" style=\"max-height:24px; max-width: 28px;\" /> D217",
            "display": "D217"
        },
        {
            "id": "D218",
            "text": "D218",
            "html": "<img src=\"/Search/Image?key=D218\" alt=\"D218\" style=\"max-height:24px; max-width: 28px;\" /> D218",
            "display": "D218"
        },
        {
            "id": "D22",
            "text": "D22: mouth with two strokes [broad]",
            "html": "<span class=\"uni\">&#x1308C;</span> D22: mouth with two strokes",
            "display": "D22"
        },
        {
            "id": "D228",
            "text": "D228",
            "html": "<img src=\"/Search/Image?key=D228\" alt=\"D228\" style=\"max-height:24px; max-width: 28px;\" /> D228",
            "display": "D228"
        },
        {
            "id": "D23",
            "text": "D23: mouth with three strokes",
            "html": "<span class=\"uni\">&#x1308D;</span> D23: mouth with three strokes",
            "display": "D23"
        },
        {
            "id": "D235",
            "text": "D235",
            "html": "<img src=\"/Search/Image?key=D235\" alt=\"D235\" style=\"max-height:24px; max-width: 28px;\" /> D235",
            "display": "D235"
        },
        {
            "id": "D24",
            "text": "D24: upper lip with teeth [broad] [spt]",
            "html": "<span class=\"uni\">&#x1308E;</span> D24: upper lip with teeth",
            "display": "D24"
        },
        {
            "id": "D245",
            "text": "D245",
            "html": "<img src=\"/Search/Image?key=D245\" alt=\"D245\" style=\"max-height:24px; max-width: 28px;\" /> D245",
            "display": "D245"
        },
        {
            "id": "D248",
            "text": "D248",
            "html": "<img src=\"/Search/Image?key=D248\" alt=\"D248\" style=\"max-height:24px; max-width: 28px;\" /> D248",
            "display": "D248"
        },
        {
            "id": "D249",
            "text": "D249",
            "html": "D249",
            "display": "D249"
        },
        {
            "id": "D25",
            "text": "D25: lips with teeth [broad] [spty]",
            "html": "<span class=\"uni\">&#x1308F;</span> D25: lips with teeth",
            "display": "D25"
        },
        {
            "id": "D253",
            "text": "D253",
            "html": "<img src=\"/Search/Image?key=D253\" alt=\"D253\" style=\"max-height:24px; max-width: 28px;\" /> D253",
            "display": "D253"
        },
        {
            "id": "D254",
            "text": "D254",
            "html": "<img src=\"/Search/Image?key=D254\" alt=\"D254\" style=\"max-height:24px; max-width: 28px;\" /> D254",
            "display": "D254"
        },
        {
            "id": "D258",
            "text": "D258",
            "html": "<img src=\"/Search/Image?key=D258\" alt=\"D258\" style=\"max-height:24px; max-width: 28px;\" /> D258",
            "display": "D258"
        },
        {
            "id": "D26",
            "text": "D26: liquid issuing from lips [narrow]",
            "html": "<span class=\"uni\">&#x13090;</span> D26: liquid issuing from lips",
            "display": "D26"
        },
        {
            "id": "D266",
            "text": "D266",
            "html": "<img src=\"/Search/Image?key=D266\" alt=\"D266\" style=\"max-height:24px; max-width: 28px;\" /> D266",
            "display": "D266"
        },
        {
            "id": "D267",
            "text": "D267",
            "html": "<img src=\"/Search/Image?key=D267\" alt=\"D267\" style=\"max-height:24px; max-width: 28px;\" /> D267",
            "display": "D267"
        },
        {
            "id": "D26a",
            "text": "D26A: liquid issuing from lips",
            "html": "<img src=\"/Search/Image?key=D26A\" alt=\"D26A\" style=\"max-height:24px; max-width: 28px;\" /> D26A: liquid issuing from lips",
            "display": "D26a"
        },
        {
            "id": "D26b",
            "text": "D26B: liquid issuing from lips",
            "html": "<img src=\"/Search/Image?key=D26B\" alt=\"D26B\" style=\"max-height:24px; max-width: 28px;\" /> D26B: liquid issuing from lips",
            "display": "D26b"
        },
        {
            "id": "D27",
            "text": "D27: small breast [mnD]",
            "html": "<span class=\"uni\">&#x13091;</span> D27: small breast",
            "display": "D27"
        },
        {
            "id": "D271",
            "text": "D271",
            "html": "<img src=\"/Search/Image?key=D271\" alt=\"D271\" style=\"max-height:24px; max-width: 28px;\" /> D271",
            "display": "D271"
        },
        {
            "id": "D272",
            "text": "D272",
            "html": "<img src=\"/Search/Image?key=D272\" alt=\"D272\" style=\"max-height:24px; max-width: 28px;\" /> D272",
            "display": "D272"
        },
        {
            "id": "D27a",
            "text": "D27A: large breast",
            "html": "<span class=\"uni\">&#x13092;</span> D27A: large breast",
            "display": "D27a"
        },
        {
            "id": "D28",
            "text": "D28: arms in <span class=\"egytransl\">kA</span>-posture [kA]",
            "html": "<span class=\"uni\">&#x13093;</span> D28: arms in <span class=\"egytransl\">kA</span>-posture",
            "display": "D28"
        },
        {
            "id": "D280",
            "text": "D280",
            "html": "<img src=\"/Search/Image?key=D280\" alt=\"D280\" style=\"max-height:24px; max-width: 28px;\" /> D280",
            "display": "D280"
        },
        {
            "id": "D280a",
            "text": "D280A",
            "html": "<img src=\"/Search/Image?key=D280A\" alt=\"D280A\" style=\"max-height:24px; max-width: 28px;\" /> D280A",
            "display": "D280a"
        },
        {
            "id": "D283",
            "text": "D283",
            "html": "<img src=\"/Search/Image?key=D283\" alt=\"D283\" style=\"max-height:24px; max-width: 28px;\" /> D283",
            "display": "D283"
        },
        {
            "id": "D284",
            "text": "D284",
            "html": "<img src=\"/Search/Image?key=D284\" alt=\"D284\" style=\"max-height:24px; max-width: 28px;\" /> D284",
            "display": "D284"
        },
        {
            "id": "D288",
            "text": "D288",
            "html": "<img src=\"/Search/Image?key=D288\" alt=\"D288\" style=\"max-height:24px; max-width: 28px;\" /> D288",
            "display": "D288"
        },
        {
            "id": "D29",
            "text": "D29: combination of D28 and R12",
            "html": "<span class=\"uni\">&#x13094;</span> D29: combination of D28 and R12",
            "display": "D29"
        },
        {
            "id": "D291",
            "text": "D291",
            "html": "<img src=\"/Search/Image?key=D291\" alt=\"D291\" style=\"max-height:24px; max-width: 28px;\" /> D291",
            "display": "D291"
        },
        {
            "id": "D292",
            "text": "D292",
            "html": "<img src=\"/Search/Image?key=D292\" alt=\"D292\" style=\"max-height:24px; max-width: 28px;\" /> D292",
            "display": "D292"
        },
        {
            "id": "D293",
            "text": "D293",
            "html": "<img src=\"/Search/Image?key=D293\" alt=\"D293\" style=\"max-height:24px; max-width: 28px;\" /> D293",
            "display": "D293"
        },
        {
            "id": "D2a",
            "text": "D2A: face",
            "html": "<img src=\"/Search/Image?key=D2A\" alt=\"D2A\" style=\"max-height:24px; max-width: 28px;\" /> D2A: face",
            "display": "D2a"
        },
        {
            "id": "D3",
            "text": "D3: hair [Sny]",
            "html": "<span class=\"uni\">&#x13078;</span> D3: hair",
            "display": "D3"
        },
        {
            "id": "D30",
            "text": "D30: D28 with tail",
            "html": "<span class=\"uni\">&#x13095;</span> D30: D28 with tail",
            "display": "D30"
        },
        {
            "id": "D304",
            "text": "D304",
            "html": "<img src=\"/Search/Image?key=D304\" alt=\"D304\" style=\"max-height:24px; max-width: 28px;\" /> D304",
            "display": "D304"
        },
        {
            "id": "D307",
            "text": "D307",
            "html": "<img src=\"/Search/Image?key=D307\" alt=\"D307\" style=\"max-height:24px; max-width: 28px;\" /> D307",
            "display": "D307"
        },
        {
            "id": "D31",
            "text": "D31: combination of D32 and U36",
            "html": "<span class=\"uni\">&#x13096;</span> D31: combination of D32 and U36",
            "display": "D31"
        },
        {
            "id": "D310",
            "text": "D310",
            "html": "<img src=\"/Search/Image?key=D310\" alt=\"D310\" style=\"max-height:24px; max-width: 28px;\" /> D310",
            "display": "D310"
        },
        {
            "id": "D312",
            "text": "D312",
            "html": "<img src=\"/Search/Image?key=D312\" alt=\"D312\" style=\"max-height:24px; max-width: 28px;\" /> D312",
            "display": "D312"
        },
        {
            "id": "D313",
            "text": "D313",
            "html": "<img src=\"/Search/Image?key=D313\" alt=\"D313\" style=\"max-height:24px; max-width: 28px;\" /> D313",
            "display": "D313"
        },
        {
            "id": "D318",
            "text": "D318",
            "html": "<img src=\"/Search/Image?key=D318\" alt=\"D318\" style=\"max-height:24px; max-width: 28px;\" /> D318",
            "display": "D318"
        },
        {
            "id": "D32",
            "text": "D32: arms embracing",
            "html": "<span class=\"uni\">&#x13098;</span> D32: arms embracing",
            "display": "D32"
        },
        {
            "id": "D327",
            "text": "D327",
            "html": "<img src=\"/Search/Image?key=D327\" alt=\"D327\" style=\"max-height:24px; max-width: 28px;\" /> D327",
            "display": "D327"
        },
        {
            "id": "D328",
            "text": "D328",
            "html": "<img src=\"/Search/Image?key=D328\" alt=\"D328\" style=\"max-height:24px; max-width: 28px;\" /> D328",
            "display": "D328"
        },
        {
            "id": "D33",
            "text": "D33: arms rowing",
            "html": "<span class=\"uni\">&#x13099;</span> D33: arms rowing",
            "display": "D33"
        },
        {
            "id": "D33b",
            "text": "D33B: arms rowing",
            "html": "<img src=\"/Search/Image?key=D33B\" alt=\"D33B\" style=\"max-height:24px; max-width: 28px;\" /> D33B: arms rowing",
            "display": "D33b"
        },
        {
            "id": "D34",
            "text": "D34: arms holding shield and battle-axe [aHA]",
            "html": "<span class=\"uni\">&#x1309A;</span> D34: arms holding shield and battle-axe",
            "display": "D34"
        },
        {
            "id": "D343",
            "text": "D343",
            "html": "<img src=\"/Search/Image?key=D343\" alt=\"D343\" style=\"max-height:24px; max-width: 28px;\" /> D343",
            "display": "D343"
        },
        {
            "id": "D34a",
            "text": "D34A: arms holding shield and mace",
            "html": "<span class=\"uni\">&#x1309B;</span> D34A: arms holding shield and mace",
            "display": "D34a"
        },
        {
            "id": "D35",
            "text": "D35: arms in gesture of negation",
            "html": "<span class=\"uni\">&#x1309C;</span> D35: arms in gesture of negation",
            "display": "D35"
        },
        {
            "id": "D350",
            "text": "D350",
            "html": "<img src=\"/Search/Image?key=D350\" alt=\"D350\" style=\"max-height:24px; max-width: 28px;\" /> D350",
            "display": "D350"
        },
        {
            "id": "D35a",
            "text": "D35A: arms in gesture of negation",
            "html": "<img src=\"/Search/Image?key=D35A\" alt=\"D35A\" style=\"max-height:24px; max-width: 28px;\" /> D35A: arms in gesture of negation",
            "display": "D35a"
        },
        {
            "id": "D36",
            "text": "D36: forearm [a]",
            "html": "<span class=\"uni\">&#x1309D;</span> D36: forearm",
            "display": "D36"
        },
        {
            "id": "D37",
            "text": "D37: forearm with X8",
            "html": "<span class=\"uni\">&#x1309E;</span> D37: forearm with X8",
            "display": "D37"
        },
        {
            "id": "D375",
            "text": "D375",
            "html": "<img src=\"/Search/Image?key=D375\" alt=\"D375\" style=\"max-height:24px; max-width: 28px;\" /> D375",
            "display": "D375"
        },
        {
            "id": "D38",
            "text": "D38: forearm with rounded loaf",
            "html": "<span class=\"uni\">&#x1309F;</span> D38: forearm with rounded loaf",
            "display": "D38"
        },
        {
            "id": "D381",
            "text": "D381",
            "html": "<img src=\"/Search/Image?key=D381\" alt=\"D381\" style=\"max-height:24px; max-width: 28px;\" /> D381",
            "display": "D381"
        },
        {
            "id": "D384",
            "text": "D384",
            "html": "<img src=\"/Search/Image?key=D384\" alt=\"D384\" style=\"max-height:24px; max-width: 28px;\" /> D384",
            "display": "D384"
        },
        {
            "id": "D39",
            "text": "D39: forearm with W24",
            "html": "<span class=\"uni\">&#x130A0;</span> D39: forearm with W24",
            "display": "D39"
        },
        {
            "id": "D396",
            "text": "D396",
            "html": "<img src=\"/Search/Image?key=D396\" alt=\"D396\" style=\"max-height:24px; max-width: 28px;\" /> D396",
            "display": "D396"
        },
        {
            "id": "D3a",
            "text": "D3A: hair",
            "html": "<img src=\"/Search/Image?key=D3A\" alt=\"D3A\" style=\"max-height:24px; max-width: 28px;\" /> D3A: hair",
            "display": "D3a"
        },
        {
            "id": "D4",
            "text": "D4: eye [ir]",
            "html": "<span class=\"uni\">&#x13079;</span> D4: eye",
            "display": "D4"
        },
        {
            "id": "D40",
            "text": "D40: forearm with stick",
            "html": "<span class=\"uni\">&#x130A1;</span> D40: forearm with stick",
            "display": "D40"
        },
        {
            "id": "D403",
            "text": "D403",
            "html": "<img src=\"/Search/Image?key=D403\" alt=\"D403\" style=\"max-height:24px; max-width: 28px;\" /> D403",
            "display": "D403"
        },
        {
            "id": "D41",
            "text": "D41: forearm with palm down and bent upper arm",
            "html": "<span class=\"uni\">&#x130A2;</span> D41: forearm with palm down and bent upper arm",
            "display": "D41"
        },
        {
            "id": "D410",
            "text": "D410",
            "html": "<img src=\"/Search/Image?key=D410\" alt=\"D410\" style=\"max-height:24px; max-width: 28px;\" /> D410",
            "display": "D410"
        },
        {
            "id": "D410a",
            "text": "D410A",
            "html": "<img src=\"/Search/Image?key=D410A\" alt=\"D410A\" style=\"max-height:24px; max-width: 28px;\" /> D410A",
            "display": "D410a"
        },
        {
            "id": "D413",
            "text": "D413",
            "html": "<img src=\"/Search/Image?key=D413\" alt=\"D413\" style=\"max-height:24px; max-width: 28px;\" /> D413",
            "display": "D413"
        },
        {
            "id": "D42",
            "text": "D42: forearm with palm down and straight upper arm",
            "html": "<span class=\"uni\">&#x130A3;</span> D42: forearm with palm down and straight upper arm",
            "display": "D42"
        },
        {
            "id": "D43",
            "text": "D43: forearm with S45",
            "html": "<span class=\"uni\">&#x130A4;</span> D43: forearm with S45",
            "display": "D43"
        },
        {
            "id": "D44",
            "text": "D44: forearm with S42",
            "html": "<span class=\"uni\">&#x130A5;</span> D44: forearm with S42",
            "display": "D44"
        },
        {
            "id": "D45",
            "text": "D45: arm with <span class=\"egytransl\">nHbt</span>-wand [Dsr]",
            "html": "<span class=\"uni\">&#x130A6;</span> D45: arm with <span class=\"egytransl\">nHbt</span>-wand",
            "display": "D45"
        },
        {
            "id": "D46",
            "text": "D46: hand [d]",
            "html": "<span class=\"uni\">&#x130A7;</span> D46: hand",
            "display": "D46"
        },
        {
            "id": "D46a",
            "text": "D46A: liquid falling from hand",
            "html": "<span class=\"uni\">&#x130A8;</span> D46A: liquid falling from hand",
            "display": "D46a"
        },
        {
            "id": "D46c",
            "text": "D46C: hand",
            "html": "<img src=\"/Search/Image?key=D46C\" alt=\"D46C\" style=\"max-height:24px; max-width: 28px;\" /> D46C: hand",
            "display": "D46c"
        },
        {
            "id": "D46d",
            "text": "D46D: hand",
            "html": "<img src=\"/Search/Image?key=D46D\" alt=\"D46D\" style=\"max-height:24px; max-width: 28px;\" /> D46D: hand",
            "display": "D46d"
        },
        {
            "id": "D47",
            "text": "D47: hand with palm up",
            "html": "<span class=\"uni\">&#x130A9;</span> D47: hand with palm up",
            "display": "D47"
        },
        {
            "id": "D48",
            "text": "D48: hand without thumb [broad]",
            "html": "<span class=\"uni\">&#x130AA;</span> D48: hand without thumb",
            "display": "D48"
        },
        {
            "id": "D49",
            "text": "D49: fist",
            "html": "<span class=\"uni\">&#x130AC;</span> D49: fist",
            "display": "D49"
        },
        {
            "id": "D5",
            "text": "D5: eye touched up with paint",
            "html": "<span class=\"uni\">&#x1307A;</span> D5: eye touched up with paint",
            "display": "D5"
        },
        {
            "id": "D50",
            "text": "D50: finger vertically [Dba]",
            "html": "<span class=\"uni\">&#x130AD;</span> D50: finger vertically",
            "display": "D50"
        },
        {
            "id": "D51",
            "text": "D51: finger horizontally [broad]",
            "html": "<span class=\"uni\">&#x130B7;</span> D51: finger horizontally",
            "display": "D51"
        },
        {
            "id": "D52",
            "text": "D52: phallus [mt]",
            "html": "<span class=\"uni\">&#x130B8;</span> D52: phallus",
            "display": "D52"
        },
        {
            "id": "D52a",
            "text": "D52A: combination of D52 and S29",
            "html": "<span class=\"uni\">&#x130B9;</span> D52A: combination of D52 and S29",
            "display": "D52a"
        },
        {
            "id": "D53",
            "text": "D53: liquid issuing from phallus",
            "html": "<span class=\"uni\">&#x130BA;</span> D53: liquid issuing from phallus",
            "display": "D53"
        },
        {
            "id": "D54",
            "text": "D54: legs walking",
            "html": "<span class=\"uni\">&#x130BB;</span> D54: legs walking",
            "display": "D54"
        },
        {
            "id": "D54a",
            "text": "D54A: hieratic legs walking",
            "html": "<span class=\"uni\">&#x130BC;</span> D54A: hieratic legs walking",
            "display": "D54a"
        },
        {
            "id": "D55",
            "text": "D55: legs walking backwards",
            "html": "<span class=\"uni\">&#x130BD;</span> D55: legs walking backwards",
            "display": "D55"
        },
        {
            "id": "D56",
            "text": "D56: leg [gHs]",
            "html": "<span class=\"uni\">&#x130BE;</span> D56: leg",
            "display": "D56"
        },
        {
            "id": "D57",
            "text": "D57: combination of D56 and T30",
            "html": "<span class=\"uni\">&#x130BF;</span> D57: combination of D56 and T30",
            "display": "D57"
        },
        {
            "id": "D58",
            "text": "D58: foot [b]",
            "html": "<span class=\"uni\">&#x130C0;</span> D58: foot",
            "display": "D58"
        },
        {
            "id": "D59",
            "text": "D59: combination of D58 and D36 [ab]",
            "html": "<span class=\"uni\">&#x130C1;</span> D59: combination of D58 and D36",
            "display": "D59"
        },
        {
            "id": "D6",
            "text": "D6: eye with painted upper lid",
            "html": "<span class=\"uni\">&#x1307B;</span> D6: eye with painted upper lid",
            "display": "D6"
        },
        {
            "id": "D60",
            "text": "D60: D58 under vase from which water flows [wab]",
            "html": "<span class=\"uni\">&#x130C2;</span> D60: D58 under vase from which water flows",
            "display": "D60"
        },
        {
            "id": "D61",
            "text": "D61: three toes oriented leftward [sAH]",
            "html": "<span class=\"uni\">&#x130C3;</span> D61: three toes oriented leftward",
            "display": "D61"
        },
        {
            "id": "D62",
            "text": "D62: three toes oriented rightward",
            "html": "<span class=\"uni\">&#x130C4;</span> D62: three toes oriented rightward",
            "display": "D62"
        },
        {
            "id": "D63",
            "text": "D63: two toes oriented leftward",
            "html": "<span class=\"uni\">&#x130C5;</span> D63: two toes oriented leftward",
            "display": "D63"
        },
        {
            "id": "D65",
            "text": "D65: lock of hair",
            "html": "<span class=\"uni\">&#x130C7;</span> D65: lock of hair",
            "display": "D65"
        },
        {
            "id": "D68",
            "text": "D68",
            "html": "<img src=\"/Search/Image?key=D68\" alt=\"D68\" style=\"max-height:24px; max-width: 28px;\" /> D68",
            "display": "D68"
        },
        {
            "id": "D69",
            "text": "D69",
            "html": "<img src=\"/Search/Image?key=D69\" alt=\"D69\" style=\"max-height:24px; max-width: 28px;\" /> D69",
            "display": "D69"
        },
        {
            "id": "D7",
            "text": "D7: eye with painted lower lid",
            "html": "<span class=\"uni\">&#x1307C;</span> D7: eye with painted lower lid",
            "display": "D7"
        },
        {
            "id": "D77",
            "text": "D77",
            "html": "<img src=\"/Search/Image?key=D77\" alt=\"D77\" style=\"max-height:24px; max-width: 28px;\" /> D77",
            "display": "D77"
        },
        {
            "id": "D78",
            "text": "D78",
            "html": "<img src=\"/Search/Image?key=D78\" alt=\"D78\" style=\"max-height:24px; max-width: 28px;\" /> D78",
            "display": "D78"
        },
        {
            "id": "D79",
            "text": "D79",
            "html": "<img src=\"/Search/Image?key=D79\" alt=\"D79\" style=\"max-height:24px; max-width: 28px;\" /> D79",
            "display": "D79"
        },
        {
            "id": "D7a",
            "text": "D7A: eye with painted lower lid",
            "html": "<img src=\"/Search/Image?key=D7A\" alt=\"D7A\" style=\"max-height:24px; max-width: 28px;\" /> D7A: eye with painted lower lid",
            "display": "D7a"
        },
        {
            "id": "D7c",
            "text": "D7C: eye with painted lower lid",
            "html": "<img src=\"/Search/Image?key=D7C\" alt=\"D7C\" style=\"max-height:24px; max-width: 28px;\" /> D7C: eye with painted lower lid",
            "display": "D7c"
        },
        {
            "id": "D7d",
            "text": "D7D: eye with painted lower lid",
            "html": "<img src=\"/Search/Image?key=D7D\" alt=\"D7D\" style=\"max-height:24px; max-width: 28px;\" /> D7D: eye with painted lower lid",
            "display": "D7d"
        },
        {
            "id": "D8",
            "text": "D8: eye enclosed in N18",
            "html": "<span class=\"uni\">&#x1307D;</span> D8: eye enclosed in N18",
            "display": "D8"
        },
        {
            "id": "D81",
            "text": "D81",
            "html": "<img src=\"/Search/Image?key=D81\" alt=\"D81\" style=\"max-height:24px; max-width: 28px;\" /> D81",
            "display": "D81"
        },
        {
            "id": "D82",
            "text": "D82",
            "html": "<img src=\"/Search/Image?key=D82\" alt=\"D82\" style=\"max-height:24px; max-width: 28px;\" /> D82",
            "display": "D82"
        },
        {
            "id": "D84",
            "text": "D84",
            "html": "<img src=\"/Search/Image?key=D84\" alt=\"D84\" style=\"max-height:24px; max-width: 28px;\" /> D84",
            "display": "D84"
        },
        {
            "id": "D88",
            "text": "D88",
            "html": "<img src=\"/Search/Image?key=D88\" alt=\"D88\" style=\"max-height:24px; max-width: 28px;\" /> D88",
            "display": "D88"
        },
        {
            "id": "D8a",
            "text": "D8A: eye with painted lower lid enclosed in N18",
            "html": "<span class=\"uni\">&#x1307E;</span> D8A: eye with painted lower lid enclosed in N18",
            "display": "D8a"
        },
        {
            "id": "D9",
            "text": "D9: eye with flowing tears [rmi]",
            "html": "<span class=\"uni\">&#x1307F;</span> D9: eye with flowing tears",
            "display": "D9"
        },
        {
            "id": "D92",
            "text": "D92",
            "html": "<img src=\"/Search/Image?key=D92\" alt=\"D92\" style=\"max-height:24px; max-width: 28px;\" /> D92",
            "display": "D92"
        },
        {
            "id": "D94",
            "text": "D94",
            "html": "<img src=\"/Search/Image?key=D94\" alt=\"D94\" style=\"max-height:24px; max-width: 28px;\" /> D94",
            "display": "D94"
        },
        {
            "id": "D96",
            "text": "D96",
            "html": "<img src=\"/Search/Image?key=D96\" alt=\"D96\" style=\"max-height:24px; max-width: 28px;\" /> D96",
            "display": "D96"
        },
        {
            "id": "D97",
            "text": "D97",
            "html": "<img src=\"/Search/Image?key=D97\" alt=\"D97\" style=\"max-height:24px; max-width: 28px;\" /> D97",
            "display": "D97"
        },
        {
            "id": "D99",
            "text": "D99",
            "html": "<img src=\"/Search/Image?key=D99\" alt=\"D99\" style=\"max-height:24px; max-width: 28px;\" /> D99",
            "display": "D99"
        },
        {
            "id": "D9a",
            "text": "D9A: eye with flowing tears",
            "html": "<img src=\"/Search/Image?key=D9A\" alt=\"D9A\" style=\"max-height:24px; max-width: 28px;\" /> D9A: eye with flowing tears",
            "display": "D9a"
        },
        {
            "id": "E1",
            "text": "E1: bull",
            "html": "<span class=\"uni\">&#x130D2;</span> E1: bull",
            "display": "E1"
        },
        {
            "id": "E10",
            "text": "E10: ram",
            "html": "<span class=\"uni\">&#x130DD;</span> E10: ram",
            "display": "E10"
        },
        {
            "id": "E100",
            "text": "E100",
            "html": "<img src=\"/Search/Image?key=E100\" alt=\"E100\" style=\"max-height:24px; max-width: 28px;\" /> E100",
            "display": "E100"
        },
        {
            "id": "E100b",
            "text": "E100B",
            "html": "<img src=\"/Search/Image?key=E100B\" alt=\"E100B\" style=\"max-height:24px; max-width: 28px;\" /> E100B",
            "display": "E100b"
        },
        {
            "id": "E101",
            "text": "E101",
            "html": "<img src=\"/Search/Image?key=E101\" alt=\"E101\" style=\"max-height:24px; max-width: 28px;\" /> E101",
            "display": "E101"
        },
        {
            "id": "E101a",
            "text": "E101A",
            "html": "<img src=\"/Search/Image?key=E101A\" alt=\"E101A\" style=\"max-height:24px; max-width: 28px;\" /> E101A",
            "display": "E101a"
        },
        {
            "id": "E102b",
            "text": "E102B",
            "html": "<img src=\"/Search/Image?key=E102B\" alt=\"E102B\" style=\"max-height:24px; max-width: 28px;\" /> E102B",
            "display": "E102b"
        },
        {
            "id": "E102c",
            "text": "E102C",
            "html": "<img src=\"/Search/Image?key=E102C\" alt=\"E102C\" style=\"max-height:24px; max-width: 28px;\" /> E102C",
            "display": "E102c"
        },
        {
            "id": "E103",
            "text": "E103",
            "html": "<img src=\"/Search/Image?key=E103\" alt=\"E103\" style=\"max-height:24px; max-width: 28px;\" /> E103",
            "display": "E103"
        },
        {
            "id": "E11",
            "text": "E11: ram",
            "html": "<span class=\"uni\">&#x130DE;</span> E11: ram",
            "display": "E11"
        },
        {
            "id": "E12",
            "text": "E12: pig",
            "html": "<span class=\"uni\">&#x130DF;</span> E12: pig",
            "display": "E12"
        },
        {
            "id": "E122",
            "text": "E122",
            "html": "<img src=\"/Search/Image?key=E122\" alt=\"E122\" style=\"max-height:24px; max-width: 28px;\" /> E122",
            "display": "E122"
        },
        {
            "id": "E128",
            "text": "E128",
            "html": "<img src=\"/Search/Image?key=E128\" alt=\"E128\" style=\"max-height:24px; max-width: 28px;\" /> E128",
            "display": "E128"
        },
        {
            "id": "E13",
            "text": "E13: cat",
            "html": "<span class=\"uni\">&#x130E0;</span> E13: cat",
            "display": "E13"
        },
        {
            "id": "E130",
            "text": "E130",
            "html": "<img src=\"/Search/Image?key=E130\" alt=\"E130\" style=\"max-height:24px; max-width: 28px;\" /> E130",
            "display": "E130"
        },
        {
            "id": "E131",
            "text": "E131",
            "html": "<img src=\"/Search/Image?key=E131\" alt=\"E131\" style=\"max-height:24px; max-width: 28px;\" /> E131",
            "display": "E131"
        },
        {
            "id": "E133b",
            "text": "E133B",
            "html": "<img src=\"/Search/Image?key=E133B\" alt=\"E133B\" style=\"max-height:24px; max-width: 28px;\" /> E133B",
            "display": "E133b"
        },
        {
            "id": "E137",
            "text": "E137",
            "html": "<img src=\"/Search/Image?key=E137\" alt=\"E137\" style=\"max-height:24px; max-width: 28px;\" /> E137",
            "display": "E137"
        },
        {
            "id": "E14",
            "text": "E14: dog (saluki)",
            "html": "<span class=\"uni\">&#x130E1;</span> E14: dog (saluki)",
            "display": "E14"
        },
        {
            "id": "E141",
            "text": "E141",
            "html": "<img src=\"/Search/Image?key=E141\" alt=\"E141\" style=\"max-height:24px; max-width: 28px;\" /> E141",
            "display": "E141"
        },
        {
            "id": "E145",
            "text": "E145",
            "html": "<img src=\"/Search/Image?key=E145\" alt=\"E145\" style=\"max-height:24px; max-width: 28px;\" /> E145",
            "display": "E145"
        },
        {
            "id": "E145a",
            "text": "E145A",
            "html": "<img src=\"/Search/Image?key=E145A\" alt=\"E145A\" style=\"max-height:24px; max-width: 28px;\" /> E145A",
            "display": "E145a"
        },
        {
            "id": "E146",
            "text": "E146",
            "html": "<img src=\"/Search/Image?key=E146\" alt=\"E146\" style=\"max-height:24px; max-width: 28px;\" /> E146",
            "display": "E146"
        },
        {
            "id": "E147",
            "text": "E147",
            "html": "<img src=\"/Search/Image?key=E147\" alt=\"E147\" style=\"max-height:24px; max-width: 28px;\" /> E147",
            "display": "E147"
        },
        {
            "id": "E148d",
            "text": "E148D",
            "html": "<img src=\"/Search/Image?key=E148D\" alt=\"E148D\" style=\"max-height:24px; max-width: 28px;\" /> E148D",
            "display": "E148d"
        },
        {
            "id": "E148f",
            "text": "E148F",
            "html": "<img src=\"/Search/Image?key=E148F\" alt=\"E148F\" style=\"max-height:24px; max-width: 28px;\" /> E148F",
            "display": "E148f"
        },
        {
            "id": "E148i",
            "text": "E148I",
            "html": "<img src=\"/Search/Image?key=E148I\" alt=\"E148I\" style=\"max-height:24px; max-width: 28px;\" /> E148I",
            "display": "E148i"
        },
        {
            "id": "E14a",
            "text": "E14A: dog (saluki)",
            "html": "<img src=\"/Search/Image?key=E14A\" alt=\"E14A\" style=\"max-height:24px; max-width: 28px;\" /> E14A: dog (saluki)",
            "display": "E14a"
        },
        {
            "id": "E14b",
            "text": "E14B: dog (saluki)",
            "html": "<img src=\"/Search/Image?key=E14B\" alt=\"E14B\" style=\"max-height:24px; max-width: 28px;\" /> E14B: dog (saluki)",
            "display": "E14b"
        },
        {
            "id": "E14c",
            "text": "E14C: dog (saluki)",
            "html": "<img src=\"/Search/Image?key=E14C\" alt=\"E14C\" style=\"max-height:24px; max-width: 28px;\" /> E14C: dog (saluki)",
            "display": "E14c"
        },
        {
            "id": "E15",
            "text": "E15: lying canine",
            "html": "<span class=\"uni\">&#x130E2;</span> E15: lying canine",
            "display": "E15"
        },
        {
            "id": "E150",
            "text": "E150",
            "html": "<img src=\"/Search/Image?key=E150\" alt=\"E150\" style=\"max-height:24px; max-width: 28px;\" /> E150",
            "display": "E150"
        },
        {
            "id": "E151",
            "text": "E151",
            "html": "<img src=\"/Search/Image?key=E151\" alt=\"E151\" style=\"max-height:24px; max-width: 28px;\" /> E151",
            "display": "E151"
        },
        {
            "id": "E152",
            "text": "E152",
            "html": "<img src=\"/Search/Image?key=E152\" alt=\"E152\" style=\"max-height:24px; max-width: 28px;\" /> E152",
            "display": "E152"
        },
        {
            "id": "E154",
            "text": "E154",
            "html": "<img src=\"/Search/Image?key=E154\" alt=\"E154\" style=\"max-height:24px; max-width: 28px;\" /> E154",
            "display": "E154"
        },
        {
            "id": "E16",
            "text": "E16: lying canine on shrine",
            "html": "<span class=\"uni\">&#x130E3;</span> E16: lying canine on shrine",
            "display": "E16"
        },
        {
            "id": "E163",
            "text": "E163",
            "html": "<img src=\"/Search/Image?key=E163\" alt=\"E163\" style=\"max-height:24px; max-width: 28px;\" /> E163",
            "display": "E163"
        },
        {
            "id": "E165",
            "text": "E165",
            "html": "<img src=\"/Search/Image?key=E165\" alt=\"E165\" style=\"max-height:24px; max-width: 28px;\" /> E165",
            "display": "E165"
        },
        {
            "id": "E16a",
            "text": "E16A: lying canine on shrine with S45",
            "html": "<span class=\"uni\">&#x130E4;</span> E16A: lying canine on shrine with S45",
            "display": "E16a"
        },
        {
            "id": "E17",
            "text": "E17: jackal [zAb]",
            "html": "<span class=\"uni\">&#x130E5;</span> E17: jackal",
            "display": "E17"
        },
        {
            "id": "E177",
            "text": "E177",
            "html": "<img src=\"/Search/Image?key=E177\" alt=\"E177\" style=\"max-height:24px; max-width: 28px;\" /> E177",
            "display": "E177"
        },
        {
            "id": "E178",
            "text": "E178",
            "html": "<img src=\"/Search/Image?key=E178\" alt=\"E178\" style=\"max-height:24px; max-width: 28px;\" /> E178",
            "display": "E178"
        },
        {
            "id": "E179",
            "text": "E179",
            "html": "<img src=\"/Search/Image?key=E179\" alt=\"E179\" style=\"max-height:24px; max-width: 28px;\" /> E179",
            "display": "E179"
        },
        {
            "id": "E18",
            "text": "E18: wolf on R12 with <span class=\"egytransl\">SdSd</span>",
            "html": "<span class=\"uni\">&#x130E7;</span> E18: wolf on R12 with <span class=\"egytransl\">SdSd</span>",
            "display": "E18"
        },
        {
            "id": "E183",
            "text": "E183",
            "html": "<img src=\"/Search/Image?key=E183\" alt=\"E183\" style=\"max-height:24px; max-width: 28px;\" /> E183",
            "display": "E183"
        },
        {
            "id": "E184",
            "text": "E184",
            "html": "<img src=\"/Search/Image?key=E184\" alt=\"E184\" style=\"max-height:24px; max-width: 28px;\" /> E184",
            "display": "E184"
        },
        {
            "id": "E186",
            "text": "E186",
            "html": "<img src=\"/Search/Image?key=E186\" alt=\"E186\" style=\"max-height:24px; max-width: 28px;\" /> E186",
            "display": "E186"
        },
        {
            "id": "E19",
            "text": "E19: combination of E19 and T3",
            "html": "<span class=\"uni\">&#x130E8;</span> E19: combination of E19 and T3",
            "display": "E19"
        },
        {
            "id": "E193a",
            "text": "E193A",
            "html": "<img src=\"/Search/Image?key=E193A\" alt=\"E193A\" style=\"max-height:24px; max-width: 28px;\" /> E193A",
            "display": "E193a"
        },
        {
            "id": "E1a",
            "text": "E1A: bull",
            "html": "<img src=\"/Search/Image?key=E1A\" alt=\"E1A\" style=\"max-height:24px; max-width: 28px;\" /> E1A: bull",
            "display": "E1a"
        },
        {
            "id": "E2",
            "text": "E2: bull charging",
            "html": "<span class=\"uni\">&#x130D3;</span> E2: bull charging",
            "display": "E2"
        },
        {
            "id": "E20",
            "text": "E20: Seth-animal",
            "html": "<span class=\"uni\">&#x130E9;</span> E20: Seth-animal",
            "display": "E20"
        },
        {
            "id": "E200",
            "text": "E200",
            "html": "<img src=\"/Search/Image?key=E200\" alt=\"E200\" style=\"max-height:24px; max-width: 28px;\" /> E200",
            "display": "E200"
        },
        {
            "id": "E200a",
            "text": "E200A",
            "html": "<img src=\"/Search/Image?key=E200A\" alt=\"E200A\" style=\"max-height:24px; max-width: 28px;\" /> E200A",
            "display": "E200a"
        },
        {
            "id": "E21",
            "text": "E21: lying Seth-animal",
            "html": "<span class=\"uni\">&#x130EB;</span> E21: lying Seth-animal",
            "display": "E21"
        },
        {
            "id": "E21e",
            "text": "E21E: lying Seth-animal",
            "html": "<img src=\"/Search/Image?key=E21E\" alt=\"E21E\" style=\"max-height:24px; max-width: 28px;\" /> E21E: lying Seth-animal",
            "display": "E21e"
        },
        {
            "id": "E22",
            "text": "E22: lion [mAi]",
            "html": "<span class=\"uni\">&#x130EC;</span> E22: lion",
            "display": "E22"
        },
        {
            "id": "E22a",
            "text": "E22A: lion",
            "html": "<img src=\"/Search/Image?key=E22A\" alt=\"E22A\" style=\"max-height:24px; max-width: 28px;\" /> E22A: lion",
            "display": "E22a"
        },
        {
            "id": "E23",
            "text": "E23: lying lion [rw]",
            "html": "<span class=\"uni\">&#x130ED;</span> E23: lying lion",
            "display": "E23"
        },
        {
            "id": "E238",
            "text": "E238",
            "html": "<img src=\"/Search/Image?key=E238\" alt=\"E238\" style=\"max-height:24px; max-width: 28px;\" /> E238",
            "display": "E238"
        },
        {
            "id": "E23a",
            "text": "E23A: lying lion",
            "html": "<img src=\"/Search/Image?key=E23A\" alt=\"E23A\" style=\"max-height:24px; max-width: 28px;\" /> E23A: lying lion",
            "display": "E23a"
        },
        {
            "id": "E24",
            "text": "E24: panther [Aby]",
            "html": "<span class=\"uni\">&#x130EE;</span> E24: panther",
            "display": "E24"
        },
        {
            "id": "E241",
            "text": "E241",
            "html": "<img src=\"/Search/Image?key=E241\" alt=\"E241\" style=\"max-height:24px; max-width: 28px;\" /> E241",
            "display": "E241"
        },
        {
            "id": "E244",
            "text": "E244",
            "html": "<img src=\"/Search/Image?key=E244\" alt=\"E244\" style=\"max-height:24px; max-width: 28px;\" /> E244",
            "display": "E244"
        },
        {
            "id": "E25",
            "text": "E25: hippopotamus",
            "html": "<span class=\"uni\">&#x130EF;</span> E25: hippopotamus",
            "display": "E25"
        },
        {
            "id": "E26",
            "text": "E26: elephant",
            "html": "<span class=\"uni\">&#x130F0;</span> E26: elephant",
            "display": "E26"
        },
        {
            "id": "E263",
            "text": "E263",
            "html": "<img src=\"/Search/Image?key=E263\" alt=\"E263\" style=\"max-height:24px; max-width: 28px;\" /> E263",
            "display": "E263"
        },
        {
            "id": "E264",
            "text": "E264",
            "html": "<img src=\"/Search/Image?key=E264\" alt=\"E264\" style=\"max-height:24px; max-width: 28px;\" /> E264",
            "display": "E264"
        },
        {
            "id": "E27",
            "text": "E27: giraffe",
            "html": "<span class=\"uni\">&#x130F1;</span> E27: giraffe",
            "display": "E27"
        },
        {
            "id": "E28",
            "text": "E28: oryx",
            "html": "<span class=\"uni\">&#x130F2;</span> E28: oryx",
            "display": "E28"
        },
        {
            "id": "E29",
            "text": "E29: gazelle",
            "html": "<span class=\"uni\">&#x130F4;</span> E29: gazelle",
            "display": "E29"
        },
        {
            "id": "E3",
            "text": "E3: calf",
            "html": "<span class=\"uni\">&#x130D4;</span> E3: calf",
            "display": "E3"
        },
        {
            "id": "E30",
            "text": "E30: ibex",
            "html": "<span class=\"uni\">&#x130F5;</span> E30: ibex",
            "display": "E30"
        },
        {
            "id": "E30a",
            "text": "E30A: ibex",
            "html": "<img src=\"/Search/Image?key=E30A\" alt=\"E30A\" style=\"max-height:24px; max-width: 28px;\" /> E30A: ibex",
            "display": "E30a"
        },
        {
            "id": "E30b",
            "text": "E30B: ibex",
            "html": "<img src=\"/Search/Image?key=E30B\" alt=\"E30B\" style=\"max-height:24px; max-width: 28px;\" /> E30B: ibex",
            "display": "E30b"
        },
        {
            "id": "E31",
            "text": "E31: goat with collar",
            "html": "<span class=\"uni\">&#x130F6;</span> E31: goat with collar",
            "display": "E31"
        },
        {
            "id": "E32",
            "text": "E32: baboon",
            "html": "<span class=\"uni\">&#x130F7;</span> E32: baboon",
            "display": "E32"
        },
        {
            "id": "E33",
            "text": "E33: monkey",
            "html": "<span class=\"uni\">&#x130F8;</span> E33: monkey",
            "display": "E33"
        },
        {
            "id": "E34",
            "text": "E34: hare [wn]",
            "html": "<span class=\"uni\">&#x130F9;</span> E34: hare",
            "display": "E34"
        },
        {
            "id": "E34b",
            "text": "E34B: hare",
            "html": "<img src=\"/Search/Image?key=E34B\" alt=\"E34B\" style=\"max-height:24px; max-width: 28px;\" /> E34B: hare",
            "display": "E34b"
        },
        {
            "id": "E35",
            "text": "E35",
            "html": "<img src=\"/Search/Image?key=E35\" alt=\"E35\" style=\"max-height:24px; max-width: 28px;\" /> E35",
            "display": "E35"
        },
        {
            "id": "E36",
            "text": "E36: baboon",
            "html": "<span class=\"uni\">&#x130FB;</span> E36: baboon",
            "display": "E36"
        },
        {
            "id": "E5",
            "text": "E5: cow suckling calf",
            "html": "<span class=\"uni\">&#x130D6;</span> E5: cow suckling calf",
            "display": "E5"
        },
        {
            "id": "E51",
            "text": "E51",
            "html": "<img src=\"/Search/Image?key=E51\" alt=\"E51\" style=\"max-height:24px; max-width: 28px;\" /> E51",
            "display": "E51"
        },
        {
            "id": "E53",
            "text": "E53",
            "html": "<img src=\"/Search/Image?key=E53\" alt=\"E53\" style=\"max-height:24px; max-width: 28px;\" /> E53",
            "display": "E53"
        },
        {
            "id": "E6",
            "text": "E6: horse [zzmt]",
            "html": "<span class=\"uni\">&#x130D7;</span> E6: horse",
            "display": "E6"
        },
        {
            "id": "E69",
            "text": "E69",
            "html": "<img src=\"/Search/Image?key=E69\" alt=\"E69\" style=\"max-height:24px; max-width: 28px;\" /> E69",
            "display": "E69"
        },
        {
            "id": "E6a",
            "text": "E6A: horse",
            "html": "<img src=\"/Search/Image?key=E6A\" alt=\"E6A\" style=\"max-height:24px; max-width: 28px;\" /> E6A: horse",
            "display": "E6a"
        },
        {
            "id": "E7",
            "text": "E7: donkey",
            "html": "<span class=\"uni\">&#x130D8;</span> E7: donkey",
            "display": "E7"
        },
        {
            "id": "E8",
            "text": "E8: kid",
            "html": "<span class=\"uni\">&#x130D9;</span> E8: kid",
            "display": "E8"
        },
        {
            "id": "E80",
            "text": "E80",
            "html": "<img src=\"/Search/Image?key=E80\" alt=\"E80\" style=\"max-height:24px; max-width: 28px;\" /> E80",
            "display": "E80"
        },
        {
            "id": "E82",
            "text": "E82",
            "html": "<img src=\"/Search/Image?key=E82\" alt=\"E82\" style=\"max-height:24px; max-width: 28px;\" /> E82",
            "display": "E82"
        },
        {
            "id": "E83",
            "text": "E83",
            "html": "<img src=\"/Search/Image?key=E83\" alt=\"E83\" style=\"max-height:24px; max-width: 28px;\" /> E83",
            "display": "E83"
        },
        {
            "id": "E85",
            "text": "E85",
            "html": "<img src=\"/Search/Image?key=E85\" alt=\"E85\" style=\"max-height:24px; max-width: 28px;\" /> E85",
            "display": "E85"
        },
        {
            "id": "E8a",
            "text": "E8A: kid jumping",
            "html": "<span class=\"uni\">&#x130DA;</span> E8A: kid jumping",
            "display": "E8a"
        },
        {
            "id": "E9",
            "text": "E9: newborn bubalis or hartebeest",
            "html": "<span class=\"uni\">&#x130DB;</span> E9: newborn bubalis or hartebeest",
            "display": "E9"
        },
        {
            "id": "E90",
            "text": "E90",
            "html": "<img src=\"/Search/Image?key=E90\" alt=\"E90\" style=\"max-height:24px; max-width: 28px;\" /> E90",
            "display": "E90"
        },
        {
            "id": "E92",
            "text": "E92",
            "html": "E92",
            "display": "E92"
        },
        {
            "id": "E92a",
            "text": "E92A",
            "html": "<img src=\"/Search/Image?key=E92A\" alt=\"E92A\" style=\"max-height:24px; max-width: 28px;\" /> E92A",
            "display": "E92a"
        },
        {
            "id": "E92b",
            "text": "E92B",
            "html": "<img src=\"/Search/Image?key=E92B\" alt=\"E92B\" style=\"max-height:24px; max-width: 28px;\" /> E92B",
            "display": "E92b"
        },
        {
            "id": "E98",
            "text": "E98",
            "html": "<img src=\"/Search/Image?key=E98\" alt=\"E98\" style=\"max-height:24px; max-width: 28px;\" /> E98",
            "display": "E98"
        },
        {
            "id": "F1",
            "text": "F1: head of ox",
            "html": "<span class=\"uni\">&#x130FE;</span> F1: head of ox",
            "display": "F1"
        },
        {
            "id": "F10",
            "text": "F10: head and neck of animal [tall]",
            "html": "<span class=\"uni\">&#x13108;</span> F10: head and neck of animal",
            "display": "F10"
        },
        {
            "id": "F100",
            "text": "F100",
            "html": "<img src=\"/Search/Image?key=F100\" alt=\"F100\" style=\"max-height:24px; max-width: 28px;\" /> F100",
            "display": "F100"
        },
        {
            "id": "F102",
            "text": "F102",
            "html": "<img src=\"/Search/Image?key=F102\" alt=\"F102\" style=\"max-height:24px; max-width: 28px;\" /> F102",
            "display": "F102"
        },
        {
            "id": "F105",
            "text": "F105",
            "html": "<img src=\"/Search/Image?key=F105\" alt=\"F105\" style=\"max-height:24px; max-width: 28px;\" /> F105",
            "display": "F105"
        },
        {
            "id": "F107",
            "text": "F107",
            "html": "<img src=\"/Search/Image?key=F107\" alt=\"F107\" style=\"max-height:24px; max-width: 28px;\" /> F107",
            "display": "F107"
        },
        {
            "id": "F11",
            "text": "F11: head and neck of animal [tall]",
            "html": "<span class=\"uni\">&#x13109;</span> F11: head and neck of animal",
            "display": "F11"
        },
        {
            "id": "F112",
            "text": "F112",
            "html": "<img src=\"/Search/Image?key=F112\" alt=\"F112\" style=\"max-height:24px; max-width: 28px;\" /> F112",
            "display": "F112"
        },
        {
            "id": "F114",
            "text": "F114",
            "html": "<img src=\"/Search/Image?key=F114\" alt=\"F114\" style=\"max-height:24px; max-width: 28px;\" /> F114",
            "display": "F114"
        },
        {
            "id": "F12",
            "text": "F12: head and neck of canine [tall] [wsr]",
            "html": "<span class=\"uni\">&#x1310A;</span> F12: head and neck of canine",
            "display": "F12"
        },
        {
            "id": "F122",
            "text": "F122",
            "html": "<img src=\"/Search/Image?key=F122\" alt=\"F122\" style=\"max-height:24px; max-width: 28px;\" /> F122",
            "display": "F122"
        },
        {
            "id": "F123",
            "text": "F123",
            "html": "<img src=\"/Search/Image?key=F123\" alt=\"F123\" style=\"max-height:24px; max-width: 28px;\" /> F123",
            "display": "F123"
        },
        {
            "id": "F125",
            "text": "F125",
            "html": "<img src=\"/Search/Image?key=F125\" alt=\"F125\" style=\"max-height:24px; max-width: 28px;\" /> F125",
            "display": "F125"
        },
        {
            "id": "F128",
            "text": "F128",
            "html": "<img src=\"/Search/Image?key=F128\" alt=\"F128\" style=\"max-height:24px; max-width: 28px;\" /> F128",
            "display": "F128"
        },
        {
            "id": "F13",
            "text": "F13: horns [wp]",
            "html": "<span class=\"uni\">&#x1310B;</span> F13: horns",
            "display": "F13"
        },
        {
            "id": "F130",
            "text": "F130",
            "html": "<img src=\"/Search/Image?key=F130\" alt=\"F130\" style=\"max-height:24px; max-width: 28px;\" /> F130",
            "display": "F130"
        },
        {
            "id": "F132",
            "text": "F132",
            "html": "<img src=\"/Search/Image?key=F132\" alt=\"F132\" style=\"max-height:24px; max-width: 28px;\" /> F132",
            "display": "F132"
        },
        {
            "id": "F134",
            "text": "F134",
            "html": "<img src=\"/Search/Image?key=F134\" alt=\"F134\" style=\"max-height:24px; max-width: 28px;\" /> F134",
            "display": "F134"
        },
        {
            "id": "F14",
            "text": "F14: combination of F13 and M4",
            "html": "<span class=\"uni\">&#x1310D;</span> F14: combination of F13 and M4",
            "display": "F14"
        },
        {
            "id": "F143",
            "text": "F143",
            "html": "<img src=\"/Search/Image?key=F143\" alt=\"F143\" style=\"max-height:24px; max-width: 28px;\" /> F143",
            "display": "F143"
        },
        {
            "id": "F147",
            "text": "F147",
            "html": "<img src=\"/Search/Image?key=F147\" alt=\"F147\" style=\"max-height:24px; max-width: 28px;\" /> F147",
            "display": "F147"
        },
        {
            "id": "F15",
            "text": "F15: combination of F14 and N5",
            "html": "<span class=\"uni\">&#x1310E;</span> F15: combination of F14 and N5",
            "display": "F15"
        },
        {
            "id": "F155",
            "text": "F155",
            "html": "<img src=\"/Search/Image?key=F155\" alt=\"F155\" style=\"max-height:24px; max-width: 28px;\" /> F155",
            "display": "F155"
        },
        {
            "id": "F16",
            "text": "F16: horn [db]",
            "html": "<span class=\"uni\">&#x1310F;</span> F16: horn",
            "display": "F16"
        },
        {
            "id": "F16a",
            "text": "F16A: horn",
            "html": "<img src=\"/Search/Image?key=F16A\" alt=\"F16A\" style=\"max-height:24px; max-width: 28px;\" /> F16A: horn",
            "display": "F16a"
        },
        {
            "id": "F17",
            "text": "F17: combination of F16 with vase from which water flows",
            "html": "<span class=\"uni\">&#x13110;</span> F17: combination of F16 with vase from which water flows",
            "display": "F17"
        },
        {
            "id": "F171",
            "text": "F171",
            "html": "<img src=\"/Search/Image?key=F171\" alt=\"F171\" style=\"max-height:24px; max-width: 28px;\" /> F171",
            "display": "F171"
        },
        {
            "id": "F18",
            "text": "F18: tusk [broad] [bH]",
            "html": "<span class=\"uni\">&#x13111;</span> F18: tusk",
            "display": "F18"
        },
        {
            "id": "F183",
            "text": "F183",
            "html": "<img src=\"/Search/Image?key=F183\" alt=\"F183\" style=\"max-height:24px; max-width: 28px;\" /> F183",
            "display": "F183"
        },
        {
            "id": "F18b",
            "text": "F18B: tusk",
            "html": "<img src=\"/Search/Image?key=F18B\" alt=\"F18B\" style=\"max-height:24px; max-width: 28px;\" /> F18B: tusk",
            "display": "F18b"
        },
        {
            "id": "F19",
            "text": "F19: lower jaw-bone of ox",
            "html": "<span class=\"uni\">&#x13112;</span> F19: lower jaw-bone of ox",
            "display": "F19"
        },
        {
            "id": "F2",
            "text": "F2: head of charging ox",
            "html": "<span class=\"uni\">&#x13100;</span> F2: head of charging ox",
            "display": "F2"
        },
        {
            "id": "F20",
            "text": "F20: tongue [broad] [ns]",
            "html": "<span class=\"uni\">&#x13113;</span> F20: tongue",
            "display": "F20"
        },
        {
            "id": "F20b",
            "text": "F20B: tongue",
            "html": "<img src=\"/Search/Image?key=F20B\" alt=\"F20B\" style=\"max-height:24px; max-width: 28px;\" /> F20B: tongue",
            "display": "F20b"
        },
        {
            "id": "F21",
            "text": "F21: ear of bovine [narrow] [DrD]",
            "html": "<span class=\"uni\">&#x13114;</span> F21: ear of bovine",
            "display": "F21"
        },
        {
            "id": "F22",
            "text": "F22: hind-quarters of lion [kfA]",
            "html": "<span class=\"uni\">&#x13116;</span> F22: hind-quarters of lion",
            "display": "F22"
        },
        {
            "id": "F23",
            "text": "F23: foreleg of ox [xpS]",
            "html": "<span class=\"uni\">&#x13117;</span> F23: foreleg of ox",
            "display": "F23"
        },
        {
            "id": "F24",
            "text": "F24: F23 reversed",
            "html": "<span class=\"uni\">&#x13118;</span> F24: F23 reversed",
            "display": "F24"
        },
        {
            "id": "F25",
            "text": "F25: leg of ox [wHm]",
            "html": "<span class=\"uni\">&#x13119;</span> F25: leg of ox",
            "display": "F25"
        },
        {
            "id": "F26",
            "text": "F26: skin of goat [Xn]",
            "html": "<span class=\"uni\">&#x1311A;</span> F26: skin of goat",
            "display": "F26"
        },
        {
            "id": "F27",
            "text": "F27: skin of cow with bent tail",
            "html": "<span class=\"uni\">&#x1311B;</span> F27: skin of cow with bent tail",
            "display": "F27"
        },
        {
            "id": "F27b",
            "text": "F27B: skin of cow with bent tail",
            "html": "<img src=\"/Search/Image?key=F27B\" alt=\"F27B\" style=\"max-height:24px; max-width: 28px;\" /> F27B: skin of cow with bent tail",
            "display": "F27b"
        },
        {
            "id": "F28",
            "text": "F28: skin of cow with straight tail [tall]",
            "html": "<span class=\"uni\">&#x1311C;</span> F28: skin of cow with straight tail",
            "display": "F28"
        },
        {
            "id": "F29",
            "text": "F29: cow&amp;apos;s skin pierced by arrow [sti]",
            "html": "<span class=\"uni\">&#x1311D;</span> F29: cow&amp;apos;s skin pierced by arrow",
            "display": "F29"
        },
        {
            "id": "F29a",
            "text": "F29A: cow&amp;apos;s skin pierced by arrow",
            "html": "<img src=\"/Search/Image?key=F29A\" alt=\"F29A\" style=\"max-height:24px; max-width: 28px;\" /> F29A: cow&amp;apos;s skin pierced by arrow",
            "display": "F29a"
        },
        {
            "id": "F3",
            "text": "F3: head of hippopotamus",
            "html": "<span class=\"uni\">&#x13101;</span> F3: head of hippopotamus",
            "display": "F3"
        },
        {
            "id": "F30",
            "text": "F30: water-skin [broad] [Sd]",
            "html": "<span class=\"uni\">&#x1311E;</span> F30: water-skin",
            "display": "F30"
        },
        {
            "id": "F31",
            "text": "F31: three skins tied together [tall] [ms]",
            "html": "<span class=\"uni\">&#x1311F;</span> F31: three skins tied together",
            "display": "F31"
        },
        {
            "id": "F32",
            "text": "F32: animal&amp;apos;s belly [broad] [X]",
            "html": "<span class=\"uni\">&#x13121;</span> F32: animal&amp;apos;s belly",
            "display": "F32"
        },
        {
            "id": "F33",
            "text": "F33: tail [broad] [sd]",
            "html": "<span class=\"uni\">&#x13122;</span> F33: tail",
            "display": "F33"
        },
        {
            "id": "F33b",
            "text": "F33B: tail",
            "html": "<img src=\"/Search/Image?key=F33B\" alt=\"F33B\" style=\"max-height:24px; max-width: 28px;\" /> F33B: tail",
            "display": "F33b"
        },
        {
            "id": "F34",
            "text": "F34: heart [narrow] [ib]",
            "html": "<span class=\"uni\">&#x13123;</span> F34: heart",
            "display": "F34"
        },
        {
            "id": "F35",
            "text": "F35: heart and windpipe [tall] [nfr]",
            "html": "<span class=\"uni\">&#x13124;</span> F35: heart and windpipe",
            "display": "F35"
        },
        {
            "id": "F36",
            "text": "F36: lung and windpipe [tall] [zmA]",
            "html": "<span class=\"uni\">&#x13125;</span> F36: lung and windpipe",
            "display": "F36"
        },
        {
            "id": "F36a",
            "text": "F36A: lung and windpipe",
            "html": "<img src=\"/Search/Image?key=F36A\" alt=\"F36A\" style=\"max-height:24px; max-width: 28px;\" /> F36A: lung and windpipe",
            "display": "F36a"
        },
        {
            "id": "F36b",
            "text": "F36B: lung and windpipe",
            "html": "<img src=\"/Search/Image?key=F36B\" alt=\"F36B\" style=\"max-height:24px; max-width: 28px;\" /> F36B: lung and windpipe",
            "display": "F36b"
        },
        {
            "id": "F36c",
            "text": "F36C: lung and windpipe",
            "html": "<img src=\"/Search/Image?key=F36C\" alt=\"F36C\" style=\"max-height:24px; max-width: 28px;\" /> F36C: lung and windpipe",
            "display": "F36c"
        },
        {
            "id": "F37",
            "text": "F37: backbone and ribs and spinal cord",
            "html": "<span class=\"uni\">&#x13126;</span> F37: backbone and ribs and spinal cord",
            "display": "F37"
        },
        {
            "id": "F37a",
            "text": "F37A: backbone and ribs",
            "html": "<span class=\"uni\">&#x13127;</span> F37A: backbone and ribs",
            "display": "F37a"
        },
        {
            "id": "F37aa",
            "text": "F37AA: backbone and ribs and spinal cord",
            "html": "<img src=\"/Search/Image?key=F37J\" alt=\"F37J\" style=\"max-height:24px; max-width: 28px;\" /> F37AA: backbone and ribs and spinal cord",
            "display": "F37aa"
        },
        {
            "id": "F37b",
            "text": "F37B: backbone and ribs and spinal cord",
            "html": "<img src=\"/Search/Image?key=F37B\" alt=\"F37B\" style=\"max-height:24px; max-width: 28px;\" /> F37B: backbone and ribs and spinal cord",
            "display": "F37b"
        },
        {
            "id": "F37d",
            "text": "F37D: backbone and ribs and spinal cord",
            "html": "<img src=\"/Search/Image?key=F37D\" alt=\"F37D\" style=\"max-height:24px; max-width: 28px;\" /> F37D: backbone and ribs and spinal cord",
            "display": "F37d"
        },
        {
            "id": "F37e",
            "text": "F37E: backbone and ribs and spinal cord",
            "html": "<img src=\"/Search/Image?key=F37E\" alt=\"F37E\" style=\"max-height:24px; max-width: 28px;\" /> F37E: backbone and ribs and spinal cord",
            "display": "F37e"
        },
        {
            "id": "F37f",
            "text": "F37F: backbone and ribs and spinal cord",
            "html": "<img src=\"/Search/Image?key=F37F\" alt=\"F37F\" style=\"max-height:24px; max-width: 28px;\" /> F37F: backbone and ribs and spinal cord",
            "display": "F37f"
        },
        {
            "id": "F37n",
            "text": "F37N: backbone and ribs and spinal cord",
            "html": "<img src=\"/Search/Image?key=F37N\" alt=\"F37N\" style=\"max-height:24px; max-width: 28px;\" /> F37N: backbone and ribs and spinal cord",
            "display": "F37n"
        },
        {
            "id": "F38",
            "text": "F38: backbone and ribs [narrow]",
            "html": "<span class=\"uni\">&#x13128;</span> F38: backbone and ribs",
            "display": "F38"
        },
        {
            "id": "F38a",
            "text": "F38A: backbone and ribs and spinal cord",
            "html": "<span class=\"uni\">&#x13129;</span> F38A: backbone and ribs and spinal cord",
            "display": "F38a"
        },
        {
            "id": "F39",
            "text": "F39: backbone and spinal cord [imAx]",
            "html": "<span class=\"uni\">&#x1312A;</span> F39: backbone and spinal cord",
            "display": "F39"
        },
        {
            "id": "F39a",
            "text": "F39A: backbone and spinal cord",
            "html": "<img src=\"/Search/Image?key=F39A\" alt=\"F39A\" style=\"max-height:24px; max-width: 28px;\" /> F39A: backbone and spinal cord",
            "display": "F39a"
        },
        {
            "id": "F4",
            "text": "F4: forepart of lion [HAt]",
            "html": "<span class=\"uni\">&#x13102;</span> F4: forepart of lion",
            "display": "F4"
        },
        {
            "id": "F40",
            "text": "F40: backbone and spinal cords [Aw]",
            "html": "<span class=\"uni\">&#x1312B;</span> F40: backbone and spinal cords",
            "display": "F40"
        },
        {
            "id": "F40c",
            "text": "F40C: backbone and spinal cords",
            "html": "<img src=\"/Search/Image?key=F40C\" alt=\"F40C\" style=\"max-height:24px; max-width: 28px;\" /> F40C: backbone and spinal cords",
            "display": "F40c"
        },
        {
            "id": "F41",
            "text": "F41: vertebrae [narrow]",
            "html": "<span class=\"uni\">&#x1312C;</span> F41: vertebrae",
            "display": "F41"
        },
        {
            "id": "F41c",
            "text": "F41C: vertebrae",
            "html": "<img src=\"/Search/Image?key=F41C\" alt=\"F41C\" style=\"max-height:24px; max-width: 28px;\" /> F41C: vertebrae",
            "display": "F41c"
        },
        {
            "id": "F42",
            "text": "F42: rib [broad] [spr]",
            "html": "<span class=\"uni\">&#x1312D;</span> F42: rib",
            "display": "F42"
        },
        {
            "id": "F43",
            "text": "F43: ribs [narrow]",
            "html": "<span class=\"uni\">&#x1312E;</span> F43: ribs",
            "display": "F43"
        },
        {
            "id": "F44",
            "text": "F44: leg-bone with meat [isw]",
            "html": "<span class=\"uni\">&#x1312F;</span> F44: leg-bone with meat",
            "display": "F44"
        },
        {
            "id": "F45",
            "text": "F45: uterus [tall]",
            "html": "<span class=\"uni\">&#x13130;</span> F45: uterus",
            "display": "F45"
        },
        {
            "id": "F46",
            "text": "F46: intestine [broad] [qAb]",
            "html": "<span class=\"uni\">&#x13132;</span> F46: intestine",
            "display": "F46"
        },
        {
            "id": "F46a",
            "text": "F46A: intestine",
            "html": "<span class=\"uni\">&#x13133;</span> F46A: intestine",
            "display": "F46a"
        },
        {
            "id": "F47",
            "text": "F47: intestine [broad]",
            "html": "<span class=\"uni\">&#x13134;</span> F47: intestine",
            "display": "F47"
        },
        {
            "id": "F47a",
            "text": "F47A: intestine",
            "html": "<span class=\"uni\">&#x13135;</span> F47A: intestine",
            "display": "F47a"
        },
        {
            "id": "F48",
            "text": "F48: intestine [broad]",
            "html": "<span class=\"uni\">&#x13136;</span> F48: intestine",
            "display": "F48"
        },
        {
            "id": "F49",
            "text": "F49: intestine [broad]",
            "html": "<span class=\"uni\">&#x13137;</span> F49: intestine",
            "display": "F49"
        },
        {
            "id": "F5",
            "text": "F5: head of bubalis or hartebeest [SsA]",
            "html": "<span class=\"uni\">&#x13103;</span> F5: head of bubalis or hartebeest",
            "display": "F5"
        },
        {
            "id": "F50",
            "text": "F50: combination of F46 and S29",
            "html": "<span class=\"uni\">&#x13138;</span> F50: combination of F46 and S29",
            "display": "F50"
        },
        {
            "id": "F51",
            "text": "F51: piece of flesh [narrow]",
            "html": "<span class=\"uni\">&#x13139;</span> F51: piece of flesh",
            "display": "F51"
        },
        {
            "id": "F51a",
            "text": "F51A: three pieces of flesh horizontally",
            "html": "<span class=\"uni\">&#x1313A;</span> F51A: three pieces of flesh horizontally",
            "display": "F51a"
        },
        {
            "id": "F51b",
            "text": "F51B: three pieces of flesh vertically",
            "html": "<span class=\"uni\">&#x1313B;</span> F51B: three pieces of flesh vertically",
            "display": "F51b"
        },
        {
            "id": "F51d",
            "text": "F51D: piece of flesh",
            "html": "<img src=\"/Search/Image?key=F51D\" alt=\"F51D\" style=\"max-height:24px; max-width: 28px;\" /> F51D: piece of flesh",
            "display": "F51d"
        },
        {
            "id": "F51f",
            "text": "F51F: piece of flesh",
            "html": "<img src=\"/Search/Image?key=F51F\" alt=\"F51F\" style=\"max-height:24px; max-width: 28px;\" /> F51F: piece of flesh",
            "display": "F51f"
        },
        {
            "id": "F52",
            "text": "F52: excrement [narrow]",
            "html": "<span class=\"uni\">&#x1313D;</span> F52: excrement",
            "display": "F52"
        },
        {
            "id": "F53",
            "text": "F53: divine rod with F7",
            "html": "<span class=\"uni\">&#x1313E;</span> F53: divine rod with F7",
            "display": "F53"
        },
        {
            "id": "F6",
            "text": "F6: forepart of bubalis or hartebeest",
            "html": "<span class=\"uni\">&#x13104;</span> F6: forepart of bubalis or hartebeest",
            "display": "F6"
        },
        {
            "id": "F62",
            "text": "F62",
            "html": "<img src=\"/Search/Image?key=F62\" alt=\"F62\" style=\"max-height:24px; max-width: 28px;\" /> F62",
            "display": "F62"
        },
        {
            "id": "F63",
            "text": "F63",
            "html": "<img src=\"/Search/Image?key=F63\" alt=\"F63\" style=\"max-height:24px; max-width: 28px;\" /> F63",
            "display": "F63"
        },
        {
            "id": "F67",
            "text": "F67",
            "html": "<img src=\"/Search/Image?key=F67\" alt=\"F67\" style=\"max-height:24px; max-width: 28px;\" /> F67",
            "display": "F67"
        },
        {
            "id": "F67a",
            "text": "F67A",
            "html": "<img src=\"/Search/Image?key=F67A\" alt=\"F67A\" style=\"max-height:24px; max-width: 28px;\" /> F67A",
            "display": "F67a"
        },
        {
            "id": "F7",
            "text": "F7: head of ram",
            "html": "<span class=\"uni\">&#x13105;</span> F7: head of ram",
            "display": "F7"
        },
        {
            "id": "F72",
            "text": "F72",
            "html": "<img src=\"/Search/Image?key=F72\" alt=\"F72\" style=\"max-height:24px; max-width: 28px;\" /> F72",
            "display": "F72"
        },
        {
            "id": "F7c",
            "text": "F7C: head of ram",
            "html": "<img src=\"/Search/Image?key=F7C\" alt=\"F7C\" style=\"max-height:24px; max-width: 28px;\" /> F7C: head of ram",
            "display": "F7c"
        },
        {
            "id": "F7d",
            "text": "F7D: head of ram",
            "html": "<img src=\"/Search/Image?key=F7D\" alt=\"F7D\" style=\"max-height:24px; max-width: 28px;\" /> F7D: head of ram",
            "display": "F7d"
        },
        {
            "id": "F8",
            "text": "F8: forepart of ram",
            "html": "<span class=\"uni\">&#x13106;</span> F8: forepart of ram",
            "display": "F8"
        },
        {
            "id": "F81",
            "text": "F81",
            "html": "<img src=\"/Search/Image?key=F81\" alt=\"F81\" style=\"max-height:24px; max-width: 28px;\" /> F81",
            "display": "F81"
        },
        {
            "id": "F85",
            "text": "F85",
            "html": "<img src=\"/Search/Image?key=F85\" alt=\"F85\" style=\"max-height:24px; max-width: 28px;\" /> F85",
            "display": "F85"
        },
        {
            "id": "F88",
            "text": "F88",
            "html": "<img src=\"/Search/Image?key=F88\" alt=\"F88\" style=\"max-height:24px; max-width: 28px;\" /> F88",
            "display": "F88"
        },
        {
            "id": "F9",
            "text": "F9: head of leopard",
            "html": "<span class=\"uni\">&#x13107;</span> F9: head of leopard",
            "display": "F9"
        },
        {
            "id": "F90",
            "text": "F90",
            "html": "<img src=\"/Search/Image?key=F90\" alt=\"F90\" style=\"max-height:24px; max-width: 28px;\" /> F90",
            "display": "F90"
        },
        {
            "id": "G1",
            "text": "G1: Egyptian vulture [A]",
            "html": "<span class=\"uni\">&#x1313F;</span> G1: Egyptian vulture",
            "display": "G1"
        },
        {
            "id": "G11",
            "text": "G11: image of falcon",
            "html": "<span class=\"uni\">&#x1314C;</span> G11: image of falcon",
            "display": "G11"
        },
        {
            "id": "G117",
            "text": "G117",
            "html": "<img src=\"/Search/Image?key=G117\" alt=\"G117\" style=\"max-height:24px; max-width: 28px;\" /> G117",
            "display": "G117"
        },
        {
            "id": "G119",
            "text": "G119",
            "html": "<img src=\"/Search/Image?key=G119\" alt=\"G119\" style=\"max-height:24px; max-width: 28px;\" /> G119",
            "display": "G119"
        },
        {
            "id": "G12",
            "text": "G12: combination of G11 and S45",
            "html": "<span class=\"uni\">&#x1314E;</span> G12: combination of G11 and S45",
            "display": "G12"
        },
        {
            "id": "G121",
            "text": "G121",
            "html": "<img src=\"/Search/Image?key=G121\" alt=\"G121\" style=\"max-height:24px; max-width: 28px;\" /> G121",
            "display": "G121"
        },
        {
            "id": "G13",
            "text": "G13: image of falcon with S9",
            "html": "<span class=\"uni\">&#x1314F;</span> G13: image of falcon with S9",
            "display": "G13"
        },
        {
            "id": "G131",
            "text": "G131",
            "html": "<img src=\"/Search/Image?key=G131\" alt=\"G131\" style=\"max-height:24px; max-width: 28px;\" /> G131",
            "display": "G131"
        },
        {
            "id": "G131b",
            "text": "G131B",
            "html": "<img src=\"/Search/Image?key=G131B\" alt=\"G131B\" style=\"max-height:24px; max-width: 28px;\" /> G131B",
            "display": "G131b"
        },
        {
            "id": "G139",
            "text": "G139",
            "html": "<img src=\"/Search/Image?key=G139\" alt=\"G139\" style=\"max-height:24px; max-width: 28px;\" /> G139",
            "display": "G139"
        },
        {
            "id": "G14",
            "text": "G14: vulture [mwt]",
            "html": "<span class=\"uni\">&#x13150;</span> G14: vulture",
            "display": "G14"
        },
        {
            "id": "G142",
            "text": "G142",
            "html": "<img src=\"/Search/Image?key=G142\" alt=\"G142\" style=\"max-height:24px; max-width: 28px;\" /> G142",
            "display": "G142"
        },
        {
            "id": "G143",
            "text": "G143",
            "html": "<img src=\"/Search/Image?key=G143\" alt=\"G143\" style=\"max-height:24px; max-width: 28px;\" /> G143",
            "display": "G143"
        },
        {
            "id": "G144",
            "text": "G144",
            "html": "<img src=\"/Search/Image?key=G144\" alt=\"G144\" style=\"max-height:24px; max-width: 28px;\" /> G144",
            "display": "G144"
        },
        {
            "id": "G148",
            "text": "G148",
            "html": "<img src=\"/Search/Image?key=G148\" alt=\"G148\" style=\"max-height:24px; max-width: 28px;\" /> G148",
            "display": "G148"
        },
        {
            "id": "G15",
            "text": "G15: combination of G14 and S45",
            "html": "<span class=\"uni\">&#x13151;</span> G15: combination of G14 and S45",
            "display": "G15"
        },
        {
            "id": "G157",
            "text": "G157",
            "html": "<img src=\"/Search/Image?key=G157\" alt=\"G157\" style=\"max-height:24px; max-width: 28px;\" /> G157",
            "display": "G157"
        },
        {
            "id": "G158",
            "text": "G158",
            "html": "<img src=\"/Search/Image?key=G158\" alt=\"G158\" style=\"max-height:24px; max-width: 28px;\" /> G158",
            "display": "G158"
        },
        {
            "id": "G158a",
            "text": "G158A",
            "html": "<img src=\"/Search/Image?key=G158A\" alt=\"G158A\" style=\"max-height:24px; max-width: 28px;\" /> G158A",
            "display": "G158a"
        },
        {
            "id": "G16",
            "text": "G16: vulture and cobra each on V30 [nbty]",
            "html": "<span class=\"uni\">&#x13152;</span> G16: vulture and cobra each on V30",
            "display": "G16"
        },
        {
            "id": "G167",
            "text": "G167",
            "html": "<img src=\"/Search/Image?key=G167\" alt=\"G167\" style=\"max-height:24px; max-width: 28px;\" /> G167",
            "display": "G167"
        },
        {
            "id": "G169",
            "text": "G169",
            "html": "<img src=\"/Search/Image?key=G169\" alt=\"G169\" style=\"max-height:24px; max-width: 28px;\" /> G169",
            "display": "G169"
        },
        {
            "id": "G16a",
            "text": "G16A: vulture and cobra each on V30",
            "html": "<img src=\"/Search/Image?key=G16A\" alt=\"G16A\" style=\"max-height:24px; max-width: 28px;\" /> G16A: vulture and cobra each on V30",
            "display": "G16a"
        },
        {
            "id": "G16b",
            "text": "G16B: vulture and cobra each on V30",
            "html": "<img src=\"/Search/Image?key=G16B\" alt=\"G16B\" style=\"max-height:24px; max-width: 28px;\" /> G16B: vulture and cobra each on V30",
            "display": "G16b"
        },
        {
            "id": "G17",
            "text": "G17: owl [m]",
            "html": "<span class=\"uni\">&#x13153;</span> G17: owl",
            "display": "G17"
        },
        {
            "id": "G176",
            "text": "G176",
            "html": "<img src=\"/Search/Image?key=G176\" alt=\"G176\" style=\"max-height:24px; max-width: 28px;\" /> G176",
            "display": "G176"
        },
        {
            "id": "G177",
            "text": "G177",
            "html": "<img src=\"/Search/Image?key=G177\" alt=\"G177\" style=\"max-height:24px; max-width: 28px;\" /> G177",
            "display": "G177"
        },
        {
            "id": "G17a",
            "text": "G17A: owl",
            "html": "<img src=\"/Search/Image?key=G17A\" alt=\"G17A\" style=\"max-height:24px; max-width: 28px;\" /> G17A: owl",
            "display": "G17a"
        },
        {
            "id": "G18",
            "text": "G18: two owls [mm]",
            "html": "<span class=\"uni\">&#x13154;</span> G18: two owls",
            "display": "G18"
        },
        {
            "id": "G186",
            "text": "G186",
            "html": "<img src=\"/Search/Image?key=G186\" alt=\"G186\" style=\"max-height:24px; max-width: 28px;\" /> G186",
            "display": "G186"
        },
        {
            "id": "G195",
            "text": "G195",
            "html": "<img src=\"/Search/Image?key=G195\" alt=\"G195\" style=\"max-height:24px; max-width: 28px;\" /> G195",
            "display": "G195"
        },
        {
            "id": "G20",
            "text": "G20: combination of G17 and D36",
            "html": "<span class=\"uni\">&#x13156;</span> G20: combination of G17 and D36",
            "display": "G20"
        },
        {
            "id": "G207",
            "text": "G207",
            "html": "<img src=\"/Search/Image?key=G207\" alt=\"G207\" style=\"max-height:24px; max-width: 28px;\" /> G207",
            "display": "G207"
        },
        {
            "id": "G21",
            "text": "G21: guinea-fowl [nH]",
            "html": "<span class=\"uni\">&#x13158;</span> G21: guinea-fowl",
            "display": "G21"
        },
        {
            "id": "G212a",
            "text": "G212A",
            "html": "<img src=\"/Search/Image?key=G212A\" alt=\"G212A\" style=\"max-height:24px; max-width: 28px;\" /> G212A",
            "display": "G212a"
        },
        {
            "id": "G213",
            "text": "G213",
            "html": "<img src=\"/Search/Image?key=G213\" alt=\"G213\" style=\"max-height:24px; max-width: 28px;\" /> G213",
            "display": "G213"
        },
        {
            "id": "G22",
            "text": "G22: hoopoe [Db]",
            "html": "<span class=\"uni\">&#x13159;</span> G22: hoopoe",
            "display": "G22"
        },
        {
            "id": "G225",
            "text": "G225",
            "html": "<img src=\"/Search/Image?key=G225\" alt=\"G225\" style=\"max-height:24px; max-width: 28px;\" /> G225",
            "display": "G225"
        },
        {
            "id": "G227",
            "text": "G227",
            "html": "<img src=\"/Search/Image?key=G227\" alt=\"G227\" style=\"max-height:24px; max-width: 28px;\" /> G227",
            "display": "G227"
        },
        {
            "id": "G228",
            "text": "G228",
            "html": "<img src=\"/Search/Image?key=G228\" alt=\"G228\" style=\"max-height:24px; max-width: 28px;\" /> G228",
            "display": "G228"
        },
        {
            "id": "G229",
            "text": "G229",
            "html": "<img src=\"/Search/Image?key=G229\" alt=\"G229\" style=\"max-height:24px; max-width: 28px;\" /> G229",
            "display": "G229"
        },
        {
            "id": "G22a",
            "text": "G22A: hoopoe",
            "html": "<img src=\"/Search/Image?key=G22A\" alt=\"G22A\" style=\"max-height:24px; max-width: 28px;\" /> G22A: hoopoe",
            "display": "G22a"
        },
        {
            "id": "G23",
            "text": "G23: lawping [rxyt]",
            "html": "<span class=\"uni\">&#x1315A;</span> G23: lawping",
            "display": "G23"
        },
        {
            "id": "G237",
            "text": "G237",
            "html": "<img src=\"/Search/Image?key=G237\" alt=\"G237\" style=\"max-height:24px; max-width: 28px;\" /> G237",
            "display": "G237"
        },
        {
            "id": "G24",
            "text": "G24: lawping with twisted wings",
            "html": "<span class=\"uni\">&#x1315B;</span> G24: lawping with twisted wings",
            "display": "G24"
        },
        {
            "id": "G241",
            "text": "G241",
            "html": "<img src=\"/Search/Image?key=G241\" alt=\"G241\" style=\"max-height:24px; max-width: 28px;\" /> G241",
            "display": "G241"
        },
        {
            "id": "G244",
            "text": "G244",
            "html": "<img src=\"/Search/Image?key=G244\" alt=\"G244\" style=\"max-height:24px; max-width: 28px;\" /> G244",
            "display": "G244"
        },
        {
            "id": "G246",
            "text": "G246",
            "html": "<img src=\"/Search/Image?key=G246\" alt=\"G246\" style=\"max-height:24px; max-width: 28px;\" /> G246",
            "display": "G246"
        },
        {
            "id": "G248",
            "text": "G248",
            "html": "<img src=\"/Search/Image?key=G248\" alt=\"G248\" style=\"max-height:24px; max-width: 28px;\" /> G248",
            "display": "G248"
        },
        {
            "id": "G24a",
            "text": "G24A: lawping with twisted wings",
            "html": "<img src=\"/Search/Image?key=G24A\" alt=\"G24A\" style=\"max-height:24px; max-width: 28px;\" /> G24A: lawping with twisted wings",
            "display": "G24a"
        },
        {
            "id": "G25",
            "text": "G25: northern bald ibis [Ax]",
            "html": "<span class=\"uni\">&#x1315C;</span> G25: northern bald ibis",
            "display": "G25"
        },
        {
            "id": "G250",
            "text": "G250",
            "html": "<img src=\"/Search/Image?key=G250\" alt=\"G250\" style=\"max-height:24px; max-width: 28px;\" /> G250",
            "display": "G250"
        },
        {
            "id": "G25a",
            "text": "G25A: northern bald ibis",
            "html": "<img src=\"/Search/Image?key=G25A\" alt=\"G25A\" style=\"max-height:24px; max-width: 28px;\" /> G25A: northern bald ibis",
            "display": "G25a"
        },
        {
            "id": "G26",
            "text": "G26: sacred ibis on R12",
            "html": "<span class=\"uni\">&#x1315D;</span> G26: sacred ibis on R12",
            "display": "G26"
        },
        {
            "id": "G264a",
            "text": "G264A",
            "html": "<img src=\"/Search/Image?key=G264A\" alt=\"G264A\" style=\"max-height:24px; max-width: 28px;\" /> G264A",
            "display": "G264a"
        },
        {
            "id": "G264b",
            "text": "G264B",
            "html": "G264B",
            "display": "G264b"
        },
        {
            "id": "G26a",
            "text": "G26A: sacred ibis",
            "html": "<span class=\"uni\">&#x1315E;</span> G26A: sacred ibis",
            "display": "G26a"
        },
        {
            "id": "G26b",
            "text": "G26B: sacred ibis on R12",
            "html": "<img src=\"/Search/Image?key=G26B\" alt=\"G26B\" style=\"max-height:24px; max-width: 28px;\" /> G26B: sacred ibis on R12",
            "display": "G26b"
        },
        {
            "id": "G27",
            "text": "G27: flamingo [dSr]",
            "html": "<span class=\"uni\">&#x1315F;</span> G27: flamingo",
            "display": "G27"
        },
        {
            "id": "G276",
            "text": "G276",
            "html": "<img src=\"/Search/Image?key=G276\" alt=\"G276\" style=\"max-height:24px; max-width: 28px;\" /> G276",
            "display": "G276"
        },
        {
            "id": "G28",
            "text": "G28: glossy ibis [gm]",
            "html": "<span class=\"uni\">&#x13160;</span> G28: glossy ibis",
            "display": "G28"
        },
        {
            "id": "G29",
            "text": "G29: saddle-billed stork [bA]",
            "html": "<span class=\"uni\">&#x13161;</span> G29: saddle-billed stork",
            "display": "G29"
        },
        {
            "id": "G291",
            "text": "G291",
            "html": "<img src=\"/Search/Image?key=G291\" alt=\"G291\" style=\"max-height:24px; max-width: 28px;\" /> G291",
            "display": "G291"
        },
        {
            "id": "G29a",
            "text": "G29A: saddle-billed stork",
            "html": "<img src=\"/Search/Image?key=G29A\" alt=\"G29A\" style=\"max-height:24px; max-width: 28px;\" /> G29A: saddle-billed stork",
            "display": "G29a"
        },
        {
            "id": "G3",
            "text": "G3: combination of G1 and U1",
            "html": "<span class=\"uni\">&#x13141;</span> G3: combination of G1 and U1",
            "display": "G3"
        },
        {
            "id": "G30",
            "text": "G30: three saddle-billed storks",
            "html": "<span class=\"uni\">&#x13162;</span> G30: three saddle-billed storks",
            "display": "G30"
        },
        {
            "id": "G306",
            "text": "G306",
            "html": "<img src=\"/Search/Image?key=G306\" alt=\"G306\" style=\"max-height:24px; max-width: 28px;\" /> G306",
            "display": "G306"
        },
        {
            "id": "G30a",
            "text": "G30A: three saddle-billed storks",
            "html": "<img src=\"/Search/Image?key=G30A\" alt=\"G30A\" style=\"max-height:24px; max-width: 28px;\" /> G30A: three saddle-billed storks",
            "display": "G30a"
        },
        {
            "id": "G31",
            "text": "G31: heron",
            "html": "<span class=\"uni\">&#x13163;</span> G31: heron",
            "display": "G31"
        },
        {
            "id": "G31a",
            "text": "G31A: heron",
            "html": "<img src=\"/Search/Image?key=G31A\" alt=\"G31A\" style=\"max-height:24px; max-width: 28px;\" /> G31A: heron",
            "display": "G31a"
        },
        {
            "id": "G32",
            "text": "G32: heron on perch [baHi]",
            "html": "<span class=\"uni\">&#x13164;</span> G32: heron on perch",
            "display": "G32"
        },
        {
            "id": "G33",
            "text": "G33: cattle egret",
            "html": "<span class=\"uni\">&#x13165;</span> G33: cattle egret",
            "display": "G33"
        },
        {
            "id": "G34",
            "text": "G34: ostrich",
            "html": "<span class=\"uni\">&#x13166;</span> G34: ostrich",
            "display": "G34"
        },
        {
            "id": "G35",
            "text": "G35: cormorant [aq]",
            "html": "<span class=\"uni\">&#x13167;</span> G35: cormorant",
            "display": "G35"
        },
        {
            "id": "G36",
            "text": "G36: swallow [wr]",
            "html": "<span class=\"uni\">&#x13168;</span> G36: swallow",
            "display": "G36"
        },
        {
            "id": "G37",
            "text": "G37: sparrow",
            "html": "<span class=\"uni\">&#x1316A;</span> G37: sparrow",
            "display": "G37"
        },
        {
            "id": "G38",
            "text": "G38: white-fronted goose [gb]",
            "html": "<span class=\"uni\">&#x1316C;</span> G38: white-fronted goose",
            "display": "G38"
        },
        {
            "id": "G39",
            "text": "G39: pintail [zA]",
            "html": "<span class=\"uni\">&#x1316D;</span> G39: pintail",
            "display": "G39"
        },
        {
            "id": "G4",
            "text": "G4: buzzard [tyw]",
            "html": "<span class=\"uni\">&#x13142;</span> G4: buzzard",
            "display": "G4"
        },
        {
            "id": "G40",
            "text": "G40: pintail flying [pA]",
            "html": "<span class=\"uni\">&#x1316E;</span> G40: pintail flying",
            "display": "G40"
        },
        {
            "id": "G41",
            "text": "G41: pintail alighting [xn]",
            "html": "<span class=\"uni\">&#x1316F;</span> G41: pintail alighting",
            "display": "G41"
        },
        {
            "id": "G41a",
            "text": "G41A: pintail alighting",
            "html": "<img src=\"/Search/Image?key=G41A\" alt=\"G41A\" style=\"max-height:24px; max-width: 28px;\" /> G41A: pintail alighting",
            "display": "G41a"
        },
        {
            "id": "G42",
            "text": "G42: widgeon [wSA]",
            "html": "<span class=\"uni\">&#x13170;</span> G42: widgeon",
            "display": "G42"
        },
        {
            "id": "G43",
            "text": "G43: quail chick [w]",
            "html": "<span class=\"uni\">&#x13171;</span> G43: quail chick",
            "display": "G43"
        },
        {
            "id": "G43a",
            "text": "G43A: combination of G43 and X1",
            "html": "<span class=\"uni\">&#x13172;</span> G43A: combination of G43 and X1",
            "display": "G43a"
        },
        {
            "id": "G44",
            "text": "G44: two quail chicks [ww]",
            "html": "<span class=\"uni\">&#x13173;</span> G44: two quail chicks",
            "display": "G44"
        },
        {
            "id": "G45",
            "text": "G45: combination of G43 and D36",
            "html": "<span class=\"uni\">&#x13174;</span> G45: combination of G43 and D36",
            "display": "G45"
        },
        {
            "id": "G46",
            "text": "G46: combination of G43 and U1 [mAw]",
            "html": "<span class=\"uni\">&#x13176;</span> G46: combination of G43 and U1",
            "display": "G46"
        },
        {
            "id": "G47",
            "text": "G47: duckling [TA]",
            "html": "<span class=\"uni\">&#x13177;</span> G47: duckling",
            "display": "G47"
        },
        {
            "id": "G48",
            "text": "G48: three ducklings in nest",
            "html": "<span class=\"uni\">&#x13178;</span> G48: three ducklings in nest",
            "display": "G48"
        },
        {
            "id": "G48a",
            "text": "G48A: three ducklings in nest",
            "html": "<img src=\"/Search/Image?key=G48A\" alt=\"G48A\" style=\"max-height:24px; max-width: 28px;\" /> G48A: three ducklings in nest",
            "display": "G48a"
        },
        {
            "id": "G49",
            "text": "G49: three ducklings in pool",
            "html": "<span class=\"uni\">&#x13179;</span> G49: three ducklings in pool",
            "display": "G49"
        },
        {
            "id": "G49e",
            "text": "G49E: three ducklings in pool",
            "html": "<img src=\"/Search/Image?key=G49E\" alt=\"G49E\" style=\"max-height:24px; max-width: 28px;\" /> G49E: three ducklings in pool",
            "display": "G49e"
        },
        {
            "id": "G4a",
            "text": "G4A: buzzard",
            "html": "<img src=\"/Search/Image?key=G4A\" alt=\"G4A\" style=\"max-height:24px; max-width: 28px;\" /> G4A: buzzard",
            "display": "G4a"
        },
        {
            "id": "G5",
            "text": "G5: falcon",
            "html": "<span class=\"uni\">&#x13143;</span> G5: falcon",
            "display": "G5"
        },
        {
            "id": "G51",
            "text": "G51: bird pecking at fish",
            "html": "<span class=\"uni\">&#x1317B;</span> G51: bird pecking at fish",
            "display": "G51"
        },
        {
            "id": "G52",
            "text": "G52: goose picking up grain",
            "html": "<span class=\"uni\">&#x1317C;</span> G52: goose picking up grain",
            "display": "G52"
        },
        {
            "id": "G53",
            "text": "G53: human-headed bird with R7",
            "html": "<span class=\"uni\">&#x1317D;</span> G53: human-headed bird with R7",
            "display": "G53"
        },
        {
            "id": "G53a",
            "text": "G53A: human-headed bird with R7",
            "html": "<img src=\"/Search/Image?key=G53A\" alt=\"G53A\" style=\"max-height:24px; max-width: 28px;\" /> G53A: human-headed bird with R7",
            "display": "G53a"
        },
        {
            "id": "G54",
            "text": "G54: plucked bird [snD]",
            "html": "<span class=\"uni\">&#x1317E;</span> G54: plucked bird",
            "display": "G54"
        },
        {
            "id": "G56",
            "text": "G56",
            "html": "<img src=\"/Search/Image?key=G56\" alt=\"G56\" style=\"max-height:24px; max-width: 28px;\" /> G56",
            "display": "G56"
        },
        {
            "id": "G57",
            "text": "G57",
            "html": "<img src=\"/Search/Image?key=G57\" alt=\"G57\" style=\"max-height:24px; max-width: 28px;\" /> G57",
            "display": "G57"
        },
        {
            "id": "G58",
            "text": "G58",
            "html": "<img src=\"/Search/Image?key=G58\" alt=\"G58\" style=\"max-height:24px; max-width: 28px;\" /> G58",
            "display": "G58"
        },
        {
            "id": "G6",
            "text": "G6: combination of G5 and S45",
            "html": "<span class=\"uni\">&#x13144;</span> G6: combination of G5 and S45",
            "display": "G6"
        },
        {
            "id": "G60",
            "text": "G60",
            "html": "<img src=\"/Search/Image?key=G60\" alt=\"G60\" style=\"max-height:24px; max-width: 28px;\" /> G60",
            "display": "G60"
        },
        {
            "id": "G62",
            "text": "G62",
            "html": "<img src=\"/Search/Image?key=G62\" alt=\"G62\" style=\"max-height:24px; max-width: 28px;\" /> G62",
            "display": "G62"
        },
        {
            "id": "G67",
            "text": "G67",
            "html": "<img src=\"/Search/Image?key=G67\" alt=\"G67\" style=\"max-height:24px; max-width: 28px;\" /> G67",
            "display": "G67"
        },
        {
            "id": "G68",
            "text": "G68",
            "html": "<img src=\"/Search/Image?key=G68\" alt=\"G68\" style=\"max-height:24px; max-width: 28px;\" /> G68",
            "display": "G68"
        },
        {
            "id": "G68a",
            "text": "G68A",
            "html": "<img src=\"/Search/Image?key=G68A\" alt=\"G68A\" style=\"max-height:24px; max-width: 28px;\" /> G68A",
            "display": "G68a"
        },
        {
            "id": "G7",
            "text": "G7: falcon on R12",
            "html": "<span class=\"uni\">&#x13146;</span> G7: falcon on R12",
            "display": "G7"
        },
        {
            "id": "G79",
            "text": "G79",
            "html": "<img src=\"/Search/Image?key=G79\" alt=\"G79\" style=\"max-height:24px; max-width: 28px;\" /> G79",
            "display": "G79"
        },
        {
            "id": "G7a",
            "text": "G7A: falcon in boat",
            "html": "<span class=\"uni\">&#x13147;</span> G7A: falcon in boat",
            "display": "G7a"
        },
        {
            "id": "G7b",
            "text": "G7B: falcon in boat",
            "html": "<span class=\"uni\">&#x13148;</span> G7B: falcon in boat",
            "display": "G7b"
        },
        {
            "id": "G7c",
            "text": "G7C: falcon on R12",
            "html": "<img src=\"/Search/Image?key=G7C\" alt=\"G7C\" style=\"max-height:24px; max-width: 28px;\" /> G7C: falcon on R12",
            "display": "G7c"
        },
        {
            "id": "G8",
            "text": "G8: falcon on S12",
            "html": "<span class=\"uni\">&#x13149;</span> G8: falcon on S12",
            "display": "G8"
        },
        {
            "id": "G81",
            "text": "G81",
            "html": "<img src=\"/Search/Image?key=G81\" alt=\"G81\" style=\"max-height:24px; max-width: 28px;\" /> G81",
            "display": "G81"
        },
        {
            "id": "G87",
            "text": "G87",
            "html": "<img src=\"/Search/Image?key=G87\" alt=\"G87\" style=\"max-height:24px; max-width: 28px;\" /> G87",
            "display": "G87"
        },
        {
            "id": "G9",
            "text": "G9: falcon with N5 on head",
            "html": "<span class=\"uni\">&#x1314A;</span> G9: falcon with N5 on head",
            "display": "G9"
        },
        {
            "id": "G96",
            "text": "G96",
            "html": "<img src=\"/Search/Image?key=G96\" alt=\"G96\" style=\"max-height:24px; max-width: 28px;\" /> G96",
            "display": "G96"
        },
        {
            "id": "H1",
            "text": "H1: head of pintail",
            "html": "<span class=\"uni\">&#x1317F;</span> H1: head of pintail",
            "display": "H1"
        },
        {
            "id": "H16",
            "text": "H16",
            "html": "<img src=\"/Search/Image?key=H16\" alt=\"H16\" style=\"max-height:24px; max-width: 28px;\" /> H16",
            "display": "H16"
        },
        {
            "id": "H17",
            "text": "H17",
            "html": "<img src=\"/Search/Image?key=H17\" alt=\"H17\" style=\"max-height:24px; max-width: 28px;\" /> H17",
            "display": "H17"
        },
        {
            "id": "H18a",
            "text": "H18A",
            "html": "<img src=\"/Search/Image?key=H18A\" alt=\"H18A\" style=\"max-height:24px; max-width: 28px;\" /> H18A",
            "display": "H18a"
        },
        {
            "id": "H19",
            "text": "H19",
            "html": "<img src=\"/Search/Image?key=H19\" alt=\"H19\" style=\"max-height:24px; max-width: 28px;\" /> H19",
            "display": "H19"
        },
        {
            "id": "H2",
            "text": "H2: head of crested bird [pq]",
            "html": "<span class=\"uni\">&#x13180;</span> H2: head of crested bird",
            "display": "H2"
        },
        {
            "id": "H20",
            "text": "H20",
            "html": "<img src=\"/Search/Image?key=H20\" alt=\"H20\" style=\"max-height:24px; max-width: 28px;\" /> H20",
            "display": "H20"
        },
        {
            "id": "H25",
            "text": "H25",
            "html": "<img src=\"/Search/Image?key=H25\" alt=\"H25\" style=\"max-height:24px; max-width: 28px;\" /> H25",
            "display": "H25"
        },
        {
            "id": "H27",
            "text": "H27",
            "html": "<img src=\"/Search/Image?key=H27\" alt=\"H27\" style=\"max-height:24px; max-width: 28px;\" /> H27",
            "display": "H27"
        },
        {
            "id": "H2a",
            "text": "H2A: head of crested bird",
            "html": "<img src=\"/Search/Image?key=H2A\" alt=\"H2A\" style=\"max-height:24px; max-width: 28px;\" /> H2A: head of crested bird",
            "display": "H2a"
        },
        {
            "id": "H3",
            "text": "H3: head of spoonbill [pAq]",
            "html": "<span class=\"uni\">&#x13181;</span> H3: head of spoonbill",
            "display": "H3"
        },
        {
            "id": "H34",
            "text": "H34",
            "html": "<img src=\"/Search/Image?key=H34\" alt=\"H34\" style=\"max-height:24px; max-width: 28px;\" /> H34",
            "display": "H34"
        },
        {
            "id": "H4",
            "text": "H4: head of vulture [nr]",
            "html": "<span class=\"uni\">&#x13182;</span> H4: head of vulture",
            "display": "H4"
        },
        {
            "id": "H47",
            "text": "H47",
            "html": "<img src=\"/Search/Image?key=H47\" alt=\"H47\" style=\"max-height:24px; max-width: 28px;\" /> H47",
            "display": "H47"
        },
        {
            "id": "H5",
            "text": "H5: wing",
            "html": "<span class=\"uni\">&#x13183;</span> H5: wing",
            "display": "H5"
        },
        {
            "id": "H5a",
            "text": "H5A: wing",
            "html": "<img src=\"/Search/Image?key=H5A\" alt=\"H5A\" style=\"max-height:24px; max-width: 28px;\" /> H5A: wing",
            "display": "H5a"
        },
        {
            "id": "H6",
            "text": "H6: feather [tall] [Sw]",
            "html": "<span class=\"uni\">&#x13184;</span> H6: feather",
            "display": "H6"
        },
        {
            "id": "H6a",
            "text": "H6A: hieratic feather [tall]",
            "html": "<span class=\"uni\">&#x13185;</span> H6A: hieratic feather",
            "display": "H6a"
        },
        {
            "id": "H6b",
            "text": "H6B: feather",
            "html": "<img src=\"/Search/Image?key=H6B\" alt=\"H6B\" style=\"max-height:24px; max-width: 28px;\" /> H6B: feather",
            "display": "H6b"
        },
        {
            "id": "H7",
            "text": "H7: claw",
            "html": "<span class=\"uni\">&#x13186;</span> H7: claw",
            "display": "H7"
        },
        {
            "id": "H8",
            "text": "H8: egg [narrow]",
            "html": "<span class=\"uni\">&#x13187;</span> H8: egg",
            "display": "H8"
        },
        {
            "id": "I1",
            "text": "I1: gecko [aSA]",
            "html": "<span class=\"uni\">&#x13188;</span> I1: gecko",
            "display": "I1"
        },
        {
            "id": "I10",
            "text": "I10: cobra [D]",
            "html": "<span class=\"uni\">&#x13193;</span> I10: cobra",
            "display": "I10"
        },
        {
            "id": "I100",
            "text": "I100",
            "html": "<img src=\"/Search/Image?key=I100\" alt=\"I100\" style=\"max-height:24px; max-width: 28px;\" /> I100",
            "display": "I100"
        },
        {
            "id": "I103",
            "text": "I103",
            "html": "<img src=\"/Search/Image?key=I103\" alt=\"I103\" style=\"max-height:24px; max-width: 28px;\" /> I103",
            "display": "I103"
        },
        {
            "id": "I111",
            "text": "I111",
            "html": "<img src=\"/Search/Image?key=I111\" alt=\"I111\" style=\"max-height:24px; max-width: 28px;\" /> I111",
            "display": "I111"
        },
        {
            "id": "I114",
            "text": "I114",
            "html": "<img src=\"/Search/Image?key=I114\" alt=\"I114\" style=\"max-height:24px; max-width: 28px;\" /> I114",
            "display": "I114"
        },
        {
            "id": "I12",
            "text": "I12: erect cobra",
            "html": "<span class=\"uni\">&#x13197;</span> I12: erect cobra",
            "display": "I12"
        },
        {
            "id": "I13",
            "text": "I13: erect cobra on V30",
            "html": "<span class=\"uni\">&#x13198;</span> I13: erect cobra on V30",
            "display": "I13"
        },
        {
            "id": "I14",
            "text": "I14: snake",
            "html": "<span class=\"uni\">&#x13199;</span> I14: snake",
            "display": "I14"
        },
        {
            "id": "I14a",
            "text": "I14A: snake",
            "html": "<img src=\"/Search/Image?key=I14A\" alt=\"I14A\" style=\"max-height:24px; max-width: 28px;\" /> I14A: snake",
            "display": "I14a"
        },
        {
            "id": "I14b",
            "text": "I14B: snake",
            "html": "<img src=\"/Search/Image?key=I14B\" alt=\"I14B\" style=\"max-height:24px; max-width: 28px;\" /> I14B: snake",
            "display": "I14b"
        },
        {
            "id": "I14c",
            "text": "I14C: snake",
            "html": "<img src=\"/Search/Image?key=I14C\" alt=\"I14C\" style=\"max-height:24px; max-width: 28px;\" /> I14C: snake",
            "display": "I14c"
        },
        {
            "id": "I15",
            "text": "I15: snake",
            "html": "<span class=\"uni\">&#x1319A;</span> I15: snake",
            "display": "I15"
        },
        {
            "id": "I15b",
            "text": "I15B: snake",
            "html": "<img src=\"/Search/Image?key=I15B\" alt=\"I15B\" style=\"max-height:24px; max-width: 28px;\" /> I15B: snake",
            "display": "I15b"
        },
        {
            "id": "I2",
            "text": "I2: turtle [Styw]",
            "html": "<span class=\"uni\">&#x13189;</span> I2: turtle",
            "display": "I2"
        },
        {
            "id": "I24b",
            "text": "I24B",
            "html": "<img src=\"/Search/Image?key=I24B\" alt=\"I24B\" style=\"max-height:24px; max-width: 28px;\" /> I24B",
            "display": "I24b"
        },
        {
            "id": "I25b",
            "text": "I25B",
            "html": "<img src=\"/Search/Image?key=I25B\" alt=\"I25B\" style=\"max-height:24px; max-width: 28px;\" /> I25B",
            "display": "I25b"
        },
        {
            "id": "I3",
            "text": "I3: crocodile [mzH]",
            "html": "<span class=\"uni\">&#x1318A;</span> I3: crocodile",
            "display": "I3"
        },
        {
            "id": "I31a",
            "text": "I31A",
            "html": "<img src=\"/Search/Image?key=I31A\" alt=\"I31A\" style=\"max-height:24px; max-width: 28px;\" /> I31A",
            "display": "I31a"
        },
        {
            "id": "I31b",
            "text": "I31B",
            "html": "<img src=\"/Search/Image?key=I31B\" alt=\"I31B\" style=\"max-height:24px; max-width: 28px;\" /> I31B",
            "display": "I31b"
        },
        {
            "id": "I34",
            "text": "I34",
            "html": "<img src=\"/Search/Image?key=I34\" alt=\"I34\" style=\"max-height:24px; max-width: 28px;\" /> I34",
            "display": "I34"
        },
        {
            "id": "I3c",
            "text": "I3C: crocodile",
            "html": "<img src=\"/Search/Image?key=I3C\" alt=\"I3C\" style=\"max-height:24px; max-width: 28px;\" /> I3C: crocodile",
            "display": "I3c"
        },
        {
            "id": "I3g",
            "text": "I3G: crocodile",
            "html": "<img src=\"/Search/Image?key=I3G\" alt=\"I3G\" style=\"max-height:24px; max-width: 28px;\" /> I3G: crocodile",
            "display": "I3g"
        },
        {
            "id": "I5",
            "text": "I5: crocodile with curved tail [sAq]",
            "html": "<span class=\"uni\">&#x1318C;</span> I5: crocodile with curved tail",
            "display": "I5"
        },
        {
            "id": "I52a",
            "text": "I52A",
            "html": "<img src=\"/Search/Image?key=I52A\" alt=\"I52A\" style=\"max-height:24px; max-width: 28px;\" /> I52A",
            "display": "I52a"
        },
        {
            "id": "I55",
            "text": "I55",
            "html": "<img src=\"/Search/Image?key=I55\" alt=\"I55\" style=\"max-height:24px; max-width: 28px;\" /> I55",
            "display": "I55"
        },
        {
            "id": "I58",
            "text": "I58",
            "html": "<img src=\"/Search/Image?key=I58\" alt=\"I58\" style=\"max-height:24px; max-width: 28px;\" /> I58",
            "display": "I58"
        },
        {
            "id": "I5a",
            "text": "I5A: image of crocodile",
            "html": "<span class=\"uni\">&#x1318D;</span> I5A: image of crocodile",
            "display": "I5a"
        },
        {
            "id": "I6",
            "text": "I6: crocodile scales [narrow] [km]",
            "html": "<span class=\"uni\">&#x1318E;</span> I6: crocodile scales",
            "display": "I6"
        },
        {
            "id": "I66",
            "text": "I66",
            "html": "<img src=\"/Search/Image?key=I66\" alt=\"I66\" style=\"max-height:24px; max-width: 28px;\" /> I66",
            "display": "I66"
        },
        {
            "id": "I7",
            "text": "I7: frog",
            "html": "<span class=\"uni\">&#x1318F;</span> I7: frog",
            "display": "I7"
        },
        {
            "id": "I70b",
            "text": "I70B",
            "html": "<img src=\"/Search/Image?key=I70B\" alt=\"I70B\" style=\"max-height:24px; max-width: 28px;\" /> I70B",
            "display": "I70b"
        },
        {
            "id": "I73",
            "text": "I73",
            "html": "<img src=\"/Search/Image?key=I73\" alt=\"I73\" style=\"max-height:24px; max-width: 28px;\" /> I73",
            "display": "I73"
        },
        {
            "id": "I74",
            "text": "I74",
            "html": "<img src=\"/Search/Image?key=I74\" alt=\"I74\" style=\"max-height:24px; max-width: 28px;\" /> I74",
            "display": "I74"
        },
        {
            "id": "I75",
            "text": "I75",
            "html": "<img src=\"/Search/Image?key=I75\" alt=\"I75\" style=\"max-height:24px; max-width: 28px;\" /> I75",
            "display": "I75"
        },
        {
            "id": "I8",
            "text": "I8: tadpole [Hfn]",
            "html": "<span class=\"uni\">&#x13190;</span> I8: tadpole",
            "display": "I8"
        },
        {
            "id": "I86",
            "text": "I86",
            "html": "<img src=\"/Search/Image?key=I86\" alt=\"I86\" style=\"max-height:24px; max-width: 28px;\" /> I86",
            "display": "I86"
        },
        {
            "id": "I86a",
            "text": "I86A",
            "html": "<img src=\"/Search/Image?key=I86A\" alt=\"I86A\" style=\"max-height:24px; max-width: 28px;\" /> I86A",
            "display": "I86a"
        },
        {
            "id": "I86b",
            "text": "I86B",
            "html": "<img src=\"/Search/Image?key=I86B\" alt=\"I86B\" style=\"max-height:24px; max-width: 28px;\" /> I86B",
            "display": "I86b"
        },
        {
            "id": "I86d",
            "text": "I86D",
            "html": "<img src=\"/Search/Image?key=I86D\" alt=\"I86D\" style=\"max-height:24px; max-width: 28px;\" /> I86D",
            "display": "I86d"
        },
        {
            "id": "I86e",
            "text": "I86E",
            "html": "<img src=\"/Search/Image?key=I86E\" alt=\"I86E\" style=\"max-height:24px; max-width: 28px;\" /> I86E",
            "display": "I86e"
        },
        {
            "id": "I87",
            "text": "I87",
            "html": "<img src=\"/Search/Image?key=I87\" alt=\"I87\" style=\"max-height:24px; max-width: 28px;\" /> I87",
            "display": "I87"
        },
        {
            "id": "I9",
            "text": "I9: horned viper [f]",
            "html": "<span class=\"uni\">&#x13191;</span> I9: horned viper",
            "display": "I9"
        },
        {
            "id": "I93",
            "text": "I93",
            "html": "<img src=\"/Search/Image?key=I93\" alt=\"I93\" style=\"max-height:24px; max-width: 28px;\" /> I93",
            "display": "I93"
        },
        {
            "id": "I93a",
            "text": "I93A",
            "html": "<img src=\"/Search/Image?key=I93A\" alt=\"I93A\" style=\"max-height:24px; max-width: 28px;\" /> I93A",
            "display": "I93a"
        },
        {
            "id": "K1",
            "text": "K1: tilapia [in]",
            "html": "<span class=\"uni\">&#x1319B;</span> K1: tilapia",
            "display": "K1"
        },
        {
            "id": "K13",
            "text": "K13",
            "html": "<img src=\"/Search/Image?key=K13\" alt=\"K13\" style=\"max-height:24px; max-width: 28px;\" /> K13",
            "display": "K13"
        },
        {
            "id": "K14",
            "text": "K14",
            "html": "<img src=\"/Search/Image?key=K14\" alt=\"K14\" style=\"max-height:24px; max-width: 28px;\" /> K14",
            "display": "K14"
        },
        {
            "id": "K17",
            "text": "K17",
            "html": "<img src=\"/Search/Image?key=K17\" alt=\"K17\" style=\"max-height:24px; max-width: 28px;\" /> K17",
            "display": "K17"
        },
        {
            "id": "K18",
            "text": "K18",
            "html": "<img src=\"/Search/Image?key=K18\" alt=\"K18\" style=\"max-height:24px; max-width: 28px;\" /> K18",
            "display": "K18"
        },
        {
            "id": "K18b",
            "text": "K18B",
            "html": "<img src=\"/Search/Image?key=K18B\" alt=\"K18B\" style=\"max-height:24px; max-width: 28px;\" /> K18B",
            "display": "K18b"
        },
        {
            "id": "K2",
            "text": "K2: barbel",
            "html": "<span class=\"uni\">&#x1319C;</span> K2: barbel",
            "display": "K2"
        },
        {
            "id": "K23",
            "text": "K23",
            "html": "<img src=\"/Search/Image?key=K23\" alt=\"K23\" style=\"max-height:24px; max-width: 28px;\" /> K23",
            "display": "K23"
        },
        {
            "id": "K26",
            "text": "K26",
            "html": "<img src=\"/Search/Image?key=K26\" alt=\"K26\" style=\"max-height:24px; max-width: 28px;\" /> K26",
            "display": "K26"
        },
        {
            "id": "K3",
            "text": "K3: mullet [ad]",
            "html": "<span class=\"uni\">&#x1319D;</span> K3: mullet",
            "display": "K3"
        },
        {
            "id": "K4",
            "text": "K4: elephant-snout fish [XA]",
            "html": "<span class=\"uni\">&#x1319E;</span> K4: elephant-snout fish",
            "display": "K4"
        },
        {
            "id": "K4a",
            "text": "K4A: elephant-snout fish",
            "html": "<img src=\"/Search/Image?key=K4A\" alt=\"K4A\" style=\"max-height:24px; max-width: 28px;\" /> K4A: elephant-snout fish",
            "display": "K4a"
        },
        {
            "id": "K5",
            "text": "K5: Petrocephalus bane [bz]",
            "html": "<span class=\"uni\">&#x1319F;</span> K5: Petrocephalus bane",
            "display": "K5"
        },
        {
            "id": "K6",
            "text": "K6: fish scale [narrow] [nSmt]",
            "html": "<span class=\"uni\">&#x131A0;</span> K6: fish scale",
            "display": "K6"
        },
        {
            "id": "K7",
            "text": "K7: puffer",
            "html": "<span class=\"uni\">&#x131A1;</span> K7: puffer",
            "display": "K7"
        },
        {
            "id": "L1",
            "text": "L1: dung beetle [xpr]",
            "html": "<span class=\"uni\">&#x131A3;</span> L1: dung beetle",
            "display": "L1"
        },
        {
            "id": "L12a",
            "text": "L12A",
            "html": "<img src=\"/Search/Image?key=L12A\" alt=\"L12A\" style=\"max-height:24px; max-width: 28px;\" /> L12A",
            "display": "L12a"
        },
        {
            "id": "L17",
            "text": "L17",
            "html": "<img src=\"/Search/Image?key=L17\" alt=\"L17\" style=\"max-height:24px; max-width: 28px;\" /> L17",
            "display": "L17"
        },
        {
            "id": "L18",
            "text": "L18",
            "html": "<img src=\"/Search/Image?key=L18\" alt=\"L18\" style=\"max-height:24px; max-width: 28px;\" /> L18",
            "display": "L18"
        },
        {
            "id": "L19",
            "text": "L19",
            "html": "<img src=\"/Search/Image?key=L19\" alt=\"L19\" style=\"max-height:24px; max-width: 28px;\" /> L19",
            "display": "L19"
        },
        {
            "id": "L2",
            "text": "L2: bee [bit]",
            "html": "<span class=\"uni\">&#x131A4;</span> L2: bee",
            "display": "L2"
        },
        {
            "id": "L25",
            "text": "L25",
            "html": "<img src=\"/Search/Image?key=L25\" alt=\"L25\" style=\"max-height:24px; max-width: 28px;\" /> L25",
            "display": "L25"
        },
        {
            "id": "L3",
            "text": "L3: fly",
            "html": "<span class=\"uni\">&#x131A6;</span> L3: fly",
            "display": "L3"
        },
        {
            "id": "L3a",
            "text": "L3A: fly",
            "html": "<img src=\"/Search/Image?key=L3A\" alt=\"L3A\" style=\"max-height:24px; max-width: 28px;\" /> L3A: fly",
            "display": "L3a"
        },
        {
            "id": "L4",
            "text": "L4: locust",
            "html": "<span class=\"uni\">&#x131A7;</span> L4: locust",
            "display": "L4"
        },
        {
            "id": "L5",
            "text": "L5: centipede",
            "html": "<span class=\"uni\">&#x131A8;</span> L5: centipede",
            "display": "L5"
        },
        {
            "id": "L6",
            "text": "L6: shell [narrow]",
            "html": "<span class=\"uni\">&#x131A9;</span> L6: shell",
            "display": "L6"
        },
        {
            "id": "L7",
            "text": "L7: scorpion [tall] [srqt]",
            "html": "<span class=\"uni\">&#x131AB;</span> L7: scorpion",
            "display": "L7"
        },
        {
            "id": "M1",
            "text": "M1: tree [iAm]",
            "html": "<span class=\"uni\">&#x131AD;</span> M1: tree",
            "display": "M1"
        },
        {
            "id": "M10",
            "text": "M10: lotus bud with straight stem",
            "html": "<span class=\"uni\">&#x131B9;</span> M10: lotus bud with straight stem",
            "display": "M10"
        },
        {
            "id": "M102",
            "text": "M102",
            "html": "<img src=\"/Search/Image?key=M102\" alt=\"M102\" style=\"max-height:24px; max-width: 28px;\" /> M102",
            "display": "M102"
        },
        {
            "id": "M107",
            "text": "M107",
            "html": "<img src=\"/Search/Image?key=M107\" alt=\"M107\" style=\"max-height:24px; max-width: 28px;\" /> M107",
            "display": "M107"
        },
        {
            "id": "M11",
            "text": "M11: flower on long twisted stalk [broad] [wdn]",
            "html": "<span class=\"uni\">&#x131BB;</span> M11: flower on long twisted stalk",
            "display": "M11"
        },
        {
            "id": "M111",
            "text": "M111",
            "html": "<img src=\"/Search/Image?key=M111\" alt=\"M111\" style=\"max-height:24px; max-width: 28px;\" /> M111",
            "display": "M111"
        },
        {
            "id": "M112",
            "text": "M112",
            "html": "<img src=\"/Search/Image?key=M112\" alt=\"M112\" style=\"max-height:24px; max-width: 28px;\" /> M112",
            "display": "M112"
        },
        {
            "id": "M12",
            "text": "M12: lotus plant [tall] [xA]",
            "html": "<span class=\"uni\">&#x131BC;</span> M12: lotus plant",
            "display": "M12"
        },
        {
            "id": "M121",
            "text": "M121",
            "html": "<img src=\"/Search/Image?key=M121\" alt=\"M121\" style=\"max-height:24px; max-width: 28px;\" /> M121",
            "display": "M121"
        },
        {
            "id": "M127",
            "text": "M127",
            "html": "<img src=\"/Search/Image?key=M127\" alt=\"M127\" style=\"max-height:24px; max-width: 28px;\" /> M127",
            "display": "M127"
        },
        {
            "id": "M12b",
            "text": "M12B: ...",
            "html": "<span class=\"uni\">&#x131BE;</span> M12B: ...",
            "display": "M12b"
        },
        {
            "id": "M13",
            "text": "M13: papyrus [tall] [wAD]",
            "html": "<span class=\"uni\">&#x131C5;</span> M13: papyrus",
            "display": "M13"
        },
        {
            "id": "M131",
            "text": "M131",
            "html": "<img src=\"/Search/Image?key=M131\" alt=\"M131\" style=\"max-height:24px; max-width: 28px;\" /> M131",
            "display": "M131"
        },
        {
            "id": "M133",
            "text": "M133",
            "html": "<img src=\"/Search/Image?key=M133\" alt=\"M133\" style=\"max-height:24px; max-width: 28px;\" /> M133",
            "display": "M133"
        },
        {
            "id": "M135",
            "text": "M135",
            "html": "<img src=\"/Search/Image?key=M135\" alt=\"M135\" style=\"max-height:24px; max-width: 28px;\" /> M135",
            "display": "M135"
        },
        {
            "id": "M13a",
            "text": "M13A: papyrus",
            "html": "<img src=\"/Search/Image?key=M13A\" alt=\"M13A\" style=\"max-height:24px; max-width: 28px;\" /> M13A: papyrus",
            "display": "M13a"
        },
        {
            "id": "M13b",
            "text": "M13B: papyrus",
            "html": "M13B: papyrus",
            "display": "M13b"
        },
        {
            "id": "M14",
            "text": "M14: combination of M13 and I10",
            "html": "<span class=\"uni\">&#x131C6;</span> M14: combination of M13 and I10",
            "display": "M14"
        },
        {
            "id": "M145",
            "text": "M145",
            "html": "<img src=\"/Search/Image?key=M145\" alt=\"M145\" style=\"max-height:24px; max-width: 28px;\" /> M145",
            "display": "M145"
        },
        {
            "id": "M147",
            "text": "M147",
            "html": "<img src=\"/Search/Image?key=M147\" alt=\"M147\" style=\"max-height:24px; max-width: 28px;\" /> M147",
            "display": "M147"
        },
        {
            "id": "M15",
            "text": "M15: clump of papyrus with buds",
            "html": "<span class=\"uni\">&#x131C7;</span> M15: clump of papyrus with buds",
            "display": "M15"
        },
        {
            "id": "M156",
            "text": "M156",
            "html": "<img src=\"/Search/Image?key=M156\" alt=\"M156\" style=\"max-height:24px; max-width: 28px;\" /> M156",
            "display": "M156"
        },
        {
            "id": "M159",
            "text": "M159",
            "html": "<img src=\"/Search/Image?key=M159\" alt=\"M159\" style=\"max-height:24px; max-width: 28px;\" /> M159",
            "display": "M159"
        },
        {
            "id": "M16",
            "text": "M16: clump of papyrus [HA]",
            "html": "<span class=\"uni\">&#x131C9;</span> M16: clump of papyrus",
            "display": "M16"
        },
        {
            "id": "M161",
            "text": "M161",
            "html": "<img src=\"/Search/Image?key=M161\" alt=\"M161\" style=\"max-height:24px; max-width: 28px;\" /> M161",
            "display": "M161"
        },
        {
            "id": "M163",
            "text": "M163",
            "html": "<img src=\"/Search/Image?key=M163\" alt=\"M163\" style=\"max-height:24px; max-width: 28px;\" /> M163",
            "display": "M163"
        },
        {
            "id": "M165",
            "text": "M165",
            "html": "<img src=\"/Search/Image?key=M165\" alt=\"M165\" style=\"max-height:24px; max-width: 28px;\" /> M165",
            "display": "M165"
        },
        {
            "id": "M16b",
            "text": "M16B: clump of papyrus",
            "html": "<img src=\"/Search/Image?key=M16B\" alt=\"M16B\" style=\"max-height:24px; max-width: 28px;\" /> M16B: clump of papyrus",
            "display": "M16b"
        },
        {
            "id": "M17",
            "text": "M17: reed [tall] [i]",
            "html": "<span class=\"uni\">&#x131CB;</span> M17: reed",
            "display": "M17"
        },
        {
            "id": "M170",
            "text": "M170",
            "html": "<img src=\"/Search/Image?key=M170\" alt=\"M170\" style=\"max-height:24px; max-width: 28px;\" /> M170",
            "display": "M170"
        },
        {
            "id": "M171",
            "text": "M171",
            "html": "<img src=\"/Search/Image?key=M171\" alt=\"M171\" style=\"max-height:24px; max-width: 28px;\" /> M171",
            "display": "M171"
        },
        {
            "id": "M173",
            "text": "M173",
            "html": "<img src=\"/Search/Image?key=M173\" alt=\"M173\" style=\"max-height:24px; max-width: 28px;\" /> M173",
            "display": "M173"
        },
        {
            "id": "M174",
            "text": "M174",
            "html": "<img src=\"/Search/Image?key=M174\" alt=\"M174\" style=\"max-height:24px; max-width: 28px;\" /> M174",
            "display": "M174"
        },
        {
            "id": "M174a",
            "text": "M174A",
            "html": "<img src=\"/Search/Image?key=M174A\" alt=\"M174A\" style=\"max-height:24px; max-width: 28px;\" /> M174A",
            "display": "M174a"
        },
        {
            "id": "M177a",
            "text": "M177A",
            "html": "<img src=\"/Search/Image?key=M177A\" alt=\"M177A\" style=\"max-height:24px; max-width: 28px;\" /> M177A",
            "display": "M177a"
        },
        {
            "id": "M17a",
            "text": "M17A: two reeds",
            "html": "<span class=\"uni\">&#x131CC;</span> M17A: two reeds",
            "display": "M17a"
        },
        {
            "id": "M18",
            "text": "M18: combination of M17 and D54 [ii]",
            "html": "<span class=\"uni\">&#x131CD;</span> M18: combination of M17 and D54",
            "display": "M18"
        },
        {
            "id": "M181",
            "text": "M181",
            "html": "<img src=\"/Search/Image?key=M181\" alt=\"M181\" style=\"max-height:24px; max-width: 28px;\" /> M181",
            "display": "M181"
        },
        {
            "id": "M182",
            "text": "M182",
            "html": "<img src=\"/Search/Image?key=M182\" alt=\"M182\" style=\"max-height:24px; max-width: 28px;\" /> M182",
            "display": "M182"
        },
        {
            "id": "M184",
            "text": "M184",
            "html": "<img src=\"/Search/Image?key=M184\" alt=\"M184\" style=\"max-height:24px; max-width: 28px;\" /> M184",
            "display": "M184"
        },
        {
            "id": "M187",
            "text": "M187",
            "html": "<img src=\"/Search/Image?key=M187\" alt=\"M187\" style=\"max-height:24px; max-width: 28px;\" /> M187",
            "display": "M187"
        },
        {
            "id": "M19",
            "text": "M19: heaped conical cakes between M17 and U36",
            "html": "<span class=\"uni\">&#x131CE;</span> M19: heaped conical cakes between M17 and U36",
            "display": "M19"
        },
        {
            "id": "M190",
            "text": "M190",
            "html": "<img src=\"/Search/Image?key=M190\" alt=\"M190\" style=\"max-height:24px; max-width: 28px;\" /> M190",
            "display": "M190"
        },
        {
            "id": "M192",
            "text": "M192",
            "html": "<img src=\"/Search/Image?key=M192\" alt=\"M192\" style=\"max-height:24px; max-width: 28px;\" /> M192",
            "display": "M192"
        },
        {
            "id": "M193",
            "text": "M193",
            "html": "<img src=\"/Search/Image?key=M193\" alt=\"M193\" style=\"max-height:24px; max-width: 28px;\" /> M193",
            "display": "M193"
        },
        {
            "id": "M194",
            "text": "M194",
            "html": "<img src=\"/Search/Image?key=M194\" alt=\"M194\" style=\"max-height:24px; max-width: 28px;\" /> M194",
            "display": "M194"
        },
        {
            "id": "M195",
            "text": "M195",
            "html": "<img src=\"/Search/Image?key=M195\" alt=\"M195\" style=\"max-height:24px; max-width: 28px;\" /> M195",
            "display": "M195"
        },
        {
            "id": "M1a",
            "text": "M1A: combination of M1 and M3",
            "html": "<span class=\"uni\">&#x131AE;</span> M1A: combination of M1 and M3",
            "display": "M1a"
        },
        {
            "id": "M1c",
            "text": "M1C: tree",
            "html": "<img src=\"/Search/Image?key=M1C\" alt=\"M1C\" style=\"max-height:24px; max-width: 28px;\" /> M1C: tree",
            "display": "M1c"
        },
        {
            "id": "M2",
            "text": "M2: plant [Hn]",
            "html": "<span class=\"uni\">&#x131B0;</span> M2: plant",
            "display": "M2"
        },
        {
            "id": "M20",
            "text": "M20: field of reeds [sxt]",
            "html": "<span class=\"uni\">&#x131CF;</span> M20: field of reeds",
            "display": "M20"
        },
        {
            "id": "M200",
            "text": "M200",
            "html": "<img src=\"/Search/Image?key=M200\" alt=\"M200\" style=\"max-height:24px; max-width: 28px;\" /> M200",
            "display": "M200"
        },
        {
            "id": "M201",
            "text": "M201",
            "html": "<img src=\"/Search/Image?key=M201\" alt=\"M201\" style=\"max-height:24px; max-width: 28px;\" /> M201",
            "display": "M201"
        },
        {
            "id": "M203",
            "text": "M203",
            "html": "<img src=\"/Search/Image?key=M203\" alt=\"M203\" style=\"max-height:24px; max-width: 28px;\" /> M203",
            "display": "M203"
        },
        {
            "id": "M207",
            "text": "M207",
            "html": "<img src=\"/Search/Image?key=M207\" alt=\"M207\" style=\"max-height:24px; max-width: 28px;\" /> M207",
            "display": "M207"
        },
        {
            "id": "M20b",
            "text": "M20B: field of reeds",
            "html": "<img src=\"/Search/Image?key=M20B\" alt=\"M20B\" style=\"max-height:24px; max-width: 28px;\" /> M20B: field of reeds",
            "display": "M20b"
        },
        {
            "id": "M21",
            "text": "M21: reeds with root [sm]",
            "html": "<span class=\"uni\">&#x131D0;</span> M21: reeds with root",
            "display": "M21"
        },
        {
            "id": "M22",
            "text": "M22: rush",
            "html": "<span class=\"uni\">&#x131D1;</span> M22: rush",
            "display": "M22"
        },
        {
            "id": "M222",
            "text": "M222",
            "html": "<img src=\"/Search/Image?key=M222\" alt=\"M222\" style=\"max-height:24px; max-width: 28px;\" /> M222",
            "display": "M222"
        },
        {
            "id": "M23",
            "text": "M23: sedge [sw]",
            "html": "<span class=\"uni\">&#x131D3;</span> M23: sedge",
            "display": "M23"
        },
        {
            "id": "M23a",
            "text": "M23A: sedge",
            "html": "<img src=\"/Search/Image?key=M23A\" alt=\"M23A\" style=\"max-height:24px; max-width: 28px;\" /> M23A: sedge",
            "display": "M23a"
        },
        {
            "id": "M24",
            "text": "M24: combination of M23 and D21 [rsw]",
            "html": "<span class=\"uni\">&#x131D4;</span> M24: combination of M23 and D21",
            "display": "M24"
        },
        {
            "id": "M241a",
            "text": "M241A",
            "html": "<img src=\"/Search/Image?key=M241A\" alt=\"M241A\" style=\"max-height:24px; max-width: 28px;\" /> M241A",
            "display": "M241a"
        },
        {
            "id": "M242",
            "text": "M242",
            "html": "<img src=\"/Search/Image?key=M242\" alt=\"M242\" style=\"max-height:24px; max-width: 28px;\" /> M242",
            "display": "M242"
        },
        {
            "id": "M26",
            "text": "M26: flowering sedge [Sma]",
            "html": "<span class=\"uni\">&#x131D7;</span> M26: flowering sedge",
            "display": "M26"
        },
        {
            "id": "M27",
            "text": "M27: combination of M26 and D36",
            "html": "<span class=\"uni\">&#x131D8;</span> M27: combination of M26 and D36",
            "display": "M27"
        },
        {
            "id": "M28",
            "text": "M28: combination of M26 and V20",
            "html": "<span class=\"uni\">&#x131D9;</span> M28: combination of M26 and V20",
            "display": "M28"
        },
        {
            "id": "M29",
            "text": "M29: pod [tall] [nDm]",
            "html": "<span class=\"uni\">&#x131DB;</span> M29: pod",
            "display": "M29"
        },
        {
            "id": "M3",
            "text": "M3: branch [xt]",
            "html": "<span class=\"uni\">&#x131B1;</span> M3: branch",
            "display": "M3"
        },
        {
            "id": "M30",
            "text": "M30: root [tall] [bnr]",
            "html": "<span class=\"uni\">&#x131DC;</span> M30: root",
            "display": "M30"
        },
        {
            "id": "M31",
            "text": "M31: rhizome [narrow]",
            "html": "<span class=\"uni\">&#x131DD;</span> M31: rhizome",
            "display": "M31"
        },
        {
            "id": "M32",
            "text": "M32: rhizome [tall]",
            "html": "<span class=\"uni\">&#x131DF;</span> M32: rhizome",
            "display": "M32"
        },
        {
            "id": "M33",
            "text": "M33: 3 grains horizontally",
            "html": "<span class=\"uni\">&#x131E0;</span> M33: 3 grains horizontally",
            "display": "M33"
        },
        {
            "id": "M33a",
            "text": "M33A: 3 grains vertically",
            "html": "<span class=\"uni\">&#x131E1;</span> M33A: 3 grains vertically",
            "display": "M33a"
        },
        {
            "id": "M33b",
            "text": "M33B: 3 grains in triangular arrangement",
            "html": "<span class=\"uni\">&#x131E2;</span> M33B: 3 grains in triangular arrangement",
            "display": "M33b"
        },
        {
            "id": "M34",
            "text": "M34: ear of emmer [bdt]",
            "html": "<span class=\"uni\">&#x131E3;</span> M34: ear of emmer",
            "display": "M34"
        },
        {
            "id": "M35",
            "text": "M35: heap of grain [narrow]",
            "html": "<span class=\"uni\">&#x131E4;</span> M35: heap of grain",
            "display": "M35"
        },
        {
            "id": "M36",
            "text": "M36: bundle of flax showing bolls [narrow] [Dr]",
            "html": "<span class=\"uni\">&#x131E5;</span> M36: bundle of flax showing bolls",
            "display": "M36"
        },
        {
            "id": "M36b",
            "text": "M36B: bundle of flax showing bolls",
            "html": "<img src=\"/Search/Image?key=M36B\" alt=\"M36B\" style=\"max-height:24px; max-width: 28px;\" /> M36B: bundle of flax showing bolls",
            "display": "M36b"
        },
        {
            "id": "M37",
            "text": "M37: bundle of flax",
            "html": "<span class=\"uni\">&#x131E6;</span> M37: bundle of flax",
            "display": "M37"
        },
        {
            "id": "M37a",
            "text": "M37A: bundle of flax",
            "html": "<img src=\"/Search/Image?key=M37A\" alt=\"M37A\" style=\"max-height:24px; max-width: 28px;\" /> M37A: bundle of flax",
            "display": "M37a"
        },
        {
            "id": "M38",
            "text": "M38: wide bundle of flax",
            "html": "<span class=\"uni\">&#x131E7;</span> M38: wide bundle of flax",
            "display": "M38"
        },
        {
            "id": "M39",
            "text": "M39: basket of fruit or grain [narrow]",
            "html": "<span class=\"uni\">&#x131E8;</span> M39: basket of fruit or grain",
            "display": "M39"
        },
        {
            "id": "M39a",
            "text": "M39A: basket of fruit or grain",
            "html": "<img src=\"/Search/Image?key=M39A\" alt=\"M39A\" style=\"max-height:24px; max-width: 28px;\" /> M39A: basket of fruit or grain",
            "display": "M39a"
        },
        {
            "id": "M39b",
            "text": "M39B: basket of fruit or grain",
            "html": "<img src=\"/Search/Image?key=M39B\" alt=\"M39B\" style=\"max-height:24px; max-width: 28px;\" /> M39B: basket of fruit or grain",
            "display": "M39b"
        },
        {
            "id": "M3b",
            "text": "M3B: branch",
            "html": "<img src=\"/Search/Image?key=M3B\" alt=\"M3B\" style=\"max-height:24px; max-width: 28px;\" /> M3B: branch",
            "display": "M3b"
        },
        {
            "id": "M3d",
            "text": "M3D: branch",
            "html": "<img src=\"/Search/Image?key=M3D\" alt=\"M3D\" style=\"max-height:24px; max-width: 28px;\" /> M3D: branch",
            "display": "M3d"
        },
        {
            "id": "M4",
            "text": "M4: palm branch [tall] [rnp]",
            "html": "<span class=\"uni\">&#x131B3;</span> M4: palm branch",
            "display": "M4"
        },
        {
            "id": "M40",
            "text": "M40: bundle of reeds [tall] [iz]",
            "html": "<span class=\"uni\">&#x131E9;</span> M40: bundle of reeds",
            "display": "M40"
        },
        {
            "id": "M41",
            "text": "M41: piece of wood [narrow]",
            "html": "<span class=\"uni\">&#x131EB;</span> M41: piece of wood",
            "display": "M41"
        },
        {
            "id": "M42",
            "text": "M42: flower [narrow]",
            "html": "<span class=\"uni\">&#x131EC;</span> M42: flower",
            "display": "M42"
        },
        {
            "id": "M43",
            "text": "M43: vine on trellis",
            "html": "<span class=\"uni\">&#x131ED;</span> M43: vine on trellis",
            "display": "M43"
        },
        {
            "id": "M43a",
            "text": "M43A: vine on trellis",
            "html": "<img src=\"/Search/Image?key=M43A\" alt=\"M43A\" style=\"max-height:24px; max-width: 28px;\" /> M43A: vine on trellis",
            "display": "M43a"
        },
        {
            "id": "M43b",
            "text": "M43B: vine on trellis",
            "html": "<img src=\"/Search/Image?key=M43B\" alt=\"M43B\" style=\"max-height:24px; max-width: 28px;\" /> M43B: vine on trellis",
            "display": "M43b"
        },
        {
            "id": "M44",
            "text": "M44: thorn [tall]",
            "html": "<span class=\"uni\">&#x131EE;</span> M44: thorn",
            "display": "M44"
        },
        {
            "id": "M46",
            "text": "M46",
            "html": "<img src=\"/Search/Image?key=M46\" alt=\"M46\" style=\"max-height:24px; max-width: 28px;\" /> M46",
            "display": "M46"
        },
        {
            "id": "M46b",
            "text": "M46B",
            "html": "<img src=\"/Search/Image?key=M46B\" alt=\"M46B\" style=\"max-height:24px; max-width: 28px;\" /> M46B",
            "display": "M46b"
        },
        {
            "id": "M48",
            "text": "M48",
            "html": "<img src=\"/Search/Image?key=M48\" alt=\"M48\" style=\"max-height:24px; max-width: 28px;\" /> M48",
            "display": "M48"
        },
        {
            "id": "M4b",
            "text": "M4B: palm branch",
            "html": "<img src=\"/Search/Image?key=M4B\" alt=\"M4B\" style=\"max-height:24px; max-width: 28px;\" /> M4B: palm branch",
            "display": "M4b"
        },
        {
            "id": "M5",
            "text": "M5: combination of M4 and X1",
            "html": "<span class=\"uni\">&#x131B4;</span> M5: combination of M4 and X1",
            "display": "M5"
        },
        {
            "id": "M54",
            "text": "M54",
            "html": "<img src=\"/Search/Image?key=M54\" alt=\"M54\" style=\"max-height:24px; max-width: 28px;\" /> M54",
            "display": "M54"
        },
        {
            "id": "M54a",
            "text": "M54A",
            "html": "<img src=\"/Search/Image?key=M54A\" alt=\"M54A\" style=\"max-height:24px; max-width: 28px;\" /> M54A",
            "display": "M54a"
        },
        {
            "id": "M57",
            "text": "M57",
            "html": "<img src=\"/Search/Image?key=M57\" alt=\"M57\" style=\"max-height:24px; max-width: 28px;\" /> M57",
            "display": "M57"
        },
        {
            "id": "M5b",
            "text": "M5B: combination of M4 and X1",
            "html": "<img src=\"/Search/Image?key=M5B\" alt=\"M5B\" style=\"max-height:24px; max-width: 28px;\" /> M5B: combination of M4 and X1",
            "display": "M5b"
        },
        {
            "id": "M6",
            "text": "M6: combination of M4 and D21 [tr]",
            "html": "<span class=\"uni\">&#x131B5;</span> M6: combination of M4 and D21",
            "display": "M6"
        },
        {
            "id": "M7",
            "text": "M7: combination of M4 and Q3",
            "html": "<span class=\"uni\">&#x131B6;</span> M7: combination of M4 and Q3",
            "display": "M7"
        },
        {
            "id": "M70",
            "text": "M70",
            "html": "<img src=\"/Search/Image?key=M70\" alt=\"M70\" style=\"max-height:24px; max-width: 28px;\" /> M70",
            "display": "M70"
        },
        {
            "id": "M72",
            "text": "M72",
            "html": "<img src=\"/Search/Image?key=M72\" alt=\"M72\" style=\"max-height:24px; max-width: 28px;\" /> M72",
            "display": "M72"
        },
        {
            "id": "M77a",
            "text": "M77A",
            "html": "<img src=\"/Search/Image?key=M77A\" alt=\"M77A\" style=\"max-height:24px; max-width: 28px;\" /> M77A",
            "display": "M77a"
        },
        {
            "id": "M7a",
            "text": "M7A: combination of M4 and Q3",
            "html": "<img src=\"/Search/Image?key=M7A\" alt=\"M7A\" style=\"max-height:24px; max-width: 28px;\" /> M7A: combination of M4 and Q3",
            "display": "M7a"
        },
        {
            "id": "M8",
            "text": "M8: pool with lotus flowers [SA]",
            "html": "<span class=\"uni\">&#x131B7;</span> M8: pool with lotus flowers",
            "display": "M8"
        },
        {
            "id": "M83",
            "text": "M83",
            "html": "<img src=\"/Search/Image?key=M83\" alt=\"M83\" style=\"max-height:24px; max-width: 28px;\" /> M83",
            "display": "M83"
        },
        {
            "id": "M8a",
            "text": "M8A: pool with lotus flowers",
            "html": "<img src=\"/Search/Image?key=M8A\" alt=\"M8A\" style=\"max-height:24px; max-width: 28px;\" /> M8A: pool with lotus flowers",
            "display": "M8a"
        },
        {
            "id": "M8e",
            "text": "M8E: pool with lotus flowers",
            "html": "<img src=\"/Search/Image?key=M8E\" alt=\"M8E\" style=\"max-height:24px; max-width: 28px;\" /> M8E: pool with lotus flowers",
            "display": "M8e"
        },
        {
            "id": "M8h",
            "text": "M8H: pool with lotus flowers",
            "html": "<img src=\"/Search/Image?key=M8H\" alt=\"M8H\" style=\"max-height:24px; max-width: 28px;\" /> M8H: pool with lotus flowers",
            "display": "M8h"
        },
        {
            "id": "M9",
            "text": "M9: lotus flower [zSn]",
            "html": "<span class=\"uni\">&#x131B8;</span> M9: lotus flower",
            "display": "M9"
        },
        {
            "id": "M91",
            "text": "M91",
            "html": "<img src=\"/Search/Image?key=M91\" alt=\"M91\" style=\"max-height:24px; max-width: 28px;\" /> M91",
            "display": "M91"
        },
        {
            "id": "M96",
            "text": "M96",
            "html": "<img src=\"/Search/Image?key=M96\" alt=\"M96\" style=\"max-height:24px; max-width: 28px;\" /> M96",
            "display": "M96"
        },
        {
            "id": "M9a",
            "text": "M9A: lotus flower",
            "html": "<img src=\"/Search/Image?key=M9A\" alt=\"M9A\" style=\"max-height:24px; max-width: 28px;\" /> M9A: lotus flower",
            "display": "M9a"
        },
        {
            "id": "M9b",
            "text": "M9B: lotus flower",
            "html": "<img src=\"/Search/Image?key=M9B\" alt=\"M9B\" style=\"max-height:24px; max-width: 28px;\" /> M9B: lotus flower",
            "display": "M9b"
        },
        {
            "id": "N1",
            "text": "N1: sky [broad] [pt]",
            "html": "<span class=\"uni\">&#x131EF;</span> N1: sky",
            "display": "N1"
        },
        {
            "id": "N10",
            "text": "N10: moon with lower section obscured [narrow]",
            "html": "<span class=\"uni\">&#x131F8;</span> N10: moon with lower section obscured",
            "display": "N10"
        },
        {
            "id": "N101",
            "text": "N101",
            "html": "<img src=\"/Search/Image?key=N101\" alt=\"N101\" style=\"max-height:24px; max-width: 28px;\" /> N101",
            "display": "N101"
        },
        {
            "id": "N102",
            "text": "N102",
            "html": "<img src=\"/Search/Image?key=N102\" alt=\"N102\" style=\"max-height:24px; max-width: 28px;\" /> N102",
            "display": "N102"
        },
        {
            "id": "N104",
            "text": "N104",
            "html": "<img src=\"/Search/Image?key=N104\" alt=\"N104\" style=\"max-height:24px; max-width: 28px;\" /> N104",
            "display": "N104"
        },
        {
            "id": "N105",
            "text": "N105",
            "html": "<img src=\"/Search/Image?key=N105\" alt=\"N105\" style=\"max-height:24px; max-width: 28px;\" /> N105",
            "display": "N105"
        },
        {
            "id": "N106",
            "text": "N106",
            "html": "<img src=\"/Search/Image?key=N106\" alt=\"N106\" style=\"max-height:24px; max-width: 28px;\" /> N106",
            "display": "N106"
        },
        {
            "id": "N11",
            "text": "N11: crescent moon [broad] [iaH]",
            "html": "<span class=\"uni\">&#x131F9;</span> N11: crescent moon",
            "display": "N11"
        },
        {
            "id": "N11a",
            "text": "N11A: crescent moon",
            "html": "<img src=\"/Search/Image?key=N11A\" alt=\"N11A\" style=\"max-height:24px; max-width: 28px;\" /> N11A: crescent moon",
            "display": "N11a"
        },
        {
            "id": "N12",
            "text": "N12: crescent moon [broad]",
            "html": "<span class=\"uni\">&#x131FA;</span> N12: crescent moon",
            "display": "N12"
        },
        {
            "id": "N13",
            "text": "N13: combination of N11 and N14",
            "html": "<span class=\"uni\">&#x131FB;</span> N13: combination of N11 and N14",
            "display": "N13"
        },
        {
            "id": "N14",
            "text": "N14: star [dwA]",
            "html": "<span class=\"uni\">&#x131FC;</span> N14: star",
            "display": "N14"
        },
        {
            "id": "N15",
            "text": "N15: star in circle [narrow] [dwAt]",
            "html": "<span class=\"uni\">&#x131FD;</span> N15: star in circle",
            "display": "N15"
        },
        {
            "id": "N16",
            "text": "N16: land with grains [broad] [tA]",
            "html": "<span class=\"uni\">&#x131FE;</span> N16: land with grains",
            "display": "N16"
        },
        {
            "id": "N17",
            "text": "N17: land [broad]",
            "html": "<span class=\"uni\">&#x131FF;</span> N17: land",
            "display": "N17"
        },
        {
            "id": "N18",
            "text": "N18: sandy tract [broad] [iw]",
            "html": "<span class=\"uni\">&#x13200;</span> N18: sandy tract",
            "display": "N18"
        },
        {
            "id": "N19",
            "text": "N19: two sandy tracts",
            "html": "<span class=\"uni\">&#x13203;</span> N19: two sandy tracts",
            "display": "N19"
        },
        {
            "id": "N2",
            "text": "N2: sky with sceptre",
            "html": "<span class=\"uni\">&#x131F0;</span> N2: sky with sceptre",
            "display": "N2"
        },
        {
            "id": "N20",
            "text": "N20: tongue of land [broad] [wDb]",
            "html": "<span class=\"uni\">&#x13204;</span> N20: tongue of land",
            "display": "N20"
        },
        {
            "id": "N21",
            "text": "N21: short tongue of land [narrow]",
            "html": "<span class=\"uni\">&#x13205;</span> N21: short tongue of land",
            "display": "N21"
        },
        {
            "id": "N21a",
            "text": "N21A: short tongue of land",
            "html": "<img src=\"/Search/Image?key=N21A\" alt=\"N21A\" style=\"max-height:24px; max-width: 28px;\" /> N21A: short tongue of land",
            "display": "N21a"
        },
        {
            "id": "N22",
            "text": "N22: broad tongue of land [narrow]",
            "html": "<span class=\"uni\">&#x13206;</span> N22: broad tongue of land",
            "display": "N22"
        },
        {
            "id": "N23",
            "text": "N23: irrigation canal [narrow]",
            "html": "<span class=\"uni\">&#x13207;</span> N23: irrigation canal",
            "display": "N23"
        },
        {
            "id": "N24",
            "text": "N24: irrigation canal system [spAt]",
            "html": "<span class=\"uni\">&#x13208;</span> N24: irrigation canal system",
            "display": "N24"
        },
        {
            "id": "N24e",
            "text": "N24E: irrigation canal system",
            "html": "<img src=\"/Search/Image?key=N24E\" alt=\"N24E\" style=\"max-height:24px; max-width: 28px;\" /> N24E: irrigation canal system",
            "display": "N24e"
        },
        {
            "id": "N25",
            "text": "N25: three hills [xAst]",
            "html": "<span class=\"uni\">&#x13209;</span> N25: three hills",
            "display": "N25"
        },
        {
            "id": "N26",
            "text": "N26: two hills [Dw]",
            "html": "<span class=\"uni\">&#x1320B;</span> N26: two hills",
            "display": "N26"
        },
        {
            "id": "N27",
            "text": "N27: sun over mountain [Axt]",
            "html": "<span class=\"uni\">&#x1320C;</span> N27: sun over mountain",
            "display": "N27"
        },
        {
            "id": "N28",
            "text": "N28: rays of sun over hill [narrow] [xa]",
            "html": "<span class=\"uni\">&#x1320D;</span> N28: rays of sun over hill",
            "display": "N28"
        },
        {
            "id": "N29",
            "text": "N29: slope of hill [narrow] [q]",
            "html": "<span class=\"uni\">&#x1320E;</span> N29: slope of hill",
            "display": "N29"
        },
        {
            "id": "N30",
            "text": "N30: mound of earth [broad] [iAt]",
            "html": "<span class=\"uni\">&#x1320F;</span> N30: mound of earth",
            "display": "N30"
        },
        {
            "id": "N31",
            "text": "N31: road with shrubs [broad]",
            "html": "<span class=\"uni\">&#x13210;</span> N31: road with shrubs",
            "display": "N31"
        },
        {
            "id": "N32",
            "text": "N32: lump of clay [narrow]",
            "html": "<span class=\"uni\">&#x13211;</span> N32: lump of clay",
            "display": "N32"
        },
        {
            "id": "N33",
            "text": "N33: grain [narrow]",
            "html": "<span class=\"uni\">&#x13212;</span> N33: grain",
            "display": "N33"
        },
        {
            "id": "N33a",
            "text": "N33A: three grains",
            "html": "<span class=\"uni\">&#x13213;</span> N33A: three grains",
            "display": "N33a"
        },
        {
            "id": "N33av",
            "text": "N33AV: grain",
            "html": "<img src=\"/Search/Image?key=N33AV\" alt=\"N33AV\" style=\"max-height:24px; max-width: 28px;\" /> N33AV: grain",
            "display": "N33av"
        },
        {
            "id": "N34",
            "text": "N34: ingot of metal [narrow]",
            "html": "<span class=\"uni\">&#x13214;</span> N34: ingot of metal",
            "display": "N34"
        },
        {
            "id": "N35",
            "text": "N35: ripple of water [broad] [n]",
            "html": "<span class=\"uni\">&#x13216;</span> N35: ripple of water",
            "display": "N35"
        },
        {
            "id": "N35a",
            "text": "N35A: three ripples of water",
            "html": "<span class=\"uni\">&#x13217;</span> N35A: three ripples of water",
            "display": "N35a"
        },
        {
            "id": "N35c",
            "text": "N35C: ripple of water",
            "html": "<img src=\"/Search/Image?key=N35C\" alt=\"N35C\" style=\"max-height:24px; max-width: 28px;\" /> N35C: ripple of water",
            "display": "N35c"
        },
        {
            "id": "N36",
            "text": "N36: canal [broad]",
            "html": "<span class=\"uni\">&#x13218;</span> N36: canal",
            "display": "N36"
        },
        {
            "id": "N37",
            "text": "N37: pool [broad] [S]",
            "html": "<span class=\"uni\">&#x13219;</span> N37: pool",
            "display": "N37"
        },
        {
            "id": "N37a",
            "text": "N37A: pool",
            "html": "<span class=\"uni\">&#x1321A;</span> N37A: pool",
            "display": "N37a"
        },
        {
            "id": "N38",
            "text": "N38: deep pool [broad]",
            "html": "<span class=\"uni\">&#x1321B;</span> N38: deep pool",
            "display": "N38"
        },
        {
            "id": "N3b",
            "text": "N3B: sky with sceptre",
            "html": "<img src=\"/Search/Image?key=N3B\" alt=\"N3B\" style=\"max-height:24px; max-width: 28px;\" /> N3B: sky with sceptre",
            "display": "N3b"
        },
        {
            "id": "N4",
            "text": "N4: sky with rain [idt]",
            "html": "<span class=\"uni\">&#x131F2;</span> N4: sky with rain",
            "display": "N4"
        },
        {
            "id": "N40",
            "text": "N40: combination of N37 and D54 [Sm]",
            "html": "<span class=\"uni\">&#x1321D;</span> N40: combination of N37 and D54",
            "display": "N40"
        },
        {
            "id": "N41",
            "text": "N41: well with ripple of water [narrow] [id]",
            "html": "<span class=\"uni\">&#x1321E;</span> N41: well with ripple of water",
            "display": "N41"
        },
        {
            "id": "N42",
            "text": "N42: well with line of water [narrow]",
            "html": "<span class=\"uni\">&#x1321F;</span> N42: well with line of water",
            "display": "N42"
        },
        {
            "id": "N44",
            "text": "N44",
            "html": "<img src=\"/Search/Image?key=N44\" alt=\"N44\" style=\"max-height:24px; max-width: 28px;\" /> N44",
            "display": "N44"
        },
        {
            "id": "N45",
            "text": "N45",
            "html": "<img src=\"/Search/Image?key=N45\" alt=\"N45\" style=\"max-height:24px; max-width: 28px;\" /> N45",
            "display": "N45"
        },
        {
            "id": "N46",
            "text": "N46",
            "html": "<img src=\"/Search/Image?key=N46\" alt=\"N46\" style=\"max-height:24px; max-width: 28px;\" /> N46",
            "display": "N46"
        },
        {
            "id": "N46a",
            "text": "N46A",
            "html": "<img src=\"/Search/Image?key=N46A\" alt=\"N46A\" style=\"max-height:24px; max-width: 28px;\" /> N46A",
            "display": "N46a"
        },
        {
            "id": "N46b",
            "text": "N46B",
            "html": "<img src=\"/Search/Image?key=N46B\" alt=\"N46B\" style=\"max-height:24px; max-width: 28px;\" /> N46B",
            "display": "N46b"
        },
        {
            "id": "N49",
            "text": "N49",
            "html": "<img src=\"/Search/Image?key=N49\" alt=\"N49\" style=\"max-height:24px; max-width: 28px;\" /> N49",
            "display": "N49"
        },
        {
            "id": "N4a",
            "text": "N4A: sky with rain",
            "html": "<img src=\"/Search/Image?key=N4A\" alt=\"N4A\" style=\"max-height:24px; max-width: 28px;\" /> N4A: sky with rain",
            "display": "N4a"
        },
        {
            "id": "N4c",
            "text": "N4C: sky with rain",
            "html": "<img src=\"/Search/Image?key=N4C\" alt=\"N4C\" style=\"max-height:24px; max-width: 28px;\" /> N4C: sky with rain",
            "display": "N4c"
        },
        {
            "id": "N4e",
            "text": "N4E: sky with rain",
            "html": "<img src=\"/Search/Image?key=N4E\" alt=\"N4E\" style=\"max-height:24px; max-width: 28px;\" /> N4E: sky with rain",
            "display": "N4e"
        },
        {
            "id": "N4g",
            "text": "N4G: sky with rain",
            "html": "<img src=\"/Search/Image?key=N4G\" alt=\"N4G\" style=\"max-height:24px; max-width: 28px;\" /> N4G: sky with rain",
            "display": "N4g"
        },
        {
            "id": "N5",
            "text": "N5: sun [narrow] [hrw]",
            "html": "<span class=\"uni\">&#x131F3;</span> N5: sun",
            "display": "N5"
        },
        {
            "id": "N50",
            "text": "N50",
            "html": "<img src=\"/Search/Image?key=N50\" alt=\"N50\" style=\"max-height:24px; max-width: 28px;\" /> N50",
            "display": "N50"
        },
        {
            "id": "N55",
            "text": "N55",
            "html": "<img src=\"/Search/Image?key=N55\" alt=\"N55\" style=\"max-height:24px; max-width: 28px;\" /> N55",
            "display": "N55"
        },
        {
            "id": "N55a",
            "text": "N55A",
            "html": "<img src=\"/Search/Image?key=N55A\" alt=\"N55A\" style=\"max-height:24px; max-width: 28px;\" /> N55A",
            "display": "N55a"
        },
        {
            "id": "N57",
            "text": "N57",
            "html": "<img src=\"/Search/Image?key=N57\" alt=\"N57\" style=\"max-height:24px; max-width: 28px;\" /> N57",
            "display": "N57"
        },
        {
            "id": "N58",
            "text": "N58",
            "html": "<img src=\"/Search/Image?key=N58\" alt=\"N58\" style=\"max-height:24px; max-width: 28px;\" /> N58",
            "display": "N58"
        },
        {
            "id": "N58c",
            "text": "N58C",
            "html": "<img src=\"/Search/Image?key=N58C\" alt=\"N58C\" style=\"max-height:24px; max-width: 28px;\" /> N58C",
            "display": "N58c"
        },
        {
            "id": "N6",
            "text": "N6: sun with uraeus [narrow]",
            "html": "<span class=\"uni\">&#x131F4;</span> N6: sun with uraeus",
            "display": "N6"
        },
        {
            "id": "N62",
            "text": "N62",
            "html": "<img src=\"/Search/Image?key=N62\" alt=\"N62\" style=\"max-height:24px; max-width: 28px;\" /> N62",
            "display": "N62"
        },
        {
            "id": "N62a",
            "text": "N62A",
            "html": "<img src=\"/Search/Image?key=N62A\" alt=\"N62A\" style=\"max-height:24px; max-width: 28px;\" /> N62A",
            "display": "N62a"
        },
        {
            "id": "N63",
            "text": "N63",
            "html": "<img src=\"/Search/Image?key=N63\" alt=\"N63\" style=\"max-height:24px; max-width: 28px;\" /> N63",
            "display": "N63"
        },
        {
            "id": "N63a",
            "text": "N63A",
            "html": "<img src=\"/Search/Image?key=N63A\" alt=\"N63A\" style=\"max-height:24px; max-width: 28px;\" /> N63A",
            "display": "N63a"
        },
        {
            "id": "N65",
            "text": "N65",
            "html": "<img src=\"/Search/Image?key=N65\" alt=\"N65\" style=\"max-height:24px; max-width: 28px;\" /> N65",
            "display": "N65"
        },
        {
            "id": "N6b",
            "text": "N6B: sun with uraeus",
            "html": "<img src=\"/Search/Image?key=N6B\" alt=\"N6B\" style=\"max-height:24px; max-width: 28px;\" /> N6B: sun with uraeus",
            "display": "N6b"
        },
        {
            "id": "N7",
            "text": "N7: combination of N5 and T28",
            "html": "<span class=\"uni\">&#x131F5;</span> N7: combination of N5 and T28",
            "display": "N7"
        },
        {
            "id": "N76a",
            "text": "N76A",
            "html": "<img src=\"/Search/Image?key=N76A\" alt=\"N76A\" style=\"max-height:24px; max-width: 28px;\" /> N76A",
            "display": "N76a"
        },
        {
            "id": "N77",
            "text": "N77",
            "html": "<img src=\"/Search/Image?key=N77\" alt=\"N77\" style=\"max-height:24px; max-width: 28px;\" /> N77",
            "display": "N77"
        },
        {
            "id": "N8",
            "text": "N8: sunshine [narrow] [Hnmmt]",
            "html": "<span class=\"uni\">&#x131F6;</span> N8: sunshine",
            "display": "N8"
        },
        {
            "id": "N82",
            "text": "N82",
            "html": "<img src=\"/Search/Image?key=N82\" alt=\"N82\" style=\"max-height:24px; max-width: 28px;\" /> N82",
            "display": "N82"
        },
        {
            "id": "N89",
            "text": "N89",
            "html": "<img src=\"/Search/Image?key=N89\" alt=\"N89\" style=\"max-height:24px; max-width: 28px;\" /> N89",
            "display": "N89"
        },
        {
            "id": "N8a",
            "text": "N8A: sunshine",
            "html": "<img src=\"/Search/Image?key=N8A\" alt=\"N8A\" style=\"max-height:24px; max-width: 28px;\" /> N8A: sunshine",
            "display": "N8a"
        },
        {
            "id": "N8c",
            "text": "N8C: sunshine",
            "html": "<img src=\"/Search/Image?key=N8C\" alt=\"N8C\" style=\"max-height:24px; max-width: 28px;\" /> N8C: sunshine",
            "display": "N8c"
        },
        {
            "id": "N9",
            "text": "N9: moon with lower half obscured [narrow] [pzD]",
            "html": "<span class=\"uni\">&#x131F7;</span> N9: moon with lower half obscured",
            "display": "N9"
        },
        {
            "id": "N90",
            "text": "N90",
            "html": "<img src=\"/Search/Image?key=N90\" alt=\"N90\" style=\"max-height:24px; max-width: 28px;\" /> N90",
            "display": "N90"
        },
        {
            "id": "N99",
            "text": "N99",
            "html": "<img src=\"/Search/Image?key=N99\" alt=\"N99\" style=\"max-height:24px; max-width: 28px;\" /> N99",
            "display": "N99"
        },
        {
            "id": "O1",
            "text": "O1: house [pr]",
            "html": "<span class=\"uni\">&#x13250;</span> O1: house",
            "display": "O1"
        },
        {
            "id": "O10",
            "text": "O10: combination of O6 and G5",
            "html": "<span class=\"uni\">&#x13261;</span> O10: combination of O6 and G5",
            "display": "O10"
        },
        {
            "id": "O103",
            "text": "O103",
            "html": "<img src=\"/Search/Image?key=O103\" alt=\"O103\" style=\"max-height:24px; max-width: 28px;\" /> O103",
            "display": "O103"
        },
        {
            "id": "O104",
            "text": "O104",
            "html": "<img src=\"/Search/Image?key=O104\" alt=\"O104\" style=\"max-height:24px; max-width: 28px;\" /> O104",
            "display": "O104"
        },
        {
            "id": "O106",
            "text": "O106",
            "html": "<img src=\"/Search/Image?key=O106\" alt=\"O106\" style=\"max-height:24px; max-width: 28px;\" /> O106",
            "display": "O106"
        },
        {
            "id": "O106b",
            "text": "O106B",
            "html": "<img src=\"/Search/Image?key=O106B\" alt=\"O106B\" style=\"max-height:24px; max-width: 28px;\" /> O106B",
            "display": "O106b"
        },
        {
            "id": "O11",
            "text": "O11: palace [tall] [aH]",
            "html": "<span class=\"uni\">&#x13265;</span> O11: palace",
            "display": "O11"
        },
        {
            "id": "O118",
            "text": "O118",
            "html": "<img src=\"/Search/Image?key=O118\" alt=\"O118\" style=\"max-height:24px; max-width: 28px;\" /> O118",
            "display": "O118"
        },
        {
            "id": "O12",
            "text": "O12: combination of O11 and D36",
            "html": "<span class=\"uni\">&#x13266;</span> O12: combination of O11 and D36",
            "display": "O12"
        },
        {
            "id": "O120",
            "text": "O120",
            "html": "<img src=\"/Search/Image?key=O120\" alt=\"O120\" style=\"max-height:24px; max-width: 28px;\" /> O120",
            "display": "O120"
        },
        {
            "id": "O124a",
            "text": "O124A",
            "html": "<img src=\"/Search/Image?key=O124A\" alt=\"O124A\" style=\"max-height:24px; max-width: 28px;\" /> O124A",
            "display": "O124a"
        },
        {
            "id": "O13",
            "text": "O13: battlemented enclosure",
            "html": "<span class=\"uni\">&#x13267;</span> O13: battlemented enclosure",
            "display": "O13"
        },
        {
            "id": "O131",
            "text": "O131",
            "html": "<img src=\"/Search/Image?key=O131\" alt=\"O131\" style=\"max-height:24px; max-width: 28px;\" /> O131",
            "display": "O131"
        },
        {
            "id": "O131a",
            "text": "O131A",
            "html": "<img src=\"/Search/Image?key=O131A\" alt=\"O131A\" style=\"max-height:24px; max-width: 28px;\" /> O131A",
            "display": "O131a"
        },
        {
            "id": "O137",
            "text": "O137",
            "html": "<img src=\"/Search/Image?key=O137\" alt=\"O137\" style=\"max-height:24px; max-width: 28px;\" /> O137",
            "display": "O137"
        },
        {
            "id": "O13c",
            "text": "O13C: battlemented enclosure",
            "html": "<img src=\"/Search/Image?key=O13C\" alt=\"O13C\" style=\"max-height:24px; max-width: 28px;\" /> O13C: battlemented enclosure",
            "display": "O13c"
        },
        {
            "id": "O13d",
            "text": "O13D: battlemented enclosure",
            "html": "<img src=\"/Search/Image?key=O13D\" alt=\"O13D\" style=\"max-height:24px; max-width: 28px;\" /> O13D: battlemented enclosure",
            "display": "O13d"
        },
        {
            "id": "O14",
            "text": "O14: part of battlemented enclosure",
            "html": "<span class=\"uni\">&#x13268;</span> O14: part of battlemented enclosure",
            "display": "O14"
        },
        {
            "id": "O14a",
            "text": "O14A: part of battlemented enclosure",
            "html": "<img src=\"/Search/Image?key=O14A\" alt=\"O14A\" style=\"max-height:24px; max-width: 28px;\" /> O14A: part of battlemented enclosure",
            "display": "O14a"
        },
        {
            "id": "O14c",
            "text": "O14C: part of battlemented enclosure",
            "html": "<img src=\"/Search/Image?key=O14C\" alt=\"O14C\" style=\"max-height:24px; max-width: 28px;\" /> O14C: part of battlemented enclosure",
            "display": "O14c"
        },
        {
            "id": "O15",
            "text": "O15: enclosure with W10 and X1 [wsxt]",
            "html": "<span class=\"uni\">&#x13269;</span> O15: enclosure with W10 and X1",
            "display": "O15"
        },
        {
            "id": "O157",
            "text": "O157",
            "html": "<img src=\"/Search/Image?key=O157\" alt=\"O157\" style=\"max-height:24px; max-width: 28px;\" /> O157",
            "display": "O157"
        },
        {
            "id": "O16",
            "text": "O16: gateway with serpents",
            "html": "<span class=\"uni\">&#x1326A;</span> O16: gateway with serpents",
            "display": "O16"
        },
        {
            "id": "O169",
            "text": "O169",
            "html": "<img src=\"/Search/Image?key=O169\" alt=\"O169\" style=\"max-height:24px; max-width: 28px;\" /> O169",
            "display": "O169"
        },
        {
            "id": "O169a",
            "text": "O169A",
            "html": "<img src=\"/Search/Image?key=O169A\" alt=\"O169A\" style=\"max-height:24px; max-width: 28px;\" /> O169A",
            "display": "O169a"
        },
        {
            "id": "O16b",
            "text": "O16B: gateway with serpents",
            "html": "<img src=\"/Search/Image?key=O16B\" alt=\"O16B\" style=\"max-height:24px; max-width: 28px;\" /> O16B: gateway with serpents",
            "display": "O16b"
        },
        {
            "id": "O17",
            "text": "O17: open gateway with serpents",
            "html": "<span class=\"uni\">&#x1326B;</span> O17: open gateway with serpents",
            "display": "O17"
        },
        {
            "id": "O172",
            "text": "O172",
            "html": "<img src=\"/Search/Image?key=O172\" alt=\"O172\" style=\"max-height:24px; max-width: 28px;\" /> O172",
            "display": "O172"
        },
        {
            "id": "O174",
            "text": "O174",
            "html": "<img src=\"/Search/Image?key=O174\" alt=\"O174\" style=\"max-height:24px; max-width: 28px;\" /> O174",
            "display": "O174"
        },
        {
            "id": "O175",
            "text": "O175",
            "html": "<img src=\"/Search/Image?key=O175\" alt=\"O175\" style=\"max-height:24px; max-width: 28px;\" /> O175",
            "display": "O175"
        },
        {
            "id": "O18",
            "text": "O18: shrine in profile [kAr]",
            "html": "<span class=\"uni\">&#x1326C;</span> O18: shrine in profile",
            "display": "O18"
        },
        {
            "id": "O180",
            "text": "O180",
            "html": "<img src=\"/Search/Image?key=O180\" alt=\"O180\" style=\"max-height:24px; max-width: 28px;\" /> O180",
            "display": "O180"
        },
        {
            "id": "O189",
            "text": "O189",
            "html": "<img src=\"/Search/Image?key=O189\" alt=\"O189\" style=\"max-height:24px; max-width: 28px;\" /> O189",
            "display": "O189"
        },
        {
            "id": "O18a",
            "text": "O18A: shrine in profile",
            "html": "<img src=\"/Search/Image?key=O18A\" alt=\"O18A\" style=\"max-height:24px; max-width: 28px;\" /> O18A: shrine in profile",
            "display": "O18a"
        },
        {
            "id": "O19",
            "text": "O19: shrine with fence",
            "html": "<span class=\"uni\">&#x1326D;</span> O19: shrine with fence",
            "display": "O19"
        },
        {
            "id": "O190",
            "text": "O190",
            "html": "<img src=\"/Search/Image?key=O190\" alt=\"O190\" style=\"max-height:24px; max-width: 28px;\" /> O190",
            "display": "O190"
        },
        {
            "id": "O194",
            "text": "O194",
            "html": "<img src=\"/Search/Image?key=O194\" alt=\"O194\" style=\"max-height:24px; max-width: 28px;\" /> O194",
            "display": "O194"
        },
        {
            "id": "O194a",
            "text": "O194A",
            "html": "<img src=\"/Search/Image?key=O194A\" alt=\"O194A\" style=\"max-height:24px; max-width: 28px;\" /> O194A",
            "display": "O194a"
        },
        {
            "id": "O195a",
            "text": "O195A",
            "html": "<img src=\"/Search/Image?key=O195A\" alt=\"O195A\" style=\"max-height:24px; max-width: 28px;\" /> O195A",
            "display": "O195a"
        },
        {
            "id": "O196",
            "text": "O196",
            "html": "<img src=\"/Search/Image?key=O196\" alt=\"O196\" style=\"max-height:24px; max-width: 28px;\" /> O196",
            "display": "O196"
        },
        {
            "id": "O2",
            "text": "O2: combination of O1 and T3",
            "html": "<span class=\"uni\">&#x13252;</span> O2: combination of O1 and T3",
            "display": "O2"
        },
        {
            "id": "O20",
            "text": "O20: shrine",
            "html": "<span class=\"uni\">&#x1326F;</span> O20: shrine",
            "display": "O20"
        },
        {
            "id": "O204",
            "text": "O204",
            "html": "<img src=\"/Search/Image?key=O204\" alt=\"O204\" style=\"max-height:24px; max-width: 28px;\" /> O204",
            "display": "O204"
        },
        {
            "id": "O206",
            "text": "O206",
            "html": "<img src=\"/Search/Image?key=O206\" alt=\"O206\" style=\"max-height:24px; max-width: 28px;\" /> O206",
            "display": "O206"
        },
        {
            "id": "O207",
            "text": "O207",
            "html": "<img src=\"/Search/Image?key=O207\" alt=\"O207\" style=\"max-height:24px; max-width: 28px;\" /> O207",
            "display": "O207"
        },
        {
            "id": "O21",
            "text": "O21: fa&ccedil;ade of shrine",
            "html": "<span class=\"uni\">&#x13271;</span> O21: fa&ccedil;ade of shrine",
            "display": "O21"
        },
        {
            "id": "O210",
            "text": "O210",
            "html": "<img src=\"/Search/Image?key=O210\" alt=\"O210\" style=\"max-height:24px; max-width: 28px;\" /> O210",
            "display": "O210"
        },
        {
            "id": "O210a",
            "text": "O210A",
            "html": "<img src=\"/Search/Image?key=O210A\" alt=\"O210A\" style=\"max-height:24px; max-width: 28px;\" /> O210A",
            "display": "O210a"
        },
        {
            "id": "O211",
            "text": "O211",
            "html": "<img src=\"/Search/Image?key=O211\" alt=\"O211\" style=\"max-height:24px; max-width: 28px;\" /> O211",
            "display": "O211"
        },
        {
            "id": "O212",
            "text": "O212",
            "html": "<img src=\"/Search/Image?key=O212\" alt=\"O212\" style=\"max-height:24px; max-width: 28px;\" /> O212",
            "display": "O212"
        },
        {
            "id": "O214",
            "text": "O214",
            "html": "<img src=\"/Search/Image?key=O214\" alt=\"O214\" style=\"max-height:24px; max-width: 28px;\" /> O214",
            "display": "O214"
        },
        {
            "id": "O21b",
            "text": "O21B: fa&ccedil;ade of shrine",
            "html": "<img src=\"/Search/Image?key=O21B\" alt=\"O21B\" style=\"max-height:24px; max-width: 28px;\" /> O21B: fa&ccedil;ade of shrine",
            "display": "O21b"
        },
        {
            "id": "O22",
            "text": "O22: booth with pole [zH]",
            "html": "<span class=\"uni\">&#x13272;</span> O22: booth with pole",
            "display": "O22"
        },
        {
            "id": "O22c",
            "text": "O22C: booth with pole",
            "html": "<img src=\"/Search/Image?key=O22C\" alt=\"O22C\" style=\"max-height:24px; max-width: 28px;\" /> O22C: booth with pole",
            "display": "O22c"
        },
        {
            "id": "O23",
            "text": "O23: double platform",
            "html": "<span class=\"uni\">&#x13273;</span> O23: double platform",
            "display": "O23"
        },
        {
            "id": "O230",
            "text": "O230",
            "html": "<img src=\"/Search/Image?key=O230\" alt=\"O230\" style=\"max-height:24px; max-width: 28px;\" /> O230",
            "display": "O230"
        },
        {
            "id": "O231",
            "text": "O231",
            "html": "<img src=\"/Search/Image?key=O231\" alt=\"O231\" style=\"max-height:24px; max-width: 28px;\" /> O231",
            "display": "O231"
        },
        {
            "id": "O233",
            "text": "O233",
            "html": "<img src=\"/Search/Image?key=O233\" alt=\"O233\" style=\"max-height:24px; max-width: 28px;\" /> O233",
            "display": "O233"
        },
        {
            "id": "O238",
            "text": "O238",
            "html": "<img src=\"/Search/Image?key=O238\" alt=\"O238\" style=\"max-height:24px; max-width: 28px;\" /> O238",
            "display": "O238"
        },
        {
            "id": "O23f",
            "text": "O23F: double platform",
            "html": "<img src=\"/Search/Image?key=O23F\" alt=\"O23F\" style=\"max-height:24px; max-width: 28px;\" /> O23F: double platform",
            "display": "O23f"
        },
        {
            "id": "O24",
            "text": "O24: pyramid",
            "html": "<span class=\"uni\">&#x13274;</span> O24: pyramid",
            "display": "O24"
        },
        {
            "id": "O243",
            "text": "O243",
            "html": "<img src=\"/Search/Image?key=O243\" alt=\"O243\" style=\"max-height:24px; max-width: 28px;\" /> O243",
            "display": "O243"
        },
        {
            "id": "O24a",
            "text": "O24A: pedestal of sun temple",
            "html": "<span class=\"uni\">&#x13275;</span> O24A: pedestal of sun temple",
            "display": "O24a"
        },
        {
            "id": "O25",
            "text": "O25: obelisk [txn]",
            "html": "<span class=\"uni\">&#x13276;</span> O25: obelisk",
            "display": "O25"
        },
        {
            "id": "O26",
            "text": "O26: stela",
            "html": "<span class=\"uni\">&#x13278;</span> O26: stela",
            "display": "O26"
        },
        {
            "id": "O260b",
            "text": "O260B",
            "html": "<img src=\"/Search/Image?key=O260B\" alt=\"O260B\" style=\"max-height:24px; max-width: 28px;\" /> O260B",
            "display": "O260b"
        },
        {
            "id": "O26a",
            "text": "O26A: stela",
            "html": "<img src=\"/Search/Image?key=O26A\" alt=\"O26A\" style=\"max-height:24px; max-width: 28px;\" /> O26A: stela",
            "display": "O26a"
        },
        {
            "id": "O27",
            "text": "O27: hall of columns",
            "html": "<span class=\"uni\">&#x13279;</span> O27: hall of columns",
            "display": "O27"
        },
        {
            "id": "O28",
            "text": "O28: column [tall] [iwn]",
            "html": "<span class=\"uni\">&#x1327A;</span> O28: column",
            "display": "O28"
        },
        {
            "id": "O286",
            "text": "O286",
            "html": "<img src=\"/Search/Image?key=O286\" alt=\"O286\" style=\"max-height:24px; max-width: 28px;\" /> O286",
            "display": "O286"
        },
        {
            "id": "O289",
            "text": "O289",
            "html": "<img src=\"/Search/Image?key=O289\" alt=\"O289\" style=\"max-height:24px; max-width: 28px;\" /> O289",
            "display": "O289"
        },
        {
            "id": "O29",
            "text": "O29: horizontal wooden column [broad] [aA]",
            "html": "<span class=\"uni\">&#x1327B;</span> O29: horizontal wooden column",
            "display": "O29"
        },
        {
            "id": "O292",
            "text": "O292",
            "html": "<img src=\"/Search/Image?key=O292\" alt=\"O292\" style=\"max-height:24px; max-width: 28px;\" /> O292",
            "display": "O292"
        },
        {
            "id": "O29v",
            "text": "O29V: horizontal wooden column",
            "html": "<img src=\"/Search/Image?key=O29V\" alt=\"O29V\" style=\"max-height:24px; max-width: 28px;\" /> O29V: horizontal wooden column",
            "display": "O29v"
        },
        {
            "id": "O3",
            "text": "O3: combination of O1, P8, X3, and W22",
            "html": "<span class=\"uni\">&#x13253;</span> O3: combination of O1, P8, X3, and W22",
            "display": "O3"
        },
        {
            "id": "O30",
            "text": "O30: support [tall] [zxnt]",
            "html": "<span class=\"uni\">&#x1327D;</span> O30: support",
            "display": "O30"
        },
        {
            "id": "O307",
            "text": "O307",
            "html": "<img src=\"/Search/Image?key=O307\" alt=\"O307\" style=\"max-height:24px; max-width: 28px;\" /> O307",
            "display": "O307"
        },
        {
            "id": "O30u",
            "text": "O30U: support",
            "html": "<img src=\"/Search/Image?key=O30U\" alt=\"O30U\" style=\"max-height:24px; max-width: 28px;\" /> O30U: support",
            "display": "O30u"
        },
        {
            "id": "O31",
            "text": "O31: door [broad]",
            "html": "<span class=\"uni\">&#x1327F;</span> O31: door",
            "display": "O31"
        },
        {
            "id": "O32",
            "text": "O32: gateway",
            "html": "<span class=\"uni\">&#x13280;</span> O32: gateway",
            "display": "O32"
        },
        {
            "id": "O32a",
            "text": "O32A: gateway",
            "html": "<img src=\"/Search/Image?key=O32A\" alt=\"O32A\" style=\"max-height:24px; max-width: 28px;\" /> O32A: gateway",
            "display": "O32a"
        },
        {
            "id": "O32d",
            "text": "O32D: gateway",
            "html": "<img src=\"/Search/Image?key=O32D\" alt=\"O32D\" style=\"max-height:24px; max-width: 28px;\" /> O32D: gateway",
            "display": "O32d"
        },
        {
            "id": "O33",
            "text": "O33: fa&ccedil;ade of palace",
            "html": "<span class=\"uni\">&#x13281;</span> O33: fa&ccedil;ade of palace",
            "display": "O33"
        },
        {
            "id": "O333",
            "text": "O333",
            "html": "<img src=\"/Search/Image?key=O333\" alt=\"O333\" style=\"max-height:24px; max-width: 28px;\" /> O333",
            "display": "O333"
        },
        {
            "id": "O338",
            "text": "O338",
            "html": "<img src=\"/Search/Image?key=O338\" alt=\"O338\" style=\"max-height:24px; max-width: 28px;\" /> O338",
            "display": "O338"
        },
        {
            "id": "O34",
            "text": "O34: bolt [broad] [z] [s]",
            "html": "<span class=\"uni\">&#x13283;</span> O34: bolt",
            "display": "O34"
        },
        {
            "id": "O340",
            "text": "O340",
            "html": "<img src=\"/Search/Image?key=O340\" alt=\"O340\" style=\"max-height:24px; max-width: 28px;\" /> O340",
            "display": "O340"
        },
        {
            "id": "O35",
            "text": "O35: combination of O34 and D54 [zb]",
            "html": "<span class=\"uni\">&#x13284;</span> O35: combination of O34 and D54",
            "display": "O35"
        },
        {
            "id": "O353",
            "text": "O353",
            "html": "<img src=\"/Search/Image?key=O353\" alt=\"O353\" style=\"max-height:24px; max-width: 28px;\" /> O353",
            "display": "O353"
        },
        {
            "id": "O36",
            "text": "O36: wall [tall] [inb]",
            "html": "<span class=\"uni\">&#x13285;</span> O36: wall",
            "display": "O36"
        },
        {
            "id": "O36a",
            "text": "O36A: opening of oval fortified wall enclosure",
            "html": "<span class=\"uni\">&#x13286;</span> O36A: opening of oval fortified wall enclosure",
            "display": "O36a"
        },
        {
            "id": "O36b",
            "text": "O36B: closing of oval fortified wall enclosure",
            "html": "<span class=\"uni\">&#x13287;</span> O36B: closing of oval fortified wall enclosure",
            "display": "O36b"
        },
        {
            "id": "O36c",
            "text": "O36C: opening of square fortified wall enclosure",
            "html": "<span class=\"uni\">&#x13288;</span> O36C: opening of square fortified wall enclosure",
            "display": "O36c"
        },
        {
            "id": "O36h",
            "text": "O36H: wall",
            "html": "<img src=\"/Search/Image?key=O36H\" alt=\"O36H\" style=\"max-height:24px; max-width: 28px;\" /> O36H: wall",
            "display": "O36h"
        },
        {
            "id": "O37",
            "text": "O37: falling wall",
            "html": "<span class=\"uni\">&#x1328A;</span> O37: falling wall",
            "display": "O37"
        },
        {
            "id": "O37a",
            "text": "O37A: falling wall",
            "html": "<img src=\"/Search/Image?key=O37A\" alt=\"O37A\" style=\"max-height:24px; max-width: 28px;\" /> O37A: falling wall",
            "display": "O37a"
        },
        {
            "id": "O38",
            "text": "O38: corner of wall",
            "html": "<span class=\"uni\">&#x1328B;</span> O38: corner of wall",
            "display": "O38"
        },
        {
            "id": "O38a",
            "text": "O38A: corner of wall",
            "html": "<img src=\"/Search/Image?key=O38A\" alt=\"O38A\" style=\"max-height:24px; max-width: 28px;\" /> O38A: corner of wall",
            "display": "O38a"
        },
        {
            "id": "O39",
            "text": "O39: stone [narrow]",
            "html": "<span class=\"uni\">&#x1328C;</span> O39: stone",
            "display": "O39"
        },
        {
            "id": "O4",
            "text": "O4: shelter [h]",
            "html": "<span class=\"uni\">&#x13254;</span> O4: shelter",
            "display": "O4"
        },
        {
            "id": "O40",
            "text": "O40: stairway",
            "html": "<span class=\"uni\">&#x1328D;</span> O40: stairway",
            "display": "O40"
        },
        {
            "id": "O40a",
            "text": "O40A: stairway",
            "html": "<img src=\"/Search/Image?key=O40A\" alt=\"O40A\" style=\"max-height:24px; max-width: 28px;\" /> O40A: stairway",
            "display": "O40a"
        },
        {
            "id": "O41",
            "text": "O41: double stairway",
            "html": "<span class=\"uni\">&#x1328E;</span> O41: double stairway",
            "display": "O41"
        },
        {
            "id": "O42",
            "text": "O42: fence [broad] [Szp]",
            "html": "<span class=\"uni\">&#x1328F;</span> O42: fence",
            "display": "O42"
        },
        {
            "id": "O43",
            "text": "O43: low fence [broad]",
            "html": "<span class=\"uni\">&#x13290;</span> O43: low fence",
            "display": "O43"
        },
        {
            "id": "O44",
            "text": "O44: emblem of Min [tall]",
            "html": "<span class=\"uni\">&#x13291;</span> O44: emblem of Min",
            "display": "O44"
        },
        {
            "id": "O45",
            "text": "O45: domed building [narrow] [ipt]",
            "html": "<span class=\"uni\">&#x13292;</span> O45: domed building",
            "display": "O45"
        },
        {
            "id": "O46",
            "text": "O46: domed building [narrow]",
            "html": "<span class=\"uni\">&#x13293;</span> O46: domed building",
            "display": "O46"
        },
        {
            "id": "O46b",
            "text": "O46B: domed building",
            "html": "<img src=\"/Search/Image?key=O46B\" alt=\"O46B\" style=\"max-height:24px; max-width: 28px;\" /> O46B: domed building",
            "display": "O46b"
        },
        {
            "id": "O47",
            "text": "O47: enclosed mound [narrow] [nxn]",
            "html": "<span class=\"uni\">&#x13294;</span> O47: enclosed mound",
            "display": "O47"
        },
        {
            "id": "O48",
            "text": "O48: enclosed mound [narrow]",
            "html": "<span class=\"uni\">&#x13295;</span> O48: enclosed mound",
            "display": "O48"
        },
        {
            "id": "O48a",
            "text": "O48A: enclosed mound",
            "html": "<img src=\"/Search/Image?key=O48A\" alt=\"O48A\" style=\"max-height:24px; max-width: 28px;\" /> O48A: enclosed mound",
            "display": "O48a"
        },
        {
            "id": "O49",
            "text": "O49: village [narrow] [niwt]",
            "html": "<span class=\"uni\">&#x13296;</span> O49: village",
            "display": "O49"
        },
        {
            "id": "O4a",
            "text": "O4A: shelter",
            "html": "<img src=\"/Search/Image?key=O4A\" alt=\"O4A\" style=\"max-height:24px; max-width: 28px;\" /> O4A: shelter",
            "display": "O4a"
        },
        {
            "id": "O5",
            "text": "O5: winding wall from upper-left corner",
            "html": "<span class=\"uni\">&#x13255;</span> O5: winding wall from upper-left corner",
            "display": "O5"
        },
        {
            "id": "O50",
            "text": "O50: threshing floor [narrow] [zp]",
            "html": "<span class=\"uni\">&#x13297;</span> O50: threshing floor",
            "display": "O50"
        },
        {
            "id": "O51",
            "text": "O51: pile of grain [Snwt]",
            "html": "<span class=\"uni\">&#x1329A;</span> O51: pile of grain",
            "display": "O51"
        },
        {
            "id": "O51a",
            "text": "O51A: pile of grain",
            "html": "<img src=\"/Search/Image?key=O51A\" alt=\"O51A\" style=\"max-height:24px; max-width: 28px;\" /> O51A: pile of grain",
            "display": "O51a"
        },
        {
            "id": "O51b",
            "text": "O51B: pile of grain",
            "html": "<img src=\"/Search/Image?key=O51B\" alt=\"O51B\" style=\"max-height:24px; max-width: 28px;\" /> O51B: pile of grain",
            "display": "O51b"
        },
        {
            "id": "O53",
            "text": "O53",
            "html": "<img src=\"/Search/Image?key=O53\" alt=\"O53\" style=\"max-height:24px; max-width: 28px;\" /> O53",
            "display": "O53"
        },
        {
            "id": "O54",
            "text": "O54",
            "html": "<img src=\"/Search/Image?key=O54\" alt=\"O54\" style=\"max-height:24px; max-width: 28px;\" /> O54",
            "display": "O54"
        },
        {
            "id": "O59",
            "text": "O59",
            "html": "<img src=\"/Search/Image?key=O59\" alt=\"O59\" style=\"max-height:24px; max-width: 28px;\" /> O59",
            "display": "O59"
        },
        {
            "id": "O5u",
            "text": "O5U: winding wall from upper-left corner",
            "html": "<img src=\"/Search/Image?key=O5U\" alt=\"O5U\" style=\"max-height:24px; max-width: 28px;\" /> O5U: winding wall from upper-left corner",
            "display": "O5u"
        },
        {
            "id": "O6",
            "text": "O6: enclosure [Hwt]",
            "html": "<span class=\"uni\">&#x13257;</span> O6: enclosure",
            "display": "O6"
        },
        {
            "id": "O62",
            "text": "O62",
            "html": "<img src=\"/Search/Image?key=O62\" alt=\"O62\" style=\"max-height:24px; max-width: 28px;\" /> O62",
            "display": "O62"
        },
        {
            "id": "O64",
            "text": "O64",
            "html": "<img src=\"/Search/Image?key=O64\" alt=\"O64\" style=\"max-height:24px; max-width: 28px;\" /> O64",
            "display": "O64"
        },
        {
            "id": "O6e",
            "text": "O6E: closing of <span class=\"egytransl\">Hwt</span>-enclosure",
            "html": "<span class=\"uni\">&#x1325C;</span> O6E: closing of <span class=\"egytransl\">Hwt</span>-enclosure",
            "display": "O6e"
        },
        {
            "id": "O6f",
            "text": "O6F: closing of <span class=\"egytransl\">Hwt</span>-enclosure",
            "html": "<span class=\"uni\">&#x1325D;</span> O6F: closing of <span class=\"egytransl\">Hwt</span>-enclosure",
            "display": "O6f"
        },
        {
            "id": "O6g",
            "text": "O6G: enclosure",
            "html": "<img src=\"/Search/Image?key=O6G\" alt=\"O6G\" style=\"max-height:24px; max-width: 28px;\" /> O6G: enclosure",
            "display": "O6g"
        },
        {
            "id": "O7",
            "text": "O7: combination of O6 and X1",
            "html": "<span class=\"uni\">&#x1325E;</span> O7: combination of O6 and X1",
            "display": "O7"
        },
        {
            "id": "O70",
            "text": "O70",
            "html": "<img src=\"/Search/Image?key=O70\" alt=\"O70\" style=\"max-height:24px; max-width: 28px;\" /> O70",
            "display": "O70"
        },
        {
            "id": "O8",
            "text": "O8: combination of O7 and O29",
            "html": "<span class=\"uni\">&#x1325F;</span> O8: combination of O7 and O29",
            "display": "O8"
        },
        {
            "id": "O84",
            "text": "O84",
            "html": "<img src=\"/Search/Image?key=O84\" alt=\"O84\" style=\"max-height:24px; max-width: 28px;\" /> O84",
            "display": "O84"
        },
        {
            "id": "O85",
            "text": "O85",
            "html": "<img src=\"/Search/Image?key=O85\" alt=\"O85\" style=\"max-height:24px; max-width: 28px;\" /> O85",
            "display": "O85"
        },
        {
            "id": "O85a",
            "text": "O85A",
            "html": "<img src=\"/Search/Image?key=O85A\" alt=\"O85A\" style=\"max-height:24px; max-width: 28px;\" /> O85A",
            "display": "O85a"
        },
        {
            "id": "O88",
            "text": "O88",
            "html": "<img src=\"/Search/Image?key=O88\" alt=\"O88\" style=\"max-height:24px; max-width: 28px;\" /> O88",
            "display": "O88"
        },
        {
            "id": "O9",
            "text": "O9: combination of O7 and V30",
            "html": "<span class=\"uni\">&#x13260;</span> O9: combination of O7 and V30",
            "display": "O9"
        },
        {
            "id": "O90",
            "text": "O90",
            "html": "<img src=\"/Search/Image?key=O90\" alt=\"O90\" style=\"max-height:24px; max-width: 28px;\" /> O90",
            "display": "O90"
        },
        {
            "id": "O90a",
            "text": "O90A",
            "html": "<img src=\"/Search/Image?key=O90A\" alt=\"O90A\" style=\"max-height:24px; max-width: 28px;\" /> O90A",
            "display": "O90a"
        },
        {
            "id": "O91",
            "text": "O91",
            "html": "<img src=\"/Search/Image?key=O91\" alt=\"O91\" style=\"max-height:24px; max-width: 28px;\" /> O91",
            "display": "O91"
        },
        {
            "id": "O9b",
            "text": "O9B: combination of O7 and V30",
            "html": "<img src=\"/Search/Image?key=O9B\" alt=\"O9B\" style=\"max-height:24px; max-width: 28px;\" /> O9B: combination of O7 and V30",
            "display": "O9b"
        },
        {
            "id": "O9c",
            "text": "O9C: combination of O7 and V30",
            "html": "<img src=\"/Search/Image?key=O9C\" alt=\"O9C\" style=\"max-height:24px; max-width: 28px;\" /> O9C: combination of O7 and V30",
            "display": "O9c"
        },
        {
            "id": "P1",
            "text": "P1: boat",
            "html": "<span class=\"uni\">&#x1329B;</span> P1: boat",
            "display": "P1"
        },
        {
            "id": "P10",
            "text": "P10: steering oar",
            "html": "<span class=\"uni\">&#x132A6;</span> P10: steering oar",
            "display": "P10"
        },
        {
            "id": "P105",
            "text": "P105",
            "html": "<img src=\"/Search/Image?key=P105\" alt=\"P105\" style=\"max-height:24px; max-width: 28px;\" /> P105",
            "display": "P105"
        },
        {
            "id": "P106",
            "text": "P106",
            "html": "<img src=\"/Search/Image?key=P106\" alt=\"P106\" style=\"max-height:24px; max-width: 28px;\" /> P106",
            "display": "P106"
        },
        {
            "id": "P11",
            "text": "P11: mooring post [tall]",
            "html": "<span class=\"uni\">&#x132A7;</span> P11: mooring post",
            "display": "P11"
        },
        {
            "id": "P111",
            "text": "P111",
            "html": "<img src=\"/Search/Image?key=P111\" alt=\"P111\" style=\"max-height:24px; max-width: 28px;\" /> P111",
            "display": "P111"
        },
        {
            "id": "P114",
            "text": "P114",
            "html": "<img src=\"/Search/Image?key=P114\" alt=\"P114\" style=\"max-height:24px; max-width: 28px;\" /> P114",
            "display": "P114"
        },
        {
            "id": "P121",
            "text": "P121",
            "html": "<img src=\"/Search/Image?key=P121\" alt=\"P121\" style=\"max-height:24px; max-width: 28px;\" /> P121",
            "display": "P121"
        },
        {
            "id": "P13",
            "text": "P13",
            "html": "<img src=\"/Search/Image?key=P13\" alt=\"P13\" style=\"max-height:24px; max-width: 28px;\" /> P13",
            "display": "P13"
        },
        {
            "id": "P16a",
            "text": "P16A",
            "html": "<img src=\"/Search/Image?key=P16A\" alt=\"P16A\" style=\"max-height:24px; max-width: 28px;\" /> P16A",
            "display": "P16a"
        },
        {
            "id": "P17",
            "text": "P17",
            "html": "<img src=\"/Search/Image?key=P17\" alt=\"P17\" style=\"max-height:24px; max-width: 28px;\" /> P17",
            "display": "P17"
        },
        {
            "id": "P18",
            "text": "P18",
            "html": "<img src=\"/Search/Image?key=P18\" alt=\"P18\" style=\"max-height:24px; max-width: 28px;\" /> P18",
            "display": "P18"
        },
        {
            "id": "P19",
            "text": "P19",
            "html": "<img src=\"/Search/Image?key=P19\" alt=\"P19\" style=\"max-height:24px; max-width: 28px;\" /> P19",
            "display": "P19"
        },
        {
            "id": "P1a",
            "text": "P1A: boat upside down",
            "html": "<span class=\"uni\">&#x1329C;</span> P1A: boat upside down",
            "display": "P1a"
        },
        {
            "id": "P2",
            "text": "P2: ship under sail",
            "html": "<span class=\"uni\">&#x1329D;</span> P2: ship under sail",
            "display": "P2"
        },
        {
            "id": "P21",
            "text": "P21",
            "html": "<img src=\"/Search/Image?key=P21\" alt=\"P21\" style=\"max-height:24px; max-width: 28px;\" /> P21",
            "display": "P21"
        },
        {
            "id": "P23a",
            "text": "P23A",
            "html": "<img src=\"/Search/Image?key=P23A\" alt=\"P23A\" style=\"max-height:24px; max-width: 28px;\" /> P23A",
            "display": "P23a"
        },
        {
            "id": "P24",
            "text": "P24",
            "html": "<img src=\"/Search/Image?key=P24\" alt=\"P24\" style=\"max-height:24px; max-width: 28px;\" /> P24",
            "display": "P24"
        },
        {
            "id": "P2f",
            "text": "P2F: ship under sail",
            "html": "<img src=\"/Search/Image?key=P2F\" alt=\"P2F\" style=\"max-height:24px; max-width: 28px;\" /> P2F: ship under sail",
            "display": "P2f"
        },
        {
            "id": "P2g",
            "text": "P2G: ship under sail",
            "html": "<img src=\"/Search/Image?key=P2G\" alt=\"P2G\" style=\"max-height:24px; max-width: 28px;\" /> P2G: ship under sail",
            "display": "P2g"
        },
        {
            "id": "P2h",
            "text": "P2H: ship under sail",
            "html": "<img src=\"/Search/Image?key=P2H\" alt=\"P2H\" style=\"max-height:24px; max-width: 28px;\" /> P2H: ship under sail",
            "display": "P2h"
        },
        {
            "id": "P3",
            "text": "P3: sacred barque",
            "html": "<span class=\"uni\">&#x1329E;</span> P3: sacred barque",
            "display": "P3"
        },
        {
            "id": "P30",
            "text": "P30",
            "html": "<img src=\"/Search/Image?key=P30\" alt=\"P30\" style=\"max-height:24px; max-width: 28px;\" /> P30",
            "display": "P30"
        },
        {
            "id": "P32",
            "text": "P32",
            "html": "<img src=\"/Search/Image?key=P32\" alt=\"P32\" style=\"max-height:24px; max-width: 28px;\" /> P32",
            "display": "P32"
        },
        {
            "id": "P34",
            "text": "P34",
            "html": "<img src=\"/Search/Image?key=P34\" alt=\"P34\" style=\"max-height:24px; max-width: 28px;\" /> P34",
            "display": "P34"
        },
        {
            "id": "P36",
            "text": "P36",
            "html": "<img src=\"/Search/Image?key=P36\" alt=\"P36\" style=\"max-height:24px; max-width: 28px;\" /> P36",
            "display": "P36"
        },
        {
            "id": "P36b",
            "text": "P36B",
            "html": "<img src=\"/Search/Image?key=P36B\" alt=\"P36B\" style=\"max-height:24px; max-width: 28px;\" /> P36B",
            "display": "P36b"
        },
        {
            "id": "P37",
            "text": "P37",
            "html": "<img src=\"/Search/Image?key=P37\" alt=\"P37\" style=\"max-height:24px; max-width: 28px;\" /> P37",
            "display": "P37"
        },
        {
            "id": "P38",
            "text": "P38",
            "html": "<img src=\"/Search/Image?key=P38\" alt=\"P38\" style=\"max-height:24px; max-width: 28px;\" /> P38",
            "display": "P38"
        },
        {
            "id": "P4",
            "text": "P4: boat with net [wHa]",
            "html": "<span class=\"uni\">&#x132A0;</span> P4: boat with net",
            "display": "P4"
        },
        {
            "id": "P41a",
            "text": "P41A",
            "html": "<img src=\"/Search/Image?key=P41A\" alt=\"P41A\" style=\"max-height:24px; max-width: 28px;\" /> P41A",
            "display": "P41a"
        },
        {
            "id": "P46",
            "text": "P46",
            "html": "<img src=\"/Search/Image?key=P46\" alt=\"P46\" style=\"max-height:24px; max-width: 28px;\" /> P46",
            "display": "P46"
        },
        {
            "id": "P47",
            "text": "P47",
            "html": "<img src=\"/Search/Image?key=P47\" alt=\"P47\" style=\"max-height:24px; max-width: 28px;\" /> P47",
            "display": "P47"
        },
        {
            "id": "P47a",
            "text": "P47A",
            "html": "<img src=\"/Search/Image?key=P47A\" alt=\"P47A\" style=\"max-height:24px; max-width: 28px;\" /> P47A",
            "display": "P47a"
        },
        {
            "id": "P4a",
            "text": "P4A: boat with net",
            "html": "<img src=\"/Search/Image?key=P4A\" alt=\"P4A\" style=\"max-height:24px; max-width: 28px;\" /> P4A: boat with net",
            "display": "P4a"
        },
        {
            "id": "P4b",
            "text": "P4B: boat with net",
            "html": "<img src=\"/Search/Image?key=P4B\" alt=\"P4B\" style=\"max-height:24px; max-width: 28px;\" /> P4B: boat with net",
            "display": "P4b"
        },
        {
            "id": "P5",
            "text": "P5: sail [TAw]",
            "html": "<span class=\"uni\">&#x132A1;</span> P5: sail",
            "display": "P5"
        },
        {
            "id": "P50",
            "text": "P50",
            "html": "<img src=\"/Search/Image?key=P50\" alt=\"P50\" style=\"max-height:24px; max-width: 28px;\" /> P50",
            "display": "P50"
        },
        {
            "id": "P59",
            "text": "P59",
            "html": "<img src=\"/Search/Image?key=P59\" alt=\"P59\" style=\"max-height:24px; max-width: 28px;\" /> P59",
            "display": "P59"
        },
        {
            "id": "P6",
            "text": "P6: mast [tall] [aHa]",
            "html": "<span class=\"uni\">&#x132A2;</span> P6: mast",
            "display": "P6"
        },
        {
            "id": "P60a",
            "text": "P60A",
            "html": "<img src=\"/Search/Image?key=P60A\" alt=\"P60A\" style=\"max-height:24px; max-width: 28px;\" /> P60A",
            "display": "P60a"
        },
        {
            "id": "P60c",
            "text": "P60C",
            "html": "<img src=\"/Search/Image?key=P60C\" alt=\"P60C\" style=\"max-height:24px; max-width: 28px;\" /> P60C",
            "display": "P60c"
        },
        {
            "id": "P6b",
            "text": "P6B: mast",
            "html": "<img src=\"/Search/Image?key=P6B\" alt=\"P6B\" style=\"max-height:24px; max-width: 28px;\" /> P6B: mast",
            "display": "P6b"
        },
        {
            "id": "P7",
            "text": "P7: combination of P6 and D36",
            "html": "<span class=\"uni\">&#x132A3;</span> P7: combination of P6 and D36",
            "display": "P7"
        },
        {
            "id": "P71a",
            "text": "P71A",
            "html": "<img src=\"/Search/Image?key=P71A\" alt=\"P71A\" style=\"max-height:24px; max-width: 28px;\" /> P71A",
            "display": "P71a"
        },
        {
            "id": "P71b",
            "text": "P71B",
            "html": "<img src=\"/Search/Image?key=P71B\" alt=\"P71B\" style=\"max-height:24px; max-width: 28px;\" /> P71B",
            "display": "P71b"
        },
        {
            "id": "P77",
            "text": "P77",
            "html": "<img src=\"/Search/Image?key=P77\" alt=\"P77\" style=\"max-height:24px; max-width: 28px;\" /> P77",
            "display": "P77"
        },
        {
            "id": "P8",
            "text": "P8: oar [tall] [xrw]",
            "html": "<span class=\"uni\">&#x132A4;</span> P8: oar",
            "display": "P8"
        },
        {
            "id": "P8a",
            "text": "P8A: oar",
            "html": "<img src=\"/Search/Image?key=P8A\" alt=\"P8A\" style=\"max-height:24px; max-width: 28px;\" /> P8A: oar",
            "display": "P8a"
        },
        {
            "id": "P8h",
            "text": "P8H: oar",
            "html": "<img src=\"/Search/Image?key=P8H\" alt=\"P8H\" style=\"max-height:24px; max-width: 28px;\" /> P8H: oar",
            "display": "P8h"
        },
        {
            "id": "P9",
            "text": "P9: combination of P8 and I9",
            "html": "<span class=\"uni\">&#x132A5;</span> P9: combination of P8 and I9",
            "display": "P9"
        },
        {
            "id": "P90",
            "text": "P90",
            "html": "<img src=\"/Search/Image?key=P90\" alt=\"P90\" style=\"max-height:24px; max-width: 28px;\" /> P90",
            "display": "P90"
        },
        {
            "id": "P92",
            "text": "P92",
            "html": "<img src=\"/Search/Image?key=P92\" alt=\"P92\" style=\"max-height:24px; max-width: 28px;\" /> P92",
            "display": "P92"
        },
        {
            "id": "P93",
            "text": "P93",
            "html": "<img src=\"/Search/Image?key=P93\" alt=\"P93\" style=\"max-height:24px; max-width: 28px;\" /> P93",
            "display": "P93"
        },
        {
            "id": "P94",
            "text": "P94",
            "html": "<img src=\"/Search/Image?key=P94\" alt=\"P94\" style=\"max-height:24px; max-width: 28px;\" /> P94",
            "display": "P94"
        },
        {
            "id": "Q1",
            "text": "Q1: seat [st]",
            "html": "<span class=\"uni\">&#x132A8;</span> Q1: seat",
            "display": "Q1"
        },
        {
            "id": "Q11",
            "text": "Q11",
            "html": "<img src=\"/Search/Image?key=Q11\" alt=\"Q11\" style=\"max-height:24px; max-width: 28px;\" /> Q11",
            "display": "Q11"
        },
        {
            "id": "Q12",
            "text": "Q12",
            "html": "<img src=\"/Search/Image?key=Q12\" alt=\"Q12\" style=\"max-height:24px; max-width: 28px;\" /> Q12",
            "display": "Q12"
        },
        {
            "id": "Q12a",
            "text": "Q12A",
            "html": "<img src=\"/Search/Image?key=Q12A\" alt=\"Q12A\" style=\"max-height:24px; max-width: 28px;\" /> Q12A",
            "display": "Q12a"
        },
        {
            "id": "Q13",
            "text": "Q13",
            "html": "<img src=\"/Search/Image?key=Q13\" alt=\"Q13\" style=\"max-height:24px; max-width: 28px;\" /> Q13",
            "display": "Q13"
        },
        {
            "id": "Q14",
            "text": "Q14",
            "html": "<img src=\"/Search/Image?key=Q14\" alt=\"Q14\" style=\"max-height:24px; max-width: 28px;\" /> Q14",
            "display": "Q14"
        },
        {
            "id": "Q16",
            "text": "Q16",
            "html": "<img src=\"/Search/Image?key=Q16\" alt=\"Q16\" style=\"max-height:24px; max-width: 28px;\" /> Q16",
            "display": "Q16"
        },
        {
            "id": "Q18",
            "text": "Q18",
            "html": "<img src=\"/Search/Image?key=Q18\" alt=\"Q18\" style=\"max-height:24px; max-width: 28px;\" /> Q18",
            "display": "Q18"
        },
        {
            "id": "Q18a",
            "text": "Q18A",
            "html": "<img src=\"/Search/Image?key=Q18A\" alt=\"Q18A\" style=\"max-height:24px; max-width: 28px;\" /> Q18A",
            "display": "Q18a"
        },
        {
            "id": "Q19",
            "text": "Q19",
            "html": "<img src=\"/Search/Image?key=Q19\" alt=\"Q19\" style=\"max-height:24px; max-width: 28px;\" /> Q19",
            "display": "Q19"
        },
        {
            "id": "Q2",
            "text": "Q2: portable seat [wz]",
            "html": "<span class=\"uni\">&#x132A9;</span> Q2: portable seat",
            "display": "Q2"
        },
        {
            "id": "Q23",
            "text": "Q23",
            "html": "<img src=\"/Search/Image?key=Q23\" alt=\"Q23\" style=\"max-height:24px; max-width: 28px;\" /> Q23",
            "display": "Q23"
        },
        {
            "id": "Q24",
            "text": "Q24",
            "html": "<img src=\"/Search/Image?key=Q24\" alt=\"Q24\" style=\"max-height:24px; max-width: 28px;\" /> Q24",
            "display": "Q24"
        },
        {
            "id": "Q27",
            "text": "Q27",
            "html": "<img src=\"/Search/Image?key=Q27\" alt=\"Q27\" style=\"max-height:24px; max-width: 28px;\" /> Q27",
            "display": "Q27"
        },
        {
            "id": "Q28a",
            "text": "Q28A",
            "html": "<img src=\"/Search/Image?key=Q28A\" alt=\"Q28A\" style=\"max-height:24px; max-width: 28px;\" /> Q28A",
            "display": "Q28a"
        },
        {
            "id": "Q29",
            "text": "Q29",
            "html": "<img src=\"/Search/Image?key=Q29\" alt=\"Q29\" style=\"max-height:24px; max-width: 28px;\" /> Q29",
            "display": "Q29"
        },
        {
            "id": "Q2b",
            "text": "Q2B: portable seat",
            "html": "<img src=\"/Search/Image?key=Q2B\" alt=\"Q2B\" style=\"max-height:24px; max-width: 28px;\" /> Q2B: portable seat",
            "display": "Q2b"
        },
        {
            "id": "Q2c",
            "text": "Q2C: portable seat",
            "html": "<img src=\"/Search/Image?key=Q2C\" alt=\"Q2C\" style=\"max-height:24px; max-width: 28px;\" /> Q2C: portable seat",
            "display": "Q2c"
        },
        {
            "id": "Q3",
            "text": "Q3: stool [narrow] [p]",
            "html": "<span class=\"uni\">&#x132AA;</span> Q3: stool",
            "display": "Q3"
        },
        {
            "id": "Q32",
            "text": "Q32",
            "html": "<img src=\"/Search/Image?key=Q32\" alt=\"Q32\" style=\"max-height:24px; max-width: 28px;\" /> Q32",
            "display": "Q32"
        },
        {
            "id": "Q33",
            "text": "Q33",
            "html": "<img src=\"/Search/Image?key=Q33\" alt=\"Q33\" style=\"max-height:24px; max-width: 28px;\" /> Q33",
            "display": "Q33"
        },
        {
            "id": "Q36a",
            "text": "Q36A",
            "html": "<img src=\"/Search/Image?key=Q36A\" alt=\"Q36A\" style=\"max-height:24px; max-width: 28px;\" /> Q36A",
            "display": "Q36a"
        },
        {
            "id": "Q37",
            "text": "Q37",
            "html": "<img src=\"/Search/Image?key=Q37\" alt=\"Q37\" style=\"max-height:24px; max-width: 28px;\" /> Q37",
            "display": "Q37"
        },
        {
            "id": "Q38",
            "text": "Q38",
            "html": "<img src=\"/Search/Image?key=Q38\" alt=\"Q38\" style=\"max-height:24px; max-width: 28px;\" /> Q38",
            "display": "Q38"
        },
        {
            "id": "Q4",
            "text": "Q4: head-rest",
            "html": "<span class=\"uni\">&#x132AB;</span> Q4: head-rest",
            "display": "Q4"
        },
        {
            "id": "Q43",
            "text": "Q43",
            "html": "<img src=\"/Search/Image?key=Q43\" alt=\"Q43\" style=\"max-height:24px; max-width: 28px;\" /> Q43",
            "display": "Q43"
        },
        {
            "id": "Q5",
            "text": "Q5: chest",
            "html": "<span class=\"uni\">&#x132AC;</span> Q5: chest",
            "display": "Q5"
        },
        {
            "id": "Q6",
            "text": "Q6: coffin [qrsw]",
            "html": "<span class=\"uni\">&#x132AD;</span> Q6: coffin",
            "display": "Q6"
        },
        {
            "id": "Q6b",
            "text": "Q6B: coffin",
            "html": "<img src=\"/Search/Image?key=Q6B\" alt=\"Q6B\" style=\"max-height:24px; max-width: 28px;\" /> Q6B: coffin",
            "display": "Q6b"
        },
        {
            "id": "Q6e",
            "text": "Q6E: coffin",
            "html": "<img src=\"/Search/Image?key=Q6E\" alt=\"Q6E\" style=\"max-height:24px; max-width: 28px;\" /> Q6E: coffin",
            "display": "Q6e"
        },
        {
            "id": "Q7",
            "text": "Q7: brazier [tall]",
            "html": "<span class=\"uni\">&#x132AE;</span> Q7: brazier",
            "display": "Q7"
        },
        {
            "id": "Q7a",
            "text": "Q7A: brazier",
            "html": "<img src=\"/Search/Image?key=Q7A\" alt=\"Q7A\" style=\"max-height:24px; max-width: 28px;\" /> Q7A: brazier",
            "display": "Q7a"
        },
        {
            "id": "Q7e",
            "text": "Q7E: brazier",
            "html": "<img src=\"/Search/Image?key=Q7E\" alt=\"Q7E\" style=\"max-height:24px; max-width: 28px;\" /> Q7E: brazier",
            "display": "Q7e"
        },
        {
            "id": "Q7f",
            "text": "Q7F: brazier",
            "html": "<img src=\"/Search/Image?key=Q7F\" alt=\"Q7F\" style=\"max-height:24px; max-width: 28px;\" /> Q7F: brazier",
            "display": "Q7f"
        },
        {
            "id": "Q7g",
            "text": "Q7G: brazier",
            "html": "<img src=\"/Search/Image?key=Q7G\" alt=\"Q7G\" style=\"max-height:24px; max-width: 28px;\" /> Q7G: brazier",
            "display": "Q7g"
        },
        {
            "id": "R1",
            "text": "R1: high table with offerings [xAt]",
            "html": "<span class=\"uni\">&#x132AF;</span> R1: high table with offerings",
            "display": "R1"
        },
        {
            "id": "R10",
            "text": "R10: combination of R8, T28 and N29",
            "html": "<span class=\"uni\">&#x132BB;</span> R10: combination of R8, T28 and N29",
            "display": "R10"
        },
        {
            "id": "R100",
            "text": "R100",
            "html": "<img src=\"/Search/Image?key=R100\" alt=\"R100\" style=\"max-height:24px; max-width: 28px;\" /> R100",
            "display": "R100"
        },
        {
            "id": "R103",
            "text": "R103",
            "html": "<img src=\"/Search/Image?key=R103\" alt=\"R103\" style=\"max-height:24px; max-width: 28px;\" /> R103",
            "display": "R103"
        },
        {
            "id": "R10a",
            "text": "R10A: combination of R8 and T28",
            "html": "<span class=\"uni\">&#x132BC;</span> R10A: combination of R8 and T28",
            "display": "R10a"
        },
        {
            "id": "R10b",
            "text": "R10B: combination of R8, T28 and N29",
            "html": "<img src=\"/Search/Image?key=R10B\" alt=\"R10B\" style=\"max-height:24px; max-width: 28px;\" /> R10B: combination of R8, T28 and N29",
            "display": "R10b"
        },
        {
            "id": "R10h",
            "text": "R10H: combination of R8, T28 and N29",
            "html": "<img src=\"/Search/Image?key=R10H\" alt=\"R10H\" style=\"max-height:24px; max-width: 28px;\" /> R10H: combination of R8, T28 and N29",
            "display": "R10h"
        },
        {
            "id": "R11",
            "text": "R11: reed column [tall] [Dd]",
            "html": "<span class=\"uni\">&#x132BD;</span> R11: reed column",
            "display": "R11"
        },
        {
            "id": "R114",
            "text": "R114",
            "html": "<img src=\"/Search/Image?key=R114\" alt=\"R114\" style=\"max-height:24px; max-width: 28px;\" /> R114",
            "display": "R114"
        },
        {
            "id": "R118",
            "text": "R118",
            "html": "<img src=\"/Search/Image?key=R118\" alt=\"R118\" style=\"max-height:24px; max-width: 28px;\" /> R118",
            "display": "R118"
        },
        {
            "id": "R12",
            "text": "R12: standard",
            "html": "<span class=\"uni\">&#x132BE;</span> R12: standard",
            "display": "R12"
        },
        {
            "id": "R127a",
            "text": "R127A",
            "html": "<img src=\"/Search/Image?key=R127A\" alt=\"R127A\" style=\"max-height:24px; max-width: 28px;\" /> R127A",
            "display": "R127a"
        },
        {
            "id": "R12a",
            "text": "R12A: standard",
            "html": "<img src=\"/Search/Image?key=R12A\" alt=\"R12A\" style=\"max-height:24px; max-width: 28px;\" /> R12A: standard",
            "display": "R12a"
        },
        {
            "id": "R13",
            "text": "R13: falcon and feather on standard",
            "html": "<span class=\"uni\">&#x132BF;</span> R13: falcon and feather on standard",
            "display": "R13"
        },
        {
            "id": "R14",
            "text": "R14: feather on standard [tall] [imnt]",
            "html": "<span class=\"uni\">&#x132C0;</span> R14: feather on standard",
            "display": "R14"
        },
        {
            "id": "R15",
            "text": "R15: spear emblem [tall] [iAb]",
            "html": "<span class=\"uni\">&#x132C1;</span> R15: spear emblem",
            "display": "R15"
        },
        {
            "id": "R15a",
            "text": "R15A: spear emblem",
            "html": "<img src=\"/Search/Image?key=R15A\" alt=\"R15A\" style=\"max-height:24px; max-width: 28px;\" /> R15A: spear emblem",
            "display": "R15a"
        },
        {
            "id": "R16",
            "text": "R16: sceptre with feathers and string [tall] [wx]",
            "html": "<span class=\"uni\">&#x132C2;</span> R16: sceptre with feathers and string",
            "display": "R16"
        },
        {
            "id": "R17",
            "text": "R17: wig on pole [tall]",
            "html": "<span class=\"uni\">&#x132C4;</span> R17: wig on pole",
            "display": "R17"
        },
        {
            "id": "R18",
            "text": "R18: combination of R17 and N24",
            "html": "<span class=\"uni\">&#x132C5;</span> R18: combination of R17 and N24",
            "display": "R18"
        },
        {
            "id": "R18a",
            "text": "R18A: combination of R17 and N24",
            "html": "<img src=\"/Search/Image?key=R18A\" alt=\"R18A\" style=\"max-height:24px; max-width: 28px;\" /> R18A: combination of R17 and N24",
            "display": "R18a"
        },
        {
            "id": "R18b",
            "text": "R18B: combination of R17 and N24",
            "html": "<img src=\"/Search/Image?key=R18B\" alt=\"R18B\" style=\"max-height:24px; max-width: 28px;\" /> R18B: combination of R17 and N24",
            "display": "R18b"
        },
        {
            "id": "R19",
            "text": "R19: S40 with feather [tall]",
            "html": "<span class=\"uni\">&#x132C6;</span> R19: S40 with feather",
            "display": "R19"
        },
        {
            "id": "R19a",
            "text": "R19A: S40 with feather",
            "html": "<img src=\"/Search/Image?key=R19A\" alt=\"R19A\" style=\"max-height:24px; max-width: 28px;\" /> R19A: S40 with feather",
            "display": "R19a"
        },
        {
            "id": "R1c",
            "text": "R1C: high table with offerings",
            "html": "<img src=\"/Search/Image?key=R1C\" alt=\"R1C\" style=\"max-height:24px; max-width: 28px;\" /> R1C: high table with offerings",
            "display": "R1c"
        },
        {
            "id": "R1e",
            "text": "R1E: high table with offerings",
            "html": "<img src=\"/Search/Image?key=R1E\" alt=\"R1E\" style=\"max-height:24px; max-width: 28px;\" /> R1E: high table with offerings",
            "display": "R1e"
        },
        {
            "id": "R2",
            "text": "R2: table with slices of bread",
            "html": "<span class=\"uni\">&#x132B0;</span> R2: table with slices of bread",
            "display": "R2"
        },
        {
            "id": "R20",
            "text": "R20: flower with horns",
            "html": "<span class=\"uni\">&#x132C7;</span> R20: flower with horns",
            "display": "R20"
        },
        {
            "id": "R22",
            "text": "R22: two narrow belemnites [broad] [xm]",
            "html": "<span class=\"uni\">&#x132C9;</span> R22: two narrow belemnites",
            "display": "R22"
        },
        {
            "id": "R24",
            "text": "R24: two bows tied horizontally [broad]",
            "html": "<span class=\"uni\">&#x132CB;</span> R24: two bows tied horizontally",
            "display": "R24"
        },
        {
            "id": "R25",
            "text": "R25: two bows tied vertically",
            "html": "<span class=\"uni\">&#x132CC;</span> R25: two bows tied vertically",
            "display": "R25"
        },
        {
            "id": "R2b",
            "text": "R2B: table with slices of bread",
            "html": "<img src=\"/Search/Image?key=R2B\" alt=\"R2B\" style=\"max-height:24px; max-width: 28px;\" /> R2B: table with slices of bread",
            "display": "R2b"
        },
        {
            "id": "R3",
            "text": "R3: low table with offerings",
            "html": "<span class=\"uni\">&#x132B2;</span> R3: low table with offerings",
            "display": "R3"
        },
        {
            "id": "R30",
            "text": "R30",
            "html": "<img src=\"/Search/Image?key=R30\" alt=\"R30\" style=\"max-height:24px; max-width: 28px;\" /> R30",
            "display": "R30"
        },
        {
            "id": "R31",
            "text": "R31",
            "html": "<img src=\"/Search/Image?key=R31\" alt=\"R31\" style=\"max-height:24px; max-width: 28px;\" /> R31",
            "display": "R31"
        },
        {
            "id": "R33",
            "text": "R33",
            "html": "<img src=\"/Search/Image?key=R33\" alt=\"R33\" style=\"max-height:24px; max-width: 28px;\" /> R33",
            "display": "R33"
        },
        {
            "id": "R34",
            "text": "R34",
            "html": "<img src=\"/Search/Image?key=R34\" alt=\"R34\" style=\"max-height:24px; max-width: 28px;\" /> R34",
            "display": "R34"
        },
        {
            "id": "R36",
            "text": "R36",
            "html": "<img src=\"/Search/Image?key=R36\" alt=\"R36\" style=\"max-height:24px; max-width: 28px;\" /> R36",
            "display": "R36"
        },
        {
            "id": "R36a",
            "text": "R36A",
            "html": "<img src=\"/Search/Image?key=R36A\" alt=\"R36A\" style=\"max-height:24px; max-width: 28px;\" /> R36A",
            "display": "R36a"
        },
        {
            "id": "R36c",
            "text": "R36C",
            "html": "<img src=\"/Search/Image?key=R36C\" alt=\"R36C\" style=\"max-height:24px; max-width: 28px;\" /> R36C",
            "display": "R36c"
        },
        {
            "id": "R3a",
            "text": "R3A: low table",
            "html": "<span class=\"uni\">&#x132B3;</span> R3A: low table",
            "display": "R3a"
        },
        {
            "id": "R3ac",
            "text": "R3AC: low table with offerings",
            "html": "<img src=\"/Search/Image?key=R3AC\" alt=\"R3AC\" style=\"max-height:24px; max-width: 28px;\" /> R3AC: low table with offerings",
            "display": "R3ac"
        },
        {
            "id": "R3c",
            "text": "R3C: low table with offerings",
            "html": "<img src=\"/Search/Image?key=R3C\" alt=\"R3C\" style=\"max-height:24px; max-width: 28px;\" /> R3C: low table with offerings",
            "display": "R3c"
        },
        {
            "id": "R3i",
            "text": "R3I: low table with offerings",
            "html": "<img src=\"/Search/Image?key=R3I\" alt=\"R3I\" style=\"max-height:24px; max-width: 28px;\" /> R3I: low table with offerings",
            "display": "R3i"
        },
        {
            "id": "R3p",
            "text": "R3P: low table with offerings",
            "html": "<img src=\"/Search/Image?key=R3P\" alt=\"R3P\" style=\"max-height:24px; max-width: 28px;\" /> R3P: low table with offerings",
            "display": "R3p"
        },
        {
            "id": "R3q",
            "text": "R3Q: low table with offerings",
            "html": "<img src=\"/Search/Image?key=R3Q\" alt=\"R3Q\" style=\"max-height:24px; max-width: 28px;\" /> R3Q: low table with offerings",
            "display": "R3q"
        },
        {
            "id": "R3y",
            "text": "R3Y: low table with offerings",
            "html": "<img src=\"/Search/Image?key=R3Y\" alt=\"R3Y\" style=\"max-height:24px; max-width: 28px;\" /> R3Y: low table with offerings",
            "display": "R3y"
        },
        {
            "id": "R4",
            "text": "R4: loaf on mat [broad] [Htp]",
            "html": "<span class=\"uni\">&#x132B5;</span> R4: loaf on mat",
            "display": "R4"
        },
        {
            "id": "R40",
            "text": "R40",
            "html": "<img src=\"/Search/Image?key=R40\" alt=\"R40\" style=\"max-height:24px; max-width: 28px;\" /> R40",
            "display": "R40"
        },
        {
            "id": "R40a",
            "text": "R40A",
            "html": "<img src=\"/Search/Image?key=R40A\" alt=\"R40A\" style=\"max-height:24px; max-width: 28px;\" /> R40A",
            "display": "R40a"
        },
        {
            "id": "R42",
            "text": "R42",
            "html": "<img src=\"/Search/Image?key=R42\" alt=\"R42\" style=\"max-height:24px; max-width: 28px;\" /> R42",
            "display": "R42"
        },
        {
            "id": "R42a",
            "text": "R42A",
            "html": "<img src=\"/Search/Image?key=R42A\" alt=\"R42A\" style=\"max-height:24px; max-width: 28px;\" /> R42A",
            "display": "R42a"
        },
        {
            "id": "R5",
            "text": "R5: narrow censer [broad] [kp]",
            "html": "<span class=\"uni\">&#x132B6;</span> R5: narrow censer",
            "display": "R5"
        },
        {
            "id": "R50",
            "text": "R50",
            "html": "<img src=\"/Search/Image?key=R50\" alt=\"R50\" style=\"max-height:24px; max-width: 28px;\" /> R50",
            "display": "R50"
        },
        {
            "id": "R59",
            "text": "R59",
            "html": "<img src=\"/Search/Image?key=R59\" alt=\"R59\" style=\"max-height:24px; max-width: 28px;\" /> R59",
            "display": "R59"
        },
        {
            "id": "R6",
            "text": "R6: broad censer [broad]",
            "html": "<span class=\"uni\">&#x132B7;</span> R6: broad censer",
            "display": "R6"
        },
        {
            "id": "R60",
            "text": "R60",
            "html": "<img src=\"/Search/Image?key=R60\" alt=\"R60\" style=\"max-height:24px; max-width: 28px;\" /> R60",
            "display": "R60"
        },
        {
            "id": "R61",
            "text": "R61",
            "html": "<img src=\"/Search/Image?key=R61\" alt=\"R61\" style=\"max-height:24px; max-width: 28px;\" /> R61",
            "display": "R61"
        },
        {
            "id": "R62a",
            "text": "R62A",
            "html": "<img src=\"/Search/Image?key=R62A\" alt=\"R62A\" style=\"max-height:24px; max-width: 28px;\" /> R62A",
            "display": "R62a"
        },
        {
            "id": "R7",
            "text": "R7: bowl with smoke [narrow] [snTr]",
            "html": "<span class=\"uni\">&#x132B8;</span> R7: bowl with smoke",
            "display": "R7"
        },
        {
            "id": "R78",
            "text": "R78",
            "html": "<img src=\"/Search/Image?key=R78\" alt=\"R78\" style=\"max-height:24px; max-width: 28px;\" /> R78",
            "display": "R78"
        },
        {
            "id": "R8",
            "text": "R8: cloth on pole [tall] [nTr]",
            "html": "<span class=\"uni\">&#x132B9;</span> R8: cloth on pole",
            "display": "R8"
        },
        {
            "id": "R81",
            "text": "R81",
            "html": "<img src=\"/Search/Image?key=R81\" alt=\"R81\" style=\"max-height:24px; max-width: 28px;\" /> R81",
            "display": "R81"
        },
        {
            "id": "R88",
            "text": "R88",
            "html": "<img src=\"/Search/Image?key=R88\" alt=\"R88\" style=\"max-height:24px; max-width: 28px;\" /> R88",
            "display": "R88"
        },
        {
            "id": "R88a",
            "text": "R88A",
            "html": "<img src=\"/Search/Image?key=R88A\" alt=\"R88A\" style=\"max-height:24px; max-width: 28px;\" /> R88A",
            "display": "R88a"
        },
        {
            "id": "R89",
            "text": "R89",
            "html": "<img src=\"/Search/Image?key=R89\" alt=\"R89\" style=\"max-height:24px; max-width: 28px;\" /> R89",
            "display": "R89"
        },
        {
            "id": "R8a",
            "text": "R8A: cloth on pole",
            "html": "<img src=\"/Search/Image?key=R8A\" alt=\"R8A\" style=\"max-height:24px; max-width: 28px;\" /> R8A: cloth on pole",
            "display": "R8a"
        },
        {
            "id": "R9",
            "text": "R9: combination of R8 and V33 [tall] [bd]",
            "html": "<span class=\"uni\">&#x132BA;</span> R9: combination of R8 and V33",
            "display": "R9"
        },
        {
            "id": "R91",
            "text": "R91",
            "html": "<img src=\"/Search/Image?key=R91\" alt=\"R91\" style=\"max-height:24px; max-width: 28px;\" /> R91",
            "display": "R91"
        },
        {
            "id": "R92",
            "text": "R92",
            "html": "<img src=\"/Search/Image?key=R92\" alt=\"R92\" style=\"max-height:24px; max-width: 28px;\" /> R92",
            "display": "R92"
        },
        {
            "id": "R93",
            "text": "R93",
            "html": "<img src=\"/Search/Image?key=R93\" alt=\"R93\" style=\"max-height:24px; max-width: 28px;\" /> R93",
            "display": "R93"
        },
        {
            "id": "R97",
            "text": "R97",
            "html": "<img src=\"/Search/Image?key=R97\" alt=\"R97\" style=\"max-height:24px; max-width: 28px;\" /> R97",
            "display": "R97"
        },
        {
            "id": "S1",
            "text": "S1: white crown [HDt]",
            "html": "<span class=\"uni\">&#x132D1;</span> S1: white crown",
            "display": "S1"
        },
        {
            "id": "S10",
            "text": "S10: headband [narrow] [mDH]",
            "html": "<span class=\"uni\">&#x132DC;</span> S10: headband",
            "display": "S10"
        },
        {
            "id": "S100a",
            "text": "S100A",
            "html": "<img src=\"/Search/Image?key=S100A\" alt=\"S100A\" style=\"max-height:24px; max-width: 28px;\" /> S100A",
            "display": "S100a"
        },
        {
            "id": "S104",
            "text": "S104",
            "html": "<img src=\"/Search/Image?key=S104\" alt=\"S104\" style=\"max-height:24px; max-width: 28px;\" /> S104",
            "display": "S104"
        },
        {
            "id": "S105",
            "text": "S105",
            "html": "<img src=\"/Search/Image?key=S105\" alt=\"S105\" style=\"max-height:24px; max-width: 28px;\" /> S105",
            "display": "S105"
        },
        {
            "id": "S106",
            "text": "S106",
            "html": "<img src=\"/Search/Image?key=S106\" alt=\"S106\" style=\"max-height:24px; max-width: 28px;\" /> S106",
            "display": "S106"
        },
        {
            "id": "S107",
            "text": "S107",
            "html": "<img src=\"/Search/Image?key=S107\" alt=\"S107\" style=\"max-height:24px; max-width: 28px;\" /> S107",
            "display": "S107"
        },
        {
            "id": "S109a",
            "text": "S109A",
            "html": "<img src=\"/Search/Image?key=S109A\" alt=\"S109A\" style=\"max-height:24px; max-width: 28px;\" /> S109A",
            "display": "S109a"
        },
        {
            "id": "S10a",
            "text": "S10A: headband",
            "html": "<img src=\"/Search/Image?key=S10A\" alt=\"S10A\" style=\"max-height:24px; max-width: 28px;\" /> S10A: headband",
            "display": "S10a"
        },
        {
            "id": "S11",
            "text": "S11: broad collar [narrow] [wsx]",
            "html": "<span class=\"uni\">&#x132DD;</span> S11: broad collar",
            "display": "S11"
        },
        {
            "id": "S110",
            "text": "S110",
            "html": "<img src=\"/Search/Image?key=S110\" alt=\"S110\" style=\"max-height:24px; max-width: 28px;\" /> S110",
            "display": "S110"
        },
        {
            "id": "S111",
            "text": "S111",
            "html": "<img src=\"/Search/Image?key=S111\" alt=\"S111\" style=\"max-height:24px; max-width: 28px;\" /> S111",
            "display": "S111"
        },
        {
            "id": "S112",
            "text": "S112",
            "html": "<img src=\"/Search/Image?key=S112\" alt=\"S112\" style=\"max-height:24px; max-width: 28px;\" /> S112",
            "display": "S112"
        },
        {
            "id": "S113",
            "text": "S113",
            "html": "<img src=\"/Search/Image?key=S113\" alt=\"S113\" style=\"max-height:24px; max-width: 28px;\" /> S113",
            "display": "S113"
        },
        {
            "id": "S114",
            "text": "S114",
            "html": "<img src=\"/Search/Image?key=S114\" alt=\"S114\" style=\"max-height:24px; max-width: 28px;\" /> S114",
            "display": "S114"
        },
        {
            "id": "S115",
            "text": "S115",
            "html": "<img src=\"/Search/Image?key=S115\" alt=\"S115\" style=\"max-height:24px; max-width: 28px;\" /> S115",
            "display": "S115"
        },
        {
            "id": "S116",
            "text": "S116",
            "html": "<img src=\"/Search/Image?key=S116\" alt=\"S116\" style=\"max-height:24px; max-width: 28px;\" /> S116",
            "display": "S116"
        },
        {
            "id": "S117",
            "text": "S117",
            "html": "<img src=\"/Search/Image?key=S117\" alt=\"S117\" style=\"max-height:24px; max-width: 28px;\" /> S117",
            "display": "S117"
        },
        {
            "id": "S11b",
            "text": "S11B: broad collar",
            "html": "<img src=\"/Search/Image?key=S11B\" alt=\"S11B\" style=\"max-height:24px; max-width: 28px;\" /> S11B: broad collar",
            "display": "S11b"
        },
        {
            "id": "S12",
            "text": "S12: collar of beads [broad] [nbw]",
            "html": "<span class=\"uni\">&#x132DE;</span> S12: collar of beads",
            "display": "S12"
        },
        {
            "id": "S123",
            "text": "S123",
            "html": "<img src=\"/Search/Image?key=S123\" alt=\"S123\" style=\"max-height:24px; max-width: 28px;\" /> S123",
            "display": "S123"
        },
        {
            "id": "S125",
            "text": "S125",
            "html": "<img src=\"/Search/Image?key=S125\" alt=\"S125\" style=\"max-height:24px; max-width: 28px;\" /> S125",
            "display": "S125"
        },
        {
            "id": "S126",
            "text": "S126",
            "html": "<img src=\"/Search/Image?key=S126\" alt=\"S126\" style=\"max-height:24px; max-width: 28px;\" /> S126",
            "display": "S126"
        },
        {
            "id": "S12a",
            "text": "S12A: collar of beads",
            "html": "<img src=\"/Search/Image?key=S12A\" alt=\"S12A\" style=\"max-height:24px; max-width: 28px;\" /> S12A: collar of beads",
            "display": "S12a"
        },
        {
            "id": "S13",
            "text": "S13: combination of S12 and D58",
            "html": "<span class=\"uni\">&#x132DF;</span> S13: combination of S12 and D58",
            "display": "S13"
        },
        {
            "id": "S130",
            "text": "S130",
            "html": "<img src=\"/Search/Image?key=S130\" alt=\"S130\" style=\"max-height:24px; max-width: 28px;\" /> S130",
            "display": "S130"
        },
        {
            "id": "S131",
            "text": "S131",
            "html": "<img src=\"/Search/Image?key=S131\" alt=\"S131\" style=\"max-height:24px; max-width: 28px;\" /> S131",
            "display": "S131"
        },
        {
            "id": "S134b",
            "text": "S134B",
            "html": "<img src=\"/Search/Image?key=S134B\" alt=\"S134B\" style=\"max-height:24px; max-width: 28px;\" /> S134B",
            "display": "S134b"
        },
        {
            "id": "S14",
            "text": "S14: combination of S12 and T3",
            "html": "<span class=\"uni\">&#x132E0;</span> S14: combination of S12 and T3",
            "display": "S14"
        },
        {
            "id": "S142",
            "text": "S142",
            "html": "<img src=\"/Search/Image?key=S142\" alt=\"S142\" style=\"max-height:24px; max-width: 28px;\" /> S142",
            "display": "S142"
        },
        {
            "id": "S144",
            "text": "S144",
            "html": "<img src=\"/Search/Image?key=S144\" alt=\"S144\" style=\"max-height:24px; max-width: 28px;\" /> S144",
            "display": "S144"
        },
        {
            "id": "S14a",
            "text": "S14A: combination of S12 and S40",
            "html": "<span class=\"uni\">&#x132E1;</span> S14A: combination of S12 and S40",
            "display": "S14a"
        },
        {
            "id": "S15",
            "text": "S15: pectoral [THn]",
            "html": "<span class=\"uni\">&#x132E3;</span> S15: pectoral",
            "display": "S15"
        },
        {
            "id": "S151",
            "text": "S151",
            "html": "<img src=\"/Search/Image?key=S151\" alt=\"S151\" style=\"max-height:24px; max-width: 28px;\" /> S151",
            "display": "S151"
        },
        {
            "id": "S152",
            "text": "S152",
            "html": "<img src=\"/Search/Image?key=S152\" alt=\"S152\" style=\"max-height:24px; max-width: 28px;\" /> S152",
            "display": "S152"
        },
        {
            "id": "S152a",
            "text": "S152A",
            "html": "<img src=\"/Search/Image?key=S152A\" alt=\"S152A\" style=\"max-height:24px; max-width: 28px;\" /> S152A",
            "display": "S152a"
        },
        {
            "id": "S156",
            "text": "S156",
            "html": "<img src=\"/Search/Image?key=S156\" alt=\"S156\" style=\"max-height:24px; max-width: 28px;\" /> S156",
            "display": "S156"
        },
        {
            "id": "S15a",
            "text": "S15A: pectoral",
            "html": "<img src=\"/Search/Image?key=S15A\" alt=\"S15A\" style=\"max-height:24px; max-width: 28px;\" /> S15A: pectoral",
            "display": "S15a"
        },
        {
            "id": "S16",
            "text": "S16: pectoral",
            "html": "<span class=\"uni\">&#x132E4;</span> S16: pectoral",
            "display": "S16"
        },
        {
            "id": "S163",
            "text": "S163",
            "html": "<img src=\"/Search/Image?key=S163\" alt=\"S163\" style=\"max-height:24px; max-width: 28px;\" /> S163",
            "display": "S163"
        },
        {
            "id": "S167",
            "text": "S167",
            "html": "<img src=\"/Search/Image?key=S167\" alt=\"S167\" style=\"max-height:24px; max-width: 28px;\" /> S167",
            "display": "S167"
        },
        {
            "id": "S17",
            "text": "S17: pectoral",
            "html": "<span class=\"uni\">&#x132E5;</span> S17: pectoral",
            "display": "S17"
        },
        {
            "id": "S17a",
            "text": "S17A: girdle",
            "html": "<span class=\"uni\">&#x132E6;</span> S17A: girdle",
            "display": "S17a"
        },
        {
            "id": "S17b",
            "text": "S17B: pectoral",
            "html": "<img src=\"/Search/Image?key=S17B\" alt=\"S17B\" style=\"max-height:24px; max-width: 28px;\" /> S17B: pectoral",
            "display": "S17b"
        },
        {
            "id": "S18",
            "text": "S18: necklace with counterpoise [mnit]",
            "html": "<span class=\"uni\">&#x132E7;</span> S18: necklace with counterpoise",
            "display": "S18"
        },
        {
            "id": "S184",
            "text": "S184",
            "html": "<img src=\"/Search/Image?key=S184\" alt=\"S184\" style=\"max-height:24px; max-width: 28px;\" /> S184",
            "display": "S184"
        },
        {
            "id": "S19",
            "text": "S19: necklace with seal from side [sDAw]",
            "html": "<span class=\"uni\">&#x132E8;</span> S19: necklace with seal from side",
            "display": "S19"
        },
        {
            "id": "S193",
            "text": "S193",
            "html": "<img src=\"/Search/Image?key=S193\" alt=\"S193\" style=\"max-height:24px; max-width: 28px;\" /> S193",
            "display": "S193"
        },
        {
            "id": "S197",
            "text": "S197",
            "html": "<img src=\"/Search/Image?key=S197\" alt=\"S197\" style=\"max-height:24px; max-width: 28px;\" /> S197",
            "display": "S197"
        },
        {
            "id": "S199a",
            "text": "S199A",
            "html": "<img src=\"/Search/Image?key=S199A\" alt=\"S199A\" style=\"max-height:24px; max-width: 28px;\" /> S199A",
            "display": "S199a"
        },
        {
            "id": "S2",
            "text": "S2: combination of S1 and V30",
            "html": "<span class=\"uni\">&#x132D2;</span> S2: combination of S1 and V30",
            "display": "S2"
        },
        {
            "id": "S20",
            "text": "S20: necklace with seal from front [narrow] [xtm]",
            "html": "<span class=\"uni\">&#x132E9;</span> S20: necklace with seal from front",
            "display": "S20"
        },
        {
            "id": "S20a",
            "text": "S20A: necklace with seal from front",
            "html": "<img src=\"/Search/Image?key=S20A\" alt=\"S20A\" style=\"max-height:24px; max-width: 28px;\" /> S20A: necklace with seal from front",
            "display": "S20a"
        },
        {
            "id": "S21",
            "text": "S21: ring [narrow]",
            "html": "<span class=\"uni\">&#x132EA;</span> S21: ring",
            "display": "S21"
        },
        {
            "id": "S21a",
            "text": "S21A: ring",
            "html": "<img src=\"/Search/Image?key=S21A\" alt=\"S21A\" style=\"max-height:24px; max-width: 28px;\" /> S21A: ring",
            "display": "S21a"
        },
        {
            "id": "S22",
            "text": "S22: shoulder-knot [sT]",
            "html": "<span class=\"uni\">&#x132EB;</span> S22: shoulder-knot",
            "display": "S22"
        },
        {
            "id": "S23",
            "text": "S23: knotted cloth [dmD]",
            "html": "<span class=\"uni\">&#x132EC;</span> S23: knotted cloth",
            "display": "S23"
        },
        {
            "id": "S24",
            "text": "S24: girdle knot [broad] [Tz]",
            "html": "<span class=\"uni\">&#x132ED;</span> S24: girdle knot",
            "display": "S24"
        },
        {
            "id": "S25",
            "text": "S25: garment with ties",
            "html": "<span class=\"uni\">&#x132EE;</span> S25: garment with ties",
            "display": "S25"
        },
        {
            "id": "S26",
            "text": "S26: apron [Sndyt]",
            "html": "<span class=\"uni\">&#x132EF;</span> S26: apron",
            "display": "S26"
        },
        {
            "id": "S27",
            "text": "S27: cloth with two strands [mnxt]",
            "html": "<span class=\"uni\">&#x132F2;</span> S27: cloth with two strands",
            "display": "S27"
        },
        {
            "id": "S28",
            "text": "S28: cloth with fringe on top and S29",
            "html": "<span class=\"uni\">&#x132F3;</span> S28: cloth with fringe on top and S29",
            "display": "S28"
        },
        {
            "id": "S29",
            "text": "S29: folded cloth [tall] [s]",
            "html": "<span class=\"uni\">&#x132F4;</span> S29: folded cloth",
            "display": "S29"
        },
        {
            "id": "S29b",
            "text": "S29B: folded cloth",
            "html": "<img src=\"/Search/Image?key=S29B\" alt=\"S29B\" style=\"max-height:24px; max-width: 28px;\" /> S29B: folded cloth",
            "display": "S29b"
        },
        {
            "id": "S2a",
            "text": "S2A: combination of S1 and O49",
            "html": "<span class=\"uni\">&#x132D3;</span> S2A: combination of S1 and O49",
            "display": "S2a"
        },
        {
            "id": "S3",
            "text": "S3: red crown [N]",
            "html": "<span class=\"uni\">&#x132D4;</span> S3: red crown",
            "display": "S3"
        },
        {
            "id": "S30",
            "text": "S30: combination of S29 and I9 [sf]",
            "html": "<span class=\"uni\">&#x132F5;</span> S30: combination of S29 and I9",
            "display": "S30"
        },
        {
            "id": "S32",
            "text": "S32: cloth with fringe on the side [broad] [siA]",
            "html": "<span class=\"uni\">&#x132F7;</span> S32: cloth with fringe on the side",
            "display": "S32"
        },
        {
            "id": "S33",
            "text": "S33: sandle [Tb]",
            "html": "<span class=\"uni\">&#x132F8;</span> S33: sandle",
            "display": "S33"
        },
        {
            "id": "S34",
            "text": "S34: sandle-strap [tall] [anx]",
            "html": "<span class=\"uni\">&#x132F9;</span> S34: sandle-strap",
            "display": "S34"
        },
        {
            "id": "S35",
            "text": "S35: sunshade [Swt]",
            "html": "<span class=\"uni\">&#x132FA;</span> S35: sunshade",
            "display": "S35"
        },
        {
            "id": "S36",
            "text": "S36: sunshade [tall]",
            "html": "<span class=\"uni\">&#x132FC;</span> S36: sunshade",
            "display": "S36"
        },
        {
            "id": "S36a",
            "text": "S36A: sunshade",
            "html": "<img src=\"/Search/Image?key=S36A\" alt=\"S36A\" style=\"max-height:24px; max-width: 28px;\" /> S36A: sunshade",
            "display": "S36a"
        },
        {
            "id": "S36c",
            "text": "S36C: sunshade",
            "html": "<img src=\"/Search/Image?key=S36C\" alt=\"S36C\" style=\"max-height:24px; max-width: 28px;\" /> S36C: sunshade",
            "display": "S36c"
        },
        {
            "id": "S37",
            "text": "S37: fan [tall] [xw]",
            "html": "<span class=\"uni\">&#x132FD;</span> S37: fan",
            "display": "S37"
        },
        {
            "id": "S37a",
            "text": "S37A: fan",
            "html": "<img src=\"/Search/Image?key=S37A\" alt=\"S37A\" style=\"max-height:24px; max-width: 28px;\" /> S37A: fan",
            "display": "S37a"
        },
        {
            "id": "S38",
            "text": "S38: crook [tall] [HqA]",
            "html": "<span class=\"uni\">&#x132FE;</span> S38: crook",
            "display": "S38"
        },
        {
            "id": "S39",
            "text": "S39: shepherd&amp;apos;s crook [tall] [awt]",
            "html": "<span class=\"uni\">&#x132FF;</span> S39: shepherd&amp;apos;s crook",
            "display": "S39"
        },
        {
            "id": "S4",
            "text": "S4: combination of S3 and V30",
            "html": "<span class=\"uni\">&#x132D5;</span> S4: combination of S3 and V30",
            "display": "S4"
        },
        {
            "id": "S40",
            "text": "S40: sceptre [tall] [wAs]",
            "html": "<span class=\"uni\">&#x13300;</span> S40: sceptre",
            "display": "S40"
        },
        {
            "id": "S41",
            "text": "S41: sceptre with spiral shaft [tall] [Dam]",
            "html": "<span class=\"uni\">&#x13301;</span> S41: sceptre with spiral shaft",
            "display": "S41"
        },
        {
            "id": "S42",
            "text": "S42: sceptre of authority [tall] [sxm]",
            "html": "<span class=\"uni\">&#x13302;</span> S42: sceptre of authority",
            "display": "S42"
        },
        {
            "id": "S43",
            "text": "S43: walking stick [tall] [md]",
            "html": "<span class=\"uni\">&#x13303;</span> S43: walking stick",
            "display": "S43"
        },
        {
            "id": "S44",
            "text": "S44: walking stick with S45 [tall] [Ams]",
            "html": "<span class=\"uni\">&#x13304;</span> S44: walking stick with S45",
            "display": "S44"
        },
        {
            "id": "S44a",
            "text": "S44A: walking stick with S45",
            "html": "<img src=\"/Search/Image?key=S44A\" alt=\"S44A\" style=\"max-height:24px; max-width: 28px;\" /> S44A: walking stick with S45",
            "display": "S44a"
        },
        {
            "id": "S45",
            "text": "S45: flagellum [nxxw]",
            "html": "<span class=\"uni\">&#x13305;</span> S45: flagellum",
            "display": "S45"
        },
        {
            "id": "S47",
            "text": "S47",
            "html": "<img src=\"/Search/Image?key=S47\" alt=\"S47\" style=\"max-height:24px; max-width: 28px;\" /> S47",
            "display": "S47"
        },
        {
            "id": "S47a",
            "text": "S47A",
            "html": "<img src=\"/Search/Image?key=S47A\" alt=\"S47A\" style=\"max-height:24px; max-width: 28px;\" /> S47A",
            "display": "S47a"
        },
        {
            "id": "S5",
            "text": "S5: double crown",
            "html": "<span class=\"uni\">&#x132D6;</span> S5: double crown",
            "display": "S5"
        },
        {
            "id": "S51",
            "text": "S51",
            "html": "<img src=\"/Search/Image?key=S51\" alt=\"S51\" style=\"max-height:24px; max-width: 28px;\" /> S51",
            "display": "S51"
        },
        {
            "id": "S55",
            "text": "S55",
            "html": "<img src=\"/Search/Image?key=S55\" alt=\"S55\" style=\"max-height:24px; max-width: 28px;\" /> S55",
            "display": "S55"
        },
        {
            "id": "S56",
            "text": "S56",
            "html": "<img src=\"/Search/Image?key=S56\" alt=\"S56\" style=\"max-height:24px; max-width: 28px;\" /> S56",
            "display": "S56"
        },
        {
            "id": "S57",
            "text": "S57",
            "html": "<img src=\"/Search/Image?key=S57\" alt=\"S57\" style=\"max-height:24px; max-width: 28px;\" /> S57",
            "display": "S57"
        },
        {
            "id": "S57a",
            "text": "S57A",
            "html": "<img src=\"/Search/Image?key=S57A\" alt=\"S57A\" style=\"max-height:24px; max-width: 28px;\" /> S57A",
            "display": "S57a"
        },
        {
            "id": "S57b",
            "text": "S57B",
            "html": "<img src=\"/Search/Image?key=S57B\" alt=\"S57B\" style=\"max-height:24px; max-width: 28px;\" /> S57B",
            "display": "S57b"
        },
        {
            "id": "S57c",
            "text": "S57C",
            "html": "<img src=\"/Search/Image?key=S57C\" alt=\"S57C\" style=\"max-height:24px; max-width: 28px;\" /> S57C",
            "display": "S57c"
        },
        {
            "id": "S59",
            "text": "S59",
            "html": "<img src=\"/Search/Image?key=S59\" alt=\"S59\" style=\"max-height:24px; max-width: 28px;\" /> S59",
            "display": "S59"
        },
        {
            "id": "S6",
            "text": "S6: combination of S5 and V30 [sxmty]",
            "html": "<span class=\"uni\">&#x132D7;</span> S6: combination of S5 and V30",
            "display": "S6"
        },
        {
            "id": "S61a",
            "text": "S61A",
            "html": "<img src=\"/Search/Image?key=S61A\" alt=\"S61A\" style=\"max-height:24px; max-width: 28px;\" /> S61A",
            "display": "S61a"
        },
        {
            "id": "S62",
            "text": "S62",
            "html": "<img src=\"/Search/Image?key=S62\" alt=\"S62\" style=\"max-height:24px; max-width: 28px;\" /> S62",
            "display": "S62"
        },
        {
            "id": "S63",
            "text": "S63",
            "html": "<img src=\"/Search/Image?key=S63\" alt=\"S63\" style=\"max-height:24px; max-width: 28px;\" /> S63",
            "display": "S63"
        },
        {
            "id": "S7",
            "text": "S7: blue crown [xprS]",
            "html": "<span class=\"uni\">&#x132D9;</span> S7: blue crown",
            "display": "S7"
        },
        {
            "id": "S76",
            "text": "S76",
            "html": "<img src=\"/Search/Image?key=S76\" alt=\"S76\" style=\"max-height:24px; max-width: 28px;\" /> S76",
            "display": "S76"
        },
        {
            "id": "S8",
            "text": "S8: <span class=\"egytransl\">Atf</span>-crown [Atf]",
            "html": "<span class=\"uni\">&#x132DA;</span> S8: <span class=\"egytransl\">Atf</span>-crown",
            "display": "S8"
        },
        {
            "id": "S84",
            "text": "S84",
            "html": "S84",
            "display": "S84"
        },
        {
            "id": "S88",
            "text": "S88",
            "html": "<img src=\"/Search/Image?key=S88\" alt=\"S88\" style=\"max-height:24px; max-width: 28px;\" /> S88",
            "display": "S88"
        },
        {
            "id": "S89",
            "text": "S89",
            "html": "<img src=\"/Search/Image?key=S89\" alt=\"S89\" style=\"max-height:24px; max-width: 28px;\" /> S89",
            "display": "S89"
        },
        {
            "id": "S8a",
            "text": "S8A: <span class=\"egytransl\">Atf</span>-crown",
            "html": "<img src=\"/Search/Image?key=S8A\" alt=\"S8A\" style=\"max-height:24px; max-width: 28px;\" /> S8A: <span class=\"egytransl\">Atf</span>-crown",
            "display": "S8a"
        },
        {
            "id": "S9",
            "text": "S9: two plumes [Swty]",
            "html": "<span class=\"uni\">&#x132DB;</span> S9: two plumes",
            "display": "S9"
        },
        {
            "id": "S91a",
            "text": "S91A",
            "html": "<img src=\"/Search/Image?key=S91A\" alt=\"S91A\" style=\"max-height:24px; max-width: 28px;\" /> S91A",
            "display": "S91a"
        },
        {
            "id": "S95",
            "text": "S95",
            "html": "<img src=\"/Search/Image?key=S95\" alt=\"S95\" style=\"max-height:24px; max-width: 28px;\" /> S95",
            "display": "S95"
        },
        {
            "id": "T1",
            "text": "T1: mace with flat head [broad]",
            "html": "<span class=\"uni\">&#x13307;</span> T1: mace with flat head",
            "display": "T1"
        },
        {
            "id": "T10",
            "text": "T10: composite bow [broad] [pD]",
            "html": "<span class=\"uni\">&#x13314;</span> T10: composite bow",
            "display": "T10"
        },
        {
            "id": "T101",
            "text": "T101",
            "html": "<img src=\"/Search/Image?key=T101\" alt=\"T101\" style=\"max-height:24px; max-width: 28px;\" /> T101",
            "display": "T101"
        },
        {
            "id": "T106",
            "text": "T106",
            "html": "<img src=\"/Search/Image?key=T106\" alt=\"T106\" style=\"max-height:24px; max-width: 28px;\" /> T106",
            "display": "T106"
        },
        {
            "id": "T109",
            "text": "T109",
            "html": "<img src=\"/Search/Image?key=T109\" alt=\"T109\" style=\"max-height:24px; max-width: 28px;\" /> T109",
            "display": "T109"
        },
        {
            "id": "T11",
            "text": "T11: arrow [broad] [sXr]",
            "html": "<span class=\"uni\">&#x13315;</span> T11: arrow",
            "display": "T11"
        },
        {
            "id": "T113",
            "text": "T113",
            "html": "<img src=\"/Search/Image?key=T113\" alt=\"T113\" style=\"max-height:24px; max-width: 28px;\" /> T113",
            "display": "T113"
        },
        {
            "id": "T11b",
            "text": "T11B: arrow",
            "html": "<img src=\"/Search/Image?key=T11B\" alt=\"T11B\" style=\"max-height:24px; max-width: 28px;\" /> T11B: arrow",
            "display": "T11b"
        },
        {
            "id": "T12",
            "text": "T12: bow-string [rwD]",
            "html": "<span class=\"uni\">&#x13317;</span> T12: bow-string",
            "display": "T12"
        },
        {
            "id": "T12a",
            "text": "T12A: bow-string",
            "html": "<img src=\"/Search/Image?key=T12A\" alt=\"T12A\" style=\"max-height:24px; max-width: 28px;\" /> T12A: bow-string",
            "display": "T12a"
        },
        {
            "id": "T13",
            "text": "T13: joined pieces of wood [tall] [rs]",
            "html": "<span class=\"uni\">&#x13318;</span> T13: joined pieces of wood",
            "display": "T13"
        },
        {
            "id": "T14",
            "text": "T14: throw stick vertically [tall] [qmA]",
            "html": "<span class=\"uni\">&#x13319;</span> T14: throw stick vertically",
            "display": "T14"
        },
        {
            "id": "T14c",
            "text": "T14C: throw stick vertically",
            "html": "<img src=\"/Search/Image?key=T14C\" alt=\"T14C\" style=\"max-height:24px; max-width: 28px;\" /> T14C: throw stick vertically",
            "display": "T14c"
        },
        {
            "id": "T15",
            "text": "T15: throw stick slanted [tall]",
            "html": "<span class=\"uni\">&#x1331A;</span> T15: throw stick slanted",
            "display": "T15"
        },
        {
            "id": "T16",
            "text": "T16: scimitar",
            "html": "<span class=\"uni\">&#x1331B;</span> T16: scimitar",
            "display": "T16"
        },
        {
            "id": "T16a",
            "text": "T16A: scimitar",
            "html": "<span class=\"uni\">&#x1331C;</span> T16A: scimitar",
            "display": "T16a"
        },
        {
            "id": "T17",
            "text": "T17: chariot [wrrt]",
            "html": "<span class=\"uni\">&#x1331D;</span> T17: chariot",
            "display": "T17"
        },
        {
            "id": "T18",
            "text": "T18: crook with package attached [tall] [Sms]",
            "html": "<span class=\"uni\">&#x1331E;</span> T18: crook with package attached",
            "display": "T18"
        },
        {
            "id": "T19",
            "text": "T19: harpoon head [tall] [qs]",
            "html": "<span class=\"uni\">&#x1331F;</span> T19: harpoon head",
            "display": "T19"
        },
        {
            "id": "T19b",
            "text": "T19B: harpoon head",
            "html": "<img src=\"/Search/Image?key=T19B\" alt=\"T19B\" style=\"max-height:24px; max-width: 28px;\" /> T19B: harpoon head",
            "display": "T19b"
        },
        {
            "id": "T1a",
            "text": "T1A: mace with flat head",
            "html": "<img src=\"/Search/Image?key=T1A\" alt=\"T1A\" style=\"max-height:24px; max-width: 28px;\" /> T1A: mace with flat head",
            "display": "T1a"
        },
        {
            "id": "T2",
            "text": "T2: mace with round head diagonally [broad]",
            "html": "<span class=\"uni\">&#x13308;</span> T2: mace with round head diagonally",
            "display": "T2"
        },
        {
            "id": "T20",
            "text": "T20: harpoon head [tall]",
            "html": "<span class=\"uni\">&#x13320;</span> T20: harpoon head",
            "display": "T20"
        },
        {
            "id": "T21",
            "text": "T21: harpoon [broad]",
            "html": "<span class=\"uni\">&#x13321;</span> T21: harpoon",
            "display": "T21"
        },
        {
            "id": "T21v",
            "text": "T21V: harpoon",
            "html": "<img src=\"/Search/Image?key=T21V\" alt=\"T21V\" style=\"max-height:24px; max-width: 28px;\" /> T21V: harpoon",
            "display": "T21v"
        },
        {
            "id": "T22",
            "text": "T22: arrowhead [tall] [sn]",
            "html": "<span class=\"uni\">&#x13322;</span> T22: arrowhead",
            "display": "T22"
        },
        {
            "id": "T22d",
            "text": "T22D: arrowhead",
            "html": "<img src=\"/Search/Image?key=T22D\" alt=\"T22D\" style=\"max-height:24px; max-width: 28px;\" /> T22D: arrowhead",
            "display": "T22d"
        },
        {
            "id": "T23",
            "text": "T23: arrowhead [tall]",
            "html": "<span class=\"uni\">&#x13323;</span> T23: arrowhead",
            "display": "T23"
        },
        {
            "id": "T24",
            "text": "T24: fishing-net [iH]",
            "html": "<span class=\"uni\">&#x13324;</span> T24: fishing-net",
            "display": "T24"
        },
        {
            "id": "T24c",
            "text": "T24C: fishing-net",
            "html": "<img src=\"/Search/Image?key=T24C\" alt=\"T24C\" style=\"max-height:24px; max-width: 28px;\" /> T24C: fishing-net",
            "display": "T24c"
        },
        {
            "id": "T24d",
            "text": "T24D: fishing-net",
            "html": "<img src=\"/Search/Image?key=T24D\" alt=\"T24D\" style=\"max-height:24px; max-width: 28px;\" /> T24D: fishing-net",
            "display": "T24d"
        },
        {
            "id": "T24e",
            "text": "T24E: fishing-net",
            "html": "<img src=\"/Search/Image?key=T24E\" alt=\"T24E\" style=\"max-height:24px; max-width: 28px;\" /> T24E: fishing-net",
            "display": "T24e"
        },
        {
            "id": "T25",
            "text": "T25: floats [DbA]",
            "html": "<span class=\"uni\">&#x13325;</span> T25: floats",
            "display": "T25"
        },
        {
            "id": "T26",
            "text": "T26: bird-trap",
            "html": "<span class=\"uni\">&#x13326;</span> T26: bird-trap",
            "display": "T26"
        },
        {
            "id": "T26f",
            "text": "T26F: bird-trap",
            "html": "<img src=\"/Search/Image?key=T26F\" alt=\"T26F\" style=\"max-height:24px; max-width: 28px;\" /> T26F: bird-trap",
            "display": "T26f"
        },
        {
            "id": "T26h",
            "text": "T26H: bird-trap",
            "html": "<img src=\"/Search/Image?key=T26H\" alt=\"T26H\" style=\"max-height:24px; max-width: 28px;\" /> T26H: bird-trap",
            "display": "T26h"
        },
        {
            "id": "T27",
            "text": "T27: bird-trap",
            "html": "<span class=\"uni\">&#x13327;</span> T27: bird-trap",
            "display": "T27"
        },
        {
            "id": "T28",
            "text": "T28: butcher&amp;apos;s block [narrow] [Xr]",
            "html": "<span class=\"uni\">&#x13328;</span> T28: butcher&amp;apos;s block",
            "display": "T28"
        },
        {
            "id": "T28a",
            "text": "T28A: butcher&amp;apos;s block",
            "html": "<img src=\"/Search/Image?key=T28A\" alt=\"T28A\" style=\"max-height:24px; max-width: 28px;\" /> T28A: butcher&amp;apos;s block",
            "display": "T28a"
        },
        {
            "id": "T29",
            "text": "T29: combination of T30 and T28 [nmt]",
            "html": "<span class=\"uni\">&#x13329;</span> T29: combination of T30 and T28",
            "display": "T29"
        },
        {
            "id": "T29c",
            "text": "T29C: combination of T30 and T28",
            "html": "<img src=\"/Search/Image?key=T29C\" alt=\"T29C\" style=\"max-height:24px; max-width: 28px;\" /> T29C: combination of T30 and T28",
            "display": "T29c"
        },
        {
            "id": "T3",
            "text": "T3: mace with round head vertically [tall] [HD]",
            "html": "<span class=\"uni\">&#x13309;</span> T3: mace with round head vertically",
            "display": "T3"
        },
        {
            "id": "T30",
            "text": "T30: knife [broad]",
            "html": "<span class=\"uni\">&#x1332A;</span> T30: knife",
            "display": "T30"
        },
        {
            "id": "T30a",
            "text": "T30A: knife",
            "html": "<img src=\"/Search/Image?key=T30A\" alt=\"T30A\" style=\"max-height:24px; max-width: 28px;\" /> T30A: knife",
            "display": "T30a"
        },
        {
            "id": "T30b",
            "text": "T30B: knife",
            "html": "<img src=\"/Search/Image?key=T30B\" alt=\"T30B\" style=\"max-height:24px; max-width: 28px;\" /> T30B: knife",
            "display": "T30b"
        },
        {
            "id": "T30c",
            "text": "T30C: knife",
            "html": "<img src=\"/Search/Image?key=T30C\" alt=\"T30C\" style=\"max-height:24px; max-width: 28px;\" /> T30C: knife",
            "display": "T30c"
        },
        {
            "id": "T31",
            "text": "T31: knife-sharpener [broad] [sSm]",
            "html": "<span class=\"uni\">&#x1332B;</span> T31: knife-sharpener",
            "display": "T31"
        },
        {
            "id": "T32",
            "text": "T32: combination of T31 and D54",
            "html": "<span class=\"uni\">&#x1332C;</span> T32: combination of T31 and D54",
            "display": "T32"
        },
        {
            "id": "T33",
            "text": "T33: knife-sharpener of butcher [broad]",
            "html": "<span class=\"uni\">&#x1332E;</span> T33: knife-sharpener of butcher",
            "display": "T33"
        },
        {
            "id": "T34",
            "text": "T34: butcher&amp;apos;s knife [tall] [nm]",
            "html": "<span class=\"uni\">&#x13330;</span> T34: butcher&amp;apos;s knife",
            "display": "T34"
        },
        {
            "id": "T36",
            "text": "T36: shield",
            "html": "<span class=\"uni\">&#x13332;</span> T36: shield",
            "display": "T36"
        },
        {
            "id": "T3f",
            "text": "T3F: mace with round head vertically",
            "html": "<img src=\"/Search/Image?key=T3F\" alt=\"T3F\" style=\"max-height:24px; max-width: 28px;\" /> T3F: mace with round head vertically",
            "display": "T3f"
        },
        {
            "id": "T4",
            "text": "T4: mace with strap [tall]",
            "html": "<span class=\"uni\">&#x1330B;</span> T4: mace with strap",
            "display": "T4"
        },
        {
            "id": "T49",
            "text": "T49",
            "html": "<img src=\"/Search/Image?key=T49\" alt=\"T49\" style=\"max-height:24px; max-width: 28px;\" /> T49",
            "display": "T49"
        },
        {
            "id": "T5",
            "text": "T5: combination of T3 and I10",
            "html": "<span class=\"uni\">&#x1330C;</span> T5: combination of T3 and I10",
            "display": "T5"
        },
        {
            "id": "T51",
            "text": "T51",
            "html": "<img src=\"/Search/Image?key=T51\" alt=\"T51\" style=\"max-height:24px; max-width: 28px;\" /> T51",
            "display": "T51"
        },
        {
            "id": "T53",
            "text": "T53",
            "html": "<img src=\"/Search/Image?key=T53\" alt=\"T53\" style=\"max-height:24px; max-width: 28px;\" /> T53",
            "display": "T53"
        },
        {
            "id": "T55",
            "text": "T55",
            "html": "<img src=\"/Search/Image?key=T55\" alt=\"T55\" style=\"max-height:24px; max-width: 28px;\" /> T55",
            "display": "T55"
        },
        {
            "id": "T57",
            "text": "T57",
            "html": "<img src=\"/Search/Image?key=T57\" alt=\"T57\" style=\"max-height:24px; max-width: 28px;\" /> T57",
            "display": "T57"
        },
        {
            "id": "T6",
            "text": "T6: combination of T3 and two I10 [HDD]",
            "html": "<span class=\"uni\">&#x1330D;</span> T6: combination of T3 and two I10",
            "display": "T6"
        },
        {
            "id": "T62",
            "text": "T62",
            "html": "<img src=\"/Search/Image?key=T62\" alt=\"T62\" style=\"max-height:24px; max-width: 28px;\" /> T62",
            "display": "T62"
        },
        {
            "id": "T63c",
            "text": "T63C",
            "html": "<img src=\"/Search/Image?key=T63C\" alt=\"T63C\" style=\"max-height:24px; max-width: 28px;\" /> T63C",
            "display": "T63c"
        },
        {
            "id": "T65",
            "text": "T65",
            "html": "<img src=\"/Search/Image?key=T65\" alt=\"T65\" style=\"max-height:24px; max-width: 28px;\" /> T65",
            "display": "T65"
        },
        {
            "id": "T67",
            "text": "T67",
            "html": "<img src=\"/Search/Image?key=T67\" alt=\"T67\" style=\"max-height:24px; max-width: 28px;\" /> T67",
            "display": "T67"
        },
        {
            "id": "T69",
            "text": "T69",
            "html": "<img src=\"/Search/Image?key=T69\" alt=\"T69\" style=\"max-height:24px; max-width: 28px;\" /> T69",
            "display": "T69"
        },
        {
            "id": "T7",
            "text": "T7: axe [broad]",
            "html": "<span class=\"uni\">&#x1330E;</span> T7: axe",
            "display": "T7"
        },
        {
            "id": "T79",
            "text": "T79",
            "html": "<img src=\"/Search/Image?key=T79\" alt=\"T79\" style=\"max-height:24px; max-width: 28px;\" /> T79",
            "display": "T79"
        },
        {
            "id": "T7a",
            "text": "T7A: axe [tall]",
            "html": "<span class=\"uni\">&#x1330F;</span> T7A: axe",
            "display": "T7a"
        },
        {
            "id": "T7b",
            "text": "T7B: axe",
            "html": "<img src=\"/Search/Image?key=T7B\" alt=\"T7B\" style=\"max-height:24px; max-width: 28px;\" /> T7B: axe",
            "display": "T7b"
        },
        {
            "id": "T8",
            "text": "T8: dagger [tall]",
            "html": "<span class=\"uni\">&#x13310;</span> T8: dagger",
            "display": "T8"
        },
        {
            "id": "T80",
            "text": "T80",
            "html": "<img src=\"/Search/Image?key=T80\" alt=\"T80\" style=\"max-height:24px; max-width: 28px;\" /> T80",
            "display": "T80"
        },
        {
            "id": "T80a",
            "text": "T80A",
            "html": "<img src=\"/Search/Image?key=T80A\" alt=\"T80A\" style=\"max-height:24px; max-width: 28px;\" /> T80A",
            "display": "T80a"
        },
        {
            "id": "T80b",
            "text": "T80B",
            "html": "<img src=\"/Search/Image?key=T80B\" alt=\"T80B\" style=\"max-height:24px; max-width: 28px;\" /> T80B",
            "display": "T80b"
        },
        {
            "id": "T86",
            "text": "T86",
            "html": "<img src=\"/Search/Image?key=T86\" alt=\"T86\" style=\"max-height:24px; max-width: 28px;\" /> T86",
            "display": "T86"
        },
        {
            "id": "T87",
            "text": "T87",
            "html": "<img src=\"/Search/Image?key=T87\" alt=\"T87\" style=\"max-height:24px; max-width: 28px;\" /> T87",
            "display": "T87"
        },
        {
            "id": "T88",
            "text": "T88",
            "html": "<img src=\"/Search/Image?key=T88\" alt=\"T88\" style=\"max-height:24px; max-width: 28px;\" /> T88",
            "display": "T88"
        },
        {
            "id": "T89",
            "text": "T89",
            "html": "<img src=\"/Search/Image?key=T89\" alt=\"T89\" style=\"max-height:24px; max-width: 28px;\" /> T89",
            "display": "T89"
        },
        {
            "id": "T8a",
            "text": "T8A: dagger [tall]",
            "html": "<span class=\"uni\">&#x13311;</span> T8A: dagger",
            "display": "T8a"
        },
        {
            "id": "T9",
            "text": "T9: bow [broad] [pd]",
            "html": "<span class=\"uni\">&#x13312;</span> T9: bow",
            "display": "T9"
        },
        {
            "id": "T90",
            "text": "T90",
            "html": "<img src=\"/Search/Image?key=T90\" alt=\"T90\" style=\"max-height:24px; max-width: 28px;\" /> T90",
            "display": "T90"
        },
        {
            "id": "T91",
            "text": "T91",
            "html": "<img src=\"/Search/Image?key=T91\" alt=\"T91\" style=\"max-height:24px; max-width: 28px;\" /> T91",
            "display": "T91"
        },
        {
            "id": "T93",
            "text": "T93",
            "html": "<img src=\"/Search/Image?key=T93\" alt=\"T93\" style=\"max-height:24px; max-width: 28px;\" /> T93",
            "display": "T93"
        },
        {
            "id": "T9a",
            "text": "T9A: bow [broad]",
            "html": "<span class=\"uni\">&#x13313;</span> T9A: bow",
            "display": "T9a"
        },
        {
            "id": "T9c",
            "text": "T9C: bow",
            "html": "<img src=\"/Search/Image?key=T9C\" alt=\"T9C\" style=\"max-height:24px; max-width: 28px;\" /> T9C: bow",
            "display": "T9c"
        },
        {
            "id": "T9d",
            "text": "T9D: bow",
            "html": "<img src=\"/Search/Image?key=T9D\" alt=\"T9D\" style=\"max-height:24px; max-width: 28px;\" /> T9D: bow",
            "display": "T9d"
        },
        {
            "id": "U1",
            "text": "U1: sickle [mA]",
            "html": "<span class=\"uni\">&#x13333;</span> U1: sickle",
            "display": "U1"
        },
        {
            "id": "U10",
            "text": "U10: U9 beneath M33 [it]",
            "html": "<span class=\"uni\">&#x1333E;</span> U10: U9 beneath M33",
            "display": "U10"
        },
        {
            "id": "U103",
            "text": "U103",
            "html": "<img src=\"/Search/Image?key=U103\" alt=\"U103\" style=\"max-height:24px; max-width: 28px;\" /> U103",
            "display": "U103"
        },
        {
            "id": "U107",
            "text": "U107",
            "html": "<img src=\"/Search/Image?key=U107\" alt=\"U107\" style=\"max-height:24px; max-width: 28px;\" /> U107",
            "display": "U107"
        },
        {
            "id": "U108",
            "text": "U108",
            "html": "<img src=\"/Search/Image?key=U108\" alt=\"U108\" style=\"max-height:24px; max-width: 28px;\" /> U108",
            "display": "U108"
        },
        {
            "id": "U109",
            "text": "U109",
            "html": "<img src=\"/Search/Image?key=U109\" alt=\"U109\" style=\"max-height:24px; max-width: 28px;\" /> U109",
            "display": "U109"
        },
        {
            "id": "U10a",
            "text": "U10A: U9 beneath M33",
            "html": "<img src=\"/Search/Image?key=U10A\" alt=\"U10A\" style=\"max-height:24px; max-width: 28px;\" /> U10A: U9 beneath M33",
            "display": "U10a"
        },
        {
            "id": "U11",
            "text": "U11: combination of S38 and U9 [HqAt]",
            "html": "<span class=\"uni\">&#x1333F;</span> U11: combination of S38 and U9",
            "display": "U11"
        },
        {
            "id": "U112",
            "text": "U112",
            "html": "<img src=\"/Search/Image?key=U112\" alt=\"U112\" style=\"max-height:24px; max-width: 28px;\" /> U112",
            "display": "U112"
        },
        {
            "id": "U116",
            "text": "U116",
            "html": "<img src=\"/Search/Image?key=U116\" alt=\"U116\" style=\"max-height:24px; max-width: 28px;\" /> U116",
            "display": "U116"
        },
        {
            "id": "U12",
            "text": "U12: combination of D50 and U9",
            "html": "<span class=\"uni\">&#x13340;</span> U12: combination of D50 and U9",
            "display": "U12"
        },
        {
            "id": "U120",
            "text": "U120",
            "html": "U120",
            "display": "U120"
        },
        {
            "id": "U122",
            "text": "U122",
            "html": "<img src=\"/Search/Image?key=U122\" alt=\"U122\" style=\"max-height:24px; max-width: 28px;\" /> U122",
            "display": "U122"
        },
        {
            "id": "U13",
            "text": "U13: plough [Sna]",
            "html": "<span class=\"uni\">&#x13341;</span> U13: plough",
            "display": "U13"
        },
        {
            "id": "U14a",
            "text": "U14A: two joined branches",
            "html": "<img src=\"/Search/Image?key=U14A\" alt=\"U14A\" style=\"max-height:24px; max-width: 28px;\" /> U14A: two joined branches",
            "display": "U14a"
        },
        {
            "id": "U15",
            "text": "U15: sledge [broad] [tm]",
            "html": "<span class=\"uni\">&#x13343;</span> U15: sledge",
            "display": "U15"
        },
        {
            "id": "U16",
            "text": "U16: sledge with head of jackal [broad] [biA]",
            "html": "<span class=\"uni\">&#x13344;</span> U16: sledge with head of jackal",
            "display": "U16"
        },
        {
            "id": "U16a",
            "text": "U16A: sledge with head of jackal",
            "html": "<img src=\"/Search/Image?key=U16A\" alt=\"U16A\" style=\"max-height:24px; max-width: 28px;\" /> U16A: sledge with head of jackal",
            "display": "U16a"
        },
        {
            "id": "U16b",
            "text": "U16B: sledge with head of jackal",
            "html": "<img src=\"/Search/Image?key=U16B\" alt=\"U16B\" style=\"max-height:24px; max-width: 28px;\" /> U16B: sledge with head of jackal",
            "display": "U16b"
        },
        {
            "id": "U17",
            "text": "U17: pick in ground [broad] [grg]",
            "html": "<span class=\"uni\">&#x13345;</span> U17: pick in ground",
            "display": "U17"
        },
        {
            "id": "U18",
            "text": "U18: pick in basin [broad]",
            "html": "<span class=\"uni\">&#x13346;</span> U18: pick in basin",
            "display": "U18"
        },
        {
            "id": "U19",
            "text": "U19: adze [broad]",
            "html": "<span class=\"uni\">&#x13347;</span> U19: adze",
            "display": "U19"
        },
        {
            "id": "U19a",
            "text": "U19A: adze",
            "html": "<img src=\"/Search/Image?key=U19A\" alt=\"U19A\" style=\"max-height:24px; max-width: 28px;\" /> U19A: adze",
            "display": "U19a"
        },
        {
            "id": "U1a",
            "text": "U1A: sickle",
            "html": "<img src=\"/Search/Image?key=U1A\" alt=\"U1A\" style=\"max-height:24px; max-width: 28px;\" /> U1A: sickle",
            "display": "U1a"
        },
        {
            "id": "U1b",
            "text": "U1B: sickle",
            "html": "<img src=\"/Search/Image?key=U1B\" alt=\"U1B\" style=\"max-height:24px; max-width: 28px;\" /> U1B: sickle",
            "display": "U1b"
        },
        {
            "id": "U2",
            "text": "U2: sickle (low)",
            "html": "<span class=\"uni\">&#x13334;</span> U2: sickle (low)",
            "display": "U2"
        },
        {
            "id": "U20",
            "text": "U20: adze [broad]",
            "html": "<span class=\"uni\">&#x13348;</span> U20: adze",
            "display": "U20"
        },
        {
            "id": "U21",
            "text": "U21: adze on wood [broad] [stp]",
            "html": "<span class=\"uni\">&#x13349;</span> U21: adze on wood",
            "display": "U21"
        },
        {
            "id": "U21a",
            "text": "U21A: adze on wood",
            "html": "<img src=\"/Search/Image?key=U21A\" alt=\"U21A\" style=\"max-height:24px; max-width: 28px;\" /> U21A: adze on wood",
            "display": "U21a"
        },
        {
            "id": "U22",
            "text": "U22: chisel [mnx]",
            "html": "<span class=\"uni\">&#x1334A;</span> U22: chisel",
            "display": "U22"
        },
        {
            "id": "U23",
            "text": "U23: chisel [tall] [Ab]",
            "html": "<span class=\"uni\">&#x1334B;</span> U23: chisel",
            "display": "U23"
        },
        {
            "id": "U24",
            "text": "U24: drill for stone [tall] [Hmt]",
            "html": "<span class=\"uni\">&#x1334D;</span> U24: drill for stone",
            "display": "U24"
        },
        {
            "id": "U25",
            "text": "U25: drill for stone [tall]",
            "html": "<span class=\"uni\">&#x1334E;</span> U25: drill for stone",
            "display": "U25"
        },
        {
            "id": "U26",
            "text": "U26: drill for beads [tall] [wbA]",
            "html": "<span class=\"uni\">&#x1334F;</span> U26: drill for beads",
            "display": "U26"
        },
        {
            "id": "U27",
            "text": "U27: drill for beads [tall]",
            "html": "<span class=\"uni\">&#x13350;</span> U27: drill for beads",
            "display": "U27"
        },
        {
            "id": "U28",
            "text": "U28: fire-drill [tall] [DA]",
            "html": "<span class=\"uni\">&#x13351;</span> U28: fire-drill",
            "display": "U28"
        },
        {
            "id": "U29",
            "text": "U29: fire-drill [tall]",
            "html": "<span class=\"uni\">&#x13352;</span> U29: fire-drill",
            "display": "U29"
        },
        {
            "id": "U29a",
            "text": "U29A: fire-drill with string",
            "html": "<span class=\"uni\">&#x13353;</span> U29A: fire-drill with string",
            "display": "U29a"
        },
        {
            "id": "U3",
            "text": "U3: combination of U1 and D4",
            "html": "<span class=\"uni\">&#x13335;</span> U3: combination of U1 and D4",
            "display": "U3"
        },
        {
            "id": "U30",
            "text": "U30: kiln [narrow]",
            "html": "<span class=\"uni\">&#x13354;</span> U30: kiln",
            "display": "U30"
        },
        {
            "id": "U31",
            "text": "U31: baker&amp;apos;s rake [broad] [rtH]",
            "html": "<span class=\"uni\">&#x13355;</span> U31: baker&amp;apos;s rake",
            "display": "U31"
        },
        {
            "id": "U32",
            "text": "U32: pestle and mortar [tall] [zmn]",
            "html": "<span class=\"uni\">&#x13356;</span> U32: pestle and mortar",
            "display": "U32"
        },
        {
            "id": "U32b",
            "text": "U32B: pestle and mortar",
            "html": "<img src=\"/Search/Image?key=U32B\" alt=\"U32B\" style=\"max-height:24px; max-width: 28px;\" /> U32B: pestle and mortar",
            "display": "U32b"
        },
        {
            "id": "U33",
            "text": "U33: pestle [tall] [ti]",
            "html": "<span class=\"uni\">&#x13358;</span> U33: pestle",
            "display": "U33"
        },
        {
            "id": "U34",
            "text": "U34: spindle [tall] [xsf]",
            "html": "<span class=\"uni\">&#x13359;</span> U34: spindle",
            "display": "U34"
        },
        {
            "id": "U35",
            "text": "U35: combination of U34 and I9",
            "html": "<span class=\"uni\">&#x1335A;</span> U35: combination of U34 and I9",
            "display": "U35"
        },
        {
            "id": "U36",
            "text": "U36: club [tall] [Hm]",
            "html": "<span class=\"uni\">&#x1335B;</span> U36: club",
            "display": "U36"
        },
        {
            "id": "U37",
            "text": "U37: razor",
            "html": "<span class=\"uni\">&#x1335C;</span> U37: razor",
            "display": "U37"
        },
        {
            "id": "U38",
            "text": "U38: balance [mxAt]",
            "html": "<span class=\"uni\">&#x1335D;</span> U38: balance",
            "display": "U38"
        },
        {
            "id": "U38a",
            "text": "U38A: balance",
            "html": "<img src=\"/Search/Image?key=U38A\" alt=\"U38A\" style=\"max-height:24px; max-width: 28px;\" /> U38A: balance",
            "display": "U38a"
        },
        {
            "id": "U38b",
            "text": "U38B: balance",
            "html": "<img src=\"/Search/Image?key=U38B\" alt=\"U38B\" style=\"max-height:24px; max-width: 28px;\" /> U38B: balance",
            "display": "U38b"
        },
        {
            "id": "U39",
            "text": "U39: post of balance [tall]",
            "html": "<span class=\"uni\">&#x1335E;</span> U39: post of balance",
            "display": "U39"
        },
        {
            "id": "U39a",
            "text": "U39A: post of balance",
            "html": "<img src=\"/Search/Image?key=U39A\" alt=\"U39A\" style=\"max-height:24px; max-width: 28px;\" /> U39A: post of balance",
            "display": "U39a"
        },
        {
            "id": "U39b",
            "text": "U39B: post of balance",
            "html": "<img src=\"/Search/Image?key=U39B\" alt=\"U39B\" style=\"max-height:24px; max-width: 28px;\" /> U39B: post of balance",
            "display": "U39b"
        },
        {
            "id": "U39c",
            "text": "U39C: post of balance",
            "html": "<img src=\"/Search/Image?key=U39C\" alt=\"U39C\" style=\"max-height:24px; max-width: 28px;\" /> U39C: post of balance",
            "display": "U39c"
        },
        {
            "id": "U39d",
            "text": "U39D: post of balance",
            "html": "<img src=\"/Search/Image?key=U39D\" alt=\"U39D\" style=\"max-height:24px; max-width: 28px;\" /> U39D: post of balance",
            "display": "U39d"
        },
        {
            "id": "U39f",
            "text": "U39F: post of balance",
            "html": "<img src=\"/Search/Image?key=U39F\" alt=\"U39F\" style=\"max-height:24px; max-width: 28px;\" /> U39F: post of balance",
            "display": "U39f"
        },
        {
            "id": "U39i",
            "text": "U39I: post of balance",
            "html": "<img src=\"/Search/Image?key=U39I\" alt=\"U39I\" style=\"max-height:24px; max-width: 28px;\" /> U39I: post of balance",
            "display": "U39i"
        },
        {
            "id": "U39k",
            "text": "U39K: post of balance",
            "html": "<img src=\"/Search/Image?key=U39K\" alt=\"U39K\" style=\"max-height:24px; max-width: 28px;\" /> U39K: post of balance",
            "display": "U39k"
        },
        {
            "id": "U39q",
            "text": "U39Q: post of balance",
            "html": "<img src=\"/Search/Image?key=U39Q\" alt=\"U39Q\" style=\"max-height:24px; max-width: 28px;\" /> U39Q: post of balance",
            "display": "U39q"
        },
        {
            "id": "U4",
            "text": "U4: combination of U1 and <canvas class=\"res\">Aa11</canvas> Aa11",
            "html": "<span class=\"uni\">&#x13336;</span> U4: combination of U1 and <canvas class=\"res\">Aa11</canvas> Aa11",
            "display": "U4"
        },
        {
            "id": "U40",
            "text": "U40: hieratic post of balance",
            "html": "<span class=\"uni\">&#x1335F;</span> U40: hieratic post of balance",
            "display": "U40"
        },
        {
            "id": "U43",
            "text": "U43",
            "html": "<img src=\"/Search/Image?key=U43\" alt=\"U43\" style=\"max-height:24px; max-width: 28px;\" /> U43",
            "display": "U43"
        },
        {
            "id": "U5",
            "text": "U5: combination of U2 and <canvas class=\"res\">Aa11</canvas> Aa11",
            "html": "<span class=\"uni\">&#x13337;</span> U5: combination of U2 and <canvas class=\"res\">Aa11</canvas> Aa11",
            "display": "U5"
        },
        {
            "id": "U50a",
            "text": "U50A",
            "html": "<img src=\"/Search/Image?key=U50A\" alt=\"U50A\" style=\"max-height:24px; max-width: 28px;\" /> U50A",
            "display": "U50a"
        },
        {
            "id": "U54a",
            "text": "U54A",
            "html": "<img src=\"/Search/Image?key=U54A\" alt=\"U54A\" style=\"max-height:24px; max-width: 28px;\" /> U54A",
            "display": "U54a"
        },
        {
            "id": "U58",
            "text": "U58",
            "html": "<img src=\"/Search/Image?key=U58\" alt=\"U58\" style=\"max-height:24px; max-width: 28px;\" /> U58",
            "display": "U58"
        },
        {
            "id": "U6",
            "text": "U6: diagonal hoe [mr]",
            "html": "<span class=\"uni\">&#x13338;</span> U6: diagonal hoe",
            "display": "U6"
        },
        {
            "id": "U63",
            "text": "U63",
            "html": "<img src=\"/Search/Image?key=U63\" alt=\"U63\" style=\"max-height:24px; max-width: 28px;\" /> U63",
            "display": "U63"
        },
        {
            "id": "U7",
            "text": "U7: horizontal hoe",
            "html": "<span class=\"uni\">&#x1333B;</span> U7: horizontal hoe",
            "display": "U7"
        },
        {
            "id": "U7a",
            "text": "U7A: horizontal hoe",
            "html": "<img src=\"/Search/Image?key=U7A\" alt=\"U7A\" style=\"max-height:24px; max-width: 28px;\" /> U7A: horizontal hoe",
            "display": "U7a"
        },
        {
            "id": "U8",
            "text": "U8: hoe without connecting rope",
            "html": "<span class=\"uni\">&#x1333C;</span> U8: hoe without connecting rope",
            "display": "U8"
        },
        {
            "id": "U89",
            "text": "U89",
            "html": "<img src=\"/Search/Image?key=U89\" alt=\"U89\" style=\"max-height:24px; max-width: 28px;\" /> U89",
            "display": "U89"
        },
        {
            "id": "U9",
            "text": "U9: grain-measure with grain",
            "html": "<span class=\"uni\">&#x1333D;</span> U9: grain-measure with grain",
            "display": "U9"
        },
        {
            "id": "U91",
            "text": "U91",
            "html": "<img src=\"/Search/Image?key=U91\" alt=\"U91\" style=\"max-height:24px; max-width: 28px;\" /> U91",
            "display": "U91"
        },
        {
            "id": "U92",
            "text": "U92",
            "html": "<img src=\"/Search/Image?key=U92\" alt=\"U92\" style=\"max-height:24px; max-width: 28px;\" /> U92",
            "display": "U92"
        },
        {
            "id": "U93",
            "text": "U93",
            "html": "<img src=\"/Search/Image?key=U93\" alt=\"U93\" style=\"max-height:24px; max-width: 28px;\" /> U93",
            "display": "U93"
        },
        {
            "id": "U97",
            "text": "U97",
            "html": "<img src=\"/Search/Image?key=U97\" alt=\"U97\" style=\"max-height:24px; max-width: 28px;\" /> U97",
            "display": "U97"
        },
        {
            "id": "U97b",
            "text": "U97B",
            "html": "<img src=\"/Search/Image?key=U97B\" alt=\"U97B\" style=\"max-height:24px; max-width: 28px;\" /> U97B",
            "display": "U97b"
        },
        {
            "id": "V1",
            "text": "V1: coil of rope [narrow] [100]",
            "html": "<span class=\"uni\">&#x13362;</span> V1: coil of rope",
            "display": "V1"
        },
        {
            "id": "V10",
            "text": "V10: oval cartouche",
            "html": "<span class=\"uni\">&#x13377;</span> V10: oval cartouche",
            "display": "V10"
        },
        {
            "id": "V102",
            "text": "V102",
            "html": "<img src=\"/Search/Image?key=V102\" alt=\"V102\" style=\"max-height:24px; max-width: 28px;\" /> V102",
            "display": "V102"
        },
        {
            "id": "V11",
            "text": "V11: end of cartouche",
            "html": "<span class=\"uni\">&#x13378;</span> V11: end of cartouche",
            "display": "V11"
        },
        {
            "id": "V110",
            "text": "V110",
            "html": "<img src=\"/Search/Image?key=V110\" alt=\"V110\" style=\"max-height:24px; max-width: 28px;\" /> V110",
            "display": "V110"
        },
        {
            "id": "V11a",
            "text": "V11A: opening of cartouche",
            "html": "<span class=\"uni\">&#x13379;</span> V11A: opening of cartouche",
            "display": "V11a"
        },
        {
            "id": "V12",
            "text": "V12: string [arq]",
            "html": "<span class=\"uni\">&#x1337C;</span> V12: string",
            "display": "V12"
        },
        {
            "id": "V13",
            "text": "V13: rope [broad] [T]",
            "html": "<span class=\"uni\">&#x1337F;</span> V13: rope",
            "display": "V13"
        },
        {
            "id": "V139",
            "text": "V139",
            "html": "<img src=\"/Search/Image?key=V139\" alt=\"V139\" style=\"max-height:24px; max-width: 28px;\" /> V139",
            "display": "V139"
        },
        {
            "id": "V14",
            "text": "V14: rope with tick [broad]",
            "html": "<span class=\"uni\">&#x13380;</span> V14: rope with tick",
            "display": "V14"
        },
        {
            "id": "V15",
            "text": "V15: combination of V13 and D54 [iTi]",
            "html": "<span class=\"uni\">&#x13381;</span> V15: combination of V13 and D54",
            "display": "V15"
        },
        {
            "id": "V16",
            "text": "V16: looped cord [broad]",
            "html": "<span class=\"uni\">&#x13382;</span> V16: looped cord",
            "display": "V16"
        },
        {
            "id": "V17",
            "text": "V17: shelter of papyrus [tall]",
            "html": "<span class=\"uni\">&#x13383;</span> V17: shelter of papyrus",
            "display": "V17"
        },
        {
            "id": "V19",
            "text": "V19: hobble with cross-bar [narrow] [TmA]",
            "html": "<span class=\"uni\">&#x13385;</span> V19: hobble with cross-bar",
            "display": "V19"
        },
        {
            "id": "V2",
            "text": "V2: combination of O34 and V1 [broad] [sTA]",
            "html": "<span class=\"uni\">&#x1336C;</span> V2: combination of O34 and V1",
            "display": "V2"
        },
        {
            "id": "V20",
            "text": "V20: hobble [narrow] [mD]",
            "html": "<span class=\"uni\">&#x13386;</span> V20: hobble",
            "display": "V20"
        },
        {
            "id": "V21",
            "text": "V21: combination of V20 and I10",
            "html": "<span class=\"uni\">&#x13393;</span> V21: combination of V20 and I10",
            "display": "V21"
        },
        {
            "id": "V21a",
            "text": "V21A: combination of V20 and I10",
            "html": "<img src=\"/Search/Image?key=V21A\" alt=\"V21A\" style=\"max-height:24px; max-width: 28px;\" /> V21A: combination of V20 and I10",
            "display": "V21a"
        },
        {
            "id": "V22",
            "text": "V22: whip [broad] [mH]",
            "html": "<span class=\"uni\">&#x13394;</span> V22: whip",
            "display": "V22"
        },
        {
            "id": "V24",
            "text": "V24: cord on stick [tall] [wD]",
            "html": "<span class=\"uni\">&#x13397;</span> V24: cord on stick",
            "display": "V24"
        },
        {
            "id": "V25",
            "text": "V25: cord on stick with tick [tall]",
            "html": "<span class=\"uni\">&#x13398;</span> V25: cord on stick with tick",
            "display": "V25"
        },
        {
            "id": "V26",
            "text": "V26: netting needle [broad] [aD]",
            "html": "<span class=\"uni\">&#x13399;</span> V26: netting needle",
            "display": "V26"
        },
        {
            "id": "V26a",
            "text": "V26A: netting needle",
            "html": "<img src=\"/Search/Image?key=V26A\" alt=\"V26A\" style=\"max-height:24px; max-width: 28px;\" /> V26A: netting needle",
            "display": "V26a"
        },
        {
            "id": "V27",
            "text": "V27: netting needle [broad]",
            "html": "<span class=\"uni\">&#x1339A;</span> V27: netting needle",
            "display": "V27"
        },
        {
            "id": "V27b",
            "text": "V27B: netting needle",
            "html": "<img src=\"/Search/Image?key=V27B\" alt=\"V27B\" style=\"max-height:24px; max-width: 28px;\" /> V27B: netting needle",
            "display": "V27b"
        },
        {
            "id": "V28",
            "text": "V28: wick [tall] [H]",
            "html": "<span class=\"uni\">&#x1339B;</span> V28: wick",
            "display": "V28"
        },
        {
            "id": "V28a",
            "text": "V28A: combination of V28 and D36",
            "html": "<span class=\"uni\">&#x1339C;</span> V28A: combination of V28 and D36",
            "display": "V28a"
        },
        {
            "id": "V28c",
            "text": "V28C: wick",
            "html": "<img src=\"/Search/Image?key=V28C\" alt=\"V28C\" style=\"max-height:24px; max-width: 28px;\" /> V28C: wick",
            "display": "V28c"
        },
        {
            "id": "V29",
            "text": "V29: swab [tall] [sk]",
            "html": "<span class=\"uni\">&#x1339D;</span> V29: swab",
            "display": "V29"
        },
        {
            "id": "V30",
            "text": "V30: basket [broad] [nb]",
            "html": "<span class=\"uni\">&#x1339F;</span> V30: basket",
            "display": "V30"
        },
        {
            "id": "V31",
            "text": "V31: basket with right handle [broad] [k]",
            "html": "<span class=\"uni\">&#x133A1;</span> V31: basket with right handle",
            "display": "V31"
        },
        {
            "id": "V31a",
            "text": "V31A: basket with left handle",
            "html": "<span class=\"uni\">&#x133A2;</span> V31A: basket with left handle",
            "display": "V31a"
        },
        {
            "id": "V32",
            "text": "V32: frail [broad] [msn]",
            "html": "<span class=\"uni\">&#x133A3;</span> V32: frail",
            "display": "V32"
        },
        {
            "id": "V33",
            "text": "V33: bag [narrow] [sSr]",
            "html": "<span class=\"uni\">&#x133A4;</span> V33: bag",
            "display": "V33"
        },
        {
            "id": "V35",
            "text": "V35: bag [narrow]",
            "html": "<span class=\"uni\">&#x133A7;</span> V35: bag",
            "display": "V35"
        },
        {
            "id": "V36",
            "text": "V36: receptacle [tall]",
            "html": "<span class=\"uni\">&#x133A8;</span> V36: receptacle",
            "display": "V36"
        },
        {
            "id": "V36g",
            "text": "V36G: receptacle",
            "html": "<img src=\"/Search/Image?key=V36G\" alt=\"V36G\" style=\"max-height:24px; max-width: 28px;\" /> V36G: receptacle",
            "display": "V36g"
        },
        {
            "id": "V37",
            "text": "V37: bandage [narrow] [idr]",
            "html": "<span class=\"uni\">&#x133A9;</span> V37: bandage",
            "display": "V37"
        },
        {
            "id": "V38",
            "text": "V38: bandage [tall]",
            "html": "<span class=\"uni\">&#x133AB;</span> V38: bandage",
            "display": "V38"
        },
        {
            "id": "V39",
            "text": "V39: knot-amulet [tall]",
            "html": "<span class=\"uni\">&#x133AC;</span> V39: knot-amulet",
            "display": "V39"
        },
        {
            "id": "V4",
            "text": "V4: lasso [wA]",
            "html": "<span class=\"uni\">&#x1336F;</span> V4: lasso",
            "display": "V4"
        },
        {
            "id": "V40",
            "text": "V40: hobble on its side",
            "html": "<span class=\"uni\">&#x133AD;</span> V40: hobble on its side",
            "display": "V40"
        },
        {
            "id": "V41",
            "text": "V41",
            "html": "<img src=\"/Search/Image?key=V41\" alt=\"V41\" style=\"max-height:24px; max-width: 28px;\" /> V41",
            "display": "V41"
        },
        {
            "id": "V42",
            "text": "V42",
            "html": "<img src=\"/Search/Image?key=V42\" alt=\"V42\" style=\"max-height:24px; max-width: 28px;\" /> V42",
            "display": "V42"
        },
        {
            "id": "V45",
            "text": "V45",
            "html": "<img src=\"/Search/Image?key=V45\" alt=\"V45\" style=\"max-height:24px; max-width: 28px;\" /> V45",
            "display": "V45"
        },
        {
            "id": "V48",
            "text": "V48",
            "html": "<img src=\"/Search/Image?key=V48\" alt=\"V48\" style=\"max-height:24px; max-width: 28px;\" /> V48",
            "display": "V48"
        },
        {
            "id": "V49",
            "text": "V49",
            "html": "<img src=\"/Search/Image?key=V49\" alt=\"V49\" style=\"max-height:24px; max-width: 28px;\" /> V49",
            "display": "V49"
        },
        {
            "id": "V49a",
            "text": "V49A",
            "html": "<img src=\"/Search/Image?key=V49A\" alt=\"V49A\" style=\"max-height:24px; max-width: 28px;\" /> V49A",
            "display": "V49a"
        },
        {
            "id": "V5",
            "text": "V5: looped rope [snT]",
            "html": "<span class=\"uni\">&#x13370;</span> V5: looped rope",
            "display": "V5"
        },
        {
            "id": "V50",
            "text": "V50",
            "html": "<img src=\"/Search/Image?key=V50\" alt=\"V50\" style=\"max-height:24px; max-width: 28px;\" /> V50",
            "display": "V50"
        },
        {
            "id": "V51",
            "text": "V51",
            "html": "<img src=\"/Search/Image?key=V51\" alt=\"V51\" style=\"max-height:24px; max-width: 28px;\" /> V51",
            "display": "V51"
        },
        {
            "id": "V5a",
            "text": "V5A: looped rope",
            "html": "<img src=\"/Search/Image?key=V5A\" alt=\"V5A\" style=\"max-height:24px; max-width: 28px;\" /> V5A: looped rope",
            "display": "V5a"
        },
        {
            "id": "V6",
            "text": "V6: cord with ends upward [narrow] [Ss]",
            "html": "<span class=\"uni\">&#x13371;</span> V6: cord with ends upward",
            "display": "V6"
        },
        {
            "id": "V60",
            "text": "V60",
            "html": "<img src=\"/Search/Image?key=V60\" alt=\"V60\" style=\"max-height:24px; max-width: 28px;\" /> V60",
            "display": "V60"
        },
        {
            "id": "V65",
            "text": "V65",
            "html": "<img src=\"/Search/Image?key=V65\" alt=\"V65\" style=\"max-height:24px; max-width: 28px;\" /> V65",
            "display": "V65"
        },
        {
            "id": "V7",
            "text": "V7: cord with ends downward [narrow] [Sn]",
            "html": "<span class=\"uni\">&#x13372;</span> V7: cord with ends downward",
            "display": "V7"
        },
        {
            "id": "V71",
            "text": "V71",
            "html": "<img src=\"/Search/Image?key=V71\" alt=\"V71\" style=\"max-height:24px; max-width: 28px;\" /> V71",
            "display": "V71"
        },
        {
            "id": "V78",
            "text": "V78",
            "html": "<img src=\"/Search/Image?key=V78\" alt=\"V78\" style=\"max-height:24px; max-width: 28px;\" /> V78",
            "display": "V78"
        },
        {
            "id": "V8",
            "text": "V8: cord downward [narrow]",
            "html": "<span class=\"uni\">&#x13375;</span> V8: cord downward",
            "display": "V8"
        },
        {
            "id": "V81",
            "text": "V81",
            "html": "<img src=\"/Search/Image?key=V81\" alt=\"V81\" style=\"max-height:24px; max-width: 28px;\" /> V81",
            "display": "V81"
        },
        {
            "id": "V83",
            "text": "V83",
            "html": "<img src=\"/Search/Image?key=V83\" alt=\"V83\" style=\"max-height:24px; max-width: 28px;\" /> V83",
            "display": "V83"
        },
        {
            "id": "V84",
            "text": "V84",
            "html": "<img src=\"/Search/Image?key=V84\" alt=\"V84\" style=\"max-height:24px; max-width: 28px;\" /> V84",
            "display": "V84"
        },
        {
            "id": "V9",
            "text": "V9: round cartouche [narrow]",
            "html": "<span class=\"uni\">&#x13376;</span> V9: round cartouche",
            "display": "V9"
        },
        {
            "id": "V90",
            "text": "V90",
            "html": "<img src=\"/Search/Image?key=V90\" alt=\"V90\" style=\"max-height:24px; max-width: 28px;\" /> V90",
            "display": "V90"
        },
        {
            "id": "V96",
            "text": "V96",
            "html": "<img src=\"/Search/Image?key=V96\" alt=\"V96\" style=\"max-height:24px; max-width: 28px;\" /> V96",
            "display": "V96"
        },
        {
            "id": "V97",
            "text": "V97",
            "html": "<img src=\"/Search/Image?key=V97\" alt=\"V97\" style=\"max-height:24px; max-width: 28px;\" /> V97",
            "display": "V97"
        },
        {
            "id": "V98",
            "text": "V98",
            "html": "<img src=\"/Search/Image?key=V98\" alt=\"V98\" style=\"max-height:24px; max-width: 28px;\" /> V98",
            "display": "V98"
        },
        {
            "id": "V99",
            "text": "V99",
            "html": "<img src=\"/Search/Image?key=V99\" alt=\"V99\" style=\"max-height:24px; max-width: 28px;\" /> V99",
            "display": "V99"
        },
        {
            "id": "W1",
            "text": "W1: oil jar with ties",
            "html": "<span class=\"uni\">&#x133AF;</span> W1: oil jar with ties",
            "display": "W1"
        },
        {
            "id": "W10",
            "text": "W10: cup [narrow] [iab]",
            "html": "<span class=\"uni\">&#x133BA;</span> W10: cup",
            "display": "W10"
        },
        {
            "id": "W10a",
            "text": "W10A: pot with tick [narrow]",
            "html": "<span class=\"uni\">&#x133BB;</span> W10A: pot with tick",
            "display": "W10a"
        },
        {
            "id": "W10b",
            "text": "W10B: cup",
            "html": "<img src=\"/Search/Image?key=W10B\" alt=\"W10B\" style=\"max-height:24px; max-width: 28px;\" /> W10B: cup",
            "display": "W10b"
        },
        {
            "id": "W11",
            "text": "W11: round ring stand [narrow] [g]",
            "html": "<span class=\"uni\">&#x133BC;</span> W11: round ring stand",
            "display": "W11"
        },
        {
            "id": "W112a",
            "text": "W112A",
            "html": "<img src=\"/Search/Image?key=W112A\" alt=\"W112A\" style=\"max-height:24px; max-width: 28px;\" /> W112A",
            "display": "W112a"
        },
        {
            "id": "W113",
            "text": "W113",
            "html": "<img src=\"/Search/Image?key=W113\" alt=\"W113\" style=\"max-height:24px; max-width: 28px;\" /> W113",
            "display": "W113"
        },
        {
            "id": "W115",
            "text": "W115",
            "html": "<img src=\"/Search/Image?key=W115\" alt=\"W115\" style=\"max-height:24px; max-width: 28px;\" /> W115",
            "display": "W115"
        },
        {
            "id": "W12",
            "text": "W12: square ring stand [narrow]",
            "html": "<span class=\"uni\">&#x133BD;</span> W12: square ring stand",
            "display": "W12"
        },
        {
            "id": "W121",
            "text": "W121",
            "html": "<img src=\"/Search/Image?key=W121\" alt=\"W121\" style=\"max-height:24px; max-width: 28px;\" /> W121",
            "display": "W121"
        },
        {
            "id": "W122",
            "text": "W122",
            "html": "<img src=\"/Search/Image?key=W122\" alt=\"W122\" style=\"max-height:24px; max-width: 28px;\" /> W122",
            "display": "W122"
        },
        {
            "id": "W125",
            "text": "W125",
            "html": "<img src=\"/Search/Image?key=W125\" alt=\"W125\" style=\"max-height:24px; max-width: 28px;\" /> W125",
            "display": "W125"
        },
        {
            "id": "W13",
            "text": "W13: earthenware pot [narrow]",
            "html": "<span class=\"uni\">&#x133BE;</span> W13: earthenware pot",
            "display": "W13"
        },
        {
            "id": "W14",
            "text": "W14: water jar [Hz]",
            "html": "<span class=\"uni\">&#x133BF;</span> W14: water jar",
            "display": "W14"
        },
        {
            "id": "W14a",
            "text": "W14A: combination of V28, W14 and O34",
            "html": "<span class=\"uni\">&#x133C0;</span> W14A: combination of V28, W14 and O34",
            "display": "W14a"
        },
        {
            "id": "W15",
            "text": "W15: water jar with water",
            "html": "<span class=\"uni\">&#x133C1;</span> W15: water jar with water",
            "display": "W15"
        },
        {
            "id": "W15a",
            "text": "W15A: water jar with water",
            "html": "<img src=\"/Search/Image?key=W15A\" alt=\"W15A\" style=\"max-height:24px; max-width: 28px;\" /> W15A: water jar with water",
            "display": "W15a"
        },
        {
            "id": "W15b",
            "text": "W15B: water jar with water",
            "html": "<img src=\"/Search/Image?key=W15B\" alt=\"W15B\" style=\"max-height:24px; max-width: 28px;\" /> W15B: water jar with water",
            "display": "W15b"
        },
        {
            "id": "W16",
            "text": "W16: water jar with water in ring stand",
            "html": "<span class=\"uni\">&#x133C2;</span> W16: water jar with water in ring stand",
            "display": "W16"
        },
        {
            "id": "W17",
            "text": "W17: three water jars in rack [xnt]",
            "html": "<span class=\"uni\">&#x133C3;</span> W17: three water jars in rack",
            "display": "W17"
        },
        {
            "id": "W17a",
            "text": "W17A: three water jars in rack (simplified)",
            "html": "<span class=\"uni\">&#x133C4;</span> W17A: three water jars in rack (simplified)",
            "display": "W17a"
        },
        {
            "id": "W17c",
            "text": "W17C: three water jars in rack",
            "html": "<img src=\"/Search/Image?key=W17C\" alt=\"W17C\" style=\"max-height:24px; max-width: 28px;\" /> W17C: three water jars in rack",
            "display": "W17c"
        },
        {
            "id": "W17d",
            "text": "W17D: three water jars in rack",
            "html": "<img src=\"/Search/Image?key=W17D\" alt=\"W17D\" style=\"max-height:24px; max-width: 28px;\" /> W17D: three water jars in rack",
            "display": "W17d"
        },
        {
            "id": "W18",
            "text": "W18: four water jars in rack",
            "html": "<span class=\"uni\">&#x133C5;</span> W18: four water jars in rack",
            "display": "W18"
        },
        {
            "id": "W19",
            "text": "W19: milk jug in net [tall] [mi]",
            "html": "<span class=\"uni\">&#x133C7;</span> W19: milk jug in net",
            "display": "W19"
        },
        {
            "id": "W1b",
            "text": "W1B: oil jar with ties",
            "html": "<img src=\"/Search/Image?key=W1B\" alt=\"W1B\" style=\"max-height:24px; max-width: 28px;\" /> W1B: oil jar with ties",
            "display": "W1b"
        },
        {
            "id": "W2",
            "text": "W2: oil jar [bAs]",
            "html": "<span class=\"uni\">&#x133B0;</span> W2: oil jar",
            "display": "W2"
        },
        {
            "id": "W20",
            "text": "W20: milk jug with leaf [narrow]",
            "html": "<span class=\"uni\">&#x133C8;</span> W20: milk jug with leaf",
            "display": "W20"
        },
        {
            "id": "W21",
            "text": "W21: twin wine jars [narrow]",
            "html": "<span class=\"uni\">&#x133C9;</span> W21: twin wine jars",
            "display": "W21"
        },
        {
            "id": "W21a",
            "text": "W21A: twin wine jars",
            "html": "<img src=\"/Search/Image?key=W21A\" alt=\"W21A\" style=\"max-height:24px; max-width: 28px;\" /> W21A: twin wine jars",
            "display": "W21a"
        },
        {
            "id": "W22",
            "text": "W22: beer jug [Hnqt]",
            "html": "<span class=\"uni\">&#x133CA;</span> W22: beer jug",
            "display": "W22"
        },
        {
            "id": "W23",
            "text": "W23: jar with handles",
            "html": "<span class=\"uni\">&#x133CB;</span> W23: jar with handles",
            "display": "W23"
        },
        {
            "id": "W24",
            "text": "W24: bowl [nw]",
            "html": "<span class=\"uni\">&#x133CC;</span> W24: bowl",
            "display": "W24"
        },
        {
            "id": "W25",
            "text": "W25: combination of W24 and D54 [ini]",
            "html": "<span class=\"uni\">&#x133CE;</span> W25: combination of W24 and D54",
            "display": "W25"
        },
        {
            "id": "W27b",
            "text": "W27B",
            "html": "<img src=\"/Search/Image?key=W27B\" alt=\"W27B\" style=\"max-height:24px; max-width: 28px;\" /> W27B",
            "display": "W27b"
        },
        {
            "id": "W29",
            "text": "W29",
            "html": "<img src=\"/Search/Image?key=W29\" alt=\"W29\" style=\"max-height:24px; max-width: 28px;\" /> W29",
            "display": "W29"
        },
        {
            "id": "W2b",
            "text": "W2B: oil jar",
            "html": "<img src=\"/Search/Image?key=W2B\" alt=\"W2B\" style=\"max-height:24px; max-width: 28px;\" /> W2B: oil jar",
            "display": "W2b"
        },
        {
            "id": "W3",
            "text": "W3: alabaster basin [broad] [Hb]",
            "html": "<span class=\"uni\">&#x133B1;</span> W3: alabaster basin",
            "display": "W3"
        },
        {
            "id": "W30",
            "text": "W30",
            "html": "<img src=\"/Search/Image?key=W30\" alt=\"W30\" style=\"max-height:24px; max-width: 28px;\" /> W30",
            "display": "W30"
        },
        {
            "id": "W31",
            "text": "W31",
            "html": "<img src=\"/Search/Image?key=W31\" alt=\"W31\" style=\"max-height:24px; max-width: 28px;\" /> W31",
            "display": "W31"
        },
        {
            "id": "W33",
            "text": "W33",
            "html": "<img src=\"/Search/Image?key=W33\" alt=\"W33\" style=\"max-height:24px; max-width: 28px;\" /> W33",
            "display": "W33"
        },
        {
            "id": "W37d",
            "text": "W37D",
            "html": "<img src=\"/Search/Image?key=W37D\" alt=\"W37D\" style=\"max-height:24px; max-width: 28px;\" /> W37D",
            "display": "W37d"
        },
        {
            "id": "W4",
            "text": "W4: combination of O22 and W3",
            "html": "<span class=\"uni\">&#x133B3;</span> W4: combination of O22 and W3",
            "display": "W4"
        },
        {
            "id": "W40",
            "text": "W40",
            "html": "<img src=\"/Search/Image?key=W40\" alt=\"W40\" style=\"max-height:24px; max-width: 28px;\" /> W40",
            "display": "W40"
        },
        {
            "id": "W45",
            "text": "W45",
            "html": "<img src=\"/Search/Image?key=W45\" alt=\"W45\" style=\"max-height:24px; max-width: 28px;\" /> W45",
            "display": "W45"
        },
        {
            "id": "W4a",
            "text": "W4A: combination of O22 and W3",
            "html": "<img src=\"/Search/Image?key=W4A\" alt=\"W4A\" style=\"max-height:24px; max-width: 28px;\" /> W4A: combination of O22 and W3",
            "display": "W4a"
        },
        {
            "id": "W5",
            "text": "W5: combination of T28 and W3",
            "html": "<span class=\"uni\">&#x133B4;</span> W5: combination of T28 and W3",
            "display": "W5"
        },
        {
            "id": "W54",
            "text": "W54",
            "html": "<img src=\"/Search/Image?key=W54\" alt=\"W54\" style=\"max-height:24px; max-width: 28px;\" /> W54",
            "display": "W54"
        },
        {
            "id": "W54a",
            "text": "W54A",
            "html": "<img src=\"/Search/Image?key=W54A\" alt=\"W54A\" style=\"max-height:24px; max-width: 28px;\" /> W54A",
            "display": "W54a"
        },
        {
            "id": "W56",
            "text": "W56",
            "html": "<img src=\"/Search/Image?key=W56\" alt=\"W56\" style=\"max-height:24px; max-width: 28px;\" /> W56",
            "display": "W56"
        },
        {
            "id": "W57",
            "text": "W57",
            "html": "<img src=\"/Search/Image?key=W57\" alt=\"W57\" style=\"max-height:24px; max-width: 28px;\" /> W57",
            "display": "W57"
        },
        {
            "id": "W59",
            "text": "W59",
            "html": "<img src=\"/Search/Image?key=W59\" alt=\"W59\" style=\"max-height:24px; max-width: 28px;\" /> W59",
            "display": "W59"
        },
        {
            "id": "W5a",
            "text": "W5A: combination of T28 and W3",
            "html": "<img src=\"/Search/Image?key=W5A\" alt=\"W5A\" style=\"max-height:24px; max-width: 28px;\" /> W5A: combination of T28 and W3",
            "display": "W5a"
        },
        {
            "id": "W6",
            "text": "W6: metal vessel [narrow]",
            "html": "<span class=\"uni\">&#x133B5;</span> W6: metal vessel",
            "display": "W6"
        },
        {
            "id": "W60",
            "text": "W60",
            "html": "<img src=\"/Search/Image?key=W60\" alt=\"W60\" style=\"max-height:24px; max-width: 28px;\" /> W60",
            "display": "W60"
        },
        {
            "id": "W61",
            "text": "W61",
            "html": "<img src=\"/Search/Image?key=W61\" alt=\"W61\" style=\"max-height:24px; max-width: 28px;\" /> W61",
            "display": "W61"
        },
        {
            "id": "W62",
            "text": "W62",
            "html": "<img src=\"/Search/Image?key=W62\" alt=\"W62\" style=\"max-height:24px; max-width: 28px;\" /> W62",
            "display": "W62"
        },
        {
            "id": "W64",
            "text": "W64",
            "html": "<img src=\"/Search/Image?key=W64\" alt=\"W64\" style=\"max-height:24px; max-width: 28px;\" /> W64",
            "display": "W64"
        },
        {
            "id": "W65",
            "text": "W65",
            "html": "<img src=\"/Search/Image?key=W65\" alt=\"W65\" style=\"max-height:24px; max-width: 28px;\" /> W65",
            "display": "W65"
        },
        {
            "id": "W66",
            "text": "W66",
            "html": "<img src=\"/Search/Image?key=W66\" alt=\"W66\" style=\"max-height:24px; max-width: 28px;\" /> W66",
            "display": "W66"
        },
        {
            "id": "W67",
            "text": "W67",
            "html": "<img src=\"/Search/Image?key=W67\" alt=\"W67\" style=\"max-height:24px; max-width: 28px;\" /> W67",
            "display": "W67"
        },
        {
            "id": "W69",
            "text": "W69",
            "html": "<img src=\"/Search/Image?key=W69\" alt=\"W69\" style=\"max-height:24px; max-width: 28px;\" /> W69",
            "display": "W69"
        },
        {
            "id": "W6a",
            "text": "W6A: metal vessel",
            "html": "<img src=\"/Search/Image?key=W6A\" alt=\"W6A\" style=\"max-height:24px; max-width: 28px;\" /> W6A: metal vessel",
            "display": "W6a"
        },
        {
            "id": "W7",
            "text": "W7: granite bowl [narrow]",
            "html": "<span class=\"uni\">&#x133B6;</span> W7: granite bowl",
            "display": "W7"
        },
        {
            "id": "W70",
            "text": "W70",
            "html": "<img src=\"/Search/Image?key=W70\" alt=\"W70\" style=\"max-height:24px; max-width: 28px;\" /> W70",
            "display": "W70"
        },
        {
            "id": "W72",
            "text": "W72",
            "html": "<img src=\"/Search/Image?key=W72\" alt=\"W72\" style=\"max-height:24px; max-width: 28px;\" /> W72",
            "display": "W72"
        },
        {
            "id": "W73",
            "text": "W73",
            "html": "<img src=\"/Search/Image?key=W73\" alt=\"W73\" style=\"max-height:24px; max-width: 28px;\" /> W73",
            "display": "W73"
        },
        {
            "id": "W76",
            "text": "W76",
            "html": "<img src=\"/Search/Image?key=W76\" alt=\"W76\" style=\"max-height:24px; max-width: 28px;\" /> W76",
            "display": "W76"
        },
        {
            "id": "W77",
            "text": "W77",
            "html": "<img src=\"/Search/Image?key=W77\" alt=\"W77\" style=\"max-height:24px; max-width: 28px;\" /> W77",
            "display": "W77"
        },
        {
            "id": "W78",
            "text": "W78",
            "html": "<img src=\"/Search/Image?key=W78\" alt=\"W78\" style=\"max-height:24px; max-width: 28px;\" /> W78",
            "display": "W78"
        },
        {
            "id": "W78a",
            "text": "W78A",
            "html": "<img src=\"/Search/Image?key=W78A\" alt=\"W78A\" style=\"max-height:24px; max-width: 28px;\" /> W78A",
            "display": "W78a"
        },
        {
            "id": "W79",
            "text": "W79",
            "html": "<img src=\"/Search/Image?key=W79\" alt=\"W79\" style=\"max-height:24px; max-width: 28px;\" /> W79",
            "display": "W79"
        },
        {
            "id": "W7a",
            "text": "W7A: granite bowl",
            "html": "<img src=\"/Search/Image?key=W7A\" alt=\"W7A\" style=\"max-height:24px; max-width: 28px;\" /> W7A: granite bowl",
            "display": "W7a"
        },
        {
            "id": "W8",
            "text": "W8: deformed granite bowl [broad]",
            "html": "<span class=\"uni\">&#x133B7;</span> W8: deformed granite bowl",
            "display": "W8"
        },
        {
            "id": "W81",
            "text": "W81",
            "html": "<img src=\"/Search/Image?key=W81\" alt=\"W81\" style=\"max-height:24px; max-width: 28px;\" /> W81",
            "display": "W81"
        },
        {
            "id": "W83",
            "text": "W83",
            "html": "<img src=\"/Search/Image?key=W83\" alt=\"W83\" style=\"max-height:24px; max-width: 28px;\" /> W83",
            "display": "W83"
        },
        {
            "id": "W85",
            "text": "W85",
            "html": "<img src=\"/Search/Image?key=W85\" alt=\"W85\" style=\"max-height:24px; max-width: 28px;\" /> W85",
            "display": "W85"
        },
        {
            "id": "W88",
            "text": "W88",
            "html": "<img src=\"/Search/Image?key=W88\" alt=\"W88\" style=\"max-height:24px; max-width: 28px;\" /> W88",
            "display": "W88"
        },
        {
            "id": "W89",
            "text": "W89",
            "html": "<img src=\"/Search/Image?key=W89\" alt=\"W89\" style=\"max-height:24px; max-width: 28px;\" /> W89",
            "display": "W89"
        },
        {
            "id": "W9",
            "text": "W9: jug with left handle [Xnm]",
            "html": "<span class=\"uni\">&#x133B8;</span> W9: jug with left handle",
            "display": "W9"
        },
        {
            "id": "W93",
            "text": "W93",
            "html": "<img src=\"/Search/Image?key=W93\" alt=\"W93\" style=\"max-height:24px; max-width: 28px;\" /> W93",
            "display": "W93"
        },
        {
            "id": "W97",
            "text": "W97",
            "html": "<img src=\"/Search/Image?key=W97\" alt=\"W97\" style=\"max-height:24px; max-width: 28px;\" /> W97",
            "display": "W97"
        },
        {
            "id": "W98",
            "text": "W98",
            "html": "<img src=\"/Search/Image?key=W98\" alt=\"W98\" style=\"max-height:24px; max-width: 28px;\" /> W98",
            "display": "W98"
        },
        {
            "id": "W9c",
            "text": "W9C: jug with left handle",
            "html": "<img src=\"/Search/Image?key=W9C\" alt=\"W9C\" style=\"max-height:24px; max-width: 28px;\" /> W9C: jug with left handle",
            "display": "W9c"
        },
        {
            "id": "X1",
            "text": "X1: flat loaf [narrow] [t]",
            "html": "<span class=\"uni\">&#x133CF;</span> X1: flat loaf",
            "display": "X1"
        },
        {
            "id": "X11",
            "text": "X11",
            "html": "<img src=\"/Search/Image?key=X11\" alt=\"X11\" style=\"max-height:24px; max-width: 28px;\" /> X11",
            "display": "X11"
        },
        {
            "id": "X2",
            "text": "X2: tall loaf [narrow]",
            "html": "<span class=\"uni\">&#x133D0;</span> X2: tall loaf",
            "display": "X2"
        },
        {
            "id": "X2d",
            "text": "X2D: tall loaf",
            "html": "<img src=\"/Search/Image?key=X2D\" alt=\"X2D\" style=\"max-height:24px; max-width: 28px;\" /> X2D: tall loaf",
            "display": "X2d"
        },
        {
            "id": "X3",
            "text": "X3: tall loaf [narrow]",
            "html": "<span class=\"uni\">&#x133D1;</span> X3: tall loaf",
            "display": "X3"
        },
        {
            "id": "X3a",
            "text": "X3A: tall loaf",
            "html": "<img src=\"/Search/Image?key=X3A\" alt=\"X3A\" style=\"max-height:24px; max-width: 28px;\" /> X3A: tall loaf",
            "display": "X3a"
        },
        {
            "id": "X4",
            "text": "X4: roll of bread [broad]",
            "html": "<span class=\"uni\">&#x133D2;</span> X4: roll of bread",
            "display": "X4"
        },
        {
            "id": "X4a",
            "text": "X4A: roll of bread",
            "html": "<span class=\"uni\">&#x133D3;</span> X4A: roll of bread",
            "display": "X4a"
        },
        {
            "id": "X4d",
            "text": "X4D: roll of bread",
            "html": "<img src=\"/Search/Image?key=X4D\" alt=\"X4D\" style=\"max-height:24px; max-width: 28px;\" /> X4D: roll of bread",
            "display": "X4d"
        },
        {
            "id": "X4e",
            "text": "X4E: roll of bread",
            "html": "<img src=\"/Search/Image?key=X4E\" alt=\"X4E\" style=\"max-height:24px; max-width: 28px;\" /> X4E: roll of bread",
            "display": "X4e"
        },
        {
            "id": "X4h",
            "text": "X4H: roll of bread",
            "html": "<img src=\"/Search/Image?key=X4H\" alt=\"X4H\" style=\"max-height:24px; max-width: 28px;\" /> X4H: roll of bread",
            "display": "X4h"
        },
        {
            "id": "X5",
            "text": "X5: hieratic roll of bread [broad]",
            "html": "<span class=\"uni\">&#x133D5;</span> X5: hieratic roll of bread",
            "display": "X5"
        },
        {
            "id": "X6",
            "text": "X6: round loaf [narrow]",
            "html": "<span class=\"uni\">&#x133D6;</span> X6: round loaf",
            "display": "X6"
        },
        {
            "id": "X6a",
            "text": "X6A: round loaf",
            "html": "<span class=\"uni\">&#x133D7;</span> X6A: round loaf",
            "display": "X6a"
        },
        {
            "id": "X6b",
            "text": "X6B: round loaf",
            "html": "<img src=\"/Search/Image?key=X6B\" alt=\"X6B\" style=\"max-height:24px; max-width: 28px;\" /> X6B: round loaf",
            "display": "X6b"
        },
        {
            "id": "X7",
            "text": "X7: half-loaf [narrow]",
            "html": "<span class=\"uni\">&#x133D8;</span> X7: half-loaf",
            "display": "X7"
        },
        {
            "id": "X8",
            "text": "X8: conical loaf [di]",
            "html": "<span class=\"uni\">&#x133D9;</span> X8: conical loaf",
            "display": "X8"
        },
        {
            "id": "Y1",
            "text": "Y1: scroll with ties [broad] [mDAt]",
            "html": "<span class=\"uni\">&#x133DB;</span> Y1: scroll with ties",
            "display": "Y1"
        },
        {
            "id": "Y14",
            "text": "Y14",
            "html": "<img src=\"/Search/Image?key=Y14\" alt=\"Y14\" style=\"max-height:24px; max-width: 28px;\" /> Y14",
            "display": "Y14"
        },
        {
            "id": "Y15",
            "text": "Y15",
            "html": "<img src=\"/Search/Image?key=Y15\" alt=\"Y15\" style=\"max-height:24px; max-width: 28px;\" /> Y15",
            "display": "Y15"
        },
        {
            "id": "Y17",
            "text": "Y17",
            "html": "<img src=\"/Search/Image?key=Y17\" alt=\"Y17\" style=\"max-height:24px; max-width: 28px;\" /> Y17",
            "display": "Y17"
        },
        {
            "id": "Y18b",
            "text": "Y18B",
            "html": "<img src=\"/Search/Image?key=Y18B\" alt=\"Y18B\" style=\"max-height:24px; max-width: 28px;\" /> Y18B",
            "display": "Y18b"
        },
        {
            "id": "Y1v",
            "text": "Y1V: scroll with ties",
            "html": "<img src=\"/Search/Image?key=Y1V\" alt=\"Y1V\" style=\"max-height:24px; max-width: 28px;\" /> Y1V: scroll with ties",
            "display": "Y1v"
        },
        {
            "id": "Y2",
            "text": "Y2: scroll [broad]",
            "html": "<span class=\"uni\">&#x133DD;</span> Y2: scroll",
            "display": "Y2"
        },
        {
            "id": "Y21",
            "text": "Y21",
            "html": "<img src=\"/Search/Image?key=Y21\" alt=\"Y21\" style=\"max-height:24px; max-width: 28px;\" /> Y21",
            "display": "Y21"
        },
        {
            "id": "Y22",
            "text": "Y22",
            "html": "<img src=\"/Search/Image?key=Y22\" alt=\"Y22\" style=\"max-height:24px; max-width: 28px;\" /> Y22",
            "display": "Y22"
        },
        {
            "id": "Y23",
            "text": "Y23",
            "html": "<img src=\"/Search/Image?key=Y23\" alt=\"Y23\" style=\"max-height:24px; max-width: 28px;\" /> Y23",
            "display": "Y23"
        },
        {
            "id": "Y24",
            "text": "Y24",
            "html": "<img src=\"/Search/Image?key=Y24\" alt=\"Y24\" style=\"max-height:24px; max-width: 28px;\" /> Y24",
            "display": "Y24"
        },
        {
            "id": "Y25",
            "text": "Y25",
            "html": "<img src=\"/Search/Image?key=Y25\" alt=\"Y25\" style=\"max-height:24px; max-width: 28px;\" /> Y25",
            "display": "Y25"
        },
        {
            "id": "Y2v",
            "text": "Y2V: scroll",
            "html": "<img src=\"/Search/Image?key=Y2V\" alt=\"Y2V\" style=\"max-height:24px; max-width: 28px;\" /> Y2V: scroll",
            "display": "Y2v"
        },
        {
            "id": "Y3",
            "text": "Y3: scribe&amp;apos;s outfit with palette on left [zS]",
            "html": "<span class=\"uni\">&#x133DE;</span> Y3: scribe&amp;apos;s outfit with palette on left",
            "display": "Y3"
        },
        {
            "id": "Y4",
            "text": "Y4: scribe&amp;apos;s outfit with palette on right",
            "html": "<span class=\"uni\">&#x133DF;</span> Y4: scribe&amp;apos;s outfit with palette on right",
            "display": "Y4"
        },
        {
            "id": "Y5",
            "text": "Y5: game board [mn]",
            "html": "<span class=\"uni\">&#x133E0;</span> Y5: game board",
            "display": "Y5"
        },
        {
            "id": "Y6",
            "text": "Y6: game piece [narrow] [ibA]",
            "html": "<span class=\"uni\">&#x133E1;</span> Y6: game piece",
            "display": "Y6"
        },
        {
            "id": "Y7",
            "text": "Y7: harp",
            "html": "<span class=\"uni\">&#x133E2;</span> Y7: harp",
            "display": "Y7"
        },
        {
            "id": "Y8",
            "text": "Y8: sistrum [tall] [zSSt]",
            "html": "<span class=\"uni\">&#x133E3;</span> Y8: sistrum",
            "display": "Y8"
        },
        {
            "id": "Y8a",
            "text": "Y8A: sistrum",
            "html": "<img src=\"/Search/Image?key=Y8A\" alt=\"Y8A\" style=\"max-height:24px; max-width: 28px;\" /> Y8A: sistrum",
            "display": "Y8a"
        },
        {
            "id": "Z1",
            "text": "Z1: stroke",
            "html": "<span class=\"uni\">&#x133E4;</span> Z1: stroke",
            "display": "Z1"
        },
        {
            "id": "Z10",
            "text": "Z10: wide diagonal cross [narrow]",
            "html": "<span class=\"uni\">&#x133F5;</span> Z10: wide diagonal cross",
            "display": "Z10"
        },
        {
            "id": "Z11",
            "text": "Z11: cross [tall] [imi]",
            "html": "<span class=\"uni\">&#x133F6;</span> Z11: cross",
            "display": "Z11"
        },
        {
            "id": "Z11a",
            "text": "Z11A: cross",
            "html": "<img src=\"/Search/Image?key=Z11A\" alt=\"Z11A\" style=\"max-height:24px; max-width: 28px;\" /> Z11A: cross",
            "display": "Z11a"
        },
        {
            "id": "Z12",
            "text": "Z12: hieratic striking man",
            "html": "<span class=\"uni\">&#x133F7;</span> Z12: hieratic striking man",
            "display": "Z12"
        },
        {
            "id": "Z1a",
            "text": "Z1A: stroke",
            "html": "<img src=\"/Search/Image?key=Z1A\" alt=\"Z1A\" style=\"max-height:24px; max-width: 28px;\" /> Z1A: stroke",
            "display": "Z1a"
        },
        {
            "id": "Z2",
            "text": "Z2: three Z1 horizontally",
            "html": "<span class=\"uni\">&#x133E5;</span> Z2: three Z1 horizontally",
            "display": "Z2"
        },
        {
            "id": "Z20",
            "text": "Z20",
            "html": "<img src=\"/Search/Image?key=Z20\" alt=\"Z20\" style=\"max-height:24px; max-width: 28px;\" /> Z20",
            "display": "Z20"
        },
        {
            "id": "Z22",
            "text": "Z22",
            "html": "<img src=\"/Search/Image?key=Z22\" alt=\"Z22\" style=\"max-height:24px; max-width: 28px;\" /> Z22",
            "display": "Z22"
        },
        {
            "id": "Z24",
            "text": "Z24",
            "html": "<img src=\"/Search/Image?key=Z24\" alt=\"Z24\" style=\"max-height:24px; max-width: 28px;\" /> Z24",
            "display": "Z24"
        },
        {
            "id": "Z26",
            "text": "Z26",
            "html": "<img src=\"/Search/Image?key=Z26\" alt=\"Z26\" style=\"max-height:24px; max-width: 28px;\" /> Z26",
            "display": "Z26"
        },
        {
            "id": "Z28",
            "text": "Z28",
            "html": "<img src=\"/Search/Image?key=Z28\" alt=\"Z28\" style=\"max-height:24px; max-width: 28px;\" /> Z28",
            "display": "Z28"
        },
        {
            "id": "Z2a",
            "text": "Z2A: three Z1 horizontally",
            "html": "<span class=\"uni\">&#x133E6;</span> Z2A: three Z1 horizontally",
            "display": "Z2a"
        },
        {
            "id": "Z2b",
            "text": "Z2B: three D67 horizontally",
            "html": "<span class=\"uni\">&#x133E7;</span> Z2B: three D67 horizontally",
            "display": "Z2b"
        },
        {
            "id": "Z2c",
            "text": "Z2C: three Z1 in triangular arrangement",
            "html": "<span class=\"uni\">&#x133E8;</span> Z2C: three Z1 in triangular arrangement",
            "display": "Z2c"
        },
        {
            "id": "Z3",
            "text": "Z3: three Z1 vertically",
            "html": "<span class=\"uni\">&#x133EA;</span> Z3: three Z1 vertically",
            "display": "Z3"
        },
        {
            "id": "Z30",
            "text": "Z30",
            "html": "<img src=\"/Search/Image?key=Z30\" alt=\"Z30\" style=\"max-height:24px; max-width: 28px;\" /> Z30",
            "display": "Z30"
        },
        {
            "id": "Z38",
            "text": "Z38",
            "html": "<img src=\"/Search/Image?key=Z38\" alt=\"Z38\" style=\"max-height:24px; max-width: 28px;\" /> Z38",
            "display": "Z38"
        },
        {
            "id": "Z3a",
            "text": "Z3A: three lying Z1 vertically",
            "html": "<span class=\"uni\">&#x133EB;</span> Z3A: three lying Z1 vertically",
            "display": "Z3a"
        },
        {
            "id": "Z4",
            "text": "Z4: two diagonal strokes [y]",
            "html": "<span class=\"uni\">&#x133ED;</span> Z4: two diagonal strokes",
            "display": "Z4"
        },
        {
            "id": "Z4a",
            "text": "Z4A: two Z1 horizontally",
            "html": "<span class=\"uni\">&#x133EE;</span> Z4A: two Z1 horizontally",
            "display": "Z4a"
        },
        {
            "id": "Z4b",
            "text": "Z4B: two diagonal strokes",
            "html": "<img src=\"/Search/Image?key=Z4B\" alt=\"Z4B\" style=\"max-height:24px; max-width: 28px;\" /> Z4B: two diagonal strokes",
            "display": "Z4b"
        },
        {
            "id": "Z5",
            "text": "Z5: curved diagonal stroke",
            "html": "<span class=\"uni\">&#x133EF;</span> Z5: curved diagonal stroke",
            "display": "Z5"
        },
        {
            "id": "Z5a",
            "text": "Z5A: diagonal stroke",
            "html": "<span class=\"uni\">&#x133F0;</span> Z5A: diagonal stroke",
            "display": "Z5a"
        },
        {
            "id": "Z6",
            "text": "Z6: hieratic substitute for A13 or A14 [broad]",
            "html": "<span class=\"uni\">&#x133F1;</span> Z6: hieratic substitute for A13 or A14",
            "display": "Z6"
        },
        {
            "id": "Z7",
            "text": "Z7: hieratic quail chick [narrow] [W]",
            "html": "<span class=\"uni\">&#x133F2;</span> Z7: hieratic quail chick",
            "display": "Z7"
        },
        {
            "id": "Z8",
            "text": "Z8: oval [narrow]",
            "html": "<span class=\"uni\">&#x133F3;</span> Z8: oval",
            "display": "Z8"
        },
        {
            "id": "Z9",
            "text": "Z9: diagonal cross [narrow]",
            "html": "<span class=\"uni\">&#x133F4;</span> Z9: diagonal cross",
            "display": "Z9"
        },
        {
            "id": "Aa1",
            "text": "AA1: basket from above [narrow] [x]",
            "html": "<span class=\"uni\">&#x1340D;</span> AA1: basket from above",
            "display": "Aa1"
        },
        {
            "id": "Aa10",
            "text": "AA10: unknown [broad]",
            "html": "<span class=\"uni\">&#x13418;</span> AA10: unknown",
            "display": "Aa10"
        },
        {
            "id": "Aa11",
            "text": "AA11: platform [broad]",
            "html": "<span class=\"uni\">&#x13419;</span> AA11: platform",
            "display": "Aa11"
        },
        {
            "id": "Aa12",
            "text": "AA12: platform [broad]",
            "html": "<span class=\"uni\">&#x1341A;</span> AA12: platform",
            "display": "Aa12"
        },
        {
            "id": "Aa13",
            "text": "AA13: sharp half [broad]",
            "html": "<span class=\"uni\">&#x1341B;</span> AA13: sharp half",
            "display": "Aa13"
        },
        {
            "id": "Aa14",
            "text": "AA14: bent half [broad]",
            "html": "<span class=\"uni\">&#x1341C;</span> AA14: bent half",
            "display": "Aa14"
        },
        {
            "id": "Aa15",
            "text": "AA15: blunt half [broad]",
            "html": "<span class=\"uni\">&#x1341D;</span> AA15: blunt half",
            "display": "Aa15"
        },
        {
            "id": "Aa16",
            "text": "AA16: short half [narrow]",
            "html": "<span class=\"uni\">&#x1341E;</span> AA16: short half",
            "display": "Aa16"
        },
        {
            "id": "Aa17",
            "text": "AA17: lid [narrow]",
            "html": "<span class=\"uni\">&#x1341F;</span> AA17: lid",
            "display": "Aa17"
        },
        {
            "id": "Aa18",
            "text": "AA18: square lid",
            "html": "<span class=\"uni\">&#x13420;</span> AA18: square lid",
            "display": "Aa18"
        },
        {
            "id": "Aa19",
            "text": "AA19: instrument [narrow]",
            "html": "<span class=\"uni\">&#x13421;</span> AA19: instrument",
            "display": "Aa19"
        },
        {
            "id": "Aa2",
            "text": "AA2: pustule [narrow]",
            "html": "<span class=\"uni\">&#x1340E;</span> AA2: pustule",
            "display": "Aa2"
        },
        {
            "id": "Aa20",
            "text": "AA20: bag [tall]",
            "html": "<span class=\"uni\">&#x13422;</span> AA20: bag",
            "display": "Aa20"
        },
        {
            "id": "Aa20b",
            "text": "AA20B: bag",
            "html": "<img src=\"/Search/Image?key=J20B\" alt=\"J20B\" style=\"max-height:24px; max-width: 28px;\" /> AA20B: bag",
            "display": "Aa20b"
        },
        {
            "id": "Aa21",
            "text": "AA21: instrument [tall]",
            "html": "<span class=\"uni\">&#x13423;</span> AA21: instrument",
            "display": "Aa21"
        },
        {
            "id": "Aa21a",
            "text": "AA21A: instrument",
            "html": "<img src=\"/Search/Image?key=J21A\" alt=\"J21A\" style=\"max-height:24px; max-width: 28px;\" /> AA21A: instrument",
            "display": "Aa21a"
        },
        {
            "id": "Aa22",
            "text": "AA22: combination of <canvas class=\"res\">Aa21</canvas> Aa21 and D36",
            "html": "<span class=\"uni\">&#x13424;</span> AA22: combination of <canvas class=\"res\">Aa21</canvas> Aa21 and D36",
            "display": "Aa22"
        },
        {
            "id": "Aa23",
            "text": "AA23: high warp between stakes",
            "html": "<span class=\"uni\">&#x13425;</span> AA23: high warp between stakes",
            "display": "Aa23"
        },
        {
            "id": "Aa23t",
            "text": "AA23T: high warp between stakes",
            "html": "<img src=\"/Search/Image?key=J23T\" alt=\"J23T\" style=\"max-height:24px; max-width: 28px;\" /> AA23T: high warp between stakes",
            "display": "Aa23t"
        },
        {
            "id": "Aa24",
            "text": "AA24: low warp between stakes [broad]",
            "html": "<span class=\"uni\">&#x13426;</span> AA24: low warp between stakes",
            "display": "Aa24"
        },
        {
            "id": "Aa25",
            "text": "AA25: unknown [tall]",
            "html": "<span class=\"uni\">&#x13427;</span> AA25: unknown",
            "display": "Aa25"
        },
        {
            "id": "Aa26",
            "text": "AA26: unknown [tall]",
            "html": "<span class=\"uni\">&#x13428;</span> AA26: unknown",
            "display": "Aa26"
        },
        {
            "id": "Aa27",
            "text": "AA27: spindle [tall]",
            "html": "<span class=\"uni\">&#x13429;</span> AA27: spindle",
            "display": "Aa27"
        },
        {
            "id": "Aa27b",
            "text": "AA27B: spindle",
            "html": "<img src=\"/Search/Image?key=J27B\" alt=\"J27B\" style=\"max-height:24px; max-width: 28px;\" /> AA27B: spindle",
            "display": "Aa27b"
        },
        {
            "id": "Aa27d",
            "text": "AA27D: spindle",
            "html": "<img src=\"/Search/Image?key=J27D\" alt=\"J27D\" style=\"max-height:24px; max-width: 28px;\" /> AA27D: spindle",
            "display": "Aa27d"
        },
        {
            "id": "Aa28",
            "text": "AA28: level [tall]",
            "html": "<span class=\"uni\">&#x1342A;</span> AA28: level",
            "display": "Aa28"
        },
        {
            "id": "Aa3",
            "text": "AA3: pustule with liquid [narrow]",
            "html": "<span class=\"uni\">&#x1340F;</span> AA3: pustule with liquid",
            "display": "Aa3"
        },
        {
            "id": "Aa30",
            "text": "AA30: frieze [tall]",
            "html": "<span class=\"uni\">&#x1342C;</span> AA30: frieze",
            "display": "Aa30"
        },
        {
            "id": "Aa31",
            "text": "AA31: frieze [tall]",
            "html": "<span class=\"uni\">&#x1342D;</span> AA31: frieze",
            "display": "Aa31"
        },
        {
            "id": "Aa32",
            "text": "AA32: archaic bow [tall]",
            "html": "<img src=\"/Search/Image?key=J32\" alt=\"J32\" style=\"max-height:24px; max-width: 28px;\" /> AA32: archaic bow",
            "display": "Aa32"
        },
        {
            "id": "Aa3a",
            "text": "AA3A: pustule with liquid",
            "html": "<img src=\"/Search/Image?key=J3A\" alt=\"J3A\" style=\"max-height:24px; max-width: 28px;\" /> AA3A: pustule with liquid",
            "display": "Aa3a"
        },
        {
            "id": "Aa3b",
            "text": "AA3B: pustule with liquid",
            "html": "<img src=\"/Search/Image?key=J3B\" alt=\"J3B\" style=\"max-height:24px; max-width: 28px;\" /> AA3B: pustule with liquid",
            "display": "Aa3b"
        },
        {
            "id": "Aa5",
            "text": "AA5: navigation instrument",
            "html": "<span class=\"uni\">&#x13411;</span> AA5: navigation instrument",
            "display": "Aa5"
        },
        {
            "id": "Aa51",
            "text": "AA51",
            "html": "<img src=\"/Search/Image?key=J51\" alt=\"J51\" style=\"max-height:24px; max-width: 28px;\" /> AA51",
            "display": "Aa51"
        },
        {
            "id": "Aa54",
            "text": "AA54",
            "html": "<img src=\"/Search/Image?key=J54\" alt=\"J54\" style=\"max-height:24px; max-width: 28px;\" /> AA54",
            "display": "Aa54"
        },
        {
            "id": "Aa55",
            "text": "AA55",
            "html": "<img src=\"/Search/Image?key=J55\" alt=\"J55\" style=\"max-height:24px; max-width: 28px;\" /> AA55",
            "display": "Aa55"
        },
        {
            "id": "Aa56",
            "text": "AA56",
            "html": "<img src=\"/Search/Image?key=J56\" alt=\"J56\" style=\"max-height:24px; max-width: 28px;\" /> AA56",
            "display": "Aa56"
        },
        {
            "id": "Aa5a",
            "text": "AA5A: navigation instrument",
            "html": "<img src=\"/Search/Image?key=J5A\" alt=\"J5A\" style=\"max-height:24px; max-width: 28px;\" /> AA5A: navigation instrument",
            "display": "Aa5a"
        },
        {
            "id": "Aa6",
            "text": "AA6: instrument",
            "html": "<span class=\"uni\">&#x13412;</span> AA6: instrument",
            "display": "Aa6"
        },
        {
            "id": "Aa7",
            "text": "AA7: instrument [broad]",
            "html": "<span class=\"uni\">&#x13413;</span> AA7: instrument",
            "display": "Aa7"
        },
        {
            "id": "Aa8",
            "text": "AA8: irrigation canal [broad]",
            "html": "<span class=\"uni\">&#x13416;</span> AA8: irrigation canal",
            "display": "Aa8"
        },
        {
            "id": "Aa81",
            "text": "AA81",
            "html": "<img src=\"/Search/Image?key=J81\" alt=\"J81\" style=\"max-height:24px; max-width: 28px;\" /> AA81",
            "display": "Aa81"
        },
        {
            "id": "Aa9",
            "text": "AA9: instrument [broad]",
            "html": "<span class=\"uni\">&#x13417;</span> AA9: instrument",
            "display": "Aa9"
        }
    ];
}