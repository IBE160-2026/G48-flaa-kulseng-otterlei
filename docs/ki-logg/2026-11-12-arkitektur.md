# Arkitektur med bmad-architecture

| | |
|---|---|
| **Dato** | 2026-11-03 – 2026-11-12 |
| **Hvem** | Henrik O. Kulseng |
| **Verktøy** | Claude Code (Claude Opus 5.5), BMAD-skill `bmad-architecture` i veiledet modus |
| **Commits / PR** | `d8a6bb2`, `b132987`, `258531c`, commiten med dette innlegget, pull request på branchen `docs/arkitektur` |

## Mål

Lage arkitekturen for appen etter PRD-en: velge teknologi med begrunnelse, svare på de åpne spørsmålene 1–3 i PRD-en (KI-leverandør, nøkkelordmetode og PDF-bibliotek) og fastsette regler, slik at tre gruppemedlemmer med hver sin Claude bygger kode som passer sammen.

## Viktigste prompts

1. «hva er neste steg i prosessen?»
2. «vi er 3 stykker i gruppen så den er noen som jobber med den andre branchen. Så prd-en er ikke helt ferdig enda». Arkitekturen ble satt på vent til PR #5 var flettet.
3. Svar på spørsmål om arbeidsmåte, erfaring og formål: veiledet modus, «lite erfaring, Python», og at arkitekturen også skal brukes av sensor til å kontrollere koden. Sammen med svaret ga Henrik et sammendrag av hva sensorveiledningen og faglærer ser etter, og et tips om å skrive begrunnelse og alternativer som ble valgt bort, for hvert valg.
4. «vi velger Django»
5. «vi velger Claude Opus 5.5, og lagdelt struktur er greit, Alle har claude pro»
6. «lag arkitekturen slik at den samsvarer med prd-en.»

## Hva KI gjorde

- Leste PRD-en, addendumet, faglærers tilbakemelding på briefen, og senere faglærers tilbakemelding på PRD-en og `technology.md`, som kom på `main` 2026-11-12.
- La fram alternativer med en anbefaling for hvert stort valg:
  - **rammeverk:** Django, Flask, FastAPI + React eller Streamlit
  - **KI-leverandør:** Claude, OpenAI, Gemini eller Mistral
  - **database:** SQLite eller PostgreSQL
  - **kryptering:** egne felttyper, ferdig tillegg eller SQLCipher
- Opplyste om at Claude anbefalte Claude (interessekonflikt), og sjekket databehandling og forbruksgrense i Anthropics offisielle dokumenter.
- Påpekte at Claude Pro ikke gir tilgang til API-et. Det må lages en egen konto i Claude Console.
- Skrev arkitekturen med 18 beslutninger (AD-er). Hver har regel, begrunnelse og hva som ble valgt bort. Det gruppa ikke selv hadde bestemt, er merket «[Forslag]».
- Kjørte en automatisk sjekk og tre uavhengige KI-kontrollører på utkastet:
  - Én sjekket versjoner og tekniske påstander mot nettet.
  - Én prøvde å finne deler som følger alle reglene, men likevel ikke passer sammen.
  - Én sjekket arkitekturen mot PRD-en og faglærers tilbakemeldinger.
- Rettet inn funnene. Det ble tre nye AD-er (AD-19 lagring, AD-20 feilkontrakt og AD-21 samarbeid og migreringer), og flere av de andre ble strammet inn.
- Oppdaterte README og `.gitignore`.

## Våre vurderinger og korrigeringer

