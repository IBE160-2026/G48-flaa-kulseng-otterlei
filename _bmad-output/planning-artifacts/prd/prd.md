---
title: "PRD: AI CV & Job Application Assistant"
status: draft
created: 2026-10-19
updated: 2026-10-19
---

# PRD: AI CV & Job Application Assistant

**Gutta krutt (G48)** — IBE160 Programmering med KI, Høgskolen i Molde, høst 2026
Ole A. Flaa, Henrik O. Kulseng, Haakon Remen Otterlei

_Skrevet av Claude Code i rask modus etter gruppas svar (2026-10-19). Claudes antagelser ble bekreftet av gruppa i gjennomgangen av pull request #4 og er samlet i §12. Beslutningene bak dokumentet står i [beslutningsloggen](.memlog.md)._

## 0. Om dokumentet

Denne PRD-en gjør [product brief](../product-brief.md) (versjon 2) om til konkrete, nummererte krav. Den er grunnlaget for UX-skisser, arkitektur, epics og stories. Stories og kode skal vise til kravene med ID (`FR-7`, `NFR-3`, `UJ-1`), slik at sensor kan spore koden tilbake til planen.

- Ordene i ordlisten (§3) brukes med nøyaktig samme betydning i resten av dokumentet og i stories.
- Funksjonene (§4) står i prioritert rekkefølge fra briefen. Hver funksjon har funksjonelle krav (FR) med testbare konsekvenser.
- Teknologivalg tas i arkitekturen. Notater som hører hjemme der, står i [addendum](addendum.md).
- Briefen er fortsatt kilden for problembeskrivelse, konkurrenter og visjon. Det gjentas ikke her.

## 1. Visjon

Studenter som søker sommerjobb, deltidsjobb eller første heltidsstilling, sender ofte samme generiske brev til alle stillinger, eller bruker chatboter som skriver floskler og noen ganger dikter opp erfaring. AI CV & Job Application Assistant er en nettside der studenten laster opp CV-en sin, limer inn en stillingsannonse og får se hvilke krav i annonsen CV-en dekker og hvilke som mangler. Deretter kan studenten få et søknadsbrev eller konkrete forslag, råd om CV-en og en nøkkelordanalyse.

Det som skiller appen fra konkurrentene, er at studenten selv bestemmer hvor mye KI skal skrive, og at alt appen skriver skal bygge på det som faktisk står i CV-en. Nøkkelordanalysen beregnes i kode, så den gir samme svar hver gang og kan testes mot fasit.

For kurset er målet en app som viser ansvarlig og etterprøvbar bruk av KI: den virker uten gruppas API-nøkkel (testmodus), den kan testes mot eksempeldata med fasit, og den behandler personopplysninger på en ordentlig måte.

## 2. Målbruker

### 2.1 Hva brukeren vil få gjort

- Skreddersy en søknad til én bestemt stilling uten å bruke en hel kveld på det.
- Forstå hvilke krav i annonsen CV-en ikke dekker, før søknaden sendes.
- Få hjelp til å formulere seg, men selv bestemme om KI skal skrive hele brevet eller bare foreslå.
- Være trygg på at brevet ikke påstår noe som ikke stemmer, så søkeren ikke blir avslørt i et intervju.
- Vite hva som skjer med CV-en, og kunne slette den.

### 2.2 Ikke målgruppe i v1

- Rekrutterere og arbeidsgivere. Det finnes ingen arbeidsgiverrolle.
- Erfarne arbeidssøkere med lange CV-er og spesialiserte bransjekrav. Appen er laget og testet for studenter.
- Søkere som skriver på andre språk enn norsk og engelsk.

### 2.3 Brukerreiser

Personene er oppdiktet.

**UJ-1. Emma tilpasser søknaden til en sommerjobb (kjerneflyten).**
Emma studerer IT og vil søke sommerjobb som junior utvikler. Hun åpner nettsiden, registrerer seg med e-post og passord og blir logget inn. Hun laster opp CV-en sin som PDF og ser teksten appen har hentet ut. Hun limer inn annonseteksten, velger norsk, formell tone og «fullt utkast», og trykker «Analyser». Gap-analysen viser at Python og Git matcher, mens SQL og førerkort klasse B mangler. Hun ber om søknadsbrev og får et brev som trekker fram Python-prosjektene hennes, uten å påstå at hun kan SQL. Hun kopierer brevet og bruker det som utgangspunkt for søknaden.
**Avvik:** Hvis KI-tjenesten ikke svarer, får Emma en melding om at analysen ikke ble fullført, og kan prøve igjen uten å laste opp CV-en på nytt.

