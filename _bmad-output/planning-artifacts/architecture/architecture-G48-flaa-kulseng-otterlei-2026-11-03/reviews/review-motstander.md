# Motstandergjennomgang av arkitekturen

**Dokument:** `ARCHITECTURE-SPINE.md` (status: draft, oppdatert 2026-11-12)
**Krav:** `../../prd/prd.md`
**Metode:** For hvert funn er det laget to enheter ett nivå ned (stories eller moduler som tre gruppemedlemmer bygger parallelt med hver sin Claude). Begge følger alle AD-ene bokstavelig, men passer likevel ikke sammen. Hvert slikt par er et hull som bør lukkes med en ny eller strammere AD.
**Gjennomgått av:** Claude (kontrollør), 2026-11-12. Funnene er Claudes vurderinger og må vurderes av gruppa.

## Dom

Ryggraden er god på lag, porter, kryptering og tilgangskontroll. Den fastsetter derimot nesten ingen **felles former** (signaturer, filnavn, JSON-skjema, URL-navn, feilkontrakt), og heller ingen **eier** for skrivinger på tvers av apper. Tre parallelle Claude-er vil derfor bygge deler som følger alle AD-ene, men ikke virker sammen. Tre av funnene bryter kjerneflyten for sensor (UJ-3) eller gir feil data. De bør lukkes før epics og stories skrives.

| Alvorlighet | Antall |
|---|---|
| Kritisk | 3 |
| Høy | 5 |
| Middels | 7 |
| Lav | 5 |

---

## Kritisk

### K1. Testmodus-hashen er ikke definert, så eksempelpar A–C kan gi «IkkeITestmodus»

**AD-er:** AD-6, AD-3, FR-10, UJ-3

**Paret:**
- *Story «TestmodusKlient»* (`ki/testmodus_klient.py`): normaliserer med `tekst.strip()` og hasher `sha256(cv + annonse)`. Referansehashen lages fra `testdata/eksempler/A/cv.txt` og `annonse.txt` slik filene ligger på disk (`\n`).
- *Story «Prøv med eksempel A»* (skjermbilde Ny analyse): fyller tekstfeltene med CV-tekst og annonse. Nettleseren sender tekstfelt med `\r\n`. For CV A som er PDF, hentes teksten med `les_cv`, mens TestmodusKlient kanskje leser `cv.txt` eller hasher råfila.

Begge følger AD-6 («en hash av normalisert CV-tekst og annonse»). Likevel blir hashen ulik, og sensor får FR-11-meldingen på eksempelpar A. Det er nøyaktig det UJ-3 og SM-10 ikke tåler. Det er heller ikke fastsatt hva «endret» betyr: er ett ekstra mellomrom en endring?

**Mangler i dag:** normaliseringsregel, skilletegn mellom CV og annonse, hvor referansehashen kommer fra (ferdig lagret eller regnet ut når appen kjører, fra `cv.txt` eller fra `les_cv(cv.pdf)`), og hvem som eier funksjonen.

**Forslag til ny AD-tekst (stramming av AD-6):**
> - Normalisering og hash finnes bare i `ki/eksempelpar.py`: `normaliser(tekst) -> str` gjør Unicode NFC, gjør `\r\n` og `\r` om til `\n`, fjerner mellomrom på slutten av hver linje, slår sammen tre eller flere linjeskift til to, og fjerner mellomrom først og sist. `eksempel_hash(cv_tekst, annonse) = sha256(normaliser(cv_tekst) + "\n\x1e\n" + normaliser(annonse))`.
> - Referanseteksten for et par er alltid `les_cv()` på parets CV-fil (samme funksjon som ved opplasting, AD-13) og `annonse.txt`. Hashene regnes ut når appen starter. De lagres ikke.
> - «Prøv med eksempel» og `TestmodusKlient` bruker de samme funksjonene. En test sjekker at teksten som skjemaet fyller inn, sendt tilbake med `\r\n`, gir treff for A, B og C.

### K2. Egen CV i testmodus: AD-12 og FR-11 krever motsatt oppførsel når analysen lagres

**AD-er:** AD-12, AD-8, AD-7, FR-11, FR-21

