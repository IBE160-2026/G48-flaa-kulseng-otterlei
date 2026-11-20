## Epic 0: Appen kan startes og testes

Sensor kloner repoet, følger README og starter appen i testmodus uten nøkkel, og testene kjører med én kommando. Epic 0 lager fellesmappene som alle de andre snittene bygger på, og hele epicet flettes før noen andre epics startes (AD-21). Story 0.1 kommer først. Deretter kan 0.2, 0.3 og 0.4 bygges samtidig, siden de rører hver sine filer. Delingen i fire stories og story 0.2 ble godkjent av Haakon 2026-11-19, og AD-21 og AD-18 er oppdatert.

### Story 0.1: Appen starter i testmodus etter README

Som sensor
vil jeg starte appen ved å følge README, uten API-nøkkel,
slik at jeg kan prøve den uten gruppas nøkler eller betalte tjenester.

**Krav:** FR-9, NFR-1, NFR-2, NFR-3. **Styres av:** AD-1, AD-11, AD-13, AD-14, AD-17, AD-18, AD-19, AD-21. **Issues:** #17, #29.

**Akseptansekriterier:**

**Gitt** en ny klone av repoet og Python 3.12 eller nyere
**Når** jeg følger stegene i README (`venv`, `pip install -r requirements.txt`, `python lag_env.py`, `python manage.py migrate`, `python manage.py runserver`) fra `app/`
**Så** starter appen på `localhost:8000` uten feil og uten `ANTHROPIC_API_KEY`
**Og** `settings.TESTMODUS` er sann, og bare `kjerne.testmodus.er_testmodus()` leser verdien (FR-9, AD-14)