**UJ-2. Jonas vil skrive selv, men på engelsk.**
Jonas studerer logistikk og søker et graduate-program med engelsk annonse. Han er innlogget og har allerede lastet opp CV-en. Han limer inn annonsen, velger engelsk, uformell tone og «kun forslag». Han får en punktliste med forslag til hva brevet bør ta opp, skrevet på engelsk og koblet til erfaring fra CV-en. Nøkkelordanalysen viser at «SAP» mangler. Han ber om CV-forbedringsforslag og ser hvordan lagerjobben kan beskrives tydeligere. Han skriver brevet selv.

**UJ-3. Sensor prøver appen uten API-nøkkel.**
Sensor kloner repoet, følger README og starter appen uten å legge inn noen API-nøkkel. Øverst på siden står det at appen kjører i testmodus. Sensor registrerer en bruker, trykker «Prøv med eksempel A» og går gjennom hele kjerneflyten med lagrede svar. Så laster sensor opp en egen CV: teksten hentes ut og nøkkelordanalysen vises, men der det trengs KI, forklarer appen at testmodus bare har svar for eksempelparene, og hvordan en API-nøkkel legges inn.

**UJ-4. Emma sletter dataene sine.**
Etter søknadsfristen vil Emma ikke lenger ha CV-en liggende i appen. Hun går til «Min konto» og trykker «Slett mine dokumenter». Etter en bekreftelse er CV-en og resultatet borte. Senere sletter hun hele kontoen, og da finnes ingenting om henne i databasen.

## 3. Ordliste

- **Bruker** — en person med konto i appen. Har null eller én CV og null eller ett resultat.
- **CV** — filen brukeren laster opp (PDF eller TXT). En ny opplasting erstatter den forrige.
- **CV-tekst** — teksten appen henter ut av CV-en. Det er CV-teksten, ikke filen, som analyseres.
- **Stillingsannonse** — teksten brukeren limer inn fra en annonse.
- **Krav** — en kvalifikasjon stillingsannonsen ber om, f.eks. «SQL» eller «førerkort klasse B».
- **Innstillinger** — språk (norsk/engelsk), tone (formell/uformell), svarform og eventuelle ønskede nøkkelord.
- **Svarform** — «fullt utkast» (et sammenhengende søknadsbrev) eller «kun forslag» (en punktliste med brevforslag).
- **Analyse** — én kjøring på en CV-tekst og en stillingsannonse med valgte innstillinger.
- **Resultat** — det en analyse gir: gap-analyse, søknadsbrev eller brevforslag, CV-forbedringsforslag og ATS-nøkkelordanalyse. Bare det siste resultatet lagres.
- **Gap-analyse** — listen over krav i stillingsannonsen, der hvert krav er markert «matcher» eller «mangler» ut fra CV-teksten.
- **Søknadsbrev** — et fullt brevutkast (svarform «fullt utkast»).
- **Brevforslag** — en punktliste med forslag til innhold i brevet (svarform «kun forslag»).
- **CV-forbedringsforslag** — konkrete forslag til hvordan CV-en kan tilpasses stillingsannonsen.
- **Nøkkelord** — et ord eller uttrykk fra stillingsannonsen som et ATS kan søke etter.
- **ATS-nøkkelordanalyse** — oversikt over hvilke nøkkelord som finnes og mangler i CV-teksten, beregnet i kode, med en KI-forklaring.
- **Oppdiktet påstand** — utdanning, arbeidsgiver, ferdighet eller erfaring som står i et søknadsbrev, brevforslag eller CV-forbedringsforslag, men ikke i CV-teksten.
- **KI-modus** — appen gjør ekte kall til språkmodellen. Krever API-nøkkel.
- **Testmodus** — appen bruker lagrede svar i stedet for ekte kall til språkmodellen.
- **Lagret svar** — et KI-svar som er hentet på forhånd og lagret i repoet for bruk i testmodus.
- **Eksempelpar** — en oppdiktet CV og en oppdiktet stillingsannonse (A, B eller C) med fasit.
- **Fasit** — forventet resultat for et eksempelpar: krav som matcher og mangler, nøkkelord og en sjekkliste for søknadsbrevet.