**Paret:**
- *Story «Kjør analyse»* (`analyse/tjenester.py`): følger AD-12 («Ingenting overskrives før KI-kallet har lyktes»). `gap_analyse` kaster `IkkeITestmodus`, som er en `KIFeil`. Tjenesten fanger feilen, lagrer ingenting og viser feilmeldingen.
- *Story «Nøkkelordanalyse»* (P7): FR-11 og FR-21 krever at nøkkelordanalysen vises **uten** KI-forklaring for egen CV i testmodus. Resultatsiden leser `Analyse.nokkelordresultat`, men det finnes ingen `Analyse`.

Den samme konflikten oppstår i KI-modus når gap-analysen lykkes og `nokkelord_forklaring` får tidsavbrudd. AD-12 sier ikke om «Analyser» er én eller to KI-operasjoner, og heller ikke om en delvis vellykket analyse lagres. To kall i rekkefølge kan også ta 120 sekunder, ikke 60.

**Forslag til ny AD-tekst (ny regel i AD-12 eller AD-8):**
> - «Analyser» består av: (1) `nokkelord.finn_nokkelord` + `match` (alltid), (2) `gap_analyse`, (3) `nokkelord_forklaring`. Steg 2 og 3 er hvert sitt KI-kall.
> - `IkkeITestmodus` er ikke en feil i brukerflyten. `Analyse` lagres da med `gap_analyse = None`, `forklaring = None` og `ki_status = "ikke_i_testmodus"`. Resultatsiden viser FR-11-meldingen der KI-svaret skulle stått.
> - Andre `KIFeil` i steg 2: ingenting lagres (AD-12). `KIFeil` i steg 3 etter at steg 2 har lyktes: `Analyse` lagres med `forklaring = None` og `ki_status = "forklaring_feilet"`, og siden har knappen «Prøv forklaringen igjen».
> - Feltene `gap_analyse` og `forklaring` kan være tomme (`null=True`). Malene må håndtere `None`.

### K3. Tre apper sletter de samme objektene, og retting av CV-teksten (FR-2) gir utdaterte resultater

**AD-er:** AD-8, AD-2, §5, §6 (FR-16 i `kontoer/tjenester.py`)

**Paret A – hvem sletter hva:**
- *Story «Last opp CV»* (`dokumenter/tjenester.py`): AD-8 sier at «Ny CV sletter `Analyse`, `Brev` og `CVForbedring` … i tjenestelaget». Dokumenter-Claude importerer `analyse.models` og kaller `.delete()` direkte.
- *Story «Kjør analyse»* (`analyse/tjenester.py`): lager `slett_resultat(bruker)` for «ny analyse sletter Brev og CVForbedring».
- *Story «Slett mine dokumenter»* (`kontoer/tjenester.py`, ifølge §6): sletter CV og alle tre resultatdelene med egne spørringer.

Alle tre følger AD-2 («tjenester er det eneste laget som skriver modeller»). Når `CVForbedring` får et nytt felt eller en ny relatert modell, blir den bare ryddet ett av tre steder. `dokumenter` → `analyse` og `kontoer` → begge gir også en kryssimport som lett blir sirkulær når `analyse` trenger CV-teksten.

**Paret B – retting av CV-teksten:**
- *Story FR-2 «Rett CV-tekst»* oppdaterer `CV.cv_tekst` med `cv.save()`. Det er ikke en «ny CV», så AD-8 sletter ingenting.
- *Story «Søknadsbrev»* bruker den nye `CV.cv_tekst` sammen med den gamle `Analyse.gap_analyse`. Brevet kan da vise til krav som «matcher» ut fra tekst som ikke lenger står i CV-en, og det strider mot FR-8.

Hvis rettingen ligger i samme skjema som «Analyser», skriver `analyse/tjenester.py` til `CV`, som eies av `dokumenter`. Da har modellen to eiere.

