"""Romanian translation of Kingdom Come: Deliverance (1), from scratch (user, 2026-10-27).

Plan chosen by the user after the blind model test: Haiku 5.5 on everything, Sonnet 5.5 only on jokes, wordplay and
swearing. Source = the English game tables (Localization/English_xml.pak, rows key / older draft / final English: the
third cell is what the game shows). Texts identical to one in KCD2 take the KCD2 translation (D:\\kcd2-ro\\db\\kcd.db),
so names, items and perks match across the two games and nothing is paid twice.

Tables: units(id, en, ro, file, key, ord, kind dialog|text, status new|kcd2|ok|fail|sonnet, flag, ro_haiku)
Steps: prepare -> run haiku -> run sonnet (flagged by Haiku in "m", plus swearing found by regex) -> stats

Usage: python -I -X utf8 kcd1_translate.py prepare | run haiku|sonnet [--size 40] | apply <batch> <pass> | stats
"""
import glob
import json
import os
import pathlib
import re
import sqlite3
import subprocess
import sys

sys.path.insert(0, r"D:\acs-ro\pipeline")
sys.path.insert(0, r"D:\kcd2-ro\pipeline")
import acs_translate as A  # noqa: E402
from acs_translate import Request, MessageCreateParamsNonStreaming, llm  # noqa: E402
import kcd_edit as K  # noqa: E402

ROOT = pathlib.Path(r"D:\kcd1-ro")
PLANS = ROOT / "batch"
ROW = re.compile(r"<Row>\s*<Cell>(.*?)</Cell>\s*<Cell>(.*?)</Cell>\s*<Cell>(.*?)</Cell>\s*</Row>", re.S)
RAW = re.compile(r"<|>|&(?!(?:lt|gt|amp|quot|apos|nbsp|#\d+);)")
SEP = re.compile(r"\r\n|\n")
SWEAR = re.compile(r"\b(fuck\w*|shit\w*|arse\w*|piss\w*|bastard\w*|whore\w*|damn\w*|bloody|cock\w*|prick\w*|turd\w*|"
                   r"bugger\w*|cunt\w*|bollocks|twat|horseshit|goddam\w*|son of a bitch|bitch\w*)\b", re.I)
GLOSS = (K.DOCS / "TERMENI.md").read_text(encoding="utf-8") + "\n\n" + (K.DOCS / "GLOSAR.md").read_text(encoding="utf-8")

COMMON = """- "glosar" din mesaj are termenii deja traduși în Kingdom Come: Deliverance II (iteme, talente, îndemânări,
  locuri, persoane): când termenul englez apare în rând, folosește EXACT traducerea de acolo (acordată gramatical).
- Henry e bărbat. Rolurile în -ice/-ka și prenumele în -a sunt de obicei femei.
- Termenii din glosar se scriu exact (TERMENI.md are prioritate): jupân, Sir, jude, groschen, șperaclu, Carismă,
  Vorbire; așezările rămân (Rattay, Talmberg, Skalitz, Sasau, Uzhitz, Ledetchko, Merhojed, Neuhof, Samopesh).
- Marcajele ⟦1⟧, ⟦2⟧ … sunt cod de joc: rămân toate, o dată fiecare. Diacritice cu virgulă (ș ț), ghilimele „…”.
- Nu adăuga și nu scoate informație.

GLOSAR:
""" + GLOSS

DIALOG = """Ești traducătorul român al jocului Kingdom Come: Deliverance (Boemia, 1403). Traduci replici de dialog din
engleză; fiecare are vorbitorul ("vorbitor", cod ceh: nume sau rol).
- Româna vorbită firesc, ca a unui român tânăr, dar potrivit epocii: propoziții scurte, forme scurte („n-am”, „nu-i”),
  „o să fac”, „asta”, „ca să”. Fără argou modern (mișto, nasol, ok, gen, bro), fără anglicisme, fără arhaisme
  („pururea”, „a grăi”). Jupânii, preoții și călugării vorbesc mai așezat.
- Glumele și ironiile se adaptează: o glumă românească de același fel, nu cuvânt cu cuvânt. Înjurăturile sună cum
  înjură un român, pe măsura englezei, dar de epocă („fir-ar să fie”, „la naiba”, „dracu' să te ia”, „ticălosule”).
- În câmpul "m" pune "G" dacă replica are o glumă, un joc de cuvinte, o poezie/rimă sau o insultă colorată pe care
  n-ai reușit s-o adaptezi bine (o reia un editor); altfel lasă "m" gol.
""" + COMMON + """
Răspunde DOAR cu JSON: {"t":[{"id":<id>,"f":"<traducerea>","m":""}]}, câte un rând pentru fiecare id."""

