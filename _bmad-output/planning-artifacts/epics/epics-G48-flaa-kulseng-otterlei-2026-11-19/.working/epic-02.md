## Epic 2: CV-en (steg 1)

Brukeren kan laste opp CV-en som PDF eller TXT, se og rette teksten, prøve eksempel A, B eller C i testmodus, og slette dokumentene sine. Koden ligger i `dokumenter/` (CV-en og innlesingen), `ki/eksempelpar.py` (eksempelparene, AD-6) og `analyse/` (`siste_steg`, `/` og eksempelknappen, AD-2). Steg 2 finnes ikke før Epic 3. Til da sender «Bruk denne og gå videre» brukeren tilbake til steg 1 med en bekreftelse, og Epic 3 endrer det til `/analyse/`.

### Story 2.1: Lese CV-teksten fra PDF og TXT

Som student
vil jeg at appen leser teksten riktig fra CV-en min, også når den har to kolonner,
slik at analysen bygger på det som faktisk står i CV-en.

**Krav:** FR-1, NFR-2, SM-2. **Styres av:** AD-6, AD-13, AD-17.

**Akseptansekriterier:**

**Gitt** `dokumenter/pdf_innlesing.py: les_cv(filnavn, innhold: bytes) -> str`
**Når** den får en PDF eller en TXT
**Så** er den eneste som leser CV-filer og sjekker filtype og størrelse (AD-13)
**Og** filtypen avgjøres av filendelsen og kontrolleres mot innholdet: en PDF må starte med `%PDF-`
**Og** TXT leses som UTF-8 med eller uten BOM, og ellers som cp1252

**Gitt** en fil med feil type, en fil over 5 MB eller en PDF uten tekst
**Når** `les_cv` leser den
**Så** kastes `FeilFiltype`, `ForStorFil` eller `TomPDF`, som er underklasser av `InnlesingFeil` (AD-13)

**Gitt** en PDF med to kolonner
**Når** `les_cv` leser den
**Så** finner den den loddrette stripen uten tekst mellom kolonnene og leser hver kolonne for seg med `page.crop()`, slik at teksten kommer i riktig rekkefølge (AD-13, prøvd 2026-11-12)

**Gitt** `ki/eksempelpar.py`
**Når** storyen er ferdig
**Så** finnes `hent_eksempelpar(par)`, som gir CV-fil, annonse og `Fasit` for A, B, C og D
**Og** sammenligninger av tekst bruker `kjerne.tekst.normaliser()` fra story 0.4, og funksjonen lages ikke på nytt i `ki/` (AD-6)
**Og** pydantic-modellen `Fasit` har feltene i AD-17, og fasiten leses bare gjennom `hent_eksempelpar()`

**Gitt** PDF-CV-ene til eksempelpar A og C
**Når** testene leser dem med `les_cv`
**Så** kommer ordene i `cv_kilde.txt`, uten merkene `[VENSTRE]` og `[HØYRE]`, i samme rekkefølge i CV-teksten (FR-1, SM-2)
**Og** for to-kolonne-CV-en C sjekkes hver kolonne for seg, og venstre kolonne kommer samlet, ikke blandet med høyre

**Gitt** TXT-CV-en til eksempelpar B
**Når** testen leser den med `les_cv`
**Så** gir den samme tekst som fila etter `normaliser()`