**Forslag til ny AD-tekst (stramming av AD-8):**
> - **Eierskap:** Bare appen som definerer en modell, skriver til den eller sletter den, gjennom sin egen `tjenester.py`. Andre apper kaller tjenesten (`dokumenter.tjenester.lagre_cv`, `analyse.tjenester.slett_resultat`). Avhengighetsretningen mellom appene er `kontoer ← dokumenter ← analyse`. `kontoer` importerer ikke de andre.
> - **Kaskade i stedet for manuell sletting:** `Analyse` er `OneToOne` mot `CV` med `CASCADE`. `Brev` og `CVForbedring` er `OneToOne` mot `Analyse` med `CASCADE`. «Ny CV» betyr at den gamle `CV`-raden slettes og en ny lages (aldri oppdatering av raden), så kaskaden fjerner resultatet.
> - **Retting av CV-tekst er det samme som ny CV:** Enhver endring av `cv_tekst` går gjennom `dokumenter.tjenester.lagre_cv_tekst(bruker, tekst)`. Den sletter `Analyse` (og dermed resten) når teksten endres etter `normaliser()` (K1).
> - «Slett mine dokumenter» (FR-16) = `dokumenter.tjenester.slett_cv(bruker)`. «Slett konto» (FR-17) = `bruker.delete()`.

---

## Høy

### H1. Signaturene i `KIKlient` er ikke fastsatt, og AD-3 og AD-5 sier ulike ting

**AD-er:** AD-3, AD-5, AD-2, AD-7

**Paret:**
- *Story «Søknadsbrev»* følger AD-5 («for brev og forslag de manglende kravene fra gap-analysen») og skriver `brev(cv_tekst, annonse, innstillinger, mangler: list[str])`.
- *Story «TestmodusKlient»* følger AD-3 («alle tar inn CV-tekst, stillingsannonse og innstillinger») og skriver `brev(cv_tekst, annonse, innstillinger)`.

`nokkelord_forklaring` trenger dessuten nøkkelordresultatet, som ikke er nevnt. Typen `innstillinger` er heller ikke fastsatt. `TextChoices` er Django og ligger i en app sin `models.py`. Skal `ki/` importere den, kan den ikke uten å bryte ånden i AD-2. Én Claude sender en `dict`, en annen et Django-skjema sitt `cleaned_data`, en tredje en pydantic-modell. Ønskede nøkkelord kan være en kommaseparert streng eller en liste. Hvem deler opp strengen: skjemaet eller `nokkelord`?

**Forslag til ny AD-tekst (stramming av AD-3):**
> `ki/port.py` er fastsatt slik (alle typer fra `ki/modeller.py` eller `nokkelord/modeller.py`):
> ```python
> class Innstillinger(BaseModel):  # ki/modeller.py
>     sprak: Literal["nb", "en"]; tone: Literal["formell", "uformell"]
>     svarform: Literal["fullt_utkast", "kun_forslag"]; onskede_nokkelord: list[str]
> def gap_analyse(cv_tekst, annonse, sprak) -> GapAnalyse
> def brev(cv_tekst, annonse, innstillinger, mangler: list[str]) -> Brev
> def cv_forbedring(cv_tekst, annonse, sprak, mangler: list[str]) -> CVForbedringer
> def nokkelord_forklaring(cv_tekst, annonse, sprak, resultat: Nokkelordresultat) -> Forklaring
> ```
> Parameterne viser hva svaret avhenger av, og det er det samme som nøkkelen til filnavnet for lagrede svar (H2). Django-skjemaets `TextChoices` ligger i `kjerne/valg.py` og bruker de samme verdiene. Skjemaet gjør ønskede nøkkelord om til `list[str]` (komma eller linjeskift, uten tomme, og uten duplikater når store og små bokstaver ignoreres).

### H2. Filnavn og JSON-form for lagrede svar er ikke fastsatt

**AD-er:** AD-6, §3 «KI-svar», FR-10

**Paret:**
- *Story «lag_lagrede_svar»* skriver `svar/brev_nb_formell_fullt_utkast.json`, `svar/gap_nb.json`.
- *Story «TestmodusKlient»* leser `svar/soknadsbrev-nb-formell-fullt-utkast.json`, `svar/gap-analyse.nb.json`.

Begge følger AD-6 («filnavnet sier hvilke innstillinger»). Testmodus finner ingen filer, og alle 42 svarene må lages på nytt i KI-modus, noe som koster penger.

