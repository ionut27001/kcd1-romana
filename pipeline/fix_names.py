"""Put character names back exactly as in the English game (user, 2026-10-27: "nu trebuia să ne atingem de nume").

Haiku had applied the glossary's saints rule to ordinary characters (Matthew -> Matei, Esther -> Estera, Peter ->
Petru). A line is a candidate when its English has a personal name (capitalised mid-sentence in the game text) that the
Romanian lacks. Kept as they are: titles and places with a Romanian form (Bailiff -> jude, Bohemia -> Boemia), the
historical kings Wenceslas and Charles (Venceslau, Carol, as in KCD2), and saints / holy figures (Saint X, Virgin Mary,
Jesus). Sonnet rewrites only the name (declined Romanian-style: „lui Matthew”), the rest of the line stays.

Usage: python -I -X utf8 fix_names.py kcd1 | kcd2 [--dry]
"""
import json
import re
import sqlite3
import sys

sys.path.insert(0, r"D:\acs-ro\pipeline")
sys.path.insert(0, r"D:\kcd2-ro\pipeline")
sys.path.insert(0, r"D:\kcd1-ro\pipeline")
import acs_translate as A  # noqa: E402
from acs_translate import llm  # noqa: E402
import kcd_edit as K  # noqa: E402
import kcd1_translate as T  # noqa: E402

EXEMPT = set("""Bailiff Christ Virgin Christian Christians Captain Inquisitor Jesus Huntsman Lordship Lordships Hungarian
Hungarians Hungary Rathaus Bohemia Margrave Pope Popes Overseer League Chamberlain Goodwife Goodwives Emperor Empire Chronicle
Charles Czech Czechs Queen Builder Sunday Monday Tuesday Wednesday Thursday Friday Saturday God Lord Lady Sir Master
Brother Sister Father Mother Saint Holy Heaven Hell Devil Satan Church King Kingdom Prague Rome Germany Germans German
Moravia Mary Abbot Prior Mayor Steward Marshal Burgrave Count Countess Duke Gospel Easter Christmas Bible Cumans Cuman
Jew Jews Jewish Hussite Hussites Lent Mass Scripture Bishop Archbishop Priest Inquisition Heretic Saxon Saxons Polish
Poland Pole Poles Bavarian Austrian Austria Italian Italy Venice Venetian French France English England Englishman Turk
Turks Wenceslas Jerusalem Executioner Scribe Miller Smith Blacksmith Tanner Baker Butcher Innkeeper Hunter Gamekeeper
Guard Guards Watchman Herald Knight Knights Squire Page Lords Ladies Masters Brothers Sisters Fathers Charisma Glade
Council Councillor Sheba Allure Papa Musk Mode Translators Falsehood Christendom Catholic Ladyship Hail Christianity
Thee Thou Thy Tatars Gothic Cockerel Vespers Sparrowhawk Ottoman Myths Marys Gutting Greek Greeks Danube Bibber Bearmen
Assurance Anthony Grandpa Grandma Granny Mum Mummy Dad Daddy Ma Pa Lad Lass Sire Highness Majesty Grace Reverend
Goodman Mistress Sergeant Commander Marshal Reeve Warden Elder Elders Apostle Apostles Gospels Saints Angel Angels""".split())
HOLY = re.compile(r"(Saint|St\.|Holy|Virgin|Blessed|Apostle|Father|Mother of God)\s+$")


ALSO = {"Elijah": "Ilie", "Theresa": "Terez", "Tess": "Terez", "Matty": "Mate", "Mathew": "Mate"}  # renamed beyond the first-two-letters test below
# game characters whose names Haiku romanised (checked 2026-10-27); historical kings, popes and saints keep the
# Romanian forms of the glossary (Venceslau, Carol, Grigore, Sfântul Petru), as in KCD2
PERSONS = {"Matthew", "Esther", "Theresa", "Peter", "Nicholas", "Matthias", "Elijah", "Zbyshek", "Vashek", "Peshek",
           "Nicodemus", "Tess", "Matty", "Mathew"}  # nicknames used in dialogue: Tess = Theresa, Matty = Matthew


def has_name(ro, name):
    """The English name is there: whole, or for names ending in a vowel without it (Theresa -> Theresei)."""
    name = re.sub(r"['’]s$", "", name)
    stem = name[:-1] if name[-1] in "aeiou" else name
    return re.search(r"\b" + re.escape(stem), ro) is not None


