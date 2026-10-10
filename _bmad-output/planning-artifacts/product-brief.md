# Product Brief: AI CV & Job Application Assistant

**Gutta krutt** — IBE160 Programmering med KI, Høgskolen i Molde, høst 2026
Team: Ole A. Flaa, Henrik O. Kulseng, Haakon Remen Otterlei
Vanskelighetsgrad (fra emnets idéliste): 🟠 Middels

_Versjon 2 (2026-10-10): oppdatert etter [faglærers tilbakemelding](../../docs/tilbakemeldinger/tilbakemelding-product-brief.md). Se [endringer i product brief](../../docs/endringer/endringer-product-brief.md) for hva som er endret og hvorfor._

## Executive Summary

AI CV & Job Application Assistant er et verktøy som hjelper studenter med å lage skreddersydde jobbsøknader basert på egen CV og en konkret stillingsannonse. Verktøyet leser CV-en og annonsen, identifiserer hvilke kvalifikasjoner som matcher og hvilke som mangler (gap-analyse), og genererer — etter brukerens eget valg — enten et komplett utkast til søknadsbrev eller konkrete forbedringsforslag studenten selv skriver inn. I tillegg gir det CV-forbedringsforslag og en nøkkelordanalyse for ATS (automatiske rekrutteringssystemer), og resultatet kan eksporteres til Markdown og PDF. Prosjektet bruker ekte kall til en språkmodell (LLM-API), men har også en testmodus med lagrede svar slik at appen kan kjøres og testes uten API-nøkkel. Målgruppen er norske studenter som søker sommerjobb, deltidsjobb eller sin første heltidsstilling.

## The Problem

Å skrive en god, skreddersydd søknad for hver enkelt stilling er tidkrevende. Mange studenter ender opp med å (a) sende samme generiske brev til alle stillinger, eller (b) bruke generiske AI-chatboter som produserer søknader fulle av floskler rekrutterere i dag kjenner igjen umiddelbart. Samtidig vet mange studenter for lite om hvordan automatiserte rekrutteringssystemer (ATS) faktisk filtrerer søknader, og får avslag uten å forstå hvorfor — de mangler innsikt i hvilke konkrete kvalifikasjoner som faktisk mangler for en gitt stilling.

## The Solution

Studenten logger inn, laster opp CV (PDF eller TXT) og limer inn teksten fra en konkret stillingsannonse. Brukeren kan angi ønskede nøkkelord, og velger språk (norsk/engelsk) og tone (formell/uformell). Verktøyet:

1. Kjører en gap-analyse: sammenligner CV mot annonsens krav og viser konkret hva som matcher og hva som mangler.
2. Genererer — etter brukerens valg — et fullt utkast til søknadsbrev i valgt språk og tone, eller kun konkrete forslag/forbedringspunkter studenten selv skriver inn. Brevet og forslagene skal bare bygge på det som faktisk står i CV-en.
3. Gir CV-forbedringsforslag basert på annonsen.
4. Gir en ATS-nøkkelordanalyse: hvilke nøkkelord fra annonsen som finnes og mangler i CV-en beregnes i kode (ikke av språkmodellen), og KI brukes bare til å forklare resultatet og foreslå omformuleringer.

Resultatet kan eksporteres til Markdown og PDF, eller kopieres direkte til utklippstavlen.

## What Makes This Different

Vi er ærlige på at hver enkelt del av dette allerede finnes hos etablerte aktører: Jobscan og lignende dekker ATS-scoring, Rezi/Kickresume/Enhancv dekker AI-generert søknadsbrev, og LinkedIns eget "Apply Assistant" tilbyr lignende funksjonalitet direkte i søkeflyten. Vi bygger ingen unik teknologi.

Vårt bidrag er (a) å samle gap-analyse, brevgenerering, CV-forbedring og ATS-tips i én sammenhengende flyt tilpasset norske studenter og det norske arbeidsmarkedet, og (b) å la brukeren selv styre hvor mye AI skal generere versus foreslå — i stedet for å tvinge et ferdig, generisk brev på studenten. Vi legger også vekt på at forslagene skal bygge på det som faktisk står i CV-en og ikke dikte opp erfaring — et kjent problem hos flere konkurrerende verktøy. Dette kravet er gjort testbart i suksesskriteriene under.

## Who This Serves

Primær målgruppe: norske studenter, uavhengig av studieretning, som søker sommerjobb, deltidsjobb eller sin første heltidsstilling etter studiene. De har typisk en CV, men mangler tid, erfaring eller innsikt til å skreddersy hver søknad godt, og vet ofte ikke hvorfor de siles ut av automatiske systemer.