Søknadsbrev og brevforslag har dessuten ulik form, en tekst og en punktliste. §3 fastsetter bare formen på gap-analysen. Én Claude lager `Brev(tekst: str)`, en annen `Soknadsbrev | Brevforslag`, og eksporten (AD-13) og malen gjetter hver sin.

**Forslag til ny AD-tekst (stramming av AD-6 og §3):**
> - Filnavn: `<operasjon>__<sprak>[__<tone>__<svarform>].json`, der `operasjon` er `gap_analyse`, `brev`, `cv_forbedring` eller `nokkelord_forklaring`, og verdiene er `TextChoices`-verdiene. Eksempel: `brev__nb__formell__fullt_utkast.json`, `gap_analyse__en.json`. Funksjonen `svarfil(par, operasjon, **innstillinger) -> Path` i `ki/eksempelpar.py` brukes både av kommandoen og av klienten.
> - Hver fil inneholder `model_dump(mode="json")` av returtypen og ingenting annet.
> - `Brev` har feltene `svarform`, `avsnitt: list[str]` (fullt utkast) og `punkter: list[str]` (kun forslag). Akkurat ett av de to er tomt.
> - En test sjekker at alle 42 filene finnes og validerer.

### H3. Kontrakten for feil mellom tjeneste og view er motstridende

**AD-er:** AD-12, §3 «Feil», AD-13, FR-11

AD-12 sier at tjenesten *returnerer* en norsk feilmelding og at viewet viser *samme side på nytt*. §3 sier at views viser feilene med *Django-meldinger*. Django-meldinger er laget for omdirigering, mens en side som vises på nytt bruker skjemafeil.

**Paret:**
- *Story «Kjør analyse»*: `kjor_analyse()` returnerer `tuple[Analyse | None, str | None]`, og viewet viser feilen med `form.add_error`.
- *Story «Last opp CV»*: `lagre_cv()` lar `TomPDF` gå videre, og viewet fanger `InnlesingFeil`, legger feilen i `messages.error` og omdirigerer. Rettingene brukeren har gjort, forsvinner da, i strid med NFR-5.

Det er heller ikke fastsatt om `TomPDF` er en underklasse av `InnlesingFeil`, hvilke unntak som gjelder for filtype og størrelse, eller om grensen på 5 MB sjekkes i skjemaet eller i `les_cv` (eller begge steder, med ulik tekst). Teksten fra FR-11 kan skrives inn på tre steder med ulik ordlyd.

**Forslag til ny AD-tekst (ny AD, «Feilkontrakt»):**
> - Tjenester kaster `kjerne.feil.BrukerFeil(melding: str)` og returnerer ellers resultatet. De returnerer aldri feil som verdier.
> - Tjenesten oversetter `KIFeil` og `InnlesingFeil` (med underklassene `FeilFiltype`, `ForStorFil` og `TomPDF`) til `BrukerFeil`. Alle norske feiltekster, også FR-11-teksten, står bare i `kjerne/meldinger.py`.
> - Views fanger bare `BrukerFeil` og viser skjemaet på nytt med `form.add_error(None, e.melding)` og status 200. `messages` brukes bare for bekreftelser etter omdirigering («Dokumentene er slettet»).
> - `les_cv` er den eneste som sjekker filtype og størrelse. Skjemaet sjekker bare at det finnes en fil.

### H4. Ingen regel for hvem som eier migreringene

**AD-er:** AD-11, AD-18 («Migreringene sjekkes inn i git»), AD-8

**Paret:** Henrik lager `analyse/migrations/0002_brev.py` på `feature/soknadsbrev`, og Haakon lager `analyse/migrations/0002_cvforbedring.py` på `feature/cv-forbedring`. Begge pull requestene er grønne hver for seg. Etter fletting stopper `migrate` med «Conflicting migrations». AD-11 krever dessuten at `kontoer.Bruker` finnes *før første migrering*. Lager noen `dokumenter/0001` på en branch der `AUTH_USER_MODEL` ennå ikke er satt, må alt gjøres på nytt.

