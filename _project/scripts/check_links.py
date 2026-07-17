"""
Valideert de interne link-structuur van de cursus (Fase 3 van de herstructurering).

Controleert, voor zowel de Nederlandse als de Engelse site:
  1. Elk intern anker (#...) in cursus/uitleg/oefeningen bestaat als id= ergens in het
     doelbestand.
  2. Elke les heeft precies één vorige- en één volgende-link (behalve les 1 / laatste les),
     en die vormen samen een gesloten keten 01..N zonder gaten of duplicaten.
  3. Elke les heeft een oefeningen-link die bestaat in oefeningen.html én een bijbehorende
     key in exercises-*.json.
  4. NL- en EN-lesnummering worden onderling vergeleken.

Geen wijzigingen aan site-bestanden. Print een rapport en geeft exit-code 1 als er
problemen zijn gevonden, anders exit-code 0.
"""

import re
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROBLEMS = []


def problem(msg):
    PROBLEMS.append(msg)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def all_ids(html):
    return set(re.findall(r'id="([^"]+)"', html))


def lesson_sections(html):
    """Return {lesnum(str): body} for <section id="les-NN">...</section> blocks."""
    pat = re.compile(r'<section id="les-(\d+)">(.*?)(?=<section id="les-\d+">|</main)', re.DOTALL)
    return {m.group(1): m.group(2) for m in pat.finditer(html)}


NAV_LINK_PAT = re.compile(r'<a\s+([^>]*?)>\s*<span class="label">(.*?)</span>', re.DOTALL)


def find_nav_links(body):
    """Vindt <a ...><span class="label">...</span> elementen die naar #les-NN linken.
    Attribuutvolgorde (href/class) verschilt tussen NL en EN, dus we parsen de
    attributen los in plaats van een vaste volgorde te veronderstellen. Retourneert
    (prev_target_of, next_target_of) — elk None of een lesnummer-string "les-NN"."""
    prev_target = None
    next_target = None
    prev_count = 0
    next_count = 0
    for attrs, _label in NAV_LINK_PAT.findall(body):
        href_m = re.search(r'href="#(les-\d+)"', attrs)
        if not href_m:
            continue
        is_next = 'class="next"' in attrs
        if is_next:
            next_count += 1
            next_target = href_m.group(1)
        else:
            prev_count += 1
            prev_target = href_m.group(1)
    return prev_target, next_target, prev_count, next_count


def check_site(label, cursus_path, uitleg_path, oef_path, exercises_json_path):
    uitleg_basename = os.path.basename(uitleg_path)
    oef_basename = os.path.basename(oef_path)
    cursus = read(cursus_path)
    uitleg = read(uitleg_path)
    oef = read(oef_path)
    with open(exercises_json_path, encoding="utf-8") as f:
        exercises = json.load(f)

    uitleg_ids = all_ids(uitleg)
    oef_ids = all_ids(oef)

    lessons = lesson_sections(cursus)
    nums = sorted(lessons.keys(), key=int)
    if not nums:
        problem(f"[{label}] Geen enkele lessectie gevonden in {cursus_path}")
        return set()

    n_max = int(nums[-1])
    expected = {f"{i:02d}" for i in range(1, n_max + 1)}
    actual = set(nums)
    if expected != actual:
        missing = expected - actual
        extra = actual - expected
        if missing:
            problem(f"[{label}] Ontbrekende lesnummers in de keten: {sorted(missing)}")
        if extra:
            problem(f"[{label}] Onverwachte/dubbele lesnummers: {sorted(extra)}")

    uitleg_link_pat = re.compile(r'href="' + re.escape(uitleg_basename) + r'#([^"]+)"')
    oef_link_pat = re.compile(r'href="' + re.escape(oef_basename) + r'#([^"]+)"')

    for num in nums:
        body = lessons[num]

        u = uitleg_link_pat.findall(body)
        if not u:
            problem(f"[{label}] Les {num}: geen uitleg-link gevonden")
        else:
            for anchor in u:
                if anchor not in uitleg_ids:
                    problem(f"[{label}] Les {num}: uitleg-anchor #{anchor} bestaat niet in {os.path.basename(uitleg_path)}")

        o = oef_link_pat.findall(body)
        if not o:
            problem(f"[{label}] Les {num}: geen oefeningen-link gevonden")
        else:
            for anchor in o:
                if anchor not in oef_ids:
                    problem(f"[{label}] Les {num}: oef-anchor #{anchor} bestaat niet in {os.path.basename(oef_path)}")
                lesson_key = anchor.replace("oef-", "")
                if lesson_key not in exercises:
                    problem(f"[{label}] Les {num}: geen entry '{lesson_key}' in {os.path.basename(exercises_json_path)}")

        prev_target, next_target, prev_count, next_count = find_nav_links(body)

        expected_prev = f"les-{int(num) - 1:02d}" if int(num) > 1 else None
        expected_next = f"les-{int(num) + 1:02d}" if int(num) < n_max else None

        if prev_count > 1:
            problem(f"[{label}] Les {num}: heeft {prev_count} vorige-links (verwacht: 0 of 1)")
        if next_count > 1:
            problem(f"[{label}] Les {num}: heeft {next_count} volgende-links (verwacht: 0 of 1)")

        if expected_prev is None and prev_target is not None:
            problem(f"[{label}] Les {num}: heeft een vorige-link maar zou de eerste les moeten zijn")
        if expected_prev is not None and prev_target is None:
            problem(f"[{label}] Les {num}: mist vorige-link")
        if expected_prev is not None and prev_target is not None and prev_target != expected_prev:
            problem(f"[{label}] Les {num}: vorige-link wijst naar {prev_target} i.p.v. {expected_prev}")

        if expected_next is None and next_target is not None:
            problem(f"[{label}] Les {num}: heeft een volgende-link maar zou de laatste les moeten zijn")
        if expected_next is not None and next_target is None:
            problem(f"[{label}] Les {num}: mist volgende-link")
        if expected_next is not None and next_target is not None and next_target != expected_next:
            problem(f"[{label}] Les {num}: volgende-link wijst naar {next_target} i.p.v. {expected_next}")

    return actual


