# Brief for skriverne av epic-filene

> **Historisk dokument.** Briefen beskriver planen slik den var 2026-11-19, før Haakon gikk gjennom storyene én og én. Mye er endret etterpå, for eksempel at `normaliser` ligger i `kjerne/tekst.py`, at story 5.3 er delt (36 stories), og at eierne er bestemt. Gjeldende tekst står i [`../epics.md`](../epics.md), og endringene står i [`../gjennomgang.md`](../gjennomgang.md).

_Skrevet av Claude Code 2026-11-19 på oppdrag fra Haakon. Skriverne er KI-agenter som får hver sin gruppe epics. Briefen gir dem det de trenger for å skrive én fil per epic uten å kjenne økten der epicene ble bestemt._

## Oppgaven

Gruppa vil ha **én fil per epic** i denne mappen (`.working/epic-00.md` … `.working/epic-07.md`). Etterpå setter Claude dem sammen til `../epics.md`.

Epicene og storyene er **allerede skrevet og godkjent av Haakon** i `../epics.md` (fra overskriften `## Epic 0:` og ut). Du skal derfor ikke lage storyene på nytt. Du skal:

1. Hente teksten for hvert av dine epics fra `../epics.md`, fra `## Epic N:` til neste `## Epic`.
2. Skrive den til `.working/epic-NN.md` (to sifre: `epic-00.md`, `epic-03.md`).
3. Kontrollere teksten mot kildene og reglene under, og bare rette **objektive feil**:
   - feil ID (FR, NFR, AD, UX-DR, SM, issue) eller en ID som ikke finnes
   - noe som strider mot arkitekturen, PRD-en, UX-en eller grensene i denne briefen
   - en story som avhenger av en senere story i samme epic, eller av et senere epic
   - en henvisning til et filnavn, en URL eller en funksjon som har et annet navn i arkitekturen
   - språkfeil
4. **Ikke** legge til nye stories, slette stories, endre rekkefølgen, endre titler eller utvide omfanget. Ser du at noe mangler, skriver du det i rapporten i stedet.
5. Avslutte med en rapport (under 250 ord): filene du skrev, **hver endring** med story og begrunnelse, og funn du ikke rettet.

Ikke endre andre filer, og ikke commit.

## Kilder

Alle stier er relative til roten av repoet.

- PRD: `_bmad-output/planning-artifacts/prd/prd.md` (FR-1 – FR-23, NFR-1 – NFR-11, SM-1 – SM-10, §8.1 nødplanen)
- Arkitektur: `_bmad-output/planning-artifacts/architecture/architecture-G48-flaa-kulseng-otterlei-2026-11-03/ARCHITECTURE-SPINE.md` (AD-1 – AD-22, §3 konvensjoner og URL-er, §5 mapper). Oppdatert 2026-11-19, se under.
- UX: `_bmad-output/planning-artifacts/ux-designs/ux-G48-flaa-kulseng-otterlei-2026-11-12/EXPERIENCE.md` og `DESIGN.md`
- Kravoversikten med UX-DR1 – UX-DR36 og tilleggskravene: `../epics.md`, fra `## Kravoversikt` til `## Oversikt over epicene`
- Det som allerede finnes i `app/`: `nokkelord/ordliste.json`, `testdata/eksempler/A–D/` (CV, `annonse.txt`, `fasit.json`), `testdata/lag_cv_pdf.py`, `eksport/fonter/`

`architecture/technology.md` beskriver et annet prosjekt og skal ikke brukes.

## Format

Overskriftene må være nøyaktig slik, fordi `bmad-sprint-planning` leser dem med et skript:

```
## Epic N: Tittel

Ett avsnitt om hva brukeren kan etter epicet, hvor koden ligger og hva som kan kuttes.

### Story N.M: Tittel

Som …
vil jeg …,
slik at ….

**Krav:** FR-…, NFR-…. **UX:** UX-DR…. **Styres av:** AD-….

**Akseptansekriterier:**

**Gitt** …
**Når** …
**Så** …
**Og** …
```

- Ingen andre overskrifter med ordene «Epic» eller «Story».
- Norsk bokmål. Klart og enkelt språk, korte setninger, aktiv form. Ord fra PRD-ens ordliste (§3) brukes med samme betydning.
- Kode, filnavn og URL-er i backticks. Navn i koden følger AD-16 (norsk uten æ, ø og å).
- Hvert akseptansekriterium skal kunne testes, automatisk eller manuelt.

## Beslutninger fra økten 2026-11-19

Alle er godkjent av Haakon:

- **Vertikale snitt.** Hvert epic virker fra siden, gjennom tjenesten, til databasen, og kan testes alene. Filene legges etter eierskapsreglene i AD-2, ikke etter epic. Et snitt skriver aldri til en annen apps modeller.
- **DRY med fellesmapper.** Det som brukes av flere snitt, ligger ett sted og kopieres aldri: `app/kjerne/`, `app/ki/`, `app/nokkelord/`, `app/eksport/`, `app/templates/felles/` (maldeler med `{% include %}`), `app/static/css/tokens.css` og `komponenter.css`, `app/static/js/`, `app/conftest.py`. Det som UX-en eller arkitekturen beskriver for flere steg, lages i Epic 0. Det som først trengs i ett snitt, lages der og flyttes til en fellesmappe når et snitt til trenger det.
- **Hele Epic 0 flettes før noen andre epics startes** (AD-21, endret i dag fra «den første storyen»).
- **Testene kjører på GitHub Actions** for hver pull request (AD-18, story 0.2).
- **Tomme modellskjeletter i Epic 0** (AD-21). Det er et bevisst avvik fra BMAD-regelen om å lage tabeller bare når de trengs. Felt legges til i storyen som trenger dem.
- **Nye ting i arkitekturen i dag:** `templates/felles/` og CSS-filene (AD-15, §5), `/personvern/` (åpen side, §3), avhengigheten `ki → dokumenter` bare for `pdf_innlesing` (AD-2, §1), eksempelknappen `/eksempel/<par>/` i `analyse/` (§3), `/resultat/brev/` (GET viser, POST lager brevet), `/resultat/forklaring/` (POST, «Prøv forklaringen igjen»), feltene `del_av_cv` og `forslag` i `CVForbedringer` (§3), og den skriftlige testplanen `docs/testplan.md` (AD-17).
- **Bredde:** storyene bruker 320 px (UX), som også oppfyller 360 px i NFR-7.

## Epicene og grensene mellom dem

Rekkefølgen er byggerekkefølgen. Epic 0–5 er kjerneflyten (P1–P5) og skal være ferdige til sjekkpunktet 2. desember (PRD §8.1).

| Epic | Fil | Eier av | Grense mot naboene |
|---|---|---|---|
| 0 Appen kan startes og testes | `epic-00.md` | prosjektet, `settings.py`, `lag_env.py`, `requirements.txt`, `kontoer.Bruker`, GitHub Actions, `base.html`, `templates/felles/`, CSS, `skjema.js`, `kjerne/`, `ki/port.py`, `ki/modeller.py`, `conftest.py`, tomme modellskjeletter | Ingen sider med brukerdata. |
| 1 Konto og innlogging | `epic-01.md` | `kontoer/`: registrering, `/personvern/`, innlogging og utlogging, Min konto, sletting av konto | Etter innlogging til Min konto. Epic 2 endrer det til steget brukeren står i. |
| 2 CV-en (steg 1) | `epic-02.md` | `dokumenter/` (`les_cv`, `lagre_cv`, `lagre_cv_tekst`, `slett_cv`), `ki/eksempelpar.py` (`hent_eksempelpar`, `normaliser`, `Fasit`), `analyse.tjenester.siste_steg`, eksempelknappen, «Slett mine dokumenter» | «Neste» går tilbake til steg 1 til Epic 3 finnes. |
| 3 Annonse og nøkkelordanalyse | `epic-03.md` | `nokkelord/`, `Analyse`-feltene for annonse, språk, nøkkelord, nøkkelordresultat og `ki_status`, «Analyser» med bare `nokkelord.match`, steg 2, steg 3 med nøkkelordkortet, `finn_eksempelpar` | Virker uten KI. Gap-analysen og forklaringen kommer i Epic 4. |
| 4 Gap-analyse med KI | `epic-04.md` | `TestmodusKlient`, `ClaudeKlient`, `eksempel_hash`, `svarfil`, prompter for `gap_analyse` og `nokkelord_forklaring`, `lag_lagrede_svar` med evalueringsrapport (utvidbar), kravlisten, KI-varsel og KI-merker, feiltilstander, FR-11-meldingen | KI-forklaringen er siste story og kan kuttes. Forutsetter issue #16 fra story 4.4. |
| 5 Søknadsbrev (steg 4) | `epic-05.md` | operasjonen `brev`, `Brev`-feltene, 24 lagrede brev, rapportens brevdel med par D og issue #28, «Lag søknad» i steg 3, steg 4, «Lag nytt brev», «Start ny søknad», SM-1-testen | Ingen kopiering eller nedlasting (Epic 7). |
| 6 CV-forbedringsforslag (P6) | `epic-06.md` | operasjonen `cv_forbedring`, `CVForbedring`, 6 lagrede svar, rapportens CV-del, `/resultat/cv-forbedring/`, listen i steg 3 | Hele epicet er punkt 2 i nødplanen. |
| 7 Ta med søknaden ut (P8) | `epic-07.md` | `kopier.js`, `eksport/markdown.py`, `eksport/pdf.py`, `/resultat/brev/eksport/`, avsenderskjemaet | Brevoppsettet (7.4) er siste story og punkt 1 i nødplanen. |

## Kjente risikoer som ikke skal «rettes» bort

- Steg 3 og `analyse/tjenester.py` endres i Epic 3, 4, 5 og 6. Det er et bevisst valg. Claudes råd er at steg 3 bygges med én maldel per kort, men det er ikke et krav i storyene.
- Eksempel A gir ekte lagrede svar først etter story 4.5. Før det bruker testene `falsk_ki`.