**Gitt** `fakta_i_cv` i fasiten, som er omskrevet og ikke kopiert fra CV-en
**Når** CV-ene til A, B og C sjekkes manuelt
**Så** finnes hvert punkt i CV-teksten, og sjekken står i `docs/testplan.md` (AD-17, SM-2)
**Og** en test sjekker at `cv_kilde.txt` og `fakta_i_cv` for D er like de for A, siden D bare brukes i evalueringen og har samme CV (AD-6, issue #29)

### Story 2.2: Laste opp CV og se teksten

Som student
vil jeg laste opp CV-en min og se teksten appen har hentet ut,
slik at jeg kan sjekke at ingenting har falt ut.

**Krav:** FR-1, FR-2, FR-12, FR-13, FR-14, FR-15, SM-8. **UX:** UX-DR3, UX-DR7, UX-DR8, UX-DR29, UX-DR33, UX-DR35. **Styres av:** AD-2, AD-8, AD-9, AD-10, AD-20, AD-22.

**Akseptansekriterier:**

**Gitt** at jeg er logget inn og ikke har noen CV
**Når** jeg åpner `/cv/`
**Så** ser jeg steg 1 med fremdriftslinjen og et filfelt med etikett som godtar `.pdf` og `.txt`, uten dra-og-slipp (UX-DR8)

**Gitt** en gyldig PDF eller TXT
**Når** jeg laster den opp
**Så** lagrer `dokumenter.tjenester.lagre_cv` filen, filnavnet og CV-teksten i krypterte felt, og CV-teksten vises i et redigerbart felt under «Sjekk at teksten ble riktig» (FR-1, FR-2)
**Og** har jeg en CV fra før, slettes den gamle raden og alt som henger på den gjennom `CASCADE` (FR-1, AD-8)

**Gitt** en ugyldig fil, en fil over 5 MB eller en PDF uten tekst
**Når** jeg laster den opp
**Så** oversetter tjenesten `InnlesingFeil` til `BrukerFeil`, og steg 1 vises på nytt med feiloppsummeringen og meldingen fra UX-DR33 (AD-20)

**Gitt** `analyse.tjenester.siste_steg(bruker)`
**Når** den kalles
**Så** gir den 1 uten CV, 2 med CV, 3 med `Analyse` og 4 med `Brev`, og er det eneste stedet steget regnes ut (AD-22)
**Og** etter innlogging sendes brukeren nå til steget tabellen i EXPERIENCE.md viser, ikke til Min konto: steg 1 når `siste_steg` gir 1 eller 2, og ellers steget `siste_steg` gir (UX-DR35)
**Og** også etter registrering sendes brukeren til steg 1
**Og** viderekoblingen går gjennom et view på `/` i `analyse/` som bruker `siste_steg`, fordi `kontoer` ikke importerer `analyse` (AD-2)
**Og** viewet sender innloggede brukere til steget sitt og besøkende til Logg inn, og det erstatter startsiden fra story 0.3
**Og** `LOGIN_REDIRECT_URL`, registreringen og appnavnet i topplinjen bruker `/` (UX-DR3)
**Og** åpnes et steg som ikke kan nås ennå, sendes brukeren til det siste steget som kan nås

**Gitt** to testbrukere med hver sin CV
**Når** bruker 1 åpner `/cv/`, også med endret adresse
**Så** ser bruker 1 bare sin egen CV, og ingen URL inneholder en ID (FR-14, AD-10)

**Gitt** en lagret CV
**Når** testen leser SQLite-filen direkte
**Så** finnes verken filnavnet, CV-teksten eller filinnholdet i klartekst (FR-15)

### Story 2.3: Rette CV-teksten og bruke en lagret CV

Som student
vil jeg rette CV-teksten og bruke CV-en jeg lastet opp sist,
slik at jeg kan rette feil i innlesingen og slippe å laste opp på nytt.

**Krav:** FR-2. **UX:** UX-DR9, UX-DR11, UX-DR35. **Styres av:** AD-6, AD-8, AD-15, AD-22.

**Akseptansekriterier:**

**Gitt** at jeg har rettet CV-teksten
**Når** jeg trykker «Bruk denne og gå videre»
**Så** lagrer `dokumenter.tjenester.lagre_cv_tekst` den rettede teksten, og det er den som brukes videre (FR-2)
**Og** til Epic 3 finnes, kommer jeg tilbake til steg 1 med bekreftelsen «CV-teksten er lagret»

**Gitt** en CV-tekst over 30 000 tegn etter at mellomrom først og sist er fjernet
**Når** jeg prøver å lagre den
**Så** får jeg en melding fra `kjerne/meldinger.py`, og ingenting lagres (FR-2, `CV_TEKST_MAKS`)
**Og** en tom CV-tekst, etter at mellomrom først og sist er fjernet, gir også en melding fra `kjerne/meldinger.py`, og ingenting lagres

**Gitt** at det finnes en `Analyse`
**Når** steg 1 vises
**Så** står «Dette erstatter analysen og utkastet du har nå.» over «Bruk denne og gå videre» (UX-DR11)
**Og** lagrer jeg en tekst som er endret etter `normaliser()`, slettes `Analyse`, og `CASCADE` sletter resten (FR-2, AD-8)
**Og** er teksten lik etter `normaliser()`, slettes ingenting
**Og** `dokumenter` ser analysen bare gjennom `cv.analyse` og importerer ikke `analyse` (AD-22)

**Gitt** at jeg har en lagret CV og logger inn på nytt
**Når** steg 1 vises
**Så** står «Vil du bruke cv.pdf?» med CV-teksten synlig og redigerbar, hovedknappen «Bruk denne og gå videre» og sekundærknappen «Last opp ny» (UX-DR9)
**Og** «Last opp ny» viser filfeltet fra story 2.2, og den lagrede CV-en og analysen som henger på den, slettes først når en ny fil er lastet opp

### Story 2.4: Prøve med eksempel A, B eller C

Som sensor
vil jeg fylle inn et eksempel med én knapp i testmodus,
slik at jeg kan prøve appen uten min egen CV.

**Krav:** FR-9, FR-10. **UX:** UX-DR10. **Styres av:** AD-2, AD-6, AD-14, AD-22.

**Akseptansekriterier:**

**Gitt** at appen kjører i testmodus
**Når** jeg åpner steg 1
**Så** står «… eller prøv med et eksempel: [A] [B] [C]» ved opplastingen (UX-DR10)
**Og** i KI-modus vises ikke knappene

**Gitt** knappen for et par
**Når** jeg trykker den (`POST` til `/eksempel/<A|B|C>/`)
**Så** lagres parets CV gjennom `dokumenter.tjenester.lagre_cv`, med CV-teksten fra `les_cv()` på parets CV-fil (AD-6)
**Og** viewet ligger i `analyse/`, fordi `dokumenter` aldri importerer `ki` (AD-2)
**Og** jeg blir stående i steg 1 med teksten synlig, også for to-kolonne-CV-en C
**Og** har jeg en CV fra før, erstattes den som ved opplasting, og `CASCADE` sletter analysen (AD-8). En test viser det

**Gitt** at appen kjører i KI-modus
**Når** noen sender `POST` til `/eksempel/A/`
**Så** svarer appen med 404, og ingenting lagres
**Og** `/eksempel/D/` og ukjente par gir også 404 i testmodus, og ingenting lagres, fordi D bare brukes i evalueringen (AD-6)

**Gitt** CV-teksten skjemaet fyller inn for et par
**Når** den sendes tilbake med `\r\n` som linjeskift
**Så** gir `normaliser()` samme tekst som referanseteksten til paret (AD-6)

### Story 2.5: Slette dokumentene mine

Som student
vil jeg slette CV-en og resultatet mitt,
slik at ingenting ligger igjen etter at jeg har søkt.

**Krav:** FR-16, NFR-2, SM-9. **UX:** UX-DR28, UX-DR34. **Styres av:** AD-2, AD-8, AD-9, AD-19.

**Akseptansekriterier:**

**Gitt** at jeg er logget inn og har en CV
**Når** jeg trykker «Slett mine dokumenter», som legges inn i Min konto i denne storyen
**Så** kommer jeg til bekreftelsessiden (`GET` til `/min-konto/slett-dokumenter/`, som ikke sletter noe), laget med `templates/felles/bekreftelse.html`, med «Er du sikker? CV-en, annonsen og resultatet slettes, og det kan ikke angres.» (FR-16, UX-DR28)
**Og** viewet ligger i `dokumenter/`, selv om URL-en begynner med `/min-konto/`. Min konto lenker til det med URL-navnet, uten å importere `dokumenter` (AD-2)

**Gitt** bekreftelsessiden
**Når** jeg trykker den røde knappen (`POST` til `/min-konto/slett-dokumenter/`)
**Så** sletter `dokumenter.tjenester.slett_cv` CV-raden, og `CASCADE` sletter `Analyse`, `Brev` og `CVForbedring`
**Og** `slett_cv` sletter uten å lese de krypterte feltene, for eksempel med `.only("pk")`, så slettingen virker også når dataene ikke kan dekrypteres (AD-9)
**Og** jeg ser «Dokumentene dine er slettet.», og neste gang starter jeg i steg 1 uten CV

**Gitt** at dokumentene er slettet
**Når** testen ser i databasen
**Så** finnes ingen `CV`-, `Analyse`-, `Brev`- eller `CVForbedring`-rad for brukeren, mens kontoen finnes (FR-16, AD-8)

**Gitt** siden for dekrypteringsfeil fra story 0.4
**Når** den vises
**Så** har den også knappen «Slett mine dokumenter», som går til den samme bekreftelsessiden (AD-9)
**Og** en test med en CV som ikke kan dekrypteres, viser at brukeren kommer seg videre til steg 1 uten CV etter slettingen