## 4. Funksjoner

Funksjonene står i prioritert rekkefølge (P1–P8) fra briefen. P1–P5 er kjerneflyten.

### 4.1 CV og stillingsannonse (P1)

**Beskrivelse:** Brukeren laster opp CV-en, ser CV-teksten appen har hentet ut, limer inn stillingsannonsen og velger innstillinger. Realiserer UJ-1 og UJ-2. Den største risikoen er CV-er med kolonner og tabeller (eksempel C). Derfor viser appen CV-teksten, så brukeren kan se om noe har falt ut.

#### FR-1: Laste opp CV

Brukeren kan laste opp én CV som PDF eller TXT. Realiserer UJ-1.

**Konsekvenser (testbare):**
- PDF- og TXT-filer godtas. Andre filtyper avvises med en melding om hvilke typer som er lov.
- Filer over 5 MB avvises med en forståelig melding.
- For alle tre eksempel-CV-ene, også to-kolonne-CV-en C, inneholder CV-teksten alle kvalifikasjonene fasiten lister opp.
- En PDF uten tekst (f.eks. et innskannet bilde) gir en melding om at teksten ikke kunne leses, ikke en tom analyse.
- En ny opplasting erstatter brukerens forrige CV og sletter forrige resultat.

**Utenfor:** DOC/DOCX, bilder og tekstgjenkjenning (OCR).

#### FR-2: Se og rette CV-teksten

Brukeren kan se CV-teksten appen har hentet ut, og rette den i et enkelt tekstfelt før analysen. Dette er et tiltak mot feil innlesing av PDF-er med kolonner.

**Konsekvenser (testbare):**
- CV-teksten vises etter opplasting.
- Endringer brukeren gjør, er det som brukes i analysen.

#### FR-3: Lime inn stillingsannonse

Brukeren kan lime inn teksten fra en stillingsannonse.

**Konsekvenser (testbare):**
- Et tomt felt eller en tekst under 100 tegn gir en melding, ikke et KI-kall.
- En tekst over 15 000 tegn avvises med en melding, for å holde KI-kostnaden nede.

**Utenfor:** Henting av annonser fra Finn.no, LinkedIn eller andre nettsteder.

#### FR-4: Velge innstillinger

Brukeren kan velge språk (norsk/engelsk), tone (formell/uformell), svarform («fullt utkast»/«kun forslag») og eventuelt skrive inn ønskede nøkkelord. Realiserer UJ-1 og UJ-2.

**Konsekvenser (testbare):**
- Alle valg har en forhåndsvalgt verdi: norsk, formell, fullt utkast.
- Ønskede nøkkelord tas med i ATS-nøkkelordanalysen (FR-19).

### 4.2 Gap-analyse (P2)

**Beskrivelse:** Når brukeren trykker «Analyser», sammenligner appen CV-teksten med stillingsannonsen. Resultatet er en liste over krav, der hvert krav er markert «matcher» eller «mangler», med en kort begrunnelse som viser til CV-teksten. Realiserer UJ-1. Gap-analysen og ATS-nøkkelordanalysen kjøres når brukeren trykker «Analyser». Søknadsbrev og CV-forbedringsforslag lages når brukeren ber om dem. Egne knapper gjør at P6–P8 kan legges til uavhengig av hverandre, og holder KI-kostnaden nede.

#### FR-5: Kjøre gap-analyse

Brukeren kan få en gap-analyse av CV-teksten mot stillingsannonsen. Realiserer UJ-1.

**Konsekvenser (testbare):**
- For hvert eksempelpar viser gap-analysen alle krav fasiten markerer som manglende, og markerer ingen av fasitens matchende krav som manglende. For par A: «SQL» og «førerkort klasse B» mangler, mens «Python» og «Git» matcher.
- Hvert krav som matcher, har en begrunnelse som viser hvor i CV-teksten det står.
- Gap-analysen skrives på språket brukeren har valgt.

### 4.3 Søknadsbrev og brevforslag (P3)

**Beskrivelse:** Brukeren ber om hjelp til søknaden og får et søknadsbrev eller brevforslag, avhengig av svarform. Alt som står der, skal kunne spores til CV-teksten. Krav som mangler i gap-analysen, kan nevnes som noe søkeren vil lære, men aldri som noe søkeren kan. Realiserer UJ-1 og UJ-2.

