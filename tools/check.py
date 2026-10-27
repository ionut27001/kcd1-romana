"""Checks translation files: valid JSON, nothing missing, and the game markup kept.

- key bindings and variables ($sprint, %s, {0}) and literal \\n: same as in the English line; in {$a;|label} the
  label may be translated
- voice cues (&lt;sigh&gt;, &lt;Hmm&gt;): none dropped, none invented
- book pages (&lt;paragraph&gt;, &lt;poem&gt;...): every tag kind used in the English is still there
- diacritics with a comma (ș ț), never the cedilla forms (ş ţ)
- no raw <, > or & (the text sits XML-escaped inside the game tables)

Usage: python tools/check.py [file ...]   (no arguments = every file under translations/)
"""
import collections
import json
import pathlib
import re
import sys

BINDINGS = re.compile(r"\$[A-Za-z_]+;?|%[0-9.]*[sdif](?![A-Za-z])|\{\d+\}|\\n")
TAG = re.compile(r"&lt;/?([A-Za-z]+)(?:(?!&gt;).)*&gt;")
BOOK = ("paragraph", "poem", "heading", "title", "subtitle", "newpage", "img", "years", "br", "accent")
FORMAT = ("br", "p", "b", "i", "strong", "accent", "font")  # layout tags, not voice cues
RAW = re.compile(r"<|>|&(?!(?:lt|gt|amp|quot|apos|nbsp|#\d+);)")  # the text is XML-escaped inside the game tables
ROOT = pathlib.Path(__file__).resolve().parent.parent


def tags(text):
    """opening tags only: a closing tag the English itself lost (a few game strings end in a broken "/&gt;") is fine"""
    return [m.group(1) for m in TAG.finditer(text or "") if not m.group(0).startswith("&lt;/")]


def problems_for(en, ro):
    out = []
    if en.strip() and not ro.strip():
        out.append("empty translation")
    if RAW.search(ro):
        out.append(f"raw XML character (breaks the table): {RAW.findall(ro)[:3]}")
    if ro != en and re.search(r"[şţŞŢ]", ro):  # Turkish names in the credits keep ş
        out.append("cedilla ş/ţ instead of ș/ț")
    if collections.Counter(BINDINGS.findall(en)) != collections.Counter(BINDINGS.findall(ro)):
        out.append(f"key bindings/variables differ: {BINDINGS.findall(en)} vs {BINDINGS.findall(ro)}")
    et, rt = tags(en), tags(ro)
    if any(t.lower() in BOOK for t in et):
        missing = {t for t in et if t.lower() in BOOK} - set(rt)
        if missing:
            out.append(f"book tags missing: {sorted(missing)}")
    else:  # a voice cue dropped or invented; adapted onomatopoeia ("glogloglo" -> "gluglug") is fine
        ec, rc = {t for t in et if t.lower() not in FORMAT}, {t for t in rt if t.lower() not in FORMAT}
        if bool(ec) != bool(rc):
            out.append(f"voice cues differ: {sorted(ec)} in English, {sorted(rc)} in Romanian")
    return out


def check(path):
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{path}: invalid JSON ({e})"]
    if not isinstance(doc, dict) or "table" not in doc or not isinstance(doc.get("entries"), list):
        return [f"{path}: expected {{\"table\": ..., \"entries\": [...]}}"]
    found = []
    for e in doc["entries"]:
        for field in ("ro", "ro_clasic"):
            if field in e:
                if not isinstance(e.get(field), str) or not isinstance(e.get("en"), str):
                    found.append(f"{path} {e.get('key')}: \"en\" and \"{field}\" must be text")
                    continue
                found += [f"{path} {e.get('key')} [{field}]: {p}" for p in problems_for(e["en"], e[field])]
    return found


def main():
    files = [pathlib.Path(a) for a in sys.argv[1:] if a.endswith(".json")] or \
        sorted((ROOT / "translations").glob("*.json"))
    problems = [p for f in files if f.exists() for p in check(f)]
    for p in problems:
        print(p)
    print(f"{len(files)} files checked, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