TEXT = """Ești traducătorul român al jocului Kingdom Come: Deliverance (Boemia, 1403). Traduci texte de interfață,
obiecte, misiuni, jurnal, codex și cărți.
- Interfață și obiecte: scurt, clar, termenii din glosar, imperativ la butoane și obiective („Vorbește cu”, „Găsește”).
- Jurnalul și misiunile: povestit firesc, la persoana a II-a sau cum e în engleză.
- Codexul: română actuală, ca un articol bun de istorie. Cărțile: puțin mai vechi la ton, dar NU urca deasupra
  englezei (fără „pururea”, „dibăcie”, „a grăi”).
""" + COMMON + """
Răspunde DOAR cu JSON: {"t":[{"id":<id>,"f":"<traducerea>","m":""}]}, câte un rând pentru fiecare id."""

SONNET = DIALOG.replace(
    """- În câmpul "m" pune "G" dacă replica are o glumă, un joc de cuvinte, o poezie/rimă sau o insultă colorată pe care
  n-ai reușit s-o adaptezi bine (o reia un editor); altfel lasă "m" gol.
""", """- Primești și traducerea făcută de un model mai mic ("ro"): păstreaz-o dacă e bună, dar replicile astea au glume,
  jocuri de cuvinte, rime sau înjurături, deci adaptează-le cu adevărat românește. Pune "f" final mereu.
- „Kurva” rămâne „Kurva”, exact ca în original (e înjurătura cehă a jocului). Replicile sau versurile scrise în
  cehă în original (cântece, rugăciuni, înjurături cehe) rămân în cehă, neschimbate. „ale” = bere („Un ale” → „O bere”).
  Numele cu litere cehe (Pešek, Šimon) rămân.
""")


def db():
    con = sqlite3.connect(ROOT / "db" / "kcd1.db")
    con.execute("""CREATE TABLE IF NOT EXISTS units(id INTEGER PRIMARY KEY, en TEXT UNIQUE, ro TEXT, file TEXT, key TEXT,
                   ord INTEGER, kind TEXT, status TEXT DEFAULT 'new', flag TEXT, ro_haiku TEXT)""")
    return con


def prepare():
    (ROOT / "db").mkdir(exist_ok=True)
    con = db()
    kcd2 = dict(sqlite3.connect(r"D:\kcd2-ro\db\kcd.db").execute(
        "SELECT r.en, coalesce(u.ro, r.modern) FROM rows r LEFT JOIN units u ON u.en = r.en AND u.ro_v1 = r.modern "
        "WHERE r.en != '' AND r.modern != ''"))
    n = reused = 0
    files = sorted(glob.glob(str(ROOT / "src" / "en" / "*.xml")), key=lambda f: f.endswith("dialog.xml"))
    for f in files:
        name = os.path.basename(f)
        for i, (k, _, en) in enumerate(ROW.findall(open(f, encoding="utf-8").read())):
            if not en.strip():
                continue
            kind = "dialog" if name == "text_ui_dialog.xml" else "text"
            ro = kcd2.get(en)
            st = "kcd2" if ro and ro != en and not RAW.search(ro) else "new"
            cur = con.execute("INSERT OR IGNORE INTO units(en, ro, file, key, ord, kind, status) VALUES (?,?,?,?,?,?,?)",
                              (en, ro if st == "kcd2" else None, name, k, i, kind, st))
            n += cur.rowcount
            reused += cur.rowcount and st == "kcd2"
    con.commit()
    print(f"{n} unique texts, {reused} taken from KCD2")


def kcd2_terms():
    """Short KCD2 UI terms (items, perks, skills, places, people) EN -> final RO, so KCD1 uses the same words.
    Only capitalised or multi-word terms: single common words ("Back", "Yes") would match everywhere."""
    con = sqlite3.connect(r"D:\kcd2-ro\db\kcd.db")
    seen = {}
    for en, ro in con.execute("""SELECT r.en, coalesce(u.ro, r.modern) FROM rows r LEFT JOIN units u
                                 ON u.en = r.en AND u.ro_v1 = r.modern
                                 WHERE r.file != 'text_ui_dialog.xml' AND length(r.en) BETWEEN 3 AND 45"""):
        en, ro = en.strip(), (ro or "").strip()
        if not ro or ro == en or RAW.search(ro) or K.PROTECT.search(en) or not re.match(r"[A-Z]", en):
            continue
        if len(en.split()) > 5 or re.search(r"[.!?:;,]$", en) or " " not in en and not proper(en):
            continue
        seen.setdefault(en, {}).setdefault(ro, 0)
        seen[en][ro] += 1
    terms = {en: max(v, key=v.get) for en, v in seen.items()}
    index = {}
    for en in terms:
        index.setdefault(en.split()[0], []).append(en)
    return terms, index