#### FR-6: Få søknadsbrev (fullt utkast)

Brukeren kan få et sammenhengende søknadsbrev når svarformen er «fullt utkast». Realiserer UJ-1.

**Konsekvenser (testbare):**
- Brevet er skrevet på valgt språk og i valgt tone.
- Brevet er tilpasset stillingsannonsen: det nevner stillingen og minst to krav som matcher.

#### FR-7: Få brevforslag (kun forslag)

Brukeren kan få en punktliste med brevforslag i stedet for et ferdig brev når svarformen er «kun forslag». Realiserer UJ-2.

**Konsekvenser (testbare):**
- Resultatet er en punktliste, ikke et sammenhengende brev.
- Hvert forslag viser til noe i CV-teksten eller et krav i stillingsannonsen.

#### FR-8: Ingen oppdiktede påstander

Søknadsbrev og brevforslag inneholder ingen oppdiktede påstander.

**Konsekvenser (testbare):**
- For hvert eksempelpar består søknadsbrevet og brevforslagene sjekklisten i fasiten. For par A påstår brevet ikke at søkeren kan SQL eller har førerkort.
- Sjekken gjøres manuelt etter en skriftlig sjekkliste per eksempelpar. Resultatet dokumenteres i repoet.

### 4.4 Testmodus (P4)

**Beskrivelse:** Testmodus gjør at sensor og de automatiske testene kan kjøre hele kjerneflyten uten API-nøkkel, nettverk eller kostnad. Realiserer UJ-3.

#### FR-9: Slå på testmodus

Appen kjører i testmodus når ingen API-nøkkel er satt, eller når testmodus er slått på i konfigurasjonen.

**Konsekvenser (testbare):**
- Uten API-nøkkel starter appen i testmodus uten feil.
- Så lenge testmodus er på, vises det tydelig på alle sider.
- I testmodus gjøres ingen kall til språkmodellen.

#### FR-10: Prøve med eksempelpar

I testmodus kan brukeren velge eksempelpar A, B eller C med én knapp. Da fylles CV-tekst og stillingsannonse inn automatisk, og analysen bruker lagrede svar. Realiserer UJ-3.

**Konsekvenser (testbare):**
- For hvert eksempelpar gir testmodus gap-analyse, søknadsbrev eller brevforslag, CV-forbedringsforslag og ATS-nøkkelordanalyse.
- Det finnes lagrede svar for alle kombinasjoner av innstillinger (språk × tone × svarform) for hvert eksempelpar. De lagres ved å kjøre eksempelparene én gang i KI-modus med et skript.

#### FR-11: Egen CV i testmodus

Laster brukeren opp en egen CV i testmodus, kjører de delene som ikke trenger KI. Der det trengs KI, får brukeren en forklaring. Realiserer UJ-3.

**Konsekvenser (testbare):**
- CV-teksten hentes ut og vises (FR-1, FR-2).
- ATS-nøkkelordanalysen vises uten KI-forklaring (FR-21).
- Gap-analyse, søknadsbrev, brevforslag og CV-forbedringsforslag viser meldingen: «Testmodus: KI-svar finnes bare for eksempelparene. Legg inn en API-nøkkel for å analysere din egen CV.»

### 4.5 Konto, lagring og sletting (P5)

**Beskrivelse:** Appen håndterer personopplysninger, så den har ordentlig innlogging, kryptert lagring og sletting. Bare den siste CV-en og det siste resultatet lagres. Realiserer UJ-1 og UJ-4.

**Lagringspolicy:** Data lagres til brukeren sletter dem. En ny analyse overskriver det forrige resultatet, og en ny CV erstatter den forrige. Brukeren kan slette dokumentene sine eller hele kontoen når som helst. Det er ingen automatisk sletting etter et antall dager.

#### FR-12: Registrere konto

En besøkende kan registrere seg med e-post og passord.

**Konsekvenser (testbare):**
- En e-post som allerede er registrert, gir en melding og ingen ny konto.
- Passord under 8 tegn avvises. Det er ingen andre passordregler.
- Passord lagres bare som hash med en anerkjent algoritme for passord, aldri i klartekst.

#### FR-13: Logge inn og ut

Brukeren kan logge inn med e-post og passord, og logge ut.

