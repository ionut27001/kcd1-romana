"""Build the KCD1 Romanian mod from kcd1.db: Mods\\traducere_romana\\Localization\\Turkish_xml.pak (the game has no
Romanian slot, the mod takes Turkish, like the KCD2 one), in two variants (with / without diacritics), plus a FOMOD
installer for Vortex and a zip for Nexus.

Each table is the English one (all rows, including the ones the Turkish tables lack) with the second cell = final
English and the third = Romanian (English where there is no translation). "ui_turkish" becomes "Română".
The language list in the settings is drawn with the texts of the language the menu is in (usually English, where
"ui_turkish" is "Türkçe"), so the mod also ships the English tables unchanged except that row ("Română").
Checks: every table parses as XML, same row count and keys as English, no raw markup.

Usage: python -I -X utf8 kcd1_build.py [--version 1.0.0]
"""
import glob
import os
import pathlib
import re
import shutil
import sqlite3
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = pathlib.Path(r"D:\kcd1-ro")
SRC = ROOT / "src" / "en"
OUT = ROOT / "dist"
ROW = re.compile(r"(<Row>\s*<Cell>)(.*?)(</Cell>\s*<Cell>)(.*?)(</Cell>\s*<Cell>)(.*?)(</Cell>\s*</Row>)", re.S)
STRIP = str.maketrans("ăâîșțşţĂÂÎȘȚŞŢ", "aaiststAAISTST")
VARIANTS = {"cu-diacritice": False, "fara-diacritice": True}

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
  <info>
    <name>Traducere în română</name>
    <modid>traducere_romana</modid>
    <description>Traducere în limba română pentru Kingdom Come: Deliverance.</description>
    <author>ionut270</author>
    <version>{v}</version>
    <created_on>2026-10-27</created_on>
  </info>
  <supports>
    <kcd_version>1.9.*</kcd_version>
  </supports>
</kcd_mod>
"""

FOMOD_INFO = """<?xml version="1.0" encoding="UTF-8"?>
<fomod>
  <Name>Traducere în română - Kingdom Come: Deliverance</Name>
  <Author>ionut270</Author>
  <Version MachineVersion="{v}">{v}</Version>
  <Description>Traducere completă în limba română: dialoguri, misiuni, obiecte, meniuri, codex. Jocul nu are un slot de română, așa că mod-ul îl folosește pe cel turcesc și îl redenumește „Română" în meniul de limbi.</Description>
  <Groups>
    <element>Translation</element>
    <element>User Interface</element>
  </Groups>
</fomod>
"""

FOMOD_CONFIG = """<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://qconsulting.ca/fo3/ModConfig5.0.xsd">
  <moduleName>Traducere în română</moduleName>
  <requiredInstallFiles>
    <file source="traducere_romana\\mod.manifest" destination="traducere_romana\\mod.manifest" priority="0" />
    <file source="traducere_romana\\Localization\\English_xml.pak" destination="traducere_romana\\Localization\\English_xml.pak" priority="0" />
  </requiredInstallFiles>
  <installSteps order="Explicit">
    <installStep name="Diacritice">
      <optionalFileGroups order="Explicit">
        <group name="Diacritice" type="SelectExactlyOne">
          <plugins order="Explicit">
            <plugin name="Cu diacritice (recomandat)">
              <description>ă â î ș ț, ca în română. Fonturile jocului le au.</description>
              <files>
                <file source="optiuni\\cu-diacritice.pak" destination="traducere_romana\\Localization\\Turkish_xml.pak" priority="0" />
              </files>
              <typeDescriptor><type name="Recommended" /></typeDescriptor>
            </plugin>
            <plugin name="Fără diacritice">
              <description>Text fără diacritice, pentru cine preferă să citească așa.</description>
              <files>
                <file source="optiuni\\fara-diacritice.pak" destination="traducere_romana\\Localization\\Turkish_xml.pak" priority="0" />
              </files>
              <typeDescriptor><type name="Optional" /></typeDescriptor>
            </plugin>
          </plugins>
        </group>
      </optionalFileGroups>
    </installStep>
  </installSteps>