**Gitt** at `app/requirements.txt` lages
**Når** jeg leser den
**Så** har alle pakkene i arkitekturen §4 låste versjoner, også `fpdf2==2.9.0`, `pdfplumber==0.11.10` og `fonttools==4.68.0` (issue #29)
**Og** `python testdata/lag_cv_pdf.py A` kjører fra `app/` uten å installere noe utover `requirements.txt`

**Gitt** `app/testdata/lag_cv_pdf.py`
**Når** storyen er ferdig
**Så** sier kommentarene i skriptet at samme kilde gir samme tekst, men ikke en fil som er lik byte for byte på en annen maskin, fordi komprimeringen avhenger av zlib-versjonen (issue #29, AD-13)
**Og** README sier at `cv.pdf` ikke skal committes på nytt bare fordi `git status` viser den som endret etter at skriptet er kjørt
**Og** ingen test sammenligner `cv.pdf` byte for byte

**Gitt** at det ikke finnes noen `app/.env`
**Når** jeg kjører `python lag_env.py`
**Så** kopieres `.env.example` til `.env` med nye tilfeldige verdier for `DJANGO_SECRET_KEY` og `KRYPTERINGSNOKKEL`
**Og** kjører jeg den på nytt, overskrives ikke `.env`, og skriptet sier hvorfor

**Gitt** at `DJANGO_SECRET_KEY` eller `KRYPTERINGSNOKKEL` mangler
**Når** appen startes
**Så** stopper den med en melding som viser `python lag_env.py` (AD-14)

**Gitt** prosjektet
**Når** jeg ser på `config/settings.py` og `.env.example`
**Så** leses miljøvariabler bare i `settings.py` via `python-dotenv`, og `.env.example` har alle variablene i AD-14 uten ekte verdier
**Og** `LANGUAGE_CODE = "nb"`, `TIME_ZONE = "Europe/Oslo"`, `USE_TZ = True` og `ALLOWED_HOSTS = ["localhost", "127.0.0.1"]`

**Gitt** den første migreringen
**Når** den kjøres
**Så** finnes `kontoer.Bruker` med e-post som brukernavn, og `AUTH_USER_MODEL = "kontoer.Bruker"` (AD-11)
**Og** SQLite-filen ligger i `app/db.sqlite3` med `PRAGMA secure_delete = ON` ved hver tilkobling (AD-19)

**Gitt** prosjektet
**Når** jeg kjører `pytest` fra `app/`
**Så** går minst én test mot Django 6.1 med `pytest-django` og `pytest-socket --disable-socket`, uten nettverk og uten nøkkel (NFR-2)
**Og** feiler `pytest-django` 4.14.0 mot Django 6.1, brukes `manage.py test`, og AD-17 og README oppdateres (issue #17)

**Gitt** `.gitignore`
**Når** jeg ser på den
**Så** står `app/.env`, `app/db.sqlite3` og mappen for det virtuelle miljøet der, og ingen hemmeligheter er sjekket inn (NFR-3)

### Story 0.2: Testene kjører automatisk på GitHub

Som gruppe
vil vi at testene kjører automatisk for hver pull request,
slik at feil blir oppdaget før noe flettes inn i `main`.

**Krav:** NFR-2. **Styres av:** AD-18. **Kilde:** `docs/arbeidsfordeling.md`, uke 1 («automatisk testkjøring på GitHub»).

**Akseptansekriterier:**

**Gitt** en pull request mot `main`
**Når** den opprettes eller får nye commits
**Så** kjører en GitHub Actions-jobb `pip install -r requirements.txt` og `pytest` fra `app/` med Python 3.12
**Og** jobben bruker ingen hemmeligheter og ingen API-nøkkel, og lager en midlertidig `.env` med `lag_env.py`

**Gitt** en test som feiler
**Når** jobben er ferdig
**Så** vises pull requesten med en rød sjekk
**Og** README forklarer kort hva sjekken er

### Story 0.3: Felles sideramme og designtokens

Som bruker
vil jeg at alle sidene har samme ramme, farger og testmodus-banner,
slik at appen ser ryddig ut og jeg alltid ser om den kjører i testmodus.

**Krav:** FR-9, NFR-7, NFR-8. **UX:** UX-DR1 – UX-DR7, UX-DR29, UX-DR30, UX-DR36. **Styres av:** AD-12, AD-15, AD-17, AD-21.

**Akseptansekriterier:**

**Gitt** `app/static/css/tokens.css`
**Når** jeg sammenligner med `DESIGN.md`
**Så** er alle farger, typografiroller, hjørner og avstander CSS-variabler på `:root`, med `-dark`-variantene under `prefers-color-scheme: dark`
**Og** størrelsene er i `rem`, og ingen skrift, ikoner eller skript lastes fra nettet (UX-DR1, AD-15)

**Gitt** `templates/base.html`
**Når** en side arver fra den
**Så** har siden `lang="nb"`, `viewport`, «Hopp til innhold», `<header>`, `<nav aria-label="Fremdrift">` når siden er et steg, og `<main>` med én `h1` (UX-DR2)
**Og** `<title>` settes per side og begynner med «Feil: » når skjemaet har feil

**Gitt** at appen kjører i testmodus
**Når** en hvilken som helst side vises, også før innlogging
**Så** står banneret «Testmodus: appen bruker lagrede KI-svar. Prøv eksempel A, B eller C i steg 1.» øverst, via en context processor som bruker `er_testmodus()` (FR-9, UX-DR4)
**Og** i KI-modus vises ikke banneret

**Gitt** `templates/felles/`
**Når** jeg ser i mappen
**Så** finnes maldelene `topplinje.html`, `testmodus_banner.html`, `fremdriftslinje.html`, `knapperad.html`, `feiloppsummering.html`, `ki_varsel.html`, `ki_merke.html` og `bekreftelse.html`, som tas inn med `{% include %}` (AD-15)
**Og** de felles komponentene er stylet i `static/css/komponenter.css`

**Gitt** `fremdriftslinje.html` med aktivt steg og siste steg brukeren kan nå som variabler
**Når** den vises
**Så** er fullførte steg lenker med «(fullført)», det aktive har `aria-current="step"`, og låste steg er tekst med skjult «(ikke tilgjengelig ennå)» (UX-DR7)

**Gitt** et skjema som vises på nytt med feil
**Når** `feiloppsummering.html` tas inn
**Så** står «Noe må rettes» øverst i `main` med en lenke til hvert felt med feil, og boksen får fokus (UX-DR29)

**Gitt** en KI-knapp i et skjema og `static/js/skjema.js`
**Når** knappen trykkes
**Så** får den `aria-disabled="true"`, viser «Jobber …» og stopper nye trykk, og teksten skrives i et `aria-live`-område som finnes fra start (UX-DR30, AD-12)
**Og** knappen viser en indikator og beholder fargene sine, og under den står «Dette tar vanligvis 10–30 sekunder» (UX-DR30)

**Gitt** en enkel startside
**Når** jeg åpner den på 320 px bredde og med 200 % zoom
**Så** er det ingen vannrett rulling, alle trykkflater er minst 44 × 44 px, og fokusringen synes (UX-DR5, UX-DR6, UX-DR36)
**Og** dette sjekkes for hånd i nettleseren og føres i `docs/testplan.md`, fordi pytest ikke kan måle bredde, zoom og fokusring (AD-17)
**Og** en test sjekker at alle maldelene kan vises uten feil for en bruker som ikke er logget inn. Lenkene til «Min konto», «Logg ut» og steget brukeren står i, vises bare for innloggede brukere og kommer i Epic 1 og 2

### Story 0.4: Felles kjerne og KI-grensesnitt

Som utvikler i gruppa
vil jeg ha kryptering, feiltyper, meldinger, grenser, KI-grensesnittet og tomme modeller på plass før snittene starter,
slik at alle tre bygger på de samme reglene og migreringene ikke kolliderer.

**Krav:** FR-15, NFR-2, NFR-3, NFR-8, NFR-10. **Styres av:** AD-2, AD-3, AD-6, AD-7, AD-8, AD-9, AD-12, AD-15, AD-16, AD-17, AD-20, AD-21.

**Akseptansekriterier:**

**Gitt** `kjerne/kryptering.py` og `kjerne/felt.py`
**Når** en verdi lagres i `KryptertTekstFelt`, `KryptertJSONFelt` eller `KryptertBinaerFelt`
**Så** er den kryptert med Fernet og nøkkelen fra `KRYPTERINGSNOKKEL`
**Og** en test leser SQLite-filen direkte og finner ikke teksten i klartekst (FR-15)
**Og** en verdi som ikke kan dekrypteres, gir `kjerne.feil.Dekrypteringsfeil`, og mellomvaren sender brukeren til en side som forklarer at dokumentene ikke kan leses (AD-9)
**Og** knappen for å slette dokumentene legges inn på siden i story 2.5, når «Slett mine dokumenter» finnes

**Gitt** `kjerne/`
**Når** jeg ser i mappen
**Så** finnes `feil.py` (`BrukerFeil`, `Dekrypteringsfeil`), `meldinger.py` (norske feiltekster og KI-varselet), `grenser.py` (alle konstantene i AD-15), `valg.py` (`TextChoices` for språk, tone og svarform), `las.py` (`ki_las(bruker_id)`) og `tekst.py` (`normaliser(tekst)`)
**Og** `ki_las` kaster `BrukerFeil` med «Du har allerede en forespørsel som jobber. Vent til den er ferdig.» fra `meldinger.py` når låsen er opptatt (AD-12, UX-DR31)

**Gitt** `kjerne/tekst.py: normaliser(tekst)`
**Når** den får en tekst
**Så** gjør den Unicode NFC, gjør `\r\n` og `\r` om til `\n`, fjerner mellomrom på slutten av linjene, slår sammen tre eller flere linjeskift til to og fjerner mellomrom først og sist (AD-6)
**Og** den ligger i `kjerne/`, fordi både `dokumenter` og `ki` bruker den, og `dokumenter` ikke får importere `ki` (AD-2)
**Og** tester dekker hver av reglene, også at en tekst med `\r\n` gir samme resultat som med `\n`

**Gitt** `ki/port.py` og `ki/modeller.py`
**Når** jeg ser på dem
**Så** definerer de `KIKlient` med de fire operasjonene, `Innstillinger` og returtypene, og `KIFeil` med de seks underklassene i AD-3
**Og** `nokkelord/modeller.py` med `Nokkelord` og `Nokkelordresultat` lages her, fordi `ki/port.py` trenger typene. Funksjonene i `nokkelord/` kommer i Epic 3 (AD-7)
**Og** `ki.hent_klient()` returnerer overstyringen fra testene når den er satt (AD-3, AD-17)

**Gitt** `app/conftest.py`
**Når** en test bruker fiksturen `falsk_ki(svar=..., feil=...)`
**Så** returnerer `ki.hent_klient()` den falske klienten (AD-17)

**Gitt** modellene i AD-8
**Når** migreringene i Epic 0 kjøres
**Så** finnes tomme skjeletter av `CV`, `Analyse`, `Brev` og `CVForbedring` i appene som eier dem, koblet med `OneToOne` og `CASCADE`
**Og** `python manage.py makemigrations --check` går uten endringer (AD-21)

**Gitt** hver ny modul i storyen
**Når** jeg leser docstringen
**Så** nevner den FR-ene eller AD-ene den realiserer (arkitekturen §3, NFR-10)