**Forslag til ny AD-tekst (ny regel i AD-18):**
> - Første story (Epic 0) lager `kontoer.Bruker` og tomme skjeletter av alle fire modellene i AD-8, og flettes før noe annet.
> - Før en pull request med migreringer flettes, hentes `main` inn i branchen, migreringer som ikke er flettet ennå slettes og lages på nytt med `makemigrations`, og `python manage.py makemigrations --check` må gå uten endringer. Migreringer som er flettet, endres aldri.
> - Bare én åpen pull request om gangen kan endre modellene i en bestemt app.

### H5. Formatet på fasiten og eksempelparene er ikke fastsatt, og fire deler leser dem

**AD-er:** AD-17, AD-6, AD-7, AD-13 (krav før P2)

`fasit.json` blir lest av testene for nøkkelord (FR-20), PDF-testen (SM-2), evalueringen i `lag_lagrede_svar` og kanskje «Prøv med eksempel». AD-17 lister bare *hva* fasiten inneholder, ikke nøklene. AD-17 sier i tillegg «tre lister», men nevner fem innholdsdeler.

**Paret:**
- *Story «Nøkkelordtester»* leser `fasit["nokkelord"]` som en liste med strenger.
- *Story «Eksempeldata»* skriver `{"nokkelord": [{"ord": "Python", "synonymer": [...]}], "krav": {"matcher": [...], "mangler": [...]}}`.

Det er heller ikke bestemt hvordan evalueringen sammenligner KI-ens `krav` («Erfaring med SQL», «SQL experience» på engelsk) med fasitens «SQL».

**Forslag til ny AD-tekst (stramming av AD-17):**
> - `kjerne/eksempelpar.py` (eller `ki/eksempelpar.py`, se K1) har pydantic-modellen `Fasit` og `hent_eksempelpar(par) -> Eksempelpar(cv_fil, annonse, fasit)`. Alle som leser eksempeldata, gjør det bare gjennom denne funksjonen.
> - `Fasit`: `fakta_i_cv: list[str]`, `krav_matcher: list[str]`, `krav_mangler: list[str]`, `nokkelord: list[str]` (grunnformen fra `ordliste.json`), `floskler: list[str]`, `sprak_og_tone: list[str]`.
> - Evalueringen regner et krav fra KI som treff når fasitkravet, normalisert, finnes i KI-kravet. Fasiten kan også ha `alias` per krav for engelske navn.

---

## Middels

### M1. Hvordan delene finner ut om testmodus er på, er ikke fastsatt

**AD-er:** AD-3 («hindrer at deler av appen vet om den kjører i testmodus»), AD-14, AD-7 [Forslag], FR-10

Banneret, knappene «Prøv med eksempel» og teksten om ønskede nøkkelord i AD-7 trenger alle å vite om testmodus er på. *Context processor-storyen* leser `settings.TESTMODUS`. *Story «Prøv med eksempel»* sjekker `isinstance(ki.hent_klient(), TestmodusKlient)`. *Story «Nøkkelord»* leser `os.environ["TESTMODUS"]`, som bryter AD-14, men er lett å gjøre ved et uhell. Med en tom `ANTHROPIC_API_KEY` og `TESTMODUS=false` svarer de forskjellig.

**Fiks (AD-14):** «`settings.TESTMODUS: bool` regnes ut én gang i `settings.py` (`TESTMODUS=true` eller tom nøkkel). `kjerne.testmodus.er_testmodus()` er den eneste som leser den. `hent_klient()` og context processoren bruker den. AD-3 gjelder tjenestelogikk, ikke visning.»

### M2. Testene kan ikke bytte inn en falsk KI-klient på én måte

**AD-er:** AD-3, AD-17, NFR-5

Tjeneste A skriver `from ki import hent_klient`, og tjeneste B skriver `import ki; ki.hent_klient()`. Testen for NFR-5 bytter ut `ki.hent_klient` med `monkeypatch` og treffer bare B. A kaller fortsatt TestmodusKlient, og testen går grønn uten å teste noe.

**Fiks (AD-17):** «`conftest.py` i `app/` har fiksturen `falsk_ki(feil=None, svar=None)`, som setter `ki._overstyrt_klient`. `hent_klient()` returnerer den når den er satt. Andre måter å bytte ut klienten på er ikke lov.»