**Konsekvenser (testbare):**
- Feil e-post eller feil passord gir samme generelle melding, så det ikke avsløres hvilke e-poster som finnes.
- Sider med brukerdata kan ikke åpnes uten å være innlogget.
- Etter utlogging gir tilbakeknappen ikke tilgang til brukerdata.

#### FR-14: Tilgangskontroll

En bruker kan bare se og endre sine egne data.

**Konsekvenser (testbare):**
- Testet med to testbrukere: bruker 1 får ikke tilgang til CV-en eller resultatet til bruker 2, heller ikke ved å endre adressen i nettleseren.

#### FR-15: Kryptert lagring

CV, CV-tekst, stillingsannonse og resultat lagres kryptert i databasen.

**Konsekvenser (testbare):**
- Når databasen leses direkte, er ingen av disse lesbare i klartekst.
- Krypteringsnøkkelen settes med en miljøvariabel og ligger aldri i repoet.

#### FR-16: Slette dokumenter

Brukeren kan slette CV-en og resultatet sitt. Realiserer UJ-4.

**Konsekvenser (testbare):**
- Brukeren må bekrefte før noe slettes.
- Etter sletting finnes ingen CV, CV-tekst, stillingsannonse eller resultat for brukeren i databasen.

#### FR-17: Slette konto

Brukeren kan slette kontoen sin. Realiserer UJ-4.

**Konsekvenser (testbare):**
- Brukeren må bekrefte før kontoen slettes.
- Etter sletting finnes ingen data om brukeren i databasen, og e-posten kan registreres på nytt.

### 4.6 CV-forbedringsforslag (P6)

**Beskrivelse:** Brukeren kan be om forslag til hvordan CV-en kan tilpasses stillingsannonsen, f.eks. å løfte fram relevant erfaring eller formulere den tydeligere. Realiserer UJ-2.

#### FR-18: Få CV-forbedringsforslag

Brukeren kan få CV-forbedringsforslag basert på CV-teksten og stillingsannonsen.

**Konsekvenser (testbare):**
- Hvert forslag viser til en bestemt del av CV-teksten.
- Forslagene inneholder ingen oppdiktede påstander. Krav som mangler, kan nevnes som et spørsmål («Har du erfaring med X? I så fall bør det stå i CV-en»), ikke som noe brukeren skal skrive inn.

### 4.7 ATS-nøkkelordanalyse (P7)

**Beskrivelse:** Appen finner nøkkelord i stillingsannonsen og sjekker i kode hvilke av dem som finnes i CV-teksten. KI brukes bare til å forklare resultatet og foreslå omformuleringer. Fordi matchingen gjøres i kode, kan den testes mot fasiten. Realiserer UJ-2.

#### FR-19: Finne nøkkelord i stillingsannonsen

Appen finner nøkkelordene i stillingsannonsen og tar med brukerens ønskede nøkkelord.

**Konsekvenser (testbare):**
- For hvert eksempelpar finner appen alle nøkkelordene i fasiten.
- Samme stillingsannonse gir alltid de samme nøkkelordene.
- Nøkkelordene finnes i kode, ikke av språkmodellen. Hvordan det gjøres, avgjøres i arkitekturen (åpent spørsmål 2).

#### FR-20: Beregne nøkkelordmatch i kode

Appen beregner hvilke nøkkelord som finnes og mangler i CV-teksten, og hvor stor andel som finnes.

**Konsekvenser (testbare):**
- Store og små bokstaver ignoreres.
- Samme CV-tekst og stillingsannonse gir alltid samme resultat.
- Automatiske enhetstester sjekker resultatet mot fasiten for alle tre eksempelparene.

#### FR-21: Vise ATS-nøkkelordanalysen med forklaring

Brukeren ser hvilke nøkkelord som finnes og mangler, og får en KI-forklaring med forslag til omformuleringer.

**Konsekvenser (testbare):**
- Forslagene til omformulering inneholder ingen oppdiktede påstander.
- I testmodus med egen CV vises nøkkelordene uten KI-forklaring (FR-11).

### 4.8 Eksport og kopiering (P8)

**Beskrivelse:** Brukeren kan ta med seg søknadsbrevet eller brevforslagene ut av appen. Realiserer UJ-1.

#### FR-22: Kopiere til utklippstavlen

