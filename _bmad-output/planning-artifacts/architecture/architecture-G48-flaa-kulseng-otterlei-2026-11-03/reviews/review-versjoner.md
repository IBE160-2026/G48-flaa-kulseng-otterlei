# Gjennomgang: versjoner og teknologipåstander

- **Dokument:** `ARCHITECTURE-SPINE.md` (status draft, oppdatert 2026-11-12) og `.memlog.md`
- **Gjennomgått:** 2026-11-12, av Claude (kontrollør, egen økt). Dokumentet er ikke endret.
- **Oppgave:** Sjekke at hver beslutning er kontrollert mot nettet og ikke bare hentet fra treningsdata: versjoner, at teknologiene finnes og passer, og påstandene om Claude API.
- **Metode:** PyPI JSON-API (`https://pypi.org/pypi/<pakke>/json`), offisielle dokumenter (Django, pytest-django, fpdf2, cryptography, platform.claude.com) og en liten kjøretest av fpdf2 2.9.0 på Python 3.12.5 i et midlertidig virtuelt miljø.

## Dom

Teknologivalgene holder, og de fleste Claude-påstandene stemmer med dokumentasjonen. Men §4 sier at versjonene er sjekket 2026-11-12, og to av dem var allerede utdatert den dagen: Django 6.1.2 har fått en sikkerhetsoppdatering, og anthropic 2.4.0 er fire versjoner bak. I tillegg stemmer påstanden om at fpdf2 håndterer æøå bare delvis. Den innebygde fonten krasjer på vanlige tegn i tekst fra KI, så en TTF-font må følge med.

## Funn

### H-1 (høy): Django 6.1.2 er ikke siste versjon og mangler sikkerhetsrettelser

- **Påstand:** §4 sier `Django 6.1.2`, «sjekket på PyPI … 2026-11-12». Memlog: «PyPI 2026-11-12: Django 6.1.2».
- **Fakta:** Django 6.1.3 kom ut 2026-11-03 (samtidig med 6.0.10 og 5.2.19). Den retter seks sikkerhetshull, blant annet CVE-2026-108147 (minnebruk i `MultiPartParser` ved base64-kodet filopplasting). Appen tar imot CV-filer, så dette er relevant. 6.1.3 er også første 6.1-versjon som støtter Python 3.15.
- **Konsekvens:** `requirements.txt` med låst `Django==6.1.2` låser en versjon med kjente sikkerhetshull. Det viser også at versjonssjekken i §4 ikke ble gjort på nytt 2026-11-12, slik dokumentet sier.
- **Forslag:** Bruk `Django==6.1.3` (eller nyere 6.1.x ved implementering). Rett datoen eller formuleringen i §4 og memlog.
- **Kilder:** https://pypi.org/pypi/django/json, https://docs.djangoproject.com/en/6.1/releases/6.1.3/

### H-2 (høy): fpdf2 med innebygde fonter krasjer på typografiske tegn, så en TTF-font må følge med

- **Påstand:** Memlog: «fpdf2 2.9.0 (ren Python, æøå)». AD-13 sier ingenting om font.
- **Fakta:** De innebygde fontene (Helvetica, Times, Courier) dekker bare Latin-1. Kjøretest med fpdf2 2.9.0 og `set_font("helvetica")`:
  - Fungerer: `æ ø å Æ Ø Å « » é`
  - Kaster `FPDFUnicodeEncodingException`: `–` (tankestrek), `—`, `’`, `“ ”`, `•`, `…`, `→`, `≥`, emoji, ikke-brytende bindestrek (U+2011) og smalt mellomrom (U+202F)
- **Konsekvens:** Søknadsbrev fra Claude inneholder nesten alltid `–` eller `’`. Med innebygd font vil PDF-eksporten (FR-23) feile på vanlige brev. fpdf2 tar ikke med fonter selv («fpdf2 never bundles or distributes these fonts»).
- **Forslag:** Legg en fri Unicode-font i repoet, for eksempel DejaVu Sans eller Noto Sans (OFL), i `app/eksport/fonter/`, og bruk `pdf.add_font(...)`. Skriv det inn i AD-13, med lisensen til fonten. Legg til en test som eksporterer et brev med `– ’ “ ” • …`. Vurder også å erstatte tegn fonten ikke har (for eksempel emoji) før eksport, i stedet for å la eksporten feile.
- **Kilder:** https://py-pdf.github.io/fpdf2/Unicode.html (avsnittene «Built-in Fonts vs. Unicode Fonts» og «Automatic font detection»), https://pypi.org/pypi/fpdf2/json

### M-1 (middels): pytest-django 4.14.0 støtter ikke Django 6.1 offisielt

