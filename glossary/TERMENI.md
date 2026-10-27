# Termeni obligatorii

Fiecare termen de mai jos are **o singură** traducere. Se injectează în promptul
fiecărui apel, fiindcă apelurile sunt independente și altfel același cuvânt iese
diferit de la un ecran la altul, „Charisma" a ieșit și „Carisma", și „farmec";
„Moonshine" a ieșit în șase feluri, dintre care două fără sens.

Regula pentru tot ce nu e aici: **cuvânt românesc real, cu sensul lui real**. Dacă
nu ești sigur că un arhaism există, folosește cuvântul obișnuit. „Reforgeat",
„meșteșugărit", „a se zvânta de sânge" nu sunt română.

## Regula de registru: nu urca deasupra englezei

Engleza jocului e simplă acolo unde poate fi: spune **Groschen**, nu „groats";
spune **Lockpick**, nu „picklock iron". Traducerea trebuie să facă la fel.

Greșeala pe care am făcut-o și am corectat-o: *Groschen* devenise „groși" și
*Lockpick* „cârlig de descuiat", ambele cuvinte reale, ambele mai vechi decât
originalul. Registrul de epocă vine din **ce spun personajele**, nu din a alege
sinonimul cel mai prăfuit pentru fiecare obiect.

Test rapid: dacă engleza folosește un cuvânt pe care orice vorbitor îl știe,
româna trebuie să folosească și ea unul pe care orice vorbitor îl știe.

Aceeași greșeală a doua oară, în cărți: promptul de registru cerea explicit „a
grăi", „a purcede", „a se cădea" și interzicea vocabularul modern. Rezultatul,
*ever* → „pururea", *skill* → „dibăcie", *a sure refuge* → „un liman sigur". Toate
sunt cuvinte românești reale; toate cer cititorului un pas de decodare pe care
originalul nu-l cerea. Culoarea de epocă vine din **ce spune textul** și din fraze
întregi, nu din alegerea sinonimului celui mai prăfuit.

| engleză | nu | da |
|---|---|---|
| ever | pururea | mereu |
| the first | cel dintâi | primul |
| in Him | întru El | în El |
| skill | dibăcie | iscusință |
| toil | osteneală | trudă |
| quickly | degrabă | repede |
| to speak | a grăi | a vorbi |

`tools/archaisms.py` numără marcajele astea pe felii. Codexul era la 47%, cărțile
la 44%; dialogul, interfața și obiectele, sub 1%.

## Codexul nu e o carte

Cărțile sunt obiecte din lume, scrise de oameni din 1403. **Codexul e jocul care
îți explică ție lumea**, engleza lui e proză enciclopedică simplă. Multă vreme
codexul a folosit registrul cărților (`REGISTERS['codex'] = REGISTERS['books']`),
de unde „este cu cale să se ia seama" pentru *it is important to consider* și
„vreme îndestulată" pentru *ample time*. Codexul se scrie în română actuală, ca un
articol bun de istorie. „Sursă", „informație", „perioadă", „în general" sunt
corecte acolo.

## Interfață

| engleză | română |
|---|---|
| Map | Hartă |
| Journal | Jurnal |
| Inventory | Inventar |
| Player | Jucător |
| Crafting | Meșteșug |
| Codex | Codex |
| Quest | misiune (niciodată „quest") |
| Task | sarcină |
| Skills | Îndemânări |
| Stats | Atribute |
| Buffs | Efecte |
| Combos | Înlănțuiri |
| Perk | talent |
| Sidekicks | Tovarăși |
| Completed / Failed | Îndeplinite / Eșuate |

## Atribute și îndemânări

| engleză | română |
|---|---|
| Strength | Forță |
| Agility | Agilitate |
| Vitality | Vitalitate |
| Speech | Vorbire |
| Charisma | Carismă (niciodată „farmec") |
| Conditioning | Condiție |
| Warfare | Război |
| Marksmanship | Ochire |
| Horsemanship | Călărie |
| Craftsmanship | Meșteșug |
| Scholarship | Învățătură |
| Stealth | Furișare |
| Alchemy | Alchimie |
| Herbalism | Ierburi |
| Houndmaster | Stăpân de câini |
| Maintenance | Întreținere |
| Drinking | Băutură |
| Reading | Citit |
| Lockpicking | Descuiat de lacăte |
| Pickpocketing | Buzunărit |
| Haggling | Târguială |
| Swordsmanship | Mânuirea sabiei |
| Unarmed | Luptă fără arme |
| Heavy Weapons | Arme grele |
| Polearms | Arme cu mâner lung |
| Bow / Crossbow | Arc / Arbaletă |
| Reputation | Reputație |
| Stamina | Vlagă |
| Health | Sănătate |
| Nourishment | Sațietate |

## Verbe de interacțiune (imperativ, scurt)

| engleză | română |
|---|---|
| Examine | Cercetează |
| Investigate | Cercetează |
| Search | Caută |
| Talk to | Vorbește cu |
| Take / Loot | Ia / Jefuiește |
| Read | Citește |
| Use | Folosește |
| Return | Întoarce-te |
| Jump | Sari |
| Fail | Eșec |

## Luptă

| engleză | română |
|---|---|
| Masterstrike | Lovitură de maestru |
| Riposte | Ripostă |
| Perfect block | Parare perfectă |
| Thrust / stab | împunsătură (niciodată „lovitură de înjunghiere") |
| Slash | tăietură |
| Combat rose | roza de luptă |
| to bleed out | a sângera până la moarte (niciodată „a se zvânta") |

## Obiecte și materiale

| engleză | română |
|---|---|
| Moonshine / hooch | rachiu de casă |
| Spade | cazma |
| Shovel | lopată |
| Handgonne | archebuză de mână |
| Reforged | reforjat |
| Groschen | groschen (ca în engleză, nu „groși") |
| Lockpick | șperaclu (nu „cârlig de descuiat") |
| Thunderstone | piatră de trăsnet |
| Potion | poțiune |
| Whetstone | cute |
| turn (unitate de timp la alchimie) | clocot (niciodată „rotație") |
| handful | pumn |
| to grind | a pisa |
| to distil | a distila |
| cauldron | cazan |

## Nume proprii care NU se traduc

Numele de produse și mărci din lumea jocului rămân neschimbate: parfumurile
**Mintha**, **Lion**; numele de așezări (Kuttenberg, Trosky, Sedletz, Skalitz).

Numele de persoane primesc forma românească doar când există un exonim
consacrat: Wenceslas → **Venceslau**, Charles → **Carol**, Sigismund →
**Sigismund**. Personajele jocului rămân exact ca în engleză (Matthew, Theresa, Peter, Radzig, Jobst).

## Registru liturgic

Formă **catolică**, potrivită cu Boemia din 1403: „Pâinea noastră cea de toate
zilele", „Creatorul cerului și al pământului", „Isus Cristos", „Bucură-te,
Marie". Textele canonice se substituie, nu se traduc, vezi `tools/liturgy.py`.