Brukeren kan kopiere søknadsbrevet eller brevforslagene med én knapp.

**Konsekvenser (testbare):**
- Brukeren får en bekreftelse på at teksten er kopiert.

#### FR-23: Eksportere til Markdown og PDF

Brukeren kan laste ned søknadsbrevet eller brevforslagene som Markdown eller PDF.

**Konsekvenser (testbare):**
- Den eksporterte filen inneholder hele teksten.
- Æ, ø og å vises riktig i begge formatene.

**Utenfor:** DOC/DOCX og eksport av gap-analysen. Bare søknadsbrev og brevforslag eksporteres.

## 5. Ikke-funksjonelle krav

**NFR-1 Kjørbar for sensor.** Appen kan startes lokalt ved å følge README, uten gruppas API-nøkkel, betalte kontoer eller tjenester gruppa driver. Det skal ta under 15 minutter. Repoet har en `.env.example` med alle miljøvariabler og uten ekte verdier.

**NFR-2 Automatiske tester.** Testene kjøres med én kommando som står i README. De kjører i testmodus, uten nettverk og uten API-nøkkel. De dekker minst nøkkelordmatchen (FR-20), innlesing av CV (FR-1), tilgangskontroll (FR-14), kryptering (FR-15) og sletting (FR-16, FR-17).

**NFR-3 Sikkerhet.** Hemmeligheter (API-nøkkel, krypteringsnøkkel) leses fra miljøvariabler og ligger aldri i koden eller i git-historikken. All tekst fra brukeren og fra språkmodellen vises slik at den ikke kan kjøres som kode i nettleseren. Skjemaer valideres både i nettleseren og på serveren.

**NFR-4 Personvern og språkmodell.** Bare CV-teksten, stillingsannonsen og innstillingene sendes til språkmodellen, aldri e-post eller passord. Appen forteller brukeren at CV-teksten sendes til en ekstern KI-tjeneste. Valget av leverandør begrunnes i arkitekturen, blant annet ut fra hvordan leverandøren behandler data. Repoet inneholder bare oppdiktede CV-er og personer.

**NFR-5 Feil fra KI-tjenesten.** Hvis språkmodellen ikke svarer, bruker for lang tid, sier nei på grunn av forbruksgrensen eller gir et svar appen ikke kan lese, får brukeren en forståelig melding og kan prøve igjen. Appen krasjer ikke, og CV og innstillinger beholdes. Tidsgrensen er 60 sekunder per kall.

**NFR-6 Tilbakemelding underveis.** Mens appen venter på språkmodellen, ser brukeren at noe skjer. Knappen kan ikke trykkes på nytt før svaret er kommet, så dobbeltklikk ikke gir to kall.

**NFR-7 Tilgjengelighet.** Grunnleggende universell utforming: alle skjemafelt har etiketter, alt kan brukes med tastaturet, kontrasten er lesbar, og bilder har alternativtekst. Siden virker på skjermer fra mobilbredde (360 px) til PC. Målet er WCAG 2.1 AA der det er rimelig, uten formell revisjon.

**NFR-8 Grensesnittspråk.** Menyer, knapper og meldinger er på norsk. Språkvalget (FR-4) gjelder bare det KI skriver.

**NFR-9 Kostnad.** Gruppa setter en forbruksgrense hos KI-leverandøren. Når grensen er nådd, behandles det som en feil etter NFR-5.

**NFR-10 Sporbarhet.** Stories viser til FR-ene de realiserer, og pull requests viser til stories. Når koden avviker fra denne PRD-en, oppdateres PRD-en eller avviket forklares i `docs/endringer/`.

## 6. Skjermbilder

Et utgangspunkt for UX-skissene. Inndelingen skal prøves ut i UX-steget.

1. **Registrer / logg inn**
2. **Ny analyse:** opplasting av CV, CV-teksten, stillingsannonsen, innstillingene og knappen «Analyser». I testmodus også knappene «Prøv med eksempel A / B / C».
3. **Resultat:** gap-analysen og ATS-nøkkelordanalysen øverst, og knapper for søknadsbrev eller brevforslag og for CV-forbedringsforslag. Kopier og eksporter ved brevet.
4. **Min konto:** slett dokumenter, slett konto og informasjon om hva som lagres og hva som sendes til KI-tjenesten.

## 7. Ikke-mål