- **Påstand:** AD-17 og §4: `pytest-django 4.14.0` sammen med Django 6.1.
- **Fakta:** 4.14.0 (2026-08-10) er siste versjon på PyPI. Klassifikatorene stopper på Django 6.0. I endringsloggen står «Official Django 6.1 support» under v4.15.0, som ikke er utgitt ennå.
- **Konsekvens:** Det fungerer trolig, siden 6.1 er en mindre versjon, men det er ikke bekreftet. Risikoen er størst i oppsettet av testdatabasen og i `settings`-fiksturen.
- **Forslag:** Skriv det som en kjent risiko i AD-17. Kjør en røyktest (`pytest` med én `django_db`-test) tidlig i P1, og bytt til 4.15.0 når den kommer ut.
- **Kilder:** https://pypi.org/pypi/pytest-django/json, https://raw.githubusercontent.com/pytest-dev/pytest-django/main/docs/changelog.rst

### M-2 (middels): anthropic 2.4.0 er utdatert, og SDK 2.x har endringer som ikke er nevnt

- **Påstand:** §4: `anthropic 2.4.0`.
- **Fakta:** Siste versjon er 2.8.0 (2026-11-10). Etter 2.4.0 (2026-11-02) har det kommet 2.5.0, 2.6.0, 2.7.0 og 2.8.0. SDK 2.0 bruker API-versjon `2026-10-21`, som har endringer som bryter med eldre kode:
  - `temperature`, `top_p` og `top_k` gir HTTP 400 og finnes ikke lenger i SDK-en.
  - SDK-en bruker `httpx2` i stedet for `httpx`.
  - Uten `api_key` leter klienten også etter `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_PROFILE` og en profil lagret på disk.
- **Konsekvens:** Eksempler i treningsdata og på nettet (også fra Claude) bruker ofte `temperature=0` for «deterministiske» svar. Med denne SDK-en gir det feil. Det kan friste i `lag_lagrede_svar` og evalueringen (AD-6).
- **Forslag:** Lås nyeste 2.x ved implementering. Skriv i AD-4 at SDK-en er 2.x (API-versjon 2026-10-21), at sampling-parametre ikke brukes, og at `ClaudeKlient` får `api_key` fra innstillingene, ikke fra oppslag i miljøet.
- **Kilder:** https://pypi.org/pypi/anthropic/json, https://platform.claude.com/docs/en/api/migration-2026-10-21, https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python

### M-3 (middels): Ventetid og kostnad for Opus 5.5 er antatt, ikke målt (adaptiv tenkning er alltid på)

- **Påstand:** AD-4 og AD-12: ett kall varer høyst 60 sekunder, og kostnaden er under 0,50 kr per kall.
- **Fakta:**
  - Claude Opus 5.5 har adaptiv tenkning som alltid er på og ikke kan skrus av. Standard `effort` er `medium`, og ventetiden er oppgitt som «Moderate».
  - Tenketokens faktureres som utdata (4 USD / 20 USD per million tokens).
  - Første kall med et nytt JSON-skjema tar ekstra tid, fordi grammatikken kompileres. Den caches i 24 timer.
  - Grov regning: 4k tokens inn og 2k tokens ut (med tenkning) koster omtrent 0,056 USD, altså rundt 0,6 kr. Det er over grensen i AD-4.
- **Konsekvens:** 60 sekunder er en grense klienten setter (`timeout=60`), ikke en garanti for at svaret kommer i tide. Et brev med høy `effort` kan få tidsavbrudd hver gang.
- **Forslag:**
  - Sett `effort` (for eksempel `low` eller `medium`) og `max_tokens` eksplisitt i AD-4.
  - Mål ventetid og tokenbruk i den første kjøringen av `lag_lagrede_svar`, og skriv tallene i evalueringsrapporten.
  - Gjør kostnadsanslaget om til et regnestykke med kilde, eller merk det som anslag.
- **Kilder:** https://platform.claude.com/docs/en/models/opus-5-5/overview, https://platform.claude.com/docs/en/about-claude/models/overview, https://platform.claude.com/docs/en/build-with-claude/structured-outputs (avsnittet «Grammar compilation and caching»)

### M-4 (middels): Strukturerte svar kan bryte skjemaet ved `refusal` og `max_tokens`

- **Påstand:** AD-4: svaret valideres mot pydantic, og et ugyldig svar gir `KIUgyldigSvar`.
- **Fakta:** Påstanden stemmer: `client.messages.parse(..., output_format=<PydanticModell>)` er anbefalt metode i Python. SDK-en sender det som `output_config.format`, validerer svaret og legger resultatet i `parsed_output`. Men dokumentasjonen nevner tre tilfeller der svaret kan avvike fra skjemaet:
  - `stop_reason: "refusal"`, med HTTP 200
  - `stop_reason: "max_tokens"`, der svaret er avkortet
  - `enum`-verdier kan få annen stor eller liten forbokstav