### M3. URL-navn og navnerom mangler, og flere URL-er er ikke nevnt

**AD-er:** §3 «URL-er», AD-10

§3 gir fem stier, men ingen `name=` og ingen `app_name`. Én mal bruker `{% url 'analyse' %}`, en annen `{% url 'analyse:ny' %}`. Mange URL-er står ikke nevnt: opplasting og retting av CV, brev, CV-forbedring, eksempelpar, eksport (md/pdf), slett dokumenter, slett konto og logg ut (må være POST i Django 5 og nyere). To Claude-er kan lage `/brev/` og `/resultat/brev/` for det samme.

**Fiks (§3, ny tabell):** fullstendig liste med sti, navn (`<app>:<handling>`), metode og view-eier, for eksempel `analyse:brev` POST `/resultat/brev/`, `eksport:pdf` POST `/resultat/brev/pdf/`, `kontoer:logg_ut` POST `/logg-ut/`.

### M4. «Avvis ny analyse mens én kjører» har ingen fastsatt mekanisme

**AD-er:** AD-12 [Forslag]

Én Claude bruker et flagg i økten, mens en annen bruker en kolonne `Analyse.kjorer`. Den kolonnen kan ikke finnes, fordi `Analyse` ikke lages før kallet har lyktes (AD-12). En tredje bruker `threading.Lock` per prosess. Det er heller ikke sagt om regelen også gjelder brev og CV-forbedring, og hva som skjer når et kall krasjer og låsen blir stående.

**Fiks:** «`kjerne/las.py: ki_las(bruker_id)` er en kontekstbehandler med `threading.Lock` per bruker i minnet, og den slipper automatisk når kallet er ferdig. Den gjelder alle tjenester som kaller KI. Er låsen opptatt, kastes `BrukerFeil("En KI-forespørsel kjører allerede …")`.» Det holder fordi appen bare kjøres lokalt med én prosess (AD-18).

### M5. Det er uklart hvordan pydantic-objekter og dataklasser lagres i `KryptertJSONFelt`

**AD-er:** AD-9, AD-2, AD-7

AD-2 tillater både dataklasser og pydantic. `Nokkelordresultat` som dataklasse kan ikke serialiseres til JSON. Én Claude gir feltet `GapAnalyse`-objektet direkte og forventer at feltet tar seg av resten. En annen lagrer `model_dump()`. En tredje lagrer `asdict()`. Når de leser feltet igjen, får de `dict`, objekt eller unntak. Det er heller ikke sagt om `andel` er 0–1 eller 0–100.

**Fiks (AD-9 og AD-7):** «`Krypterte*`-felt tar bare imot og gir tilbake verdier som er gyldig JSON. Tjenestene gjør `model_dump(mode="json")` og `Modell.model_validate()`. Alle returtyper fra `ki/` og `nokkelord/` er pydantic-modeller (`nokkelord/modeller.py`). `andel` er en `float` fra 0 til 1, og visningen gjør den om til prosent.»

### M6. Avsenderopplysningene ved PDF-eksport kan havne i loggene

**AD-er:** AD-10, AD-13, FR-23

*Story «PDF-eksport»* lager eksporten som en lenke, `GET /resultat/brev/pdf/?navn=…&epost=…`. Det bryter ingen AD, men `runserver` skriver hele URL-en til loggen, og nettleseren lagrer den i historikken. Da blir avsenderopplysningene lagret, i strid med FR-23 og AD-10.

**Fiks (AD-13):** «Eksport som tar imot avsenderopplysninger, er alltid `POST` med CSRF. Opplysningene står aldri i URL-en.»

### M7. Tone og svarform kan hentes fra to steder

**AD-er:** AD-8 («Tone og svarform kan velges på nytt når brukeren ber om brev»), FR-4

`Analyse` lagrer innstillingene fra FR-4 (med tone og svarform), og `Brev` lagrer tonen og svarformen brevet ble laget med. *Story «Resultatside»* bruker forvalg fra `Analyse` i brevskjemaet. *Story «Eksport»* velger brevoppsett ut fra `Analyse.innstillinger.svarform` i stedet for `Brev.svarform`. Etter at brukeren har laget et nytt brev med en annen svarform, får et brevforslag da brevoppsett.

