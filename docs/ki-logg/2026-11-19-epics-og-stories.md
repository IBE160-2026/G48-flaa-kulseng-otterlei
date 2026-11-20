# Epics og stories med bmad-create-epics-and-stories

| | |
|---|---|
| **Dato** | 2026-11-19 – 2026-11-20 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5), `bmad-create-epics-and-stories`, KI-subagenter |
| **Commits / PR** | Commitene på branchen `docs/epics-og-stories` og pull requesten med denne loggen |

## Mål

Dele kravene i PRD-en, arkitekturen og UX-en opp i epics og stories som kan bygges én om gangen, med akseptansekriterier som kan testes. Neste steg etter dette er sprint-planlegging og Epic 0.

## Viktigste prompts

1. «/bmad-create-epics-and-stories», og deretter «bruk anbefalingen din og lag en datert mappe»
2. «eg ønsker at du legger inn Epics som "vertical slices" dvs at koden er så isolert som mulig. Men det er selfølgelig vesentlig at du gjennbruker komponenter (dry-prinsippet). Lag fellesfoldere for felleskomponenter eller biblioteker.»
3. «kan du lage subagener for å lage stories for kvar epic?»
4. «Write a BRIEF.md in a .working folder, spawn writers for groups of epics, each writing epic-NN.md, then reconcile and assemble everything into epics.md. i want one file per epic.»
5. «professoren anbefaler at vi har human in the loop og review per epic og per story. så han anbefaler en og en story.»
6. «eg har ansvaret for epics og stories så la oss holde det til meg»
7. Én prompt per story og epic i gjennomgangen, for eksempel «ok med A og B, gå videre til 4.5»
8. «ok med epic 7, sett sammen epics.md» og «ja, gjør det»

## Hva KI gjorde

- **Før økten startet for alvor:** Laget en figur (SVG) som forklarer hvordan epics, stories og sprint-planlegging henger sammen, og hvorfor steget trengs. Figuren ble vist som en privat side og er ikke lagt i repoet.
- **Kravene:** Hentet ut FR-1–23, NFR-1–11, AD-1–22 og 36 UX-krav (UX-DR1–36), og la dem i `epics.md` med en tabell over hvilket epic som dekker hvilket krav.
- **Epicene:** Foreslo 8 epics (0–7) som vertikale snitt, og fellesmapper for det som deles (`kjerne/`, `ki/`, `nokkelord/`, `eksport/`, `templates/felles/`, `static/css/`, `static/js/` og `conftest.py`).
- **Storyene:** Claude skrev storyene i Epic 0–2 selv. KI-subagenter skrev først storyene i Epic 3–7. Deretter skrev Claude `.working/BRIEF.md`, og tre KI-skrivere kontrollerte hver sin gruppe epics mot arkitekturen og skrev én fil per epic (`epic-00.md`–`epic-07.md`). Claude avstemte funnene fra skriverne og satte filene sammen til `epics.md`.
- **Hull i arkitekturen:** Både skriverne og gjennomgangen fant ting arkitekturen ikke sa noe om. Claude foreslo endringer, og alle står i beslutningsloggen til arkitekturen (`.memlog.md`):
  - `ki → dokumenter` (bare `les_cv`), og eksempelknappen i `analyse/`
  - `/personvern/`, `/` og `GET`/`POST` for bekreftelsessidene
  - `normaliser()` i `kjerne/tekst.py`, så `dokumenter` slipper å importere `ki`
  - låseteksten fra UX-en i AD-12
  - hashene for eksempelparene regnes ut første gang de trengs, og `EKSEMPLER_DIR` er en innstilling
  - grensen `AVSENDER_MAKS`
- **Gjennomgangen:** Claude viste hver av de 35 storyene med kriteriene, og pekte på hull og uklarheter med forslag til hvordan de kunne rettes. Etter siste story i hvert epic så Claude på epicet som helhet.
- **Kontroller til slutt:** Overskriftene leses riktig av `bmad-sprint-planning` (8 epics og 35 stories). Alle FR, NFR, UX-DR, SM og AD er nevnt i storyene.

