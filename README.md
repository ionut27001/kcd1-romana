# Kingdom Come: Deliverance — Traducere în limba română

Traducere neoficială, făcută de fani, a **întregului text** din Kingdom Come: Deliverance: dialoguri și subtitrări,
misiuni, obiecte, meniuri, cărțile care se pot citi și codexul. Aproximativ 81.000 de intrări. Vocile rămân cum le ai.
Termenii sunt aceiași ca în [traducerea pentru KCD2](https://github.com/ionut27001/kcd2-romana), ca cele două jocuri
să se lege.

**Descarcă mod-ul:** Nexus Mods: https://www.nexusmods.com/kingdomcomedeliverance/mods/2436 (sau din [Releases](../../releases))

Acest repository e locul unde **oricine poate corecta traducerea**: o replică ciudată, un gen greșit, un termen
tradus inconsecvent. Corecturile acceptate intră în următoarea versiune a mod-ului.

## Cum funcționează mod-ul

Jocul nu are slot pentru română, așa că mod-ul folosește slotul **Turkish**: în joc alegi
**Settings → Language → Text: Română**. Engleza rămâne intactă. La instalare (Vortex) alegi dacă vrei diacritice.

La prima pornire cu mod-uri, KCD1 poate muta folderul `Mods` în `mods_old`. Dacă vezi limba în turcă, mută
`traducere_romana` înapoi în `Mods` și pornește jocul din nou.

## Cum ajuți

- **Ai găsit o greșeală, dar nu vrei să editezi fișiere?** Deschide un
  [Issue „Greșeală de traducere”](../../issues/new/choose): scrii unde apare, ce e greșit și ce ai propune.
  O captură de ecran ajută mult.
- **Vrei să corectezi direct?** Vezi [CONTRIBUTING.md](CONTRIBUTING.md): găsești textul în `translations/`, editezi
  câmpul `"ro"` și trimiți un Pull Request. Se poate face și din browser, fără să instalezi nimic.

## Ce e în repository

| Folder | Ce conține |
|---|---|
| `translations/` | Tot textul, câte un fișier JSON pentru fiecare tabel al jocului: cheia, originalul (`en`) și traducerea (`ro`). Tabelele mari sunt împărțite în bucăți `.001.json`, `.002.json`... |
| `glossary/TERMENI.md` | Termenii obligatorii (atribute, îndemânări, interfață, obiecte), comuni cu KCD2 |
| `glossary/GLOSAR.md` | Toponime, persoane, titluri, termeni de epocă, ortografie, markup |
| `tools/check.py` | Verificarea automată rulată pe fiecare Pull Request |
| `pipeline/` | Scripturile cu care e tradus textul și construit mod-ul (pentru cine e curios) |

## Cum a fost făcută

Textul a fost tradus cu modele de limbaj AI: Claude Haiku pe tot jocul, Claude Sonnet pe glume, înjurături și
replicile în cehă. Tot ce era identic cu KCD2 a preluat traducerea de acolo, iar fiecare lot a primit termenii
KCD2 care apar în el. Apoi verificare automată (markup, substituenți, lungime), numele personajelor puse înapoi exact
ca în engleză și testat în joc. Tocmai de aceea ajută orice corectură venită de la oameni care joacă.

## Alte traduceri și susținere

Am tradus și [Kingdom Come: Deliverance II](https://github.com/ionut27001/kcd2-romana),
[Cyberpunk 2077](https://github.com/ionut27001/cp77-romana),
[Assassin's Creed Shadows](https://github.com/ionut27001/acs-romana) și
[Palworld](https://github.com/ionut27001/palworld-romana). Vrei alt joc în română? Scrie-mi pe Nexus în
comentarii. Dacă vrei să mă susții, îmi poți face cadou jocul pe care vrei să-l traduc, pe
[Steam](https://steamcommunity.com/profiles/76561199120542317). Nu e obligatoriu: traducerile rămân gratuite.

Licențe și drepturi: vezi [NOTICE.md](NOTICE.md).