_CAPS = None


def proper(word):
    """A single word counts as a name (Talmberg, Radzig, Groschen) only if, inside sentences of the KCD1 English, it is
    written capitalised at least 80% of the time; "Well", "You", "Examine" are capitalised only at sentence start."""
    global _CAPS
    if _CAPS is None:
        _CAPS = {}
        for f in glob.glob(str(ROOT / "src" / "en" / "*.xml")):
            for _, _, en in ROW.findall(open(f, encoding="utf-8").read()):
                for m in re.finditer(r"(?<=[a-z,;] )([A-Za-z][\w'’-]+)", en):
                    w = m.group(1)
                    c = _CAPS.setdefault(w.lower(), [0, 0])
                    c[0 if w[0].isupper() else 1] += 1
    up, low = _CAPS.get(word.lower(), (0, 0))
    return up + low >= 2 and up / (up + low) >= 0.8


def lot_glossary(texts, terms, index):
    found = {}
    for t in texts:
        for w in set(re.findall(r"[A-Z][\w'’-]*", t)):
            for en in index.get(w, ()):
                if en not in found and re.search(r"(?<![\w])" + re.escape(en) + r"(?![\w])", t):
                    found[en] = terms[en]
    return dict(list(found.items())[:80])


def speaker(key):
    p = key.split("_")
    return p[3] if len(p) > 4 and p[0].startswith("t") and p[1].startswith("s") else None


def lots(rows, size, limit=6000):
    out, cur, chars = [], [], 0
    for r in rows:
        if cur and (len(cur) >= size or chars + len(r[1]) > limit):
            out.append(cur)
            cur, chars = [], 0
        cur.append(r)
        chars += len(r[1])
    return out + ([cur] if cur else [])


def run(pas, size):
    con = db()
    if pas == "haiku":
        rows = con.execute("SELECT id, en, kind, key, ro FROM units WHERE status IN ('new', 'fail') ORDER BY kind, id").fetchall()
        model = A.MODEL
    else:
        todo = flagged(con)
        rows = [r for r in con.execute("SELECT id, en, kind, key, ro FROM units WHERE kind = 'dialog' AND status = 'ok' "
                                       "ORDER BY id").fetchall() if r[0] in todo]
        model = "claude-sonnet-5-5"
    terms, index = kcd2_terms()
    reqs, plan = [], {}
    for kind in ("text", "dialog"):
        for b, lot in enumerate(lots([r for r in rows if r[2] == kind], size)):
            lines, meta = [], []
            for i, (uid, en, k_, key, ro) in enumerate(lot):
                men, toks = K.mask(en)
                line = {"id": i, "en": men}
                sp = speaker(key) if kind == "dialog" else None
                if sp:
                    line["vorbitor"] = sp
                if pas == "sonnet" and ro:
                    mro = ro
                    for j, t in enumerate(toks, 1):
                        mro = mro.replace(t, f"⟦{j}⟧", 1)
                    line["ro"] = mro
                lines.append(line)
                meta.append([uid, toks, en])
            system = SONNET if pas == "sonnet" else (DIALOG if kind == "dialog" else TEXT)
            cid = f"{pas[0]}{kind[0]}{b}"
            reqs.append(Request(custom_id=cid, params=MessageCreateParamsNonStreaming(
                model=model, max_tokens=16000,
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": json.dumps(
                    {"glosar": lot_glossary([m[2] for m in meta], terms, index), "lines": lines}, ensure_ascii=False)}],
                output_config={"effort": "medium", "format": {"type": "json_schema", "schema": llm.LINES_SCHEMA}})))
            plan[cid] = meta
    PLANS.mkdir(exist_ok=True)
    batch = A.client().messages.batches.create(requests=reqs)
    (PLANS / f"{batch.id}.json").write_text(json.dumps({"pass": pas, "model": model, "plan": plan}, ensure_ascii=False),
                                            encoding="utf-8")
    print(f"submitted {batch.id}: {pas}, {len(reqs)} requests, {len(rows)} units", flush=True)
    A.wait(batch.id)
    apply(batch.id)


EXTRA = re.compile(r"\bales?\b|\bkurv\w*|[ěščřžůĚŠČŘŽŮ]", re.I)  # ale = beer; Kurva and Czech lines stay Czech


def flagged(con):
    return {uid for uid, en, flag in con.execute("SELECT id, en, flag FROM units WHERE kind = 'dialog' AND status = 'ok'")
            if flag == "G" or SWEAR.search(en) or EXTRA.search(en)}


