# Glosar: traducere română KCD1 (aceiași termeni ca la KCD2)

Deciziile de mai jos se aplică identic în toate batch-urile. Când apare un termen
nou care se va repeta, se adaugă aici înainte de a fi folosit.

## Principiu general

Registrul e de **cronică medievală românească**, nu română modernă neutră și nici
arhaizare forțată. Concret: topică ușor inversată, „a grăi/a povesti/a se
întâmpla", perfect compus, fără neologisme moderne (`a realiza`, `situație`,
`a gestiona`, `problemă`). Textul trebuie să sune ca o carte din 1403, dar să fie
citibil fără efort.

## Toponime

Regula: **numele reale cu exonim românesc consacrat se traduc**; **numele de
așezări din lumea jocului rămân neschimbate**, fiindcă harta și interfața rămân
în engleză și jucătorul trebuie să le poată lega între ele.

| Engleză | Română | Notă |
|---|---|---|
| Bohemia | Boemia | |
| Moravia | Moravia | |
| Prague | Praga | |
| Jerusalem | Ierusalim | |
| Rome | Roma | |
| Hungary | Ungaria | |
| Kuttenberg | Kuttenberg | pe hartă, nu se traduce |
| Sedletz | Sedletz | idem |
| Skalitz | Skalitz | idem |
| Trosky | Trosky | idem |
| Rattay, Talmberg, Neuhof | neschimbate | idem |
| Holy Roman Empire | Sfântul Imperiu Roman | |
| Middle Ages | Evul Mediu | |

## Persoane

| Engleză | Română |
|---|---|
| Wenceslas (IV) | Venceslau (al IV-lea) |
| Charles (IV) | Carol (al IV-lea) |
| Sigismund of Luxembourg | Sigismund de Luxemburg |
| Jobst | Jobst |
| Jan Hus | Jan Hus |
| Henry | Henry (protagonistul, se păstrează) |
| Hans Capon | Hans Capon |
| Saladin | Saladin |
| Ciappelletto, Ser | Ciappelletto, ser (formă italiană, se păstrează) |

**Personajele jocului își păstrează numele exact ca în engleză**, inclusiv poreclele din dialog: Matthew
(Matty, Mathew), Theresa (Tess), Peter, Esther, Nicholas, Deutsch, Zbyshek. Se declină doar cu articol separat:
„lui Matthew”, „Theresei”. Doar papii, sfinții și regii istorici primesc forma românească: Sfântul Petru,
Biserica Sfântul Matei, Venceslau, Carol.

## Titluri și ranguri

| Engleză | Română | Notă |
|---|---|---|
| Lord (nobil) | jupân | cognat istoric direct, potrivit pentru nobilime slavă |
| Sir | Sir | se păstrează, ca în traducerile românești de ficțiune medievală |
| Lord (Dumnezeu) | Domnul | |
| King / Emperor | rege / împărat | |
| Bailiff | jude | magistratul satului |
| Burgrave | burgrav | |
| Margrave | markgraf | |
| Master (meșteșugar) | meșter | |
| Master (cărturar) | magistru | |
| Brother (călugăr) | frate | |
| Abbot | stareț | |
| Elders (ai orașului) | bătrânii orașului | |
| Town council | sfatul orașului | |

## Termeni de epocă

| Engleză | Română | Notă |
|---|---|---|
| Groschen | gros, pl. groși | termen monetar românesc real |
| Mint | monetărie | |
| Urburers | urburari | de la „urbură", darea minieră, termen real |
| Hussite(s) | husit(i) | |
| Cistercian | cistercian | |
| Inquisition | Inchiziția | |
| Council (bisericesc) | conciliu | |
| Gravedigger | gropar | |
| Caravanserai | caravanserai | |
| Brigands | tâlhari | |
| Thrush (poreclă) | Sturzul | |

## Reguli ortografice

- Diacritice **cu virgulă**: `ș` U+0219, `ț` U+021B, `Ș` U+0218, `Ț` U+021A.
  Niciodată variantele cu sedilă (`ş`, `ţ`), `verify.py` le respinge.
- Ghilimele românești: `„text"` (U+201E jos, U+201D sus). Ambele există în fonturi.
- `â` în interiorul cuvântului, `î` la început și la sfârșit (normă 1993).

## Markup: regulă absolută

Etichetele `<paragraph>`, `<heading>`, `<accent>`, `<italic>`, `<subtitle>`,
`<poem>`, `<title>`, `<inc>`, `<years>`, `<br/>`, `<newpage/>`, `<img .../>` se
păstrează **identic, în aceeași ordine și în același număr**. Se traduce doar
textul dintre ele. `verify.py` compară semnătura de etichete între engleză și
română și pică build-ul dacă diferă.
