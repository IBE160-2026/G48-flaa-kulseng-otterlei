## Epic 6: CV-forbedringsforslag (P6)

Brukeren kan be om forslag til hvordan CV-en kan tilpasses stillingsannonsen. Hvert forslag viser til en del av CV-teksten, og krav som mangler, står som spørsmål. Koden ligger i `ki/` (operasjonen og prompten) og `analyse/` (`CVForbedring`, tjenesten og steg 3), etter AD-2. Epicet er nummer 2 i kuttrekkefølgen i nødplanen (PRD §8.1). Kuttes det, står det i `docs/endringer/`, og knappen i steg 3 fjernes. Det tomme skjelettet `CVForbedring` fra Epic 0 står da igjen, og det forklares i den samme filen.

### Story 6.1: KI-operasjonen for CV-forbedringsforslag med lagrede svar

Som student
vil jeg at appen kan lage forslag til CV-en min som bare bygger på det som står der,
slik at jeg får råd jeg faktisk kan bruke uten å dikte opp erfaring.

**Krav:** FR-10, FR-18, NFR-3, NFR-4, NFR-11, SM-4. **Styres av:** AD-3, AD-4, AD-5, AD-6, AD-8, AD-9, AD-12, AD-17.

**Akseptansekriterier:**

**Gitt** `ki/modeller.py`
**Når** storyen er ferdig
**Så** finnes returtypen `CVForbedringer` med en liste forslag, der hvert forslag har `del_av_cv` (den delen av CV-teksten det gjelder) og `forslag`, og krav som mangler, kan stå som et spørsmål (FR-18)
**Og** typen brukes av både `ClaudeKlient` og `TestmodusKlient` gjennom `cv_forbedring(cv_tekst, annonse, sprak, mangler) -> CVForbedringer` (AD-3)
**Og** `mangler` lages med `ki.mangler.samle_mangler()` fra story 5.1

**Gitt** prompten for CV-forbedring i `ki/prompter/`
**Når** jeg leser den
**Så** sier den at CV-teksten og annonsen er data og ikke instruksjoner, at hvert forslag skal vise til en del av CV-teksten, og at krav i `mangler` bare kan stå som spørsmål («Har du erfaring med X? I så fall bør det stå i CV-en»), aldri som noe brukeren skal skrive inn (FR-18, AD-5)
**Og** den sier at `del_av_cv` siteres ordrett fra CV-teksten

**Gitt** `ClaudeKlient.cv_forbedring`
**Når** KI-tjenesten svarer
**Så** hentes svaret som strukturert utdata validert mot `CVForbedringer`, og feil oversettes til `KIFeil` på samme måte som for de andre operasjonene (AD-4)

**Gitt** `analyse/models.py`
**Når** migreringen for storyen kjøres
**Så** har `CVForbedring` et `KryptertJSONFelt` med forslagene, og raden peker på `Analyse` med `OneToOne` og `CASCADE` (AD-8, AD-9)
**Og** `analyse.tjenester.lag_cv_forbedring(bruker)` kjører kallet inne i `ki_las`, utenfor en databasetransaksjon, og overskriver bare `CVForbedring`, ikke analysen eller brevet (AD-8, AD-12)

**Gitt** `python manage.py lag_lagrede_svar`
**Når** kommandoen kjøres i KI-modus
**Så** lager den også `cv_forbedring__nb.json` og `cv_forbedring__en.json` for par A, B og C, til sammen 6 filer, med `meta` og `svar` som AD-6 beskriver (FR-10)
**Og** `TestmodusKlient.cv_forbedring` leser riktig fil ut fra `eksempel_hash` og språket, og kaster `IkkeITestmodus` når hashen ikke treffer et par (AD-6)