- **Ventet på PRD-gjennomgangen:** Henrik ba om at arkitekturen skulle vente til endringene fra PR #5 var flettet, siden en annen i gruppa jobbet med PRD-en.
- **Rammeverk:** Gruppa valgte Django.
- **KI-leverandør og struktur:** Gruppa valgte Claude Opus 5.5 og godtok lagdelt struktur.
- **Begrunnelser i dokumentet:** Etter Henriks tips står begrunnelse og alternativer som ble valgt bort, i selve arkitekturen, ikke bare i beslutningsloggen. Det er et bevisst avvik fra BMAD-standarden.
- **CV-filen:** Claude foreslo å ikke lagre selve CV-filen, bare teksten. Gruppa ba om at arkitekturen skal følge PRD-en, og PRD-en sier at CV-en (filen) lagres kryptert. Forslaget ble derfor forkastet.
- **Rettet av KI-kontrollørene:**
  - Claudes eget versjonsoppslag ga utdaterte tall: Django 6.1.2 og anthropic 2.4.0. Kontrolløren fant 6.1.3, med sikkerhetsrettelser, og 2.8.0. Det ble bekreftet med et nytt oppslag.
  - PDF-eksporten ville krasjet på tankestrek og typografiske anførselstegn. Løsningen er en egen font, DejaVu Sans.
  - «Prøv med eksempel A» kunne bommet på sine egne lagrede svar på grunn av ulike linjeskift.
  - Egen CV i testmodus ville ikke fått noen nøkkelordanalyse, i strid med FR-11.
  - Djangos standardregler for passord bryter med FR-12.
- **Må bekreftes av gruppa:** Alle punkter merket «[Forslag]» i arkitekturen. Det gjelder blant annet SQLite, Resultat i tre deler, grensen på 30 000 tegn for CV-teksten og eksempelpar D for prompt-injeksjon.

## Resultat

- Arkitekturen ligger i `_bmad-output/planning-artifacts/architecture/architecture-G48-flaa-kulseng-otterlei-2026-11-03/`, sammen med beslutningsloggen og de tre KI-gjennomgangene i `reviews/`.
- PRD-ens åpne spørsmål 1–3 har nå et svar: Claude Opus 5.5 (AD-4), en ordliste i kode (AD-7) og pdfplumber, som må testes mot CV C før P2 (AD-13).

**Gjenstår:**
- Gruppa går gjennom pull requesten og bekrefter eller retter «[Forslag]».
- PRD-en oppdateres etter faglærers tilbakemelding og arkitekturen (§8 punkt 1 i arkitekturen), og gruppa bestemmer en kuttrekkefølge.
- Noen i gruppa lager API-konto i Claude Console og setter forbruksgrense.
- Eksempelparene med fasit lages, og pdfplumber testes mot CV C.
- UX (`bmad-ux`), deretter epics og stories.

## Oppfølging etter gjennomgang i PR #13 (2026-11-12)

**Prompts:**
- «fikk dette som kommentar på arkitekturen, hvordan fikser vi dette?» Henrik limte inn Oles kommentar.
- «hva betyr KI-laget, og hva gjør PR #12?»
- «ja, Ole tar KI-laget, og opprett issuene nå»

**Hva KI gjorde:**
- Fant ut at PR #14 (PRD rettet etter faglærers tilbakemelding) allerede var flettet. Oles punkt om å oppdatere PRD-en og bestemme kuttrekkefølgen var dermed løst.
- Flettet `main` inn i `docs/arkitektur`. Den eneste konflikten var tabellen i `docs/ki-logg/README.md`, og begge radene ble beholdt.
- Satt `status` i arkitekturen tilbake til `draft` og oppdaterte åpne punkter: PRD-punktet er løst, og fristen for eksempeldataene er lagt inn.
- Oppdaterte `docs/arbeidsfordeling.md`. Henrik har arkitektur, UX og frontend, og Ole har KI-laget.
- Opprettet issue #16 (API-konto), #17 (pytest-django) og #18 (bekrefte [Forslag]) med etiketten `agent`, slik Ole foreslo.

**Gruppas vurderinger:**
- Ole og Henrik er enige i [Forslag]-punktene SQLite, resultat i tre deler, 30 000 tegn, eksempelpar D og pip. Haakon har ikke svart.
- Av de avanserte delene Ole nevnte, valgte Henrik å merke bare **hash-testen** som mulig kutt. Låsen mot dobbeltklikk og eksempelpar D beholdes.
- Henrik godtok Oles forslag om at Ole tar KI-laget (`ki/`).
- Henrik ba om at issuene ble opprettet nå, selv om PR #12 (åpne punkter som issues) ikke er flettet.