**Feil KI fant og rettet selv:**
- Claude foreslo først å legge `samle_mangler()` i `analyse/tjenester.py`. Da det skulle skrives inn, så Claude at `lag_lagrede_svar` i `ki/` ikke får importere `analyse` (AD-2). Funksjonen ble lagt i `ki/mangler.py` i stedet, og Haakon fikk vite det.
- Beslutningsloggen sa at personvernteksten skulle ligge i `templates/felles/`. Skriverne flyttet den til `templates/kontoer/`, fordi bare `kontoer` bruker den. Loggen har fått et nytt innlegg som retter det.
- SM-8 og SM-9 var dekket av storyene, men ikke nevnt med ID. Det ble funnet i den siste kontrollen og rettet.

## Våre vurderinger og korrigeringer

- **Vertikale snitt og DRY** var Haakons krav. Haakon godtok Claudes forslag om at snittene er vertikale i det de leverer, mens filene legges etter eierskapsreglene i AD-2.
- **Epic 0 i fire stories:** Haakon godtok at Epic 0 deles i fire stories, og at hele Epic 0 flettes før noen andre epics startes (AD-21 er endret).
- **Én story om gangen:** Faglærer anbefaler at et menneske går gjennom hver story og hvert epic. Haakon gjorde det for alle 35 storyene og alle 8 epicene. Hver godkjenning og endring står i [gjennomgang.md](../../_bmad-output/planning-artifacts/epics/epics-G48-flaa-kulseng-otterlei-2026-11-19/gjennomgang.md).
- **Hvem som godkjenner:** Claude foreslo også at eieren av hvert epic skulle gå over det. Haakon sa først ja, men presiserte så at han har ansvaret for epics og stories og godkjenner dem alene. Ole og Henrik gir tilbakemelding i pull requesten før den flettes.
- **Hva gjennomgangen endret:** 32 av 35 stories ble endret. Haakon godtok Claudes forslag i alle disse. Eksempler:
  - Tester som ikke kunne kjøres slik de var skrevet: `fakta_i_cv` er omskrevet og kan ikke søkes etter (2.1), og regelen for når økten er utløpt manglet (1.2).
  - Feil som ville gitt krasj eller tap av data: deling på null når annonsen ikke har nøkkelord (3.1), sletting som leser krypterte felt (2.5), og «Last opp ny», som slettet CV-en for tidlig (2.3).
  - En regel for «vil lære» og påstander i evalueringen. Den løser issue #28 (5.2).
- **Én anbefaling ble ikke fulgt:** Claude nevnte at story 0.3 kunne deles i sideramme og felles komponenter. Haakon beholdt den samlet.
- **Tekst Claude foreslo:** Noen meldinger og etiketter står ikke i UX-en, og ordlyden er Claudes forslag. Det gjelder blant annet meldingen når annonsen ikke har nøkkelord, meldingen om en API-nøkkel som ikke godtas, «Lag nye forslag», etikettene på brevfeltet og filnavnene ved nedlasting. Det står i `gjennomgang.md`, så gruppa kan endre dem.
- **Issue #16:** Claude pekte på at 4.4–4.6 og Epic 5 trenger API-kontoen. Haakon opplyste at Ole har tatt issuen og lukker den når kreditt er kjøpt og forbruksgrensen er satt.

## Resultat

- `_bmad-output/planning-artifacts/epics/epics-G48-flaa-kulseng-otterlei-2026-11-19/`:
  - `epics.md` med kravene, oversikten og 8 epics med 35 stories
  - `gjennomgang.md` med godkjenningene
  - `.working/` med én fil per epic og briefen til skriverne
- Arkitekturen (`ARCHITECTURE-SPINE.md`) og beslutningsloggen er oppdatert med endringene over.
- README og statuslinja i `CLAUDE.md` er oppdatert.
- **Gjenstår:**
  - Ole og Henrik ser over pull requesten.
  - Sprint-planlegging (`bmad-sprint-planning`).
  - Hvem som eier hvilke epics, er ikke bestemt. `epics.md` har bare Claudes forslag.
  - Teksten står nå både i `epics.md` og i `.working/epic-NN.md`. Endres en story, må den endres begge steder.