**Gitt** evalueringsrapporten fra `lag_lagrede_svar`
**Når** den skrives
**Så** har den en CV-del per par med antall krav fra `krav_mangler` som er påstått som noe søkeren kan i forslagene (må være 0), og antall forslag der `normaliser(del_av_cv)` ikke finnes i `normaliser(cv_tekst)` (NFR-11, SM-4)
**Og** regelen fra story 5.2 (issue #28) utvides: en setning som slutter med «?», er et spørsmål og ikke en påstand. Det gjelder også brevene
**Og** testene av regelen får med «Har du erfaring med SQL?» og «Do you have experience with SQL?»

**Gitt** testene for storyen
**Når** de kjøres uten nettverk
**Så** sjekker de at `TestmodusKlient` gir gyldige `CVForbedringer` for hvert par og begge språk, at hashen av promptfilen stemmer med `meta` i de lagrede svarene (AD-6), og at `lag_cv_forbedring` med `falsk_ki(feil=KITidsavbrudd())` ikke lagrer noe (AD-17)

### Story 6.2: Vise CV-forslagene i steg 3

Som student
vil jeg trykke på en knapp i steg 3 og se forslagene til CV-en min,
slik at jeg kan tilpasse CV-en til stillingen før jeg søker.

**Krav:** FR-11, FR-14, FR-18, NFR-3, NFR-4, NFR-5, NFR-6, NFR-7. **UX:** UX-DR15, UX-DR18, UX-DR29 – UX-DR32, UX-DR35, UX-DR36. **Styres av:** AD-2, AD-8, AD-10, AD-15, AD-20, AD-22.

**Akseptansekriterier:**

**Gitt** at jeg står i steg 3 og ikke har CV-forslag
**Når** siden vises
**Så** står knappen «Vis forslag til CV-en» under nøkkelordkortet, i et `POST`-skjema til `/resultat/cv-forbedring/` (UX-DR18, AD-22)

**Gitt** at jeg trykker «Vis forslag til CV-en»
**Når** svaret kommer
**Så** blir jeg sendt tilbake til `/resultat/` med Post/Redirect/Get, og forslagene vises som en liste på samme side, i et kort med merket «Laget av KI» og `lang` etter valgt språk (UX-DR15, UX-DR18, UX-DR35, UX-DR36)
**Og** hvert forslag viser hvilken del av CV-teksten det gjelder, og krav som mangler, står som spørsmål (FR-18)
**Og** all tekst vises med Djangos escaping (NFR-3, AD-15)

**Gitt** at knappen er trykket
**Når** KI-kallet pågår
**Så** viser knappen «Jobber …» med den felles ventetilstanden fra `skjema.js`, og et nytt trykk gir ikke et nytt kall (NFR-6, UX-DR30)

**Gitt** at KI-tjenesten ikke svarer, gir feil eller forbruksgrensen er nådd
**Når** jeg har trykket knappen
**Så** vises steg 3 på nytt med feiloppsummeringen og den faste meldingen fra `kjerne/meldinger.py`, og analysen og brevet er urørt (NFR-5, UX-DR29, UX-DR31, AD-20)

**Gitt** at appen kjører i testmodus med egen CV
**Når** `/resultat/cv-forbedring/` får et `POST`
**Så** oversetter tjenesten `IkkeITestmodus` til `BrukerFeil` med FR-11-meldingen fra `kjerne/meldinger.py`, og ingenting lagres (FR-11)
**Og** knappen vises ikke i dette tilfellet, siden steg 3 da har «Prøv eksempel A» i stedet (UX-DR32)

**Gitt** at jeg allerede har CV-forslag
**Når** jeg kommer tilbake til steg 3, også etter å ha laget et brev
**Så** vises de lagrede forslagene uten nytt KI-kall
**Og** knappen er da en sekundærknapp med teksten «Lag nye forslag»
**Og** trykker jeg knappen på nytt, overskrives bare `CVForbedring` (AD-8)

**Gitt** to testbrukere
**Når** bruker 1 åpner `/resultat/`
**Så** ser bruker 1 aldri forslagene til bruker 2, og URL-en har ingen ID (FR-14, AD-10)