- **Konsekvens:** Uten egen sjekk kan `parsed_output` være `None`, eller valideringen kan gi et unntak `ClaudeKlient` ikke fanger.
- **Forslag:** Skriv i AD-4 at `ClaudeKlient` sjekker `stop_reason` og gjør om `refusal`, `max_tokens` og valideringsfeil til `KIUgyldigSvar`. Hold enum-verdiene (`matcher`/`mangler` og lignende) som små enkeltord, og normaliser store og små bokstaver før validering. Merk at Python-parameteren heter `output_format`, mens REST-parameteren `output_format` er utfaset. Skriv `messages.parse` i dokumentet for å unngå forveksling.
- **Kilde:** https://platform.claude.com/docs/en/build-with-claude/structured-outputs (avsnittene «Usage», «Invalid outputs» og «Migrating from the beta»)

### L-1 (lav): Feilmeldingen for forbruksgrense finnes i en variant til

- **Påstand:** AD-4: «You have reached your specified API usage limits» (HTTP 400) eller `enforced_spend_limit_reached` (HTTP 429) gir `KIForbruksgrense`.
- **Fakta:** Begge stemmer:
  - En grense brukeren selv har satt gir HTTP 400 `invalid_request_error`, og meldingen *starter med* «You have reached your specified API usage limits».
  - Taket for API-nivået gir HTTP 429 `rate_limit_error` med `error.details.error_code = "enforced_spend_limit_reached"` og uten `retry-after`.
  - For en grense satt på et arbeidsområde (workspace) er meldingen derimot «You have reached your specified **workspace** API usage limits».
- **Forslag:** Sjekk på `BadRequestError` der meldingen starter med «You have reached your specified» og inneholder «usage limits», og på `RateLimitError` med `error_code == "enforced_spend_limit_reached"`. Ikke sjekk på den nøyaktige setningen. Memlog sier at grensen settes «under Billing», men siden heter nå *Spend limits* (`platform.claude.com/settings/spend-limits`). README bør vise dit. Grenser kan ikke settes på standardarbeidsområdet.
- **Kilder:** https://platform.claude.com/docs/en/api/rate-limits (avsnittene «Reaching your spend cap» og «Setting your own spend limit»), https://platform.claude.com/docs/en/api/errors

### L-2 (lav): `timeout=60` er en tidsgrense per fase, ikke for hele kallet

- **Fakta:** Python-SDK-en har `timeout` (standard 10 minutter) og `max_retries` (standard 2), og ved tidsavbrudd kastes `APITimeoutError`. AD-4 stemmer altså. Et tall gis likevel videre til `httpx2.Timeout`, som gjelder hver fase for seg (tilkobling, lesing og skriving), ikke totaltiden. Ved et vanlig kall uten strømming kommer svaret først når det er ferdig, så i praksis blir det omtrent 60 sekunder. Det er likevel ikke en hard grense.
- **Forslag:** Godta det, eller skriv det i AD-4. Ingen endring er nødvendig.
- **Kilde:** https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python (avsnittene «Retries» og «Timeouts»)

### L-3 (lav): «Python 3.12 eller nyere» er ikke testet oppover

- **Fakta:**
  - Django 6.1 støtter Python 3.12, 3.13, 3.14 og 3.15. Støtten for 3.15 kom først i 6.1.3.
  - fpdf2 krever ≥ 3.11. cryptography, pydantic og pytest har klassifikatorer til 3.15.
  - pdfplumber, python-dotenv, anthropic og pytest-django har klassifikatorer bare til 3.14. Hjul for 3.15 finnes for pydantic-core, cryptography, jiter og Pillow.
  - Django støtter offisielt bare siste mikroversjon av hver Python-serie. Lokal Python er 3.12.5.
- **Forslag:** Skriv «Python 3.12–3.14 (testet på 3.12.x)» i AD-18 og README, eller test på 3.15 før innlevering.
- **Kilder:** https://docs.djangoproject.com/en/6.1/faq/install/, PyPI JSON for hver pakke

### L-4 (lav): Lisensen til fpdf2 er ikke nevnt

- **Fakta:** pdfplumber er MIT (bekreftet i `LICENSE.txt` og klassifikator). PyMuPDF er dobbeltlisensiert under AGPL-3.0 og en kommersiell lisens, så det er riktig valgt bort. fpdf2 er derimot LGPL-3.0-only. Det er uproblematisk for denne bruken, men dokumentet sier ingenting om det. pdfplumber krever `pdfminer.six==20260107` og `pypdfium2`. Begge har ferdige hjul, så det stemmer at sensor ikke trenger systembiblioteker.
- **Forslag:** Nevn lisensene kort i AD-13, siden sensor ser etter begrunnede valg.
- **Kilder:** https://pypi.org/pypi/pdfplumber/json, https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt, https://pypi.org/pypi/PyMuPDF/json, https://pypi.org/pypi/fpdf2/json