## Success Criteria

Kriteriene under er skrevet slik at de kan bli testtilfeller. De refererer til eksempeldataene med fasit beskrevet i neste avsnitt.

1. **Kjerneflyt ende-til-ende:** Med CV A og annonse A kan en ny bruker registrere seg, logge inn, laste opp CV, lime inn annonse og få både gap-analyse og søknadsbrev uten feil — både med ekte LLM-kall og i testmodus.
2. **Innlesing av CV:** For alle tre eksempel-CV-ene (inkludert to-kolonne-CV-en C i PDF) finnes alle kvalifikasjonene som fasiten lister opp, i teksten appen henter ut av filen.
3. **Gap-analyse:** For hvert eksempelpar viser gap-analysen alle krav fasiten markerer som manglende (for par A: «SQL» og «førerkort klasse B»), og markerer ingen av fasitens matchende krav som manglende.
4. **Ingen oppdiktet erfaring:** Søknadsbrev og forslag for hvert eksempelpar nevner ingen utdanning, arbeidsgiver, ferdighet eller erfaring som ikke står i CV-en. Konkret: brevet for par A påstår ikke at søkeren kan SQL eller har førerkort. Sjekkes mot en skriftlig sjekkliste per eksempelpar.
5. **Brukervalg respekteres:** Valget «fullt utkast» gir et sammenhengende brev, mens «kun forslag» gir en punktliste uten ferdig brev. Valgt språk (norsk/engelsk) og tone (formell/uformell) gjenspeiles i resultatet.
6. **ATS-nøkkelordanalyse:** Nøkkelord-matchen beregnes i kode, gir samme resultat hver gang for samme input, og har automatiske enhetstester mot fasiten for alle tre eksempelparene.
7. **Eksport:** Søknadsbrevet kan eksporteres til Markdown og PDF og kopieres til utklippstavlen, og den eksporterte filen inneholder hele brevet med norske tegn (æ, ø, å) korrekt gjengitt.
8. **Tilgangskontroll og kryptering:** En innlogget bruker kan ikke se en annen brukers dokumenter (testet med to testbrukere), og lagrede CV-er og brev er ikke lesbare i klartekst i databasen.
9. **Sletting:** Når en bruker sletter et dokument eller kontoen sin, er tilhørende data borte fra databasen.
10. **Kjørbar for sensor:** Appen kan startes lokalt etter README uten gruppens API-nøkkel, og testmodus kjører hele kjerneflyten (kriterium 1) med eksempeldataene.

## Eksempeldata med fasit

Gruppa lager tre oppdiktede eksempelpar (CV + stillingsannonse) med forventet resultat. De brukes i automatiske tester, i manuell kvalitetskontroll av KI-svarene og i testmodusen for sensor. Alle personer, arbeidsgivere og annonser er oppdiktet — ingen ekte personopplysninger legges i repoet.

| Par | CV | Annonse | Forventet match | Forventet mangler | Hva paret tester |
|---|---|---|---|---|---|
| A | IT-student, Python, Git, deltid i kundeservice (PDF, enkel layout) | Sommerjobb som junior utvikler (norsk) — krav: Python, SQL, Git, førerkort klasse B | Python, Git | SQL, førerkort klasse B | Grunnleggende kjerneflyt og «ikke dikte opp» |
| B | Økonomistudent, Excel, regnskapsfag, butikkerfaring (TXT) | Deltidsjobb som regnskapsassistent (norsk) — krav: Excel, regnskapsforståelse, Tripletex | Excel, regnskapsforståelse | Tripletex | TXT-opplasting og uformell tone |
| C | Logistikkstudent, bachelor logistikk, Excel, lagerjobb (PDF, to kolonner) | Graduate trainee innen logistikk (engelsk) — krav: bachelor i logistikk/økonomi, SAP, flytende engelsk | Bachelorgrad, engelsk | SAP | Vanskelig PDF-layout og engelsk språk |

Den endelige fasiten (eksakt liste over krav, nøkkelord og sjekkliste for søknadsbrevet) skrives ned sammen med eksempelfilene, slik at testene kan peke på den.

## Scope

**I V1 (rangert etter prioritet):**

Kjerneflyten bygges ferdig og stabil før resten startes.