## Etter gjennomgangen av issue #17 og #29 (2026-11-20)

**Prompts:** «kan du gå gjennom issue 17 og 29 og sjekke om det er noe eg ikkje har fått med meg?» og «ja, legg inn punkt 1–5 og push til PR #35»

Henrik hadde gjort en forhåndssjekk av begge issuene med Claude Code samme dag. Claude sammenlignet funnene med storyene:

- **#17:** Var allerede dekket av story 0.1. Henrik fant at `pytest-django` 4.14.0 virker med Django 6.1.3.
- **#29:** Fem ting manglet. Haakon ba om å få alle lagt inn:
  1. `lag_cv_pdf.py` skal kjøre uten ekstra installasjon (0.1).
  2. `fonttools==4.68.0` låses og står i §4 i arkitekturen.
  3. PDF-ene blir ikke like byte for byte, fordi zlib avgjør komprimeringen. Kommentaren i skriptet og README rettes i 0.1, og ingen test sammenligner PDF-ene byte for byte.
  4. Testen i 2.1 sjekker også at `fakta_i_cv` er lik for A og D.
  5. Kravet før P2 i AD-13 sa «alle `fakta_i_cv`», som ikke kan måles. Det er rettet til testen på ord fra 2.1.

Henrik kom fram til det samme som Haakon bestemte i gjennomgangen av 2.1: test ordene i `cv_kilde.txt`, ikke `fakta_i_cv` ordrett.

## Etter Oles og Henriks gjennomgang av PR #35 (2026-11-20)

**Prompts:** «ole og henrik har kommentert på pr #35 kan du gå over den igjen», «så det du foreslår å gjøre er å fikse opp i det de har kommentert» og «A, gjør det og push til PR #35 forklar dette til ole og henrik»

Henrik gikk gjennom sidene og eksporten (0.3, Epic 5 og 7), og Ole gikk gjennom KI-laget (Epic 4–6) mot PR #33 og #34. Begge brukte Claude Code. Claude sorterte kommentarene i det som allerede var gjort, det som trengte endring og det som hører til eierdiskusjonen (#36).

| Endring | Fra | Story |
|---|---|---|
| Bredde, zoom, trykkflater og fokusring sjekkes for hånd i `docs/testplan.md` | Henrik | 0.3 |
| Ventetilstanden har indikator, farger og «Dette tar vanligvis 10–30 sekunder» (UX-DR30) | Henrik | 0.3 |
| `fpdf2` logger tegn fra brevet når fonten mangler dem. Loggeren dempes og testes (AD-10) | Henrik | 7.3 |
| Markdown-filen har aldri avsender | Henrik | 7.4 |
| «Jobber …» er et eget kriterium, ikke en del av feilscenarioet | Henrik | 5.4 |
| Promptfilen for operasjonen med `## System` og `## Melding` | Ole | 4.4, 4.6, 5.1, 6.1 |
| Feltene i `Forklaring` | Ole | 4.6 og arkitekturen §3 |
| `svarform` settes av koden, ikke av KI | Claude, fra PR #34 | 5.1 |
| Koden fjerner `<cv>`- og `<annonse>`-merker fra brukerens tekst | Claude, fra PR #34 | 4.4 |

**Deling av 5.3:** Henrik foreslo å dele storyen i steg 3 og steg 4. Claude var enig i delingen, men pekte på at steg 3 først ikke kan testes alene, fordi «Lag søknad» sender brukeren til et steg 4 som ikke finnes. Claude foreslo tre valg: dele med steg 4 først, dele med steg 3 først, eller beholde storyen samlet. Haakon valgte å dele med steg 4 først: 5.3 Vise søknaden i steg 4 (testene lager `Brev` selv) og 5.4 Be om søknad i steg 3. Gamle 5.4–5.7 heter nå 5.5–5.8, og planen har 36 stories.

**Ikke endret:** Punktet fra issue #29 om 0.1 var allerede lagt inn. At 5.8 venter på issue #16, stod allerede i storyen. Henriks forslag om at Ole tar 5.1–5.2 og Henrik tar 5.3–5.8, hører til issue #36.