**Fiks (AD-8):** «`Analyse` lagrer bare `sprak` og `onskede_nokkelord`. Tone og svarform finnes bare på `Brev`. Brevskjemaet bruker standardverdiene fra FR-4 første gang, og deretter verdiene fra `Brev`. Alt som skal vise eller eksportere brevet, leser `Brev.svarform`.» Dette må gruppa bekrefte, fordi det endrer hva FR-4 lagrer.

---

## Lav

### L1. `nokkelord` står som Django-app i §3, men AD-2 sier at den ikke importerer Django

§3 regner opp `nokkelord` blant «Django-apper», og AD-17 legger tester i `<app>/tests/` med pytest-django. Én Claude legger appen i `INSTALLED_APPS` og lager `apps.py`, og bryter dermed AD-2. **Fiks:** «`nokkelord/` er en vanlig Python-pakke, ikke en Django-app. Testene bruker ikke `@pytest.mark.django_db`.» Det samme må avklares for `ki/`, som har en management-kommando og derfor *må* være en Django-app.

### L2. Stien til `docs/evaluering/` ligger utenfor `app/`

Kommandoen kjøres fra `app/`. Én Claude skriver til `docs/evaluering/` relativt til arbeidsmappa, altså `app/docs/evaluering/`. En annen bruker `BASE_DIR.parent / "docs/evaluering"`. **Fiks:** `settings.EVALUERING_DIR = BASE_DIR.parent / "docs" / "evaluering"` og et fast filnavn: `<dato>-<promptversjon eller kort commit-hash>.md`.

### L3. Det er ikke fastsatt hvor dekrypteringsfeil fanges

Med AD-9 [Forslag] kaster `from_db_value` en feil når nøkkelen er byttet. Den feilen kan oppstå i et hvilket som helst view. **Fiks:** «Feltet kaster `kjerne.feil.Dekrypteringsfeil`. En mellomvare i `kjerne/` fanger den og omdirigerer til en side som tilbyr å slette dokumentene. Views fanger den ikke selv.»

### L4. Det er ikke bestemt hvem som eier `base.html` og felles maldeler

To stories lager hver sin `templates/base.html`, og den ene får testmodus-banneret mens den andre får menyen. **Fiks:** Epic 0 eier `base.html`, `kjerne/context_processors.py` og `static/js/skjema.js`. Malene ligger i `templates/<app>/<side>.html`.

### L5. Språket i KI-kravene samsvarer ikke med språket i fasiten

Engelsk gap-analyse (`sprak=en`) gir krav på engelsk, mens fasiten er på norsk. Det henger sammen med H5 og lukkes med `alias` i fasiten, eller ved at evalueringen bare kjøres med `sprak=nb` for gap-analysen.

---

## Oppsummering av forslagene

| Funn | Hvor | Type endring |
|---|---|---|
| K1 | AD-6 | Strammes: `normaliser()`, `eksempel_hash()` og én eier |
| K2 | AD-12, AD-8 | Ny regel: delvis vellykket analyse og `ki_status` |
| K3 | AD-8, AD-2 | Strammes: én eier per modell, kaskade, retting av CV-tekst = ny CV |
| H1 | AD-3 | Strammes: fastsatte signaturer og `Innstillinger` |
| H2 | AD-6, §3 | Strammes: filnavnmønster og form på `Brev` |
| H3 | Ny AD | Feilkontrakt: `BrukerFeil` og `kjerne/meldinger.py` |
| H4 | AD-18 | Ny regel: eierskap til migreringer og Epic 0 |
| H5 | AD-17 | Strammes: `Fasit`-modell og én funksjon som laster eksempelpar |
| M1–M7 | AD-14, AD-17, §3, AD-12, AD-9, AD-13, AD-8 | Mindre strammere regler |
| L1–L5 | §3, AD-6, AD-9, §5, AD-17 | Avklaringer |

Alle forslagene er Claudes. Gruppa må bestemme hvilke som tas inn. M7 og K2 endrer i tillegg hva som lagres, og kan kreve en endring i PRD-en (FR-4, FR-11).