- Appen er ingen generell chatbot. Brukeren kan ikke stille egne spørsmål til KI.
- Appen sender ikke søknader og henter ikke annonser.
- Appen lærer ikke brukerens skrivestil (flyttet til Vision i briefen).
- Appen gir ingen poengsum for hvor sannsynlig det er å få jobben.
- Det finnes ingen administrator- eller arbeidsgiverrolle.

## 8. Omfang og prioritering

### 8.1 Med i v1

Målet er at alle åtte funksjonene kommer med. De bygges i denne rekkefølgen, og hver funksjon skal være ferdig og stabil før neste startes.

| Prioritet | Funksjon | Krav |
|---|---|---|
| P1 | CV og stillingsannonse | FR-1 – FR-4 |
| P2 | Gap-analyse | FR-5 |
| P3 | Søknadsbrev og brevforslag | FR-6 – FR-8 |
| P4 | Testmodus | FR-9 – FR-11 |
| P5 | Konto, lagring og sletting | FR-12 – FR-17 |
| P6 | CV-forbedringsforslag | FR-18 |
| P7 | ATS-nøkkelordanalyse | FR-19 – FR-21 |
| P8 | Eksport og kopiering | FR-22 – FR-23 |

P1–P5 er kjerneflyten. NFR-1 – NFR-10 gjelder for alle funksjonene.

**Sjekkpunkt:** Fristen er om 4–5 uker (ca. 16.–23. november 2026). Hvis kjerneflyten (P1–P5) ikke er ferdig ved slutten av uke 3 (ca. 8. november), kutter gruppa bakfra: først P8, så P7, så P6. Kuttet begrunnes i `docs/endringer/`, og denne PRD-en oppdateres.

### 8.2 Utenfor v1

| Hva | Hvorfor |
|---|---|
| «Glemt passord» | Krever en e-posttjeneste og en hemmelighet til, og sensor kan ikke teste det uten eget oppsett. |
| Historikk over tidligere analyser | Gruppa vil at brukeren bare ser siste resultat. Det gir enklere datamodell, færre skjermbilder og mindre lagrede personopplysninger. |
| Automatisk sletting etter et antall dager | Krever en bakgrunnsjobb. Siden bare siste resultat lagres, blir det lite data, og brukeren kan slette selv. |
| Læring av skrivestil | Flyttet til Vision etter faglærers tilbakemelding. |
| DOC/DOCX (opplasting og eksport) | Lite brukt, mer krevende å lese og ikke nødvendig for kjerneflyten. |
| Henting av annonser fra Finn.no, LinkedIn o.l. | Brukeren limer inn teksten selv. |
| Andre språk enn norsk og engelsk | Holder testingen overkommelig. |
| Betaling og automatisk innsending av søknader | Ikke en del av problemet appen løser. |

## 9. Suksesskriterier

Kriteriene er hentet fra briefen og koblet til kravene. Hvert kriterium skal bli et testtilfelle, automatisk eller manuelt etter en skriftlig testplan.

- **SM-1 Kjerneflyt ende-til-ende:** Med eksempelpar A kan en ny bruker registrere seg, logge inn, laste opp CV, lime inn stillingsannonse og få gap-analyse og søknadsbrev uten feil, både i KI-modus og i testmodus. Validerer FR-1 – FR-6, FR-9, FR-10, FR-12, FR-13.
- **SM-2 Innlesing av CV:** For alle tre eksempel-CV-ene inneholder CV-teksten alle kvalifikasjonene fasiten lister opp. Validerer FR-1.
- **SM-3 Gap-analyse:** For hvert eksempelpar stemmer krav som matcher og mangler med fasiten. Validerer FR-5.
- **SM-4 Ingen oppdiktede påstander:** Søknadsbrev, brevforslag og CV-forbedringsforslag for hvert eksempelpar består sjekklisten i fasiten. Validerer FR-8, FR-18, FR-21.
- **SM-5 Brukervalg respekteres:** «Fullt utkast» gir et sammenhengende brev, mens «kun forslag» gir en punktliste. Valgt språk og tone gjenspeiles. Validerer FR-4, FR-6, FR-7.
- **SM-6 ATS-nøkkelordanalyse:** Enhetstestene for alle tre eksempelparene består, og samme input gir samme resultat. Validerer FR-19, FR-20.
- **SM-7 Eksport:** Eksportert Markdown og PDF inneholder hele brevet med riktige æ, ø og å. Validerer FR-22, FR-23.
- **SM-8 Tilgangskontroll og kryptering:** Testbruker 1 får ikke tilgang til dataene til testbruker 2, og ingen dokumenter er lesbare i klartekst i databasen. Validerer FR-14, FR-15.
- **SM-9 Sletting:** Etter sletting av dokumenter eller konto er dataene borte fra databasen. Validerer FR-16, FR-17.
- **SM-10 Kjørbar for sensor:** Appen startes etter README uten gruppas API-nøkkel, og testmodus kjører SM-1. Validerer FR-9 – FR-11, NFR-1.