</config>
"""


def lookup(ro, en):
    """the Romanian for a game text; the db keys multi-line texts with \\n, a few tables (loading hints, prayers)
    use \\r\\n, which kept 243 texts in English in 1.0.0"""
    if en in ro:
        return ro[en]
    lf = en.replace("\r\n", "\n")
    return ro[lf].replace("\n", "\r\n") if lf != en and lf in ro else None


def build_pak(ro, strip, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(glob.glob(str(SRC / "*.xml"))):
            text = open(f, encoding="utf-8", newline="").read()

            def repl(m):
                key, en = m.group(2), m.group(6)
                r = "Română" if key == "ui_turkish" else (lookup(ro, en) or en)
                if strip and r != en and key != "ui_turkish":
                    r = r.translate(STRIP)
                return m.group(1) + key + m.group(3) + en + m.group(5) + r + m.group(7)
            new = ROW.sub(repl, text)
            old_rows, new_rows = ROW.findall(text), ROW.findall(new)
            assert len(old_rows) == len(new_rows), f
            assert all(a[1] == b[1] for a, b in zip(old_rows, new_rows)), f
            root = ET.fromstring(new.encode("utf-8"))
            assert len(root.findall("Row")) == len(re.findall(r"<Row>", text)), f
            z.writestr(os.path.basename(f), new.encode("utf-8"))


def build_english(dst):
    """the game's English tables as they are, only the name of the Turkish slot in the language list changed"""
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(glob.glob(str(SRC / "*.xml"))):
            text = open(f, encoding="utf-8", newline="").read()
            new = ROW.sub(lambda m: m.group(0) if m.group(2) != "ui_turkish" else
                          m.group(1) + "ui_turkish" + m.group(3) + "Română" + m.group(5) + "Română" + m.group(7), text)
            assert (new != text) == (os.path.basename(f) == "text_ui_menus.xml"), f
            ET.fromstring(new.encode("utf-8"))
            z.writestr(os.path.basename(f), new.encode("utf-8"))


def main():
    v = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "1.0.0"
    con = sqlite3.connect(ROOT / "db" / "kcd1.db")
    ro = {en: r for en, r in con.execute("SELECT en, ro FROM units WHERE ro IS NOT NULL AND status IN ('ok', 'kcd2', 'sonnet')")}
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "optiuni").mkdir(parents=True)
    (OUT / "traducere_romana").mkdir()
    (OUT / "fomod").mkdir()
    for name, strip in VARIANTS.items():
        p = OUT / "optiuni" / f"{name}.pak"
        build_pak(ro, strip, p)
        print(f"{p.name}: {p.stat().st_size / 1e6:.1f} MB")
    (OUT / "traducere_romana" / "Localization").mkdir()
    build_english(OUT / "traducere_romana" / "Localization" / "English_xml.pak")
    (OUT / "traducere_romana" / "mod.manifest").write_text(MANIFEST.format(v=v), encoding="utf-8")
    (OUT / "fomod" / "info.xml").write_text(FOMOD_INFO.format(v=v), encoding="utf-8")
    (OUT / "fomod" / "ModuleConfig.xml").write_text(FOMOD_CONFIG, encoding="utf-8")
    if (ROOT / "mod_README.md").exists():
        shutil.copy2(ROOT / "mod_README.md", OUT / "README.md")
    for f in ("GLOSAR.md", "TERMENI.md"):
        shutil.copy2(pathlib.Path(r"D:\kcd2-ro\orig\v121") / f, OUT / f)
    total = con.execute("SELECT count(*) FROM units").fetchone()[0]
    done = len(ro)
    print(f"translated {done}/{total} unique texts")
    z = ROOT / f"KCD1 Traducere Romana {v}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(OUT.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(OUT).as_posix())
    print(f"{z} ({z.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