### L-5 (lav): Fernet er fortsatt riktig valg, og `MultiFernet` gjør nøkkelbytte enkelt

- **Fakta:** Fernet ligger i «recipes»-laget i cryptography 50.0.2, og ingenting tyder på at det skal fases ut. Dokumentasjonen nevner `MultiFernet.rotate()` for nøkkelbytte. Eneste begrensning er at hele meldingen må ligge i minnet. Med en grense på 5 MB per fil er det ikke et problem.
- **Forslag:** Ingen endring er nødvendig. I §7 kan dere nevne at nøkkelbytte senere kan gjøres med `MultiFernet` uten å endre felttypene.
- **Kilder:** https://cryptography.io/en/stable/fernet/, https://pypi.org/pypi/cryptography/json

### L-6 (lav): Påstanden om personvern er riktig, men har unntak

- **Fakta:** Inn- og utdata i API-et slettes innen 30 dager. Unntak er tjenester med lengre lagring, avtaler og lagring for å håndheve bruksvilkårene (Usage Policy). Data brukes ikke til trening uten uttrykkelig samtykke. Opus 5.5 er ikke en «Covered Model» med krav om 30 dagers lagring.
- **Forslag:** Skriv «slettes innen 30 dager (med unntak for håndheving av bruksvilkår)» i AD-4.
- **Kilder:** https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data, https://platform.claude.com/docs/en/manage-claude/api-and-data-retention

## Bekreftet uten anmerkning

| Påstand | Status | Kilde |
|---|---|---|
| Modell-ID `claude-opus-5-5` | Stemmer. Gjeldende modell, pensjoneres tidligst 2027-09-22 (etter fristen) | https://platform.claude.com/docs/en/about-claude/models/overview |
| Pris for Opus 5.5: 4 USD / 20 USD per million tokens | Stemmer | samme |
| Strukturerte svar er stabile (ikke beta) og støttes av Opus 5.5 | Stemmer | https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| `max_retries` er 2 som standard (gir 180 s med `timeout=60`) | Stemmer | https://platform.claude.com/docs/en/api/errors |
| cryptography 50.0.2, pdfplumber 0.11.10, fpdf2 2.9.0, pydantic 2.14.3, python-dotenv 1.2.4, pytest 9.2.0, pypdf 7.0.1 (reserve) | Siste versjon per 2026-11-12 | PyPI JSON |
| Django 6.1 krever Python ≥ 3.12 | Stemmer | https://docs.djangoproject.com/en/6.1/faq/install/ |
| pdfplumber er MIT, PyMuPDF er AGPL | Stemmer | se L-4 |

## Versjonstabell (PyPI 2026-11-12)

| Pakke | I dokumentet | Siste | Utgitt | Python | Merknad |
|---|---|---|---|---|---|
| Django | 6.1.2 | **6.1.3** | 2026-11-03 | ≥ 3.12 | Sikkerhetsoppdatering (H-1) |
| anthropic | 2.4.0 | **2.8.0** | 2026-11-10 | ≥ 3.10 | M-2 |
| cryptography | 50.0.2 | 50.0.2 | 2026-09-30 | ≥ 3.9 | OK |
| pdfplumber | 0.11.10 | 0.11.10 | 2026-06-15 | ≥ 3.8 | OK, MIT |
| fpdf2 | 2.9.0 | 2.9.0 | 2026-10-29 | ≥ 3.11 | OK, LGPL-3.0 (H-2, L-4) |
| pydantic | 2.14.3 | 2.14.3 | 2026-11-05 | ≥ 3.10 | OK |
| python-dotenv | 1.2.4 | 1.2.4 | 2026-10-01 | ≥ 3.10 | OK |
| pytest | 9.2.0 | 9.2.0 | 2026-10-27 | ≥ 3.10 | OK |
| pytest-django | 4.14.0 | 4.14.0 | 2026-08-10 | ≥ 3.10 | Ikke offisiell støtte for Django 6.1 (M-1) |
| pypdf (reserve) | 7.0.1 | 7.0.1 | 2026-11-10 | ≥ 3.10 | OK |

## Merknad om prosessen

Memlog viser at Claude API-påstandene ble kontrollert mot offisielle dokumenter 2026-11-03, og de holder. Versjonslinjen datert 2026-11-12 ser derimot ut til å blande et øyeblikksbilde fra 2026-11-03 (Django 6.1.2, anthropic 2.4.0) med nyere oppslag (pydantic 2.14.3 fra 2026-11-05, pypdf 7.0.1 fra 2026-11-10). Gruppa bør enten gjøre sjekken på nytt og oppdatere datoen, eller skrive i §4 at versjonene låses på nytt når `requirements.txt` lages i P1.