**Hva vi ikke skal optimalisere for**

- **SM-C1 Høy nøkkelordmatch.** Appen skal ikke foreslå å fylle CV-en med nøkkelord brukeren ikke har dekning for, bare for å få en høyere andel. SM-4 går foran SM-6.
- **SM-C2 «Imponerende» brev.** Et brev som høres sterkere ut, men inneholder oppdiktede påstander, er en feil, ikke en forbedring.

## 10. Eksempeldata med fasit

Eksempelparene A, B og C er beskrevet i [briefen](../product-brief.md#eksempeldata-med-fasit). Fasiten for hvert par skal ligge i en egen testdata-mappe sammen med eksempelfilene: krav som matcher og mangler, nøkkelord og sjekklisten for søknadsbrevet. Både de automatiske testene, testmodusen og den manuelle sjekken av KI-svarene (SM-4) bruker disse filene. Eksempeldataene bør lages før kodingen av P2 starter, siden testene og de lagrede svarene avhenger av dem.

## 11. Åpne spørsmål

1. **Hvilken KI-leverandør og modell?** Avgjøres i arkitekturen ut fra norsk språkkvalitet, kostnad og databehandling (NFR-4).
2. **Hvordan finner koden nøkkelordene i stillingsannonsen (FR-19)?** Det er bestemt at koden skal gjøre det, ikke språkmodellen, men ikke hvordan. Én mulighet er en ordliste over vanlige ferdigheter, verktøy og sertifikater. Avgjøres i arkitekturen.
3. **Hvilket bibliotek for PDF-innlesing?** Må testes mot eksempel-CV C (to kolonner) tidlig i arkitekturen, før resten bygges på det.
4. **Hvordan skal brevet se ut i PDF-eksporten?** Holder enkel tekst, eller trengs et brevoppsett med dato og avsender?

## 12. Antagelser bekreftet av gruppa

Claude foreslo disse punktene i første utkast, uten at gruppa hadde bestemt dem. Gruppa gikk gjennom dem i pull request #4 (2026-10-19) og bekreftet alle uten endringer.

- §4.1 FR-1: Maks filstørrelse 5 MB.
- §4.1 FR-2: Brukeren kan se og rette CV-teksten (tiltak mot feil innlesing av PDF med kolonner).
- §4.1 FR-3: Stillingsannonsen må være mellom 100 og 15 000 tegn.
- §4.1 FR-4: Forhåndsvalg er norsk, formell og fullt utkast. Ønskede nøkkelord brukes i ATS-nøkkelordanalysen.
- §4.2: «Analyser» kjører gap-analysen og ATS-nøkkelordanalysen. Søknadsbrev og CV-forbedringsforslag har egne knapper.
- §4.2 FR-5: Gap-analysen skrives på valgt språk.
- §4.3: Krav som mangler, kan nevnes som noe søkeren vil lære, ikke som noe søkeren kan.
- §4.4 FR-10: Lagrede svar for alle kombinasjoner av innstillinger, laget med et skript.
- §4.5 FR-12: Passord må ha minst 8 tegn, ingen andre regler.
- §4.6 FR-18: Krav som mangler, nevnes som spørsmål i CV-forbedringsforslagene.
- §4.7 FR-19: Nøkkelordene finnes i kode, ikke av språkmodellen.
- §4.8 FR-23: Bare søknadsbrev og brevforslag eksporteres.
- §5 NFR-5: Tidsgrense på 60 sekunder per KI-kall.
- §5 NFR-7: WCAG 2.1 AA som mål der det er rimelig.
- §5 NFR-8: Grensesnittet er bare på norsk.
- §6: Inndelingen i fire skjermbilder.
