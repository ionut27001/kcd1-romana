# Cum corectezi traducerea

## 1. Găsește textul

Toată traducerea e în `translations/`, câte un fișier pentru fiecare tabel al jocului:

- `text_ui_dialog.*.json`: dialoguri și subtitrări (cheia conține scena și vorbitorul, de ex. `t19093_s35644_0_p_henry_...`)
- `text_ui_quest.*.json`: misiuni și jurnal
- `text_ui_items.*.json`: obiecte și cărți (paginile cărților au etichete `&lt;paragraph&gt;`)
- `text_ui_menus.*.json`, `text_ui_soul.*.json`, `text_ui_misc.*.json`...: meniuri, talente, atribute, codex

Cel mai simplu: apasă `T` pe pagina repository-ului (sau folosește căutarea GitHub) și caută textul **în engleză**
sau o bucată din traducerea greșită.

## 2. Editează doar câmpul `"ro"`

```json
{
 "key": "t19093_s35644_0_p_henry_he_t9Nw",
 "en": "I wonder what Theresa's up to? I haven’t seen her for a long time. Maybe I could go and see her...",
 "ro": "Oare ce mai face Theresa? N-am văzut-o de mult. Poate ar trebui s-o caut..."
}
```

- Schimbi **doar** `"ro"`. **Nu** schimba `"key"`, `"en"` sau `"table"`.
- Păstrează exact marcajele: comenzile (`$sprint;`, `{$attack_primary;|...}`), `%s`, `\n`, indicațiile de voce
  (`&lt;sighs&gt;`, rămân în engleză) și etichetele cărților (`&lt;paragraph&gt;`, `&lt;br/&gt;`...).
  Verificarea automată respinge textul dacă lipsesc.
- Scrie **cu diacritice** (ă, â, î, ș, ț cu virgulă). Varianta fără diacritice se face automat.
- Un text englezesc care apare de mai multe ori are aceeași traducere peste tot; ajunge să-l corectezi o dată.

Din browser: deschizi fișierul pe GitHub, apeși creionul (Edit), modifici, apoi **Commit changes → Create a new branch
→ Propose changes**. GitHub face singur fork-ul și Pull Request-ul.

## 3. Regulile, pe scurt

Detaliile sunt în [glossary/TERMENI.md](glossary/TERMENI.md) (are prioritate) și [glossary/GLOSAR.md](glossary/GLOSAR.md).

- **Numele personajelor rămân ca în engleză**: Matthew, Theresa, Peter, Deutsch, inclusiv poreclele (Tess,
  Matty). Doar sfinții și regii istorici au forme românești (Sfântul Petru, Venceslau).
- **Henry e bărbat**: tot ce spune despre el și tot ce i se spune, la masculin.
- **Nu urca deasupra englezei**: dacă engleza folosește un cuvânt obișnuit, și româna folosește unul obișnuit
  („mereu”, nu „pururea”; „a vorbi”, nu „a grăi”). Nici argou sau anglicisme („gardă de corp”, nu „bodyguard”).
- Replicile sună vorbit: „o să fac”, nu „voi face”; „asta”, nu „această”; „ca să”, nu „pentru a”.
- Termenii din glosar se scriu **exact** așa (Carismă, Vorbire, jupân, groschen, șperaclu). Dacă vrei să schimbi un
  termen, deschide întâi un Issue: el apare în multe locuri.
- Așezările din joc rămân (Skalitz, Rattay, Talmberg, Sasau); exonimele românești consacrate se folosesc (Praga, Boemia).