1. Opplasting av CV (PDF eller TXT) og innliming av stillingsannonsetekst
2. Gap-analyse mot annonsen
3. Søknadsbrev med brukervalg mellom fullt utkast og forslag/punkter, samt valg av språk (norsk/engelsk) og tone (formell/uformell)
4. Testmodus med lagrede LLM-svar for de tre eksempelparene
5. Innlogging, kryptert lagring av dokumenter og sletting av data (reell implementasjon, ikke forenklet)

Deretter, i denne rekkefølgen:

6. CV-forbedringsforslag
7. ATS-nøkkelordanalyse beregnet i kode, med KI-forklaring og forslag til omformulering
8. Eksport til Markdown og PDF, og kopiering til utklippstavlen

**Utenfor omfang (V1):**

- Læring av brukerens skrivestil fra tidligere søknader (flyttet til Vision)
- Opplasting av DOC/DOCX og eksport til DOC/DOCX
- Automatisk innhenting av stillingsannonser fra eksterne plattformer (f.eks. Finn.no, LinkedIn) — brukeren limer inn annonseteksten selv
- Støtte for andre språk enn norsk og engelsk
- Betalings-/kjøpsfunksjonalitet
- Automatisk innsending av søknader ("auto-apply")

**Risiko å være bevisst på:** Gruppa har valgt å beholde alle fire kjernefunksjonene fremfor å gå smalt og dypt på én, men har strammet inn omfanget ved å fjerne skrivestil-læring og DOC-støtte og begrense eksporten til to formater. Rangeringen over sikrer at kjerneflyten (punkt 1–5) blir ferdig og stabil først. De største gjenværende risikoene er (a) pålitelig innlesing av CV-er med kolonner og tabeller, og (b) å kontrollere at språkmodellen ikke dikter opp erfaring. Begge håndteres med eksempeldata med fasit (se over), og ATS-delen er flyttet fra KI til kode slik at den kan testes med fasit.

## Teknologi, KI-avhengighet og kjørbarhet

Konkrete teknologivalg tas og begrunnes i arkitekturdokumentet. Briefen setter disse føringene:

- **LLM-leverandør:** Velges i arkitekturen ut fra kvalitet på norsk tekst, kostnad og hvordan leverandøren behandler data som sendes til API-et. Gruppa setter en forbruksgrense hos leverandøren for å holde kostnaden under kontroll.
- **Testmodus:** Når ingen API-nøkkel er satt (eller testmodus er slått på eksplisitt), bruker appen lagrede svar for de tre eksempelparene i stedet for ekte LLM-kall. Slik kan sensor prøve hele kjerneflyten uten egen nøkkel eller betalt konto, og de automatiske testene blir raske, gratis og forutsigbare.
- **Konfigurasjon og hemmeligheter:** API-nøkkel og krypteringsnøkkel settes via miljøvariabler. Repoet inneholder en `.env.example` med alle nødvendige variabler, mens `.env` aldri sjekkes inn (allerede dekket av `.gitignore`).
- **Filhåndtering:** Bibliotek for PDF-lesing og PDF-eksport velges tidlig i arkitekturen og testes mot eksempel-CV C (to kolonner) før resten av flyten bygges på det.
- **Plassering i repoet:** Eksempeldata og fasit ligger i en egen testdata-mappe, planleggingsdokumentene lenkes fra README, og README beskriver hvordan appen kjøres både i testmodus og med egen API-nøkkel.

## Sikkerhet og personvern

Verktøyet håndterer personopplysninger og personlige dokumenter (CV, søknadsbrev), og krever derfor ordentlig innlogging og kryptert lagring — ikke en forenklet skoleversjon. Dette inkluderer sikker autentisering, kryptering av lagrede dokumenter, og en tydelig policy for hvor lenge data lagres og hvordan de kan slettes. Siden prosjektet bruker en ekstern LLM-API, må gruppa også ta stilling til hva som faktisk sendes til API-leverandøren, og sikre at dette er i tråd med god personvernpraksis. I utvikling og testing brukes kun oppdiktede CV-er og søknader — aldri ekte personopplysninger i repoet.

## Vision

Om konseptet videreutvikles utover kurset, kan det vokse fra et generelt studentverktøy til noe tilpasset spesifikt for norske høgskoler/universiteter — for eksempel integrert med karriereveiledning ved Høgskolen i Molde, eller utvidet med tilbakemelding fra faktiske rekrutterere. Naturlige utvidelser etter V1 er læring av brukerens egen skrivestil fra tidligere søknader, og støtte for flere filformater (DOC/DOCX) ved opplasting og eksport. For kursets del er målet et solid, fungerende verktøy som viser hvordan AI kan brukes ansvarlig og presist i en rekrutteringskontekst.
