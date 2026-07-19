#!/usr/bin/env python3
"""Schrijft assets/cursus/exercises-les-06-36.json voor oefeningen.html."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "cursus" / "exercises-les-06-36.json"


def mc(q: str, options: list[str], correct: int, explain: str = "") -> dict:
    return {"type": "mc", "q": q, "options": options, "correct": correct, "explain": explain}


def fill(q: str, correct: str, explain: str = "", accept: list[str] | None = None, placeholder: str = "Antwoord") -> dict:
    d: dict = {"type": "fill", "q": q, "correct": correct, "placeholder": placeholder, "explain": explain}
    if accept:
        d["accept"] = accept
    return d


def translate(q: str, correct: str, explain: str = "", accept: list[str] | None = None) -> dict:
    d: dict = {
        "type": "translate",
        "q": q,
        "correct": correct,
        "placeholder": "Vertaling",
        "explain": explain,
    }
    if accept:
        d["accept"] = accept
    return d


def match_ex(q: str, pairs: list[dict], explain: str = "") -> dict:
    return {"type": "match", "q": q, "pairs": pairs, "explain": explain}


# Inhoud afgestemd op cursus.html (Nador-Tarifit, Mourigh & Kossmann)
ALL: dict[str, list[dict]] = {
    "les-06": [
        mc(
            "Waarom staat <span class=\"tar\">qqim</span> in woordenlijsten als basisvorm?",
            [
                "Het is de imperatief / gebiedende wijs — daarop bouwt de vervoeging",
                "Het is altijd verleden",
                "Het is een zelfstandig naamwoord",
                "Het is alleen meervoud",
            ],
            0,
            "Tarifit-woordenboeken gebruiken de korte stam (imperatief).",
        ),
        mc(
            "Wat is typisch voor Tarifit-vervoeging t.o.v. Nederlands?",
            [
                "alleen suffixen",
                "prefix én suffix rond de stam",
                "geen persoonsvorm",
                "altijd hetzelfde als het Arabisch",
            ],
            1,
        ),
        fill("Vorm voor <strong>ik zit</strong> (stam <span class=\"tar\">qqim</span>):", "qqimey", explain="1SG: stam + <span class=\"tar\">-ey</span>."),
        translate("Wat betekent <span class=\"tar\">ṯeqqimeḏ</span>?", "jij zit", accept=["jij zit"]),
        match_ex(
            "Koppel persoon en vorm (<span class=\"tar\">qqim</span>).",
            [
                {"left": "hij zit", "leftIsTar": False, "right": "<span class=\"tar\">yeqqim</span>"},
                {"left": "zij zit (vrouw)", "leftIsTar": False, "right": "<span class=\"tar\">ṯeqqim</span>"},
                {"left": "wij zitten", "leftIsTar": False, "right": "<span class=\"tar\">neqqim</span>"},
            ],
        ),
    ],
    "les-07": [
        mc(
            "Welk suffix hoort bij <strong>ik</strong> in het standaardpatroon?",
            ["-<span class=\"tar\">eḏ</span>", "-<span class=\"tar\">ey</span>", "-<span class=\"tar\">en</span>", "-<span class=\"tar\">em</span>"],
            1,
        ),
        mc(
            "Hoe scheid je <strong>hij</strong> en <strong>zij</strong> (ev.)?",
            [
                "alleen een klinker in de stam",
                "prefix <span class=\"tar\">y-</span> versus <span class=\"tar\">ṯ-</span>",
                "alleen het verschil in suffix",
                "ze zijn identiek",
            ],
            1,
        ),
        fill("Vervoeg <span class=\"tar\">cc</span> 'eten' voor <strong>hij</strong>:", "ycc"),
        translate("Letterlijk+vertaling kern: <span class=\"tar\">ṯeqqimeḏ</span> = …", "jij zit", accept=["jij zit"]),
        match_ex(
            "Patronen enkelvoud",
            [
                {"left": "ik", "leftIsTar": False, "right": "STAM-<span class=\"tar\">ey</span>"},
                {"left": "jij", "leftIsTar": False, "right": "<span class=\"tar\">ṯ</span>-STAM-<span class=\"tar\">eḏ</span>"},
                {"left": "hij", "leftIsTar": False, "right": "<span class=\"tar\">y</span>-STAM"},
            ],
        ),
    ],
    "les-08": [
        mc(
            "Welk prefix heeft <strong>wij</strong> in het voorbeeld <span class=\"tar\">neqqim</span>?",
            ["<span class=\"tar\">ṯ-</span>", "<span class=\"tar\">n-</span>", "<span class=\"tar\">y-</span>", "<span class=\"tar\">m-</span>"],
            1,
        ),
        fill("Hoe zeg je <strong>zij zitten</strong> (M/gemengd, stam <span class=\"tar\">qqim</span>)?", "qqimen", accept=["qqimen"]),
        translate("Wat betekent <span class=\"tar\">ṯeqqimem</span>?", "jullie zitten", accept=["jullie zitten"]),
        mc(
            "Wanneer gebruik je vrouwelijk meervoud <span class=\"tar\">-enṯ</span>?",
            [
                "als er minstens één man bij is",
                "alleen als de groep uitsluitend uit vrouwen bestaat",
                "altijd in verleden",
                "nooit",
            ],
            1,
        ),
        match_ex(
            "Koppel klopt bij de les",
            [
                {"left": "1PL", "leftIsTar": False, "right": "<span class=\"tar\">n</span>-STAM"},
                {"left": "2PL M", "leftIsTar": False, "right": "<span class=\"tar\">ṯ</span>-STAM-<span class=\"tar\">em</span>"},
                {"left": "3PL F", "leftIsTar": False, "right": "STAM-<span class=\"tar\">enṯ</span>"},
            ],
        ),
    ],
    "les-09": [
        mc(
            "Waar denkt Tarifit primair in: <strong>tijd</strong> of <strong>aspect</strong>?",
            ["alleen tijd", "aspect (afgerond / lopend / basis)", "alleen plaats", "alleen ontkenning"],
            1,
        ),
        mc(
            "Welke vorm hoort bij een <em>gewoonte</em> 'ik eet' volgens de les?",
            ["Perfectief", "Imperfectief", "alleen Aorist zonder hulp", "geen verschil"],
            1,
            "Voorbeeld <span class=\"tar\">tetey</span> (Imperfectief).",
        ),
        fill("Noem één van de drie hoofdaspecten uit de tabel (één woord, Nederlands).", "perfectief", accept=["perfectief", "imperfectief", "aorist"]),
        translate("Wat betekent ongeveer <span class=\"tar\">cciy</span> in de les (eten)?", "ik heb gegeten", accept=["ik at", "ik heb gegeten"]),
        match_ex(
            "Aspect",
            [
                {"left": "één afgeronde keer", "leftIsTar": False, "right": "Perfectief"},
                {"left": "bezig / gewoonte", "leftIsTar": False, "right": "Imperfectief"},
                {"left": "met <span class=\"tar\">ad</span> + toekomst", "leftIsTar": False, "right": "Aorist-clause"},
            ],
        ),
    ],
    "les-10": [
        mc(
            "Welk partikel markeert de toekomst bij <span class=\"tar\">ad cciy</span> 'ik zal eten'?",
            ["<span class=\"tar\">ṯuya</span>", "<span class=\"tar\">ad</span>", "<span class=\"tar\">qa</span>", "<span class=\"tar\">ma</span>"],
            1,
        ),
        fill("Vul aan: <span class=\"tar\">___ cciy</span> — ik zal eten / ik ga eten.", "ad", accept=["ad"]),
        translate("Vertaal: <span class=\"tar\">ad cciy</span>.", "ik zal eten", accept=["ik zal eten", "ik ga eten"]),
        mc(
            "Wat volgt na <span class=\"tar\">ad</span> in deze constructie?",
            ["Imperfectief", "Aorist (basisstam-vorm)", "alleen een naamwoord", "alleen een voorzetsel"],
            1,
        ),
        match_ex(
            "Toekomst",
            [
                {"left": "marker", "leftIsTar": False, "right": "<span class=\"tar\">ad</span>"},
                {"left": "voorbeeld 'eten' 1SG", "leftIsTar": False, "right": "<span class=\"tar\">ad cciy</span>"},
            ],
        ),
    ],
    "les-11": [
        mc(
            "Hoe ziet een typisch <strong>vrouwelijk enkelvoud</strong> eruit?",
            ["<span class=\"tar\">a-</span> … <span class=\"tar\">-en</span>", "<span class=\"tar\">ṯa-</span> … <span class=\"tar\">-ṯ</span>", "alleen <span class=\"tar\">i-</span>", "zonder prefix"],
            1,
        ),
        fill("Welk prefix heeft mannelijk enkelvoud vaak (bijv. <span class=\"tar\">aayaz</span>)?", "a", accept=["a"]),
        translate("Betekenis van <span class=\"tar\">ṯamɣaṯ</span>?", "vrouw", accept=["vrouw", "een vrouw"]),
        mc("Welk geslacht hoort bij <span class=\"tar\">aayaz</span>?", ["vrouwelijk", "mannelijk", "onzijdig", "alleen meervoud"], 1),
        match_ex(
            "Geslacht",
            [
                {"left": "M ev", "leftIsTar": False, "right": "<span class=\"tar\">a-</span>"},
                {"left": "V ev", "leftIsTar": False, "right": "<span class=\"tar\">ṯa-</span> … <span class=\"tar\">-ṯ</span>"},
            ],
        ),
    ],
    "les-12": [
        mc(
            "De hoofdregel voor mannelijk meervoud: <span class=\"tar\">a-</span> wordt …",
            ["<span class=\"tar\">u-</span>", "<span class=\"tar\">i-</span>", "<span class=\"tar\">ṯi-</span>", "verdwijnt altijd"],
            1,
        ),
        fill("Meervoud van <span class=\"tar\">afunas</span> 'rund':", "ifunasen", accept=["ifunasen"]),
        translate("Meervoud van <span class=\"tar\">ṯafunasṯ</span> 'koe':", "ṯifunasin", accept=["ṯifunasin", "tifunasin"]),
        mc(
            "Waarom zijn uitzonderingen zoals <span class=\"tar\">uma</span> → <span class=\"tar\">ayeṯma</span> belangrijk?",
            [
                "ze bestaan niet",
                "suppletieve meervouden moet je per woord leren",
                "alleen voor leenwoorden",
                "alleen in het Arabisch",
            ],
            1,
        ),
        match_ex(
            "Meervoud",
            [
                {"left": "V-ev → V-mv", "leftIsTar": False, "right": "<span class=\"tar\">ṯi-</span> … <span class=\"tar\">-in</span>"},
                {"left": "M-ev → M-mv", "leftIsTar": False, "right": "<span class=\"tar\">i-</span> … <span class=\"tar\">-en</span>"},
            ],
        ),
    ],
    "les-13": [
        fill("Familiewoord voor <strong>mijn vader</strong> (één woord):", "baba", accept=["baba"]),
        translate("Wat betekent <span class=\"tar\">yemma-c</span>?", "jouw moeder (tegen man)", accept=["jouw moeder"]),
        mc(
            "Hoe zeg je <strong>zijn broer</strong> met een familiewoord?",
            ["<span class=\"tar\">uma</span>", "<span class=\"tar\">uma-s</span>", "<span class=\"tar\">uma-ṯ</span>", "<span class=\"tar\">n uma</span>"],
            1,
        ),
        match_ex(
            "Suffixen op familiewoorden",
            [
                {"left": "jij (M)", "leftIsTar": False, "right": "-<span class=\"tar\">c</span>"},
                {"left": "zijn/haar", "leftIsTar": False, "right": "-<span class=\"tar\">s</span>"},
            ],
        ),
        mc("Waarom betekent <span class=\"tar\">baba</span> niet 'de vader in het algemeen'?", ["wel algemeen", "het is possessief: mijn vader", "omdat het Arabisch is", "geen reden"], 1),
    ],
    "les-14": [
        mc(
            "Welk achtervoegsel betekent <strong>deze</strong> (dichtbij)?",
            ["-<span class=\"tar\">in</span>", "-<span class=\"tar\">a</span>", "-<span class=\"tar\">enni</span>", "-<span class=\"tar\">u</span>"],
            1,
        ),
        fill("Hoe schrijf je <strong>deze man</strong> (<span class=\"tar\">aayaz</span> + deze)?", "aayaz-a", accept=["aayaz-a"]),
        translate("Betekenis van losse <span class=\"tar\">win</span> (M, 'die' verweg)?", "die", accept=["die"]),
        mc(
            "Wat drukt <span class=\"tar\">-enni</span> uit?",
            [
                "alleen meervoud",
                "‘die we al noemden’ / eerder genoemd",
                "alleen vrouwelijk",
                "vraag",
            ],
            1,
        ),
        match_ex(
            "Aanwijzers",
            [
                {"left": "deze (M) los", "leftIsTar": False, "right": "<span class=\"tar\">wa</span>"},
                {"left": "hier", "leftIsTar": False, "right": "<span class=\"tar\">ḏa</span>"},
            ],
        ),
    ],
    "les-15": [
        mc(
            "Wat is de <strong>vrije staat</strong>?",
            ["vorm na voorzetnsel dat bindt", "lexicale / woordenboekvorm", "alleen meervoud", "alleen werkwoord"],
            1,
        ),
        mc(
            "Na welk element volgt meestal <strong>verbonden staat</strong>?",
            ["geen voorbeeld", "veel voorzetsels en possessieve <span class=\"tar\">n</span>", "alleen in titels", "alleen bij Arabisch"],
            1,
        ),
        fill("Welke vorm gebruikt <span class=\"tar\">aayaz</span> vaak in verbonden staat (heel woord)?", "waayaz", accept=["waayaz"]),
        translate("Noem het Nederlandse kernwoord voor wat voorzetsels vaak afdwingen (binding / …).", "verbonden", accept=["verbonden", "verbonden staat"]),
        match_ex(
            "Staat",
            [
                {"left": "woordboek", "leftIsTar": False, "right": "vrij"},
                {"left": "na <span class=\"tar\">n</span> ‘van’", "leftIsTar": False, "right": "verbonden"},
            ],
        ),
    ],
    "les-16": [
        mc(
            "Welk acronym uit de les beschrijft een typische woordorde?",
            ["SVO", "VSO", "OSV", "VOS"],
            1,
        ),
        fill("In één woord: komt het werkwoord in Tarifit-verbalzinnen vaak eerder of later dan in standaard-Nederlands?", "eerder", accept=["eerder", "vroeger", "voor"]),
        translate("Wat valt op bij <span class=\"tar\">yexḏem waayaz</span> t.o.v. Nederlands?", "onderwerp na werkwoord", accept=["werkwoord eerst", "VSO", "onderwerp na werkwoord"]),
        mc("Waarom is WO studeren waard?", ["niet nodig", "clitics en topic kunnen afwijken", "Tarifit heeft geen WO", "alleen voor Engels"], 1),
        match_ex(
            "Patronen",
            [
                {"left": "werkwoord", "leftIsTar": False, "right": "kan eerst"},
                {"left": "onderwerp NP na V", "leftIsTar": False, "right": "zoals in voorbeelden"},
            ],
        ),
    ],
    "les-17": [
        fill("Voorzetsel voor <strong>in</strong> (kort):", "ḏi", accept=["ḏi", "di"]),
        translate("Betekenis van <span class=\"tar\">ɣaa</span> in de les?", "naar, bij", accept=["naar", "bij", "naar, bij"]),
        mc(
            "Welke twee voorzetsels nemen <strong>vrije staat</strong> (uitzondering)?",
            ["<span class=\"tar\">ḏi</span> en <span class=\"tar\">x</span>", "<span class=\"tar\">aṛ</span> en <span class=\"tar\">břa</span>", "<span class=\"tar\">n</span> en <span class=\"tar\">s</span>", "geen uitzonderingen"],
            1,
        ),
        match_ex(
            "Voorzetsels",
            [
                {"left": "<span class=\"tar\">x</span>", "leftIsTar": True, "right": "op"},
                {"left": "<span class=\"tar\">zi</span>", "leftIsTar": True, "right": "van / uit"},
            ],
        ),
        mc(
            "Hoe zeg je ‘ik heb een auto’ volgens de les-constructie?",
            [
                "<span class=\"tar\">yari ijjen ṯṯumubin</span>",
                "<span class=\"tar\">necc d ṯṯumubin</span>",
                "alleen Arabisch",
                "kan niet",
            ],
            0,
        ),
    ],
    "les-18": [
        fill("Hoe schrijf je <strong>2</strong> (cijfer)?", "ṯnayen", accept=["ṯnayen", "tnayen"]),
        fill("Hoe schrijf je <strong>5</strong>?", "xemsa", accept=["xemsa"]),
        translate("Vertaal: <strong>10</strong> (Tarifit).", "ɛecra", accept=["ɛecra", "ecra"]),
        mc(
            "Hoe tel je drie vrouwen op?",
            [
                "<span class=\"tar\">ṯřaṯa n ṯemɣarin</span>",
                "<span class=\"tar\">ijjen n ṯemɣarin</span>",
                "<span class=\"tar\">xemsa waayaz</span>",
                "<span class=\"tar\">ṯnayen</span> alleen",
            ],
            0,
        ),
        match_ex(
            "Structuur",
            [
                {"left": "2 en hoger + znw", "leftIsTar": False, "right": "cijfer + <span class=\"tar\">n</span> + znw"},
                {"left": "‘één’", "leftIsTar": False, "right": "geen <span class=\"tar\">n</span> ertussen"},
            ],
        ),
    ],
    "les-19": [
        fill("Vraagwoord voor <strong>wie</strong>?", "wi", accept=["wi"]),
        translate("Betekenis van <span class=\"tar\">mayemmi</span>?", "waarom", accept=["waarom"]),
        mc(
            "Welk partikel opent vaak een ja/nee-vraag?",
            ["<span class=\"tar\">illa</span>", "<span class=\"tar\">ma</span>", "<span class=\"tar\">ad</span>", "<span class=\"tar\">min</span>"],
            1,
        ),
        match_ex(
            "Vragen",
            [
                {"left": "<span class=\"tar\">min</span>", "leftIsTar": True, "right": "wat"},
                {"left": "<span class=\"tar\">mani</span>", "leftIsTar": True, "right": "waar"},
            ],
        ),
        mc("Hoe maak je informeel ‘is het deze?’ volgens de les?", ["<span class=\"tar\">d wa?</span>", "<span class=\"tar\">ma d wa?</span>", "<span class=\"tar\">min d wa?</span>", "kan niet"], 0),
    ],
    "les-20": [
        mc(
            "Het sterke ontkenningsframe in de les is:",
            [
                "<span class=\"tar\">waa</span> … <span class=\"tar\">ca</span>",
                "<span class=\"tar\">axa</span> alleen",
                "<span class=\"tar\">ad</span> … <span class=\"tar\">ca</span>",
                "dubbel geen",
            ],
            0,
        ),
        fill("Vul aan: <span class=\"tar\">waa</span> … ___", "ca", accept=["ca"]),
        translate("Vertaal: <span class=\"tar\">waa yusin ca</span>.", "hij is niet gekomen", accept=["hij kwam niet", "hij is niet gekomen"]),
        mc(
            "Ontkenning met Imperfectief vraagt soms:",
            ["geen verandering", "een eigen negatieve imperfectief-vorm", "alleen Arabisch", "alleen een emoji"],
            1,
        ),
        match_ex(
            "Ontkenning",
            [
                {"left": "kader", "leftIsTar": False, "right": "<span class=\"tar\">waa</span> … <span class=\"tar\">ca</span>"},
                {"left": "voorbeeld les", "leftIsTar": False, "right": "<span class=\"tar\">waa ssiney ca</span>"},
            ],
        ),
    ],
    "les-21": [
        mc(
            "Wat volgt op <span class=\"tar\">xes</span> ‘willen’?",
            ["Imperfectief alleen", "<span class=\"tar\">ad</span> + Aorist", "alleen een znw", "geen regel"],
            1,
        ),
        mc(
            "Wat volgt op <span class=\"tar\">bda</span> ‘beginnen’?",
            ["<span class=\"tar\">ad</span> + Aorist", "Imperfectief", "Perfectief alleen", "alleen Arabisch"],
            1,
        ),
        fill("Hulpwerkwoord voor <strong>kunnen</strong> in de tabel:", "zemmaa", accept=["zemmaa", "zemmɣa"], explain="Let op spelling in cursus."),
        translate("Wat betekent ruwweg: <span class=\"tar\">xsey ad ariy</span>?", "ik wil schrijven", accept=["ik wil schrijven"]),
        match_ex(
            "Complement",
            [
                {"left": "<span class=\"tar\">xes</span>", "leftIsTar": True, "right": "<span class=\"tar\">ad</span> + Aorist"},
                {"left": "<span class=\"tar\">bda</span>", "leftIsTar": True, "right": "Imperfectief"},
            ],
        ),
    ],
    "les-22": [
        mc(
            "Welk suffix is lijdend voorwerp <strong>hem/haar</strong> achter het werkwoord?",
            ["-<span class=\"tar\">yi</span>", "-<span class=\"tar\">ṯ</span>", "-<span class=\"tar\">c</span>", "-<span class=\"tar\">en</span>"],
            1,
        ),
        fill("Suffix voor <strong>mij</strong> (lijdend) vaak geschreven als:", "-ayi", accept=["-ayi", "ayi"]),
        translate("Wat voeg je toe in het kort om ‘ons’ als lijdend voorwerp te plakken?", "-aney", accept=["-aney", "-ay"]),
        mc(
            "Clitics kunnen:",
            ["alleen vóór het werkwoord", "verspringen (fronting) — zie les", "bestaan niet", "alleen in Engels"],
            1,
        ),
        match_ex(
            "Suffix",
            [
                {"left": "jou (M)", "leftIsTar": False, "right": "-<span class=\"tar\">c</span>"},
                {"left": "hen (M)", "leftIsTar": False, "right": "-<span class=\"tar\">ṯen</span>"},
            ],
        ),
    ],
    "les-23": [
        mc(
            "Hoe zeg je ‘en’ <em>tussen twee werkwoordzinnen</em> volgens de les?",
            [
                "altijd <span class=\"tar\">d</span>",
                "meestal geen apart woord — zinnen naast elkaar",
                "alleen <span class=\"tar\">min</span>",
                "alleen Arabisch",
            ],
            1,
            "Tussen naamwoorden: <span class=\"tar\">d</span>; tussen zinnen: vaak juxtapositie.",
        ),
        fill("Voegwoord voor ‘of’:", "niɣ", accept=["niɣ"]),
        mc(
            "Welk woord verbindt <strong>alleen naamwoordgroepen</strong> met ‘en’?",
            ["<span class=\"tar\">d</span>", "<span class=\"tar\">niɣ</span>", "<span class=\"tar\">ma</span>", "<span class=\"tar\">qa</span>"],
            0,
        ),
        translate("Een woord voor ‘maar’ (informeel) uit de les:", "maca", accept=["maca"]),
        mc(
            "Welk ‘als’ gebruik je voor een open <em>hypothese</em>?",
            ["<span class=\"tar\">mři</span>", "<span class=\"tar\">mařa</span>", "<span class=\"tar\">niɣ</span>", "<span class=\"tar\">d</span>"],
            1,
        ),
        match_ex(
            "Voegwoorden",
            [
                {"left": "ik en mijn broer (NP)", "leftIsTar": False, "right": "<span class=\"tar\">necc d uma</span>"},
                {"left": "rood of wit?", "leftIsTar": False, "right": "<span class=\"tar\">niɣ</span>"},
            ],
        ),
    ],
    "les-24": [
        mc(
            "Welk partikel zet handelingen in de context ‘vóór nu’ / verleden?",
            ["<span class=\"tar\">ad</span>", "<span class=\"tar\">tuya</span>", "<span class=\"tar\">qa</span>", "<span class=\"tar\">illa</span>"],
            1,
        ),
        fill("Hoe schrijf je ‘morgen’ volgens de tabel?", "ṯiwecca", accept=["ṯiwecca", "tiwecca"]),
        translate("‘Nu’ volgens de tijd-bijwoordentabel:", "řexxu", accept=["řexxu", "řexṯu"]),
        mc(
            "Waarom hebben jaar/maand/dag soms een <em>tweetal</em>-vorm?",
            [
                "alleen spelling",
                "Arabische dualis (twee eenheden) — zie les",
                "niet waar",
                "alleen in Engels",
            ],
            1,
        ),
        match_ex(
            "Tijd",
            [
                {"left": "twee dagen", "leftIsTar": False, "right": "<span class=\"tar\">yumayen</span>"},
                {"left": "twee jaar", "leftIsTar": False, "right": "<span class=\"tar\">ɛamayen</span>"},
            ],
        ),
    ],
    "les-25": [
        mc(
            "Welke klank komt historisch uit een <strong>l</strong> in Tarifit?",
            ["<span class=\"tar\">y</span>", "<span class=\"tar\">ř</span>", "<span class=\"tar\">q</span>", "<span class=\"tar\">ɛ</span>"],
            1,
        ),
        fill("Hoe wordt <span class=\"tar\">Naḍur</span> vaak <strong>uitgesproken</strong> (met vocalisatie)?", "Naḍuar", accept=["Naḍuar", "naḍuar", "Naduar"]),
        mc(
            "Dubbele <span class=\"tar\">ll</span> werd in tarifiyt vaak:",
            ["<span class=\"tar\">r</span>", "<span class=\"tar\">ž</span>", "<span class=\"tar\">t</span>", "ongewijzigd"],
            1,
        ),
        translate("Wat gebeurt er met <span class=\"tar\">-ar</span> aan het eind volgens vocalisatie-regels?", "wordt -aa", accept=["lange a", "-aa", "aa"]),
        match_ex(
            "L → ř",
            [
                {"left": "<span class=\"tar\">ul</span> ‘hart’", "leftIsTar": True, "right": "<span class=\"tar\">uř</span>"},
                {"left": "<span class=\"tar\">tili</span>", "leftIsTar": True, "right": "<span class=\"tar\">ṯiři</span>"},
            ],
        ),
    ],
    "les-26": [
        mc(
            "Bijvoeglijke naamwoorden gedragen zich grammaticaal vooral als:",
            ["werkwoord", "naamwoord (geslacht/getal)", "alleen voorzetsel", "alleen cijfer"],
            1,
        ),
        fill("Wat blijft vaak in <strong>vrije staat</strong>, ook als het znw verbonden is?", "bijvoeglijk", accept=["bijvoeglijk naamwoord", "adj", "epitheton"]),
        translate("Vertaal kern: <span class=\"tar\">ameqqṛan</span> (M ev).", "groot", accept=["groot"]),
        mc(
            "Welke twee woorden verbuigen <strong>niet</strong> voor geslacht/getal?",
            ["<span class=\"tar\">berkan</span> en <span class=\"tar\">azeggʷaɣ</span>", "<span class=\"tar\">jjdid</span> en <span class=\"tar\">nneɣni</span>", "<span class=\"tar\">wa</span> en <span class=\"tar\">min</span>", "geen"],
            1,
        ),
        match_ex(
            "Constructie",
            [
                {"left": "bepaald", "leftIsTar": False, "right": "naast elkaar"},
                {"left": "onbepaald", "leftIsTar": False, "right": "met <span class=\"tar\">d</span>"},
            ],
        ),
    ],
    "les-27": [
        mc(
            "Collectief vs telbaar: <span class=\"tar\">ɛenba</span> vs <span class=\"tar\">ṯaɛenbaṯ</span> — wat is het verschil?",
            [
                "geen",
                "soort algemeen vs één stuk",
                "alleen geslacht",
                "werkwoord",
            ],
            1,
        ),
        fill("Welke vorm gebruik je voor ‘ik kocht druiven (in het algemeen)’?", "ɛenba", accept=["ɛenba"], explain="<span class=\"tar\">syiy ɛenba</span> in de les."),
        translate("‘Één druif’ (kern zonder werkwoord):", "ṯaɛenbaṯ", accept=["ṯaɛenbaṯ"]),
        mc(
            "<span class=\"tar\">aman</span> ‘water’ is grammaticaal:",
            ["enkelvoud", "meervoud (plurale tantum)", "werkwoord", "voorzetsel"],
            1,
        ),
        match_ex(
            "Groente/fruit",
            [
                {"left": "algemene soort", "leftIsTar": False, "right": "collectief"},
                {"left": "meerdere stuks", "leftIsTar": False, "right": "telbaar mv"},
            ],
        ),
    ],
    "les-28": [
        mc(
            "Wat betekent prefix <span class=\"tar\">aṯ</span> in <span class=\"tar\">aṯ Naḍuar</span>?",
            ["‘zonder’", "‘die van / behorend tot’", "‘klein’", "‘twee’"],
            1,
        ),
        fill("Prefix voor ‘die met (kenmerk)’ bij mannelijk, type <span class=\"tar\">bu ṯmarṯ</span>:", "bu", accept=["bu"]),
        translate("Wat is de vrouwelijke variant (voorbeeld uit les met <span class=\"tar\">mm</span>) — noem het prefix:", "mm", accept=["mm", "m"]),
        mc(
            "<span class=\"tar\">arifi</span> ‘Riffijn’ heeft meervoud:",
            ["<span class=\"tar\">arifiyen</span>", "<span class=\"tar\">irifiyen</span>", "<span class=\"tar\">rifan</span>", "geen"],
            1,
        ),
        match_ex(
            "Patronen",
            [
                {"left": "stam-leden", "leftIsTar": False, "right": "<span class=\"tar\">i-</span> + stam (<span class=\"tar\">iqeṛɛiyen</span>)"},
                {"left": "bu-", "leftIsTar": False, "right": "kenmerk-man"},
            ],
        ),
    ],
    "les-29": [
        mc(
            "Wat doet prefix <span class=\"tar\">ss-</span> semantisch?",
            ["alleen verleden", "laten / causatief", "alleen vraag", "alleen vrouwelijk"],
            1,
        ),
        fill("Causatief van <span class=\"tar\">cc</span> ‘eten’:", "ssecc", accept=["ssecc"]),
        translate("Betekenis-truc: <span class=\"tar\">ggenfa</span> → <span class=\"tar\">sgenfa</span> na <span class=\"tar\">ss-</span> (dubbele klank):", "genezen → helen", accept=["helen", "genezen laten"]),
        mc(
            "Initiële <span class=\"tar\">a</span> van <span class=\"tar\">adef</span> wordt in causatief:",
            ["blijft <span class=\"tar\">a</span>", "<span class=\"tar\">i</span> → <span class=\"tar\">ssidef</span>", "verdwijnt", "wordt <span class=\"tar\">u</span> altijd"],
            1,
        ),
        match_ex(
            "Voorbeelden",
            [
                {"left": "<span class=\"tar\">ffey</span> uitgaan", "leftIsTar": True, "right": "<span class=\"tar\">ssufey</span> uitlaten"},
                {"left": "<span class=\"tar\">cc</span>", "leftIsTar": True, "right": "<span class=\"tar\">ssecc</span> voeren"},
            ],
        ),
    ],
    "les-30": [
        mc(
            "Wat drukt <span class=\"tar\">mm-</span> vaak uit?",
            ["alleen passief", "wederkerig / middel (elkaar)", "alleen toekomst", "alleen geslacht"],
            1,
        ),
        fill("Passief-prefix uit de lestitel:", "twa", accept=["twa", "twa-"]),
        translate("Betekenis: <span class=\"tar\">mřaya</span> van <span class=\"tar\">řaya</span> ‘roepen’:", "elkaar roepen", accept=["elkaar roepen"]),
        mc(
            "Verschil Passief vs Imperfectief bij verkoopbaar-voorbeeld auto:",
            ["geen", "Perfectief ‘verkocht’ vs Imperfectief ‘verkoopbaar’", "alleen spelling", "alleen Arabisch"],
            1,
        ),
        match_ex(
            "Prefixen",
            [
                {"left": "elkaar", "leftIsTar": False, "right": "<span class=\"tar\">mm-</span>"},
                {"left": "worden gedaan", "leftIsTar": False, "right": "<span class=\"tar\">twa-</span>"},
            ],
        ),
    ],
    "les-31": [
        mc(
            "Wat klopt voor pseudo-werkwoorden?",
            [
                "ze hebben een volledige perfectief/imperfectief-drieling",
                "geen volledige werkwoord-vervoeging, wél persoonsuffixen mogelijk",
                "ze zijn altijd zelfstandige naamwoorden",
                "ze bestaan niet in Tarifit",
            ],
            1,
        ),
        fill("Welk pseudo-werkwoord betekent ongeveer ‘kijk hier’ / presenteren?", "aqqa", accept=["aqqa"]),
        translate("Wat betekent <span class=\"tar\">ay-am</span>?", "alsjeblieft (tegen vrouw)", accept=["alsjeblieft", "hier heb je"]),
        mc(
            "Waarvoor gebruik je <span class=\"tar\">qa</span> volgens de les?",
            [
                "alleen verleden",
                "o.a. non-verbale ‘hier is’, Imperfectief-progressief, en recent perfectief",
                "alleen vraag",
                "alleen in Arabisch",
            ],
            1,
        ),
        match_ex(
            "Pseudo",
            [
                {"left": "<span class=\"tar\">aqq-ec mliḥ?</span>", "leftIsTar": True, "right": "begroeting"},
                {"left": "<span class=\"tar\">qa yetru</span>", "leftIsTar": True, "right": "aan het huilen"},
            ],
        ),
    ],
    "les-32": [
        mc(
            "Bij bepaalde relatieve bijzinnen ontbreekt:",
            ["het hoofdwoord", "anaphorisch pronomen naar het hoofd", "werkwoord", "alleen mannelijk"],
            1,
        ),
        fill("Participium-omlijsting: prefix + stam + welke uitgang in de les-voorbeelden?", "-en", accept=["-en"]),
        translate("In bijzinnen wordt <span class=\"tar\">ad</span> vaak:", "ya", accept=["ya"]),
        mc(
            "Onbepaalde bijzin plakt:",
            ["alleen vóór", "direct achter het hoofdwoord", "nooit", "alleen in Engels"],
            1,
        ),
        match_ex(
            "Relatief",
            [
                {"left": "lijdend voorwerp / prep", "leftIsTar": False, "right": "marker <span class=\"tar\">i</span>"},
                {"left": "‘aan wie’", "leftIsTar": False, "right": "<span class=\"tar\">umi</span>"},
            ],
        ),
    ],
    "les-33": [
        mc(
            "Een cleft bestaat uit predicaat (vaak met <span class=\"tar\">d</span>) plus:",
            ["geen bijzin", "relatieve bijzin met <span class=\"tar\">i</span>", "alleen Arabisch", "alleen een cijfer"],
            1,
        ),
        fill("In <span class=\"tar\">(d) Mimun i zriy</span> — wie wordt benadrukt?", "Mimoun", accept=["Mimoun", "mimoun"]),
        translate("Verschil met vraag: cleft gebruikt wel <span class=\"tar\">d</span> en ___ vóór het relatieve deel.", "i", accept=["i"]),
        mc(
            "Waarom gebruik je een cleft?",
            ["nodzaak grammaticaal", "nadruk / contrast", "alleen in geschriften", "nooit"],
            1,
        ),
        match_ex(
            "Vergelijk",
            [
                {"left": "<span class=\"tar\">d netta i d-yusin</span>", "leftIsTar": True, "right": "cleft"},
                {"left": "<span class=\"tar\">wi d-yusin?</span>", "leftIsTar": True, "right": "wie-vraag"},
            ],
        ),
    ],
    "les-34": [
        mc(
            "In <span class=\"tar\">am necc am wattas n yewdan mamec i ɛeqřey</span> betekent <span class=\"tar\">i</span> hier ruwweg:",
            ["wat", "relatieve marker ‘hoe ik…’", "en", "alleen vraag"],
            1,
        ),
        fill("Wat markeert verleden in <span class=\"tar\">ṯuya ṯessen</span>-achtige zinnen?", "ṯuya", accept=["ṯuya"]),
        translate("<span class=\"tar\">Ḥenna</span> in deze tekst:", "mijn oma / grootmoeder", accept=["oma", "grootmoeder"]),
        mc(
            "Waarom staat <span class=\"tar\">ya</span> i.p.v. <span class=\"tar\">ad</span> in bepaalde bijzinnen?",
            ["foutje", "regel bij rel. / bijzinnen (zie les 32–34)", "alleen poëzie", "Arabische leenconstructie altijd"],
            1,
        ),
        match_ex(
            "Tekst",
            [
                {"left": "<span class=\"tar\">xminni</span>", "leftIsTar": True, "right": "wanneer"},
                {"left": "<span class=\"tar\">waa … ca</span>", "leftIsTar": True, "right": "ontkenning"},
            ],
        ),
    ],
    "les-35": [
        mc(
            "Wat introduceert volgens de les traditioneel een Tarifit-sprookje?",
            [
                "<span class=\"tar\">waxxa</span> alleen",
                "<span class=\"tar\">yekkaa</span> ‘er was eens / het rees’",
                "<span class=\"tar\">qa</span> alleen",
                "geen vaste formule",
            ],
            1,
        ),
        fill("Arabisch leenwoord in de les dat ongeveer ‘ik vertel (je)’ / verhaal-opener markeert:", "Ḥajit-ek", accept=["Ḥajit-ek", "ḥajit-ek"], explain="Zoals in de cursus gespeld."),
        translate("Wat betekent <span class=\"tar\">ijjen yiyyaa</span> uit de eerste zin?", "één veld", accept=["een veld", "één veld"]),
        mc(
            "Welke voorwaardelijke woorden uit het sprookje noemt de les uitdrukkelijk?",
            ["alleen <span class=\"tar\">mařa</span>", "<span class=\"tar\">mri</span> en <span class=\"tar\">mařa</span>", "alleen <span class=\"tar\">niɣ</span>", "geen"],
            1,
        ),
        match_ex(
            "Lezen",
            [
                {"left": "bezit ‘hij heeft’", "leftIsTar": False, "right": "<span class=\"tar\">ɣaas</span>"},
                {"left": "koning in openingszin", "leftIsTar": False, "right": "<span class=\"tar\">ijj uzedjid</span>"},
            ],
        ),
    ],
    "les-36": [
        mc(
            "In dialogen leer je vooral:",
            ["alleen grammaticale tabellen", "routine, beleefdheid, turn-taking", "alleen Arabisch", "niets"],
            1,
        ),
        fill("Welke begroeting uit les 05 herken je vaak in dialogen?", "aqq-ec mliḥ", accept=["aqqa ec mliḥ", "aqq-ec mliḥ?", "aqqac mliḥ"]),
        translate("Wat betekent <span class=\"tar\">waxxa</span>?", "oké", accept=["oké", "oke"]),
        mc(
            "Code-switching met Arabisch in familiecontext is:",
            ["onbestaand", "soms normaal (zoals bij ‘bedankt’ besproken)", "verboden", "alleen in Schrift"],
            1,
        ),
        match_ex(
            "Dialoog",
            [
                {"left": "bevestigen", "leftIsTar": False, "right": "<span class=\"tar\">waxxa</span>"},
                {"left": "check welzijn", "leftIsTar": False, "right": "<span class=\"tar\">aqq</span>-… <span class=\"tar\">mliḥ</span>"},
            ],
        ),
    ],
}

def main() -> None:
    missing = [f"les-{n:02d}" for n in range(6, 37) if f"les-{n:02d}" not in ALL]
    if missing:
        raise SystemExit(f"Ontbrekende lessen in ALL: {missing}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(ALL, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", OUT, "—", len(ALL), "lessen")


if __name__ == "__main__":
    main()