def problem(en, new, toks):
    if re.search(r"⟦\d+⟧", new):
        return "markup left"
    if sorted(K.PROTECT.findall(new)) != sorted(toks):
        return "markup differs"
    if len(SEP.findall(en)) != len(SEP.findall(new)):
        return "line breaks"
    if not new.strip():
        return "empty"
    if RAW.search(new):
        return "raw xml"
    # truncation guard for long texts; short lines are often much shorter in Romanian ("You're repeating yourself." ->
    # "Te repeți.") or longer for UI labels ("Kick (in fistfight)")
    if len(en) >= 80 and not 0.5 < len(new) / len(en) < 2.2:
        return "length"
    if len(en) < 80 and not 0.25 < len(new) / max(len(en), 1) < 3.5:
        return "length"
    return None


def restore_breaks(en, new):
    so, parts = SEP.findall(en), SEP.split(new)
    return "".join(p + (so[k] if k < len(so) else "") for k, p in enumerate(parts)) if len(parts) - 1 == len(so) else new


def apply(batch_id):
    meta_all = json.loads((PLANS / f"{batch_id}.json").read_text(encoding="utf-8"))
    pas, plan = meta_all["pass"], meta_all["plan"]
    out = PLANS / f"{batch_id}.results.jsonl"
    url = A.client().messages.batches.retrieve(batch_id).results_url
    subprocess.run(["curl", "-sS", "--retry", "5", "--retry-all-errors", "-o", str(out),
                    "-H", f"x-api-key: {llm.anthropic_key()}", "-H", "anthropic-version: 2023-06-01", url], check=True)
    con = db()
    ok = failed = lost = flags = 0
    why = {}
    tok = {"in": 0, "cw": 0, "cr": 0, "out": 0}
    for line in open(out, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        meta = plan.get(r["custom_id"], [])
        if r["result"]["type"] != "succeeded":
            lost += len(meta)
            continue
        msg = r["result"]["message"]
        u = msg["usage"]
        tok["in"] += u.get("input_tokens") or 0
        tok["cw"] += u.get("cache_creation_input_tokens") or 0
        tok["cr"] += u.get("cache_read_input_tokens") or 0
        tok["out"] += u.get("output_tokens") or 0
        try:
            got = {x.get("id"): (x.get("f", ""), x.get("m", "")) for x in json.loads(
                next(c["text"] for c in msg["content"] if c["type"] == "text")).get("t", [])}
        except (ValueError, StopIteration):
            lost += len(meta)
            continue
        for i, (uid, toks, en) in enumerate(meta):
            if i not in got:
                lost += 1
                continue
            f, m = got[i]
            new = K.unmask(f, toks).replace("ş", "ș").replace("ţ", "ț").replace("Ş", "Ș").replace("Ţ", "Ț")
            lead, trail = en[:len(en) - len(en.lstrip())], en[len(en.rstrip()):]
            new = restore_breaks(en, lead + new.strip() + trail)
            p = problem(en, new, toks)
            if p:
                why[p] = why.get(p, 0) + 1
                failed += 1
                if pas == "haiku":
                    con.execute("UPDATE units SET status = 'fail' WHERE id = ?", (uid,))
                continue
            if pas == "haiku":
                flag = "G" if (m or "").strip().upper().startswith("G") else None
                flags += flag == "G"
                con.execute("UPDATE units SET ro = ?, status = 'ok', flag = ? WHERE id = ?", (new, flag, uid))
            else:
                con.execute("UPDATE units SET ro_haiku = ro, ro = ?, status = 'sonnet' WHERE id = ?", (new, uid))
            ok += 1
    con.commit()
    p = llm.PRICES[meta_all["model"]]
    usd = (tok["in"] * p[0] + tok["cw"] * p[1] + tok["cr"] * p[2] + tok["out"] * p[3]) / 1e6 / 2
    print(f"applied {batch_id} ({pas}): {ok} ok, {failed} failed {why}, {lost} lost, {flags} flagged G; cost ${usd:.2f}")


def stats():
    con = db()
    print(dict(con.execute("SELECT status, count(*) FROM units GROUP BY status")))
    print("flagged for sonnet:", len(flagged(con)))


if __name__ == "__main__":
    a = sys.argv[1:]
    size = int(a[a.index("--size") + 1]) if "--size" in a else 40
    if "--model" in a:  # e.g. Sonnet for the long codex/book texts Haiku keeps truncating
        A.MODEL = a[a.index("--model") + 1]
    {"prepare": prepare, "stats": stats}.get(a[0], lambda: None)()
    if a[0] == "run":
        run(a[1], size)
    elif a[0] == "apply":
        apply(a[1])