def renamed(ro, name):
    """True when the Romanian has the name in a Romanian form (Matei for Matthew, Estera for Esther, Zbyșek for
    Zbyshek) rather than leaving it out: a capitalised word sharing the first two letters, or a known rename."""
    name = re.sub(r"['’]s$", "", name)
    if name in ALSO and ALSO[name] in ro:
        return True
    return any(w[:2].lower() == name[:2].lower() and not w.startswith(name[:len(name) - 1])
               for w in re.findall(r"\b[A-ZĂÂÎȘȚ][a-zăâîșț]+\b", ro))


def names_in(en):
    out = set()
    for m in re.finditer(r"\b([A-Z][a-z][a-zA-Z'’-]{1,})\b", en):
        w = m.group(1)
        listed = re.sub(r"['’]s$", "", w) in PERSONS  # known characters: no need to prove they are names
        if w in EXEMPT or not (listed or T.proper(w)) or HOLY.search(en[:m.start()]):
            continue
        out.add(w)
    return out


def candidates(rows):
    out = []
    for uid, en, ro, key in rows:
        if not ro:
            continue
        missing = sorted(n for n in names_in(en)
                         if re.sub(r"['’]s$", "", n) in PERSONS and not has_name(ro, n) and renamed(ro, n))
        if missing:
            out.append((uid, en, ro, key, missing))
    return out


RULE = """
REGULĂ PENTRU LOTUL ĂSTA: numele personajelor rămân EXACT ca în engleză (Matthew, Theresa, Esther, Peter, Nicholas,
Elijah, John, Zbyshek...), nu le traduce și nu le adapta („Matei”, „Tereza”, „Petru” sunt greșite). Le declini
românește doar cu articol separat: „lui Matthew”, „Theresei” sau „lui Theresa”. În "names" ai numele care lipsesc din
traducerea actuală ("ro"): pune-le la loc. NU schimba nimic altceva din traducere."""


def fix(db, rows, apply=True):
    cand = candidates(rows)
    print(f"{len(cand)} lines with a character name missing", flush=True)
    if not apply:
        import collections
        c = collections.Counter(n for *_, miss in cand for n in miss)
        print(c.most_common(40))
        for uid, en, ro, key, miss in cand[:12]:
            print(" ", miss, "|", en[:80], "|", ro[:80])
        return
    fixed = 0
    chunks = T.lots([(c[0], c[2]) + c for c in cand], 30, 5000)  # by length too: codex pages are long
    done = 0
    for lot in chunks:
        chunk = [c[2:] for c in lot]
        b = done
        done += len(chunk)
        lines, meta = [], []
        for i, (uid, en, ro, key, miss) in enumerate(chunk):
            men, toks = K.mask(en)
            mro = ro
            for j, t in enumerate(toks, 1):
                mro = mro.replace(t, f"⟦{j}⟧", 1)
            lines.append({"id": i, "en": men, "ro": mro, "names": miss})
            meta.append((uid, toks, en, ro, miss))
        m = A.client().messages.create(
            model="claude-sonnet-5-5", max_tokens=16000, system=T.SONNET + RULE,
            messages=[{"role": "user", "content": json.dumps({"lines": lines}, ensure_ascii=False)}],
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": llm.LINES_SCHEMA}})
        try:
            got = {x["id"]: x["f"] for x in json.loads(next(c.text for c in m.content if c.type == "text"))["t"]}
        except (ValueError, StopIteration):
            print("  answer cut off, lot skipped", flush=True)
            continue
        for i, (uid, toks, en, ro, miss) in enumerate(meta):
            if i not in got:
                continue
            new = K.unmask(got[i], toks)
            lead, trail = en[:len(en) - len(en.lstrip())], en[len(en.rstrip()):]
            new = T.restore_breaks(en, lead + new.strip() + trail)
            if not T.problem(en, new, toks) and all(has_name(new, n) for n in miss):
                db.execute("UPDATE units SET ro = ? WHERE id = ?", (new, uid))
                fixed += 1
        db.commit()
        print(f"  {b + len(chunk)}/{len(cand)} done, {fixed} fixed", flush=True)
    print(f"fixed {fixed} of {len(cand)}")


def main():
    which, dry = sys.argv[1], "--dry" in sys.argv
    if which == "kcd1":
        db = T.db()
        rows = db.execute("SELECT id, en, ro, key FROM units").fetchall()
    else:
        db = sqlite3.connect(r"D:\kcd2-ro\db\kcd.db")
        rows = db.execute("SELECT id, en, ro, key FROM units").fetchall()
    fix(db, rows, apply=not dry)


if __name__ == "__main__":
    main()