INLINE_REF_PAT_NL = re.compile(r'Les (\d+)')
INLINE_REF_PAT_EN = re.compile(r'Lesson (\d+)')


def audit_inline_refs(label, cursus_path, pat, n_max):
    """Losse tekstverwijzingen ("zie Les 09", "(Lesson 21)") worden NIET door de
    renumber-scripts bijgewerkt (die raken alleen id=/href=). Dit is geen
    pass/fail-check (de tool kan niet weten of het doelnummer semantisch nog
    klopt) maar een auditrapport: elke vondst met bronles + huidige titel van de
    doellesson, zodat een mens/Claude na een volgende hernummering snel kan
    controleren of de vermelding nog correct is. Vermeldingen die buiten het
    geldige bereik vallen (bv. "Les 99" of "Les 40" op een site met 38 lessen)
    worden wél als harde PROBLEM gerapporteerd."""
    html = read(cursus_path)
    sections = lesson_sections(html)
    h2_pat = re.compile(r'<h2>(.*?)</h2>', re.DOTALL)
    h2_by_num = {}
    for num, body in sections.items():
        m = h2_pat.search(body)
        h2_by_num[num] = re.sub(r'<[^>]+>', '', m.group(1)) if m else ''

    print(f"\n--- [{label}] Inline lesverwijzingen (audit, geen fout tenzij anders vermeld) ---")
    any_found = False
    for num in sorted(sections.keys(), key=int):
        body = sections[num]
        # sluit de gestructureerde nav/sidebar-achtige stukken niet expliciet uit;
        # in de lessectie zelf komt dat toch niet voor.
        for m in pat.finditer(body):
            target = m.group(1)
            any_found = True
            if target not in h2_by_num:
                problem(f"[{label}] Les {num}: inline verwijzing naar 'Les {target}' bestaat niet (buiten bereik 01-{n_max})")
                print(f"  Les {num} -> Les {target}  ONGELDIG (bestaat niet)")
            else:
                print(f"  Les {num} -> Les {target}  (huidige titel: {h2_by_num[target]})")
    if not any_found:
        print("  (geen gevonden)")


def main():
    nl_lessons = check_site(
        "NL",
        os.path.join(ROOT, "nl", "cursus.html"),
        os.path.join(ROOT, "nl", "uitleg.html"),
        os.path.join(ROOT, "nl", "oefeningen.html"),
        os.path.join(ROOT, "assets", "oefeningen", "exercises-nl.json"),
    )
    en_lessons = check_site(
        "EN",
        os.path.join(ROOT, "en", "course.html"),
        os.path.join(ROOT, "en", "grammar.html"),
        os.path.join(ROOT, "en", "exercises.html"),
        os.path.join(ROOT, "assets", "oefeningen", "exercises-en.json"),
    )

    if nl_lessons and en_lessons and nl_lessons != en_lessons:
        missing_in_en = nl_lessons - en_lessons
        missing_in_nl = en_lessons - nl_lessons
        if missing_in_en:
            problem(f"[NL/EN] Lesnummers in NL maar niet in EN: {sorted(missing_in_en)}")
        if missing_in_nl:
            problem(f"[NL/EN] Lesnummers in EN maar niet in NL: {sorted(missing_in_nl)}")

    print(f"NL: {len(nl_lessons)} lessen gevonden. EN: {len(en_lessons)} lessen gevonden.")

    if nl_lessons:
        audit_inline_refs("NL", os.path.join(ROOT, "nl", "cursus.html"), INLINE_REF_PAT_NL, len(nl_lessons))
    if en_lessons:
        audit_inline_refs("EN", os.path.join(ROOT, "en", "course.html"), INLINE_REF_PAT_EN, len(en_lessons))

    if PROBLEMS:
        print(f"\n{len(PROBLEMS)} PROBLEEM/PROBLEMEN GEVONDEN:\n")
        for p in PROBLEMS:
            print(f"  - {p}")
        sys.exit(1)
    else:
        print("\nGeen problemen gevonden.")
        sys.exit(0)


if __name__ == "__main__":
    main()
