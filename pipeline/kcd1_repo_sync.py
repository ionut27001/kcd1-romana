"""Sync the public GitHub repo (D:\\kcd1-ro\\github\\kcd1-romana) with kcd1.db.

export: translations/<table>[.NNN].json = {"table", "entries": [{"key", "en", "ro"}]}, at most 2,000 entries per file
        (GitHub's web editor). "en" is the English the game shows (the third cell of the English tables); rows
        without English text are left out. Also copies the build scripts.
import: a changed "ro" goes back into units, keyed by the English: the same English text has one translation
        everywhere, so a fix in one place applies to every row that uses it.

Usage: python -I -X utf8 kcd1_repo_sync.py export | import
"""
import glob
import json
import pathlib
import shutil
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kcd1_build import ROW, SRC  # noqa: E402

ROOT = pathlib.Path(r"D:\kcd1-ro")
REPO = ROOT / "github" / "kcd1-romana"
CHUNK = 2000


def tables():
    for f in sorted(glob.glob(str(SRC / "*.xml"))):
        text = open(f, encoding="utf-8", newline="").read()
        yield pathlib.Path(f).name, [(m.group(2), m.group(6)) for m in ROW.finditer(text)]


def translations(con):
    return {en: ro for en, ro in con.execute(
        "SELECT en, ro FROM units WHERE ro IS NOT NULL AND status IN ('ok', 'kcd2', 'sonnet')")}


def export():
    con = sqlite3.connect(ROOT / "db" / "kcd1.db")
    ro = translations(con)
    out = REPO / "translations"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    files = n = 0
    for t, rows in tables():
        entries = [{"key": k, "en": en, "ro": "Română" if k == "ui_turkish" else ro.get(en, en)}
                   for k, en in rows if en.strip()]
        parts = [entries[i:i + CHUNK] for i in range(0, len(entries), CHUNK)]
        stem = t.removesuffix(".xml")
        for i, part in enumerate(parts, 1):
            fn = f"{stem}.{i:03}.json" if len(parts) > 1 else f"{stem}.json"
            (out / fn).write_text(json.dumps({"table": t, "entries": part}, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8", newline="\n")
            files += 1
        n += len(entries)
    pipe = REPO / "pipeline"
    pipe.mkdir(exist_ok=True)
    for f in ("kcd1_translate.py", "kcd1_build.py", "fix_names.py", "kcd1_repo_sync.py"):
        shutil.copy2(ROOT / "pipeline" / f, pipe / f)
    print(f"exported {n} rows in {files} files")


def import_():
    con = sqlite3.connect(ROOT / "db" / "kcd1.db")
    ro = translations(con)
    changed = 0
    for f in sorted((REPO / "translations").glob("*.json")):
        for e in json.loads(f.read_text(encoding="utf-8"))["entries"]:
            if e["key"] != "ui_turkish" and e["ro"] != ro.get(e["en"], e["en"]):
                con.execute("UPDATE units SET ro = ?, status = 'ok' WHERE en = ?", (e["ro"], e["en"]))
                ro[e["en"]] = e["ro"]
                changed += 1
    con.commit()
    print(f"imported {changed} changed texts from the repo")


if __name__ == "__main__":
    {"export": export, "import": import_}[sys.argv[1]]()
