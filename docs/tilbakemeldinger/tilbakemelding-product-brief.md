# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G48 – G48-flaa-kulseng-otterlei |
| **Product brief** | `product-brief.md` (commit `681c297`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Løsningen er tydelig beskrevet som en sammenhengende flyt: last opp CV, lim inn annonse, velg språk og tone, og få gap-analyse, søknadsbrev eller forslag, CV-forbedringer og ATS-tips. At brukeren selv velger mellom «fullt utkast» og «kun forslag», er et gjennomtenkt grep som skiller dere fra generiske chatboter.
2. Dere er ærlige og bevisste. «What Makes This Different» innrømmer at Jobscan, Rezi, Kickresume og LinkedIn dekker delene hver for seg, og avsnittet «Risiko å være bevisst på» viser at dere har tenkt gjennom avveiningen mellom bredde og dybde. Kravet om at forslag ikke skal «dikte opp erfaring», er et godt kvalitetsmål.

**De viktigste endringene:**

1. Reduser omfanget i v1. Læring av skrivestil fra tidligere søknader, opplasting av DOC og eksport til tre formater (PDF, DOC, Markdown) er hver for seg ekstra arbeid som ikke er nødvendig for kjerneflyten. Flytt skrivestil til Vision, og begrens filformatene.
2. Utvid suksesskriteriene. I dag er det ett samlet kriterium om en fungerende demo. Del det opp i konkrete, testbare kriterier, for eksempel «gap-analysen for eksempel-CV A og annonse B viser kravene X og Y som mangler» og «søknadsbrevet nevner ingen erfaring som ikke står i CV-en».
3. Planlegg hvordan sensor kan kjøre appen. Briefen sier at prosjektet bruker «ekte kall til en språkmodell». Det er fint, men sensor må kunne prøve appen uten deres nøkkel. Lag en testmodus med lagrede svar for en eksempel-CV og en eksempelannonse.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** 2) AI CV- og søknadsassistent (middels). Briefen er dette forslaget, som dere selv har oppgitt, utvidet med læring av skrivestil og eksport i flere formater.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Gap-analyse og ATS-tips må være forklarbare og konsistente. Lite tradisjonell beregning, men regler for hva som teller som match. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Bruker, CV, annonse, tidligere søknader, generert brev, forslag og analyseresultat. |
| Brukere, roller og innlogging | Middels | Én rolle, men «reell implementasjon» av innlogging, sikker autentisering og sletting av data. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Høy | Fire KI-funksjoner pluss stiltilpasning, to språk og flere toner. Kravet om ikke å dikte opp erfaring krever kontroll av svarene. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Middels | Ett LLM-API. Klokt at Finn.no og LinkedIn er holdt utenfor. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Hver student jobber med egne dokumenter. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Høy | Lesing av PDF/DOC/TXT og eksport til PDF/DOC/Markdown. CV-er med kolonner og tabeller er vanskelige å lese pålitelig. |
| Sikkerhet og personvern | Høy | Personopplysninger, kryptering av lagrede dokumenter, lagringstid og sletting, og vurdering av hva som sendes til LLM-leverandøren. Godt at dette er beskrevet. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer: last opp CV → lim inn annonse → se gap-analyse → få søknadsbrev eller forslag. CV-forbedringer, ATS-tips og eksport kommer deretter.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Risiko | Åtte v1-punkter, der flere (skrivestil, tre eksportformater, kryptert lagring) er store hver for seg. Gjennomførbart for tre personer med prioritering. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | OK | Funksjonene er tydelige og nummerert. Antall stories blir høyt, så rangér v1-punktene i PRD-en. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | Webapp med innlogging, database og LLM-kall er godt dokumentert. DOC-lesing og DOC-eksport er mindre vanlig og kan droppes. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Dere kan vurdere om et brev er godt, men det er vanskeligere å kontrollere systematisk at gap-analysen er riktig og at ingenting er diktet opp. Lag noen eksempel-CV-er og -annonser med fasit. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | Risiko | Innlogging, kryptering, sletting og eksport kan testes automatisk. KI-svarene må testes mot en sjekkliste. Beregnes nøkkelord-match i kode, kan også ATS-delen testes. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | Risiko | Ikke beskrevet. Uten testmodus må sensor skaffe egen API-nøkkel for å prøve kjerneflyten. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | Risiko | LLM-API er valgt, men leverandør, kostnad og testmodus er ikke nevnt. Velg modell i arkitekturen og legg inn mock-svar. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. Flytt læring av skrivestil fra tidligere søknader til Vision. Begrens opplasting til PDF og TXT, og eksport til Markdown og PDF (eller kopier til utklippstavle). Det fjerner tre krevende delprosjekter.
2. Gjør ATS-delen til en nøkkelordanalyse beregnet i kode, med KI bare for forklaring og omskriving. Da får dere en del av appen som kan testes med fasit, og som sensor kan kontrollere.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Klart hva verktøyet gjør og for hvem: norske studenter som søker sommerjobb, deltidsjobb eller første heltidsstilling. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Konkret om generiske brev, floskler fra chatboter og manglende innsikt i ATS-filtrering. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | OK | Beskriver hva studenten gjør steg for steg, og hva verktøyet gir tilbake. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Svært ærlig om konkurrentene, med et realistisk bidrag (samlet flyt, brukerstyrt KI-grad, ikke dikte opp erfaring). |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | OK | Tydelig målgruppe med konkrete behov. Det norske arbeidsmarkedet gir en god ramme for designet. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | Bare ett samlet kriterium. Del det opp i konkrete kriterier per funksjon, inkludert kvalitetskravet om ikke å dikte opp erfaring. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Juster | Tydelig inndeling, men v1 er bred. Flytt skrivestil og noen filformater ut, og rangér resten. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Integrasjon med karriereveiledning er tydelig plassert utenfor kurset. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | OK | Briefen er konkret nok til PRD. Lagre briefen under BMAD sin `_bmad-output`-struktur eller lenk til den fra README, så sensor finner planleggingsdokumentene samlet. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Juster | Mye reell funksjonalitet, men omfanget bør strammes inn slik at kjerneflyten blir stabil. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Endre | Ett samlet suksesskriterium er ikke nok til testtilfeller. Lag kriterier og eksempeldata med fasit. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | OK | Tydelig bruker og flyt. Skissér i UX-steget hvordan gap-analysen og valget mellom utkast og forslag vises. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Teknologi er ikke valgt ennå. Begrunn valg av LLM-leverandør, lagring og kryptering i arkitekturen, og velg biblioteker for filhåndtering tidlig. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Juster | Avhengig av LLM-API. Legg inn testmodus og eksempeldata, og beskriv oppsettet i README. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Bruk `.env.example` for API- og krypteringsnøkler, og bruk bare oppdiktede CV-er og søknader som testdata – aldri ekte personopplysninger i et offentlig repo. |

## 3. Neste steg for gruppen

1. Stram inn Scope: flytt skrivestil til Vision, begrens fil- og eksportformater, og rangér de gjenværende v1-punktene.
2. Skriv 6–10 konkrete suksesskriterier som kan bli testtilfeller, og lag to–tre oppdiktede eksempel-CV-er og annonser med forventet resultat.
3. Velg LLM-leverandør og beskriv i arkitekturen hvordan nøkkelen konfigureres og hvordan testmodusen for sensor skal fungere.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
