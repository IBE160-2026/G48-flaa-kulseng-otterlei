# Gjennomgang av arkitekturen: sjekkliste og avstemming mot kildene

| | |
|---|---|
| **Dokument** | `ARCHITECTURE-SPINE.md` (status `draft`, oppdatert 2026-11-12) |
| **Kilder** | `prd/prd.md`, `prd/addendum.md`, `prd/tilbakemelding-prd.md`, `docs/tilbakemeldinger/tilbakemelding-product-brief.md`, `.memlog.md` |
| **Dato** | 2026-11-12 |
| **Gjort av** | Claude (kontrollør-agent), på oppdrag fra Henrik. Funnene er Claudes vurderinger og må vurderes av gruppa |

## Dom

Arkitekturen er solid og godt begrunnet, og den dekker de fleste stedene der tre utviklere kan bygge ting som ikke passer sammen. Før den binder stories, bør gruppa rette fem punkter med høy alvorlighet. Det viktigste er at KI-grensesnittet (AD-3) ikke samsvarer med det AD-5 og AD-7 sier skal sendes inn, og at feilregelen i AD-12 motsier FR-11 (nøkkelordene skal vises for egen CV i testmodus). I tillegg er lagringsvalget (SQLite) ikke begrunnet som en egen AD, selv om faglærer ba om det, og flere krav fra PRD-en (FR-3-grensene, NFR-4-varselet, NFR-7) har ikke fått noen regel.

Ingen funn er kritiske. Fem er høye, tolv middels og ti lave.

## Oversikt

| # | Alvorlighet | Funn | Hvor |
|---|---|---|---|
| H1 | høy | Signaturen til KI-porten mangler inndata som AD-5 og AD-7 krever | AD-3, AD-5, AD-7 |
| H2 | høy | AD-12 («ingenting lagres ved KIFeil») motsier FR-11 og UJ-3 | AD-12, AD-6, AD-8 |
| H3 | høy | Lagring (SQLite) er ikke en egen AD med begrunnelse, selv om faglærer ba om det | §4, AD-mangler |
| H4 | høy | PDF-eksporten mangler et bestemt Unicode-font. Kjernefontene i fpdf2 krasjer på tegn som «–», «’» og «•» | AD-13 |
| H5 | høy | Testmodus-oppslaget (normalisering, hash og filnavn) er ikke spesifisert, så skriptet og klienten kan gli fra hverandre | AD-6 |
| M1 | middels | Databasetransaksjonen rundt KI-kallet og samtidighetssperren er uspesifisert. SQLite kan låses i 60 sekunder | AD-8, AD-12 |
| M2 | middels | Djangos standard-passordregler bryter med FR-12 («ingen andre passordregler») | AD-11 |
| M3 | middels | FR-3-grensene (100–15 000 tegn) og en øvre grense for CV-teksten står ikke i arkitekturen | AD-15, AD-13 |
| M4 | middels | NFR-4: varselet om at CV-teksten sendes til en ekstern KI-tjeneste har ingen regel. Det samme gjelder «KI kan gjøre feil» (faglærer 4.5) | AD-5, AD-15 |
| M5 | middels | NFR-7 står under «Gjelder» i AD-15, men regelen sier ingenting om tilgjengelighet | AD-15 |
| M6 | middels | Formatet til `fasit.json` og `ordliste.json` er ikke fastsatt, men tre deler av koden leser filene | AD-7, AD-17, §7 |
| M7 | middels | Evalueringsrapporten har ingen bestått-kriterier, og regelen om å kjøre skriptet på nytt kan ikke håndheves | AD-6 |
| M8 | middels | Innlesing av TXT-filer (tegnkoding) og sjekken av filtype er uspesifisert | AD-13 |
| M9 | middels | Opplastinger over 2,5 MB skrives ukryptert til en midlertidig fil på disk | AD-9 |
| M10 | middels | Slettede data kan fortsatt ligge i SQLite-filen (FR-17: «ingen data om brukeren») | AD-8, AD-11 |
| M11 | middels | Drift og miljø: DEBUG, statiske filer og hva feilsidene viser er ikke bestemt | AD-14, AD-18 |
| M12 | middels | Det er uklart hva som skjer når CV-teksten endres (FR-2), og når eksempelpar velges (FR-10) | AD-8, AD-6 |
| L1–L10 | lav | Se egen liste nedenfor | |

---

## Del 1 – Sjekkliste for en god spine

### 1.1 Fikser den de reelle stedene der tre utviklere kan bygge ting som ikke passer sammen?

Stort sett ja. Lagdelingen (AD-2), KI-grensesnittet med to implementasjoner (AD-3), krypterte felttyper (AD-9), tilgang uten ID-er (AD-10), navn (AD-16) og ett sted for konfigurasjon (AD-14) er nettopp slike punkter, og reglene er konkrete. Disse stedene mangler likevel en regel:

#### H1 (høy): Signaturen til KI-porten stemmer ikke med AD-5 og AD-7

- **Hvor:** AD-3 («Alle tar inn CV-tekst, stillingsannonse og innstillinger»), AD-5 («for brev og forslag de manglende kravene fra gap-analysen»), AD-7 («KI får resultatet bare for å forklare det»)
- **Problem:** `brev` og `cv_forbedring` trenger gap-analysen eller listen over krav som mangler, og `nokkelord_forklaring` trenger `Nokkelordresultat`. Signaturen i AD-3 tar ikke imot noe av dette. Den som bygger `ClaudeKlient`, den som bygger `TestmodusKlient` og den som skriver tjenesten, vil hver legge til parametere på sin måte. Det er akkurat dette spriket porten skal hindre.
- **Forslag:** Skriv signaturene i AD-3, for eksempel `gap_analyse(cv_tekst, annonse, innst) -> GapAnalyse`, `brev(cv_tekst, annonse, innst, gap: GapAnalyse) -> Brev`, `cv_forbedring(cv_tekst, annonse, innst, gap) -> CVForbedringer` og `nokkelord_forklaring(cv_tekst, annonse, innst, resultat: Nokkelordresultat) -> Forklaring`. Definer også `Innstillinger` som én dataklasse eller pydantic-modell i `ki/modeller.py`.

#### H2 (høy): AD-12 motsier FR-11

- **Hvor:** AD-12 («Tjenesten fanger `KIFeil` … Viewet viser samme side på nytt … Ingenting overskrives før KI-kallet har lyktes»), AD-3 (`IkkeITestmodus` er en `KIFeil`), FR-11 («ATS-nøkkelordanalysen vises uten KI-forklaring»), UJ-3
- **Problem:** Laster brukeren opp egen CV i testmodus og trykker «Analyser», kaster `gap_analyse` feilen `IkkeITestmodus`. AD-12 sier da at ingenting lagres og at skjemaet vises på nytt. FR-11 krever at nøkkelordanalysen vises, sammen med meldingen der gap-analysen skulle stått. AD-8 sier heller ikke om `Analyse` kan lagres uten gap-analyse og forklaring. To utviklere vil løse dette ulikt: én med et spesialtilfelle i tjenesten, en annen i viewet.
  - Det samme gjelder en delvis feil i KI-modus. «Analyser» gjør to KI-kall (`gap_analyse` og `nokkelord_forklaring`). Hva skjer hvis det første lykkes og det andre feiler?
- **Forslag:** Legg til en regel i AD-12, for eksempel: «`IkkeITestmodus` er ikke en feil i flyten. `Analyse` lagres med nøkkelordresultatet, og gap-analysen og forklaringen står tomme (`null`). Resultatsiden viser FR-11-meldingen i hver KI-del. Andre `KIFeil` ved «Analyser» lagrer ingenting.» Gjør feltene for gap-analysen og forklaringen valgfrie i AD-8.

#### H5 (høy): Oppslaget i testmodus er ikke spesifisert

- **Hvor:** AD-6 («sammenligne en hash av normalisert CV-tekst og annonse», «Filnavnet sier hvilke innstillinger svaret gjelder»)
- **Problem:** `lag_lagrede_svar` skriver filene, og `TestmodusKlient` leser dem. Det er ikke sagt:
  - hvordan teksten normaliseres (mellomrom, linjeskift, `\r\n`, Unicode NFC)
  - hvilken hash som brukes, og hvor hashen for hvert par ligger
  - hvordan filnavnene skal se ut

  Lager ett gruppemedlem skriptet og et annet klienten, er det stor sjanse for at oppslaget aldri treffer. Hashen avhenger også av PDF-biblioteket hvis den regnes av teksten fra `cv.pdf`. Byttes `pdfplumber` med `pypdf` (AD-13), blir alle 42 svar ugyldige.
- **Forslag:** Lag én funksjon, `ki/testmodus_nokkel.py: normaliser(tekst) -> str` og `par_nokkel(cv_tekst, annonse) -> str` (SHA-256 av normalisert tekst). Både skriptet og klienten bruker den. Legg CV-teksten for hvert par som en egen fil, `testdata/eksempler/A/cv_tekst.txt`, og la knappen i FR-10 fylle inn den. Fastsett filnavnene, for eksempel `gap_analyse.nb.json`, `brev.nb.formell.fullt_utkast.json`, `cv_forbedring.en.json` og `nokkelord_forklaring.nb.json`.

#### M1 (middels): Transaksjonen og samtidighetssperren er uspesifisert

- **Hvor:** AD-8 («Begge skjer i én databasetransaksjon i tjenestelaget»), AD-12 («Serveren avviser en ny analyse for samme bruker mens én allerede kjører»)
- **Problem:**
  1. Pakker en utvikler hele tjenesten, med KI-kallet, inn i `transaction.atomic` (eller slår på `ATOMIC_REQUESTS`), holder SQLite skrivelåsen i opptil 60 sekunder. Andre brukere får da «database is locked» etter 5 sekunder. Dette er særlig aktuelt fordi `runserver` håndterer flere forespørsler samtidig.
  2. Regelen om å avvise en analyse som allerede kjører, sier ikke hvordan det gjøres. Et felt i databasen? En lås i minnet? Hva skjer med en sperre som henger igjen hvis serveren krasjer? Regelen gjelder heller ikke for brev og CV-forbedring, der et dobbeltklikk også koster penger.
- **Forslag:** Legg til regelen: «KI-kallet gjøres utenfor transaksjonen. Etterpå lagres resultatet i en kort `transaction.atomic`. `ATOMIC_REQUESTS = False`.» Bestem sperren, for eksempel et felt `ki_kall_startet` (tidsstempel) på `Bruker` som settes med en betinget `update()` og regnes som utløpt etter 90 sekunder. La den gjelde alle de fire KI-operasjonene. Alternativt kan serversperren strykes, slik at NFR-6 bare dekkes av JavaScriptet. Da må det stå som et bevisst valg.

#### M6 (middels): Formatet til `fasit.json` og `ordliste.json` er ikke fastsatt

- **Hvor:** AD-7 («kuratert ordliste (`nokkelord/ordliste.json`, med synonymer)»), AD-17 (innholdet i fasiten), §7 («Formatet er bestemt (AD-7)»)
- **Problem:** §7 sier at formatet til ordlisten er bestemt, men AD-7 beskriver det ikke. Fasiten leses av tre deler: nøkkelordtestene, `lag_lagrede_svar` (evalueringen) og testene for gap-analysen. Ofte lages den av en fjerde person sammen med eksempeldataene. Det er nettopp der formatene spriker.
- **Forslag:** Definer `Fasit` og `Ordliste` som pydantic-modeller i én fil (for eksempel `kjerne/fasit.py` og `nokkelord/ordliste.py`), og vis et kort JSON-eksempel i AD-7 og AD-17. Rett §7, så den ikke sier at formatet er bestemt før det står i AD-7.

#### M12 (middels): Endret CV-tekst og valg av eksempelpar

- **Hvor:** AD-8, AD-6, FR-2, FR-10
- **Problem:**
  - FR-2 lar brukeren rette CV-teksten. Det står ikke om teksten lagres i `CV` før analysen, og om endringen sletter `Analyse`, `Brev` og `CVForbedring`, slik en ny opplasting gjør. `Analyse` har ingen kopi av CV-teksten. Retter brukeren teksten etter analysen og ber om brev, lages brevet fra ny tekst og gammel gap-analyse.
  - FR-10: Når brukeren trykker «Prøv med eksempel A», blir det da lagret en `CV`? Med `cv.pdf` som fil eller uten fil? Dette er ikke bestemt.
- **Forslag:** Legg til regelen: «Brukeren retter CV-teksten i samme skjema som «Analyser». Tjenesten lagrer teksten i `CV.cv_tekst` i samme transaksjon som den nye `Analyse`.» Gjør det også klart om en endret tekst uten ny analyse sletter brev og forbedring. For eksempelpar: «Knappen lagrer en `CV` med eksempelets fil og `cv_tekst.txt`, som en vanlig opplasting.»

### 1.2 Er hver AD-regel håndhevbar, og hindrer den spriket den sier?

| AD | Kan håndheves? | Kommentar |
|---|---|---|
| AD-1 | ja | |
| AD-2 | delvis | Krever disiplin i gjennomgangen. Foreslå en test som sjekker importene (for eksempel at `nokkelord/` ikke importerer `django`) eller `import-linter`. «Tjenester er det eneste laget som skriver modeller» kolliderer med `ModelForm.save()` og Djangos innloggingsskjemaer. Si om `UserCreationForm.save()` er lov (L1). |
| AD-3 | delvis | Se H1 (signaturer) og H2 (`IkkeITestmodus`). |
| AD-4 | ja | Feiloversettelsen er konkret og kan testes. 401 (ugyldig nøkkel) blir `KIUtilgjengelig`. Sensor med feil nøkkel bør få en egen melding (L2). |
| AD-5 | delvis | Det kan ikke kontrolleres at bare tillatte felt sendes. Et fast pydantic-objekt (`KIForesporsel`) som eneste inndata til `ClaudeKlient` gjør regelen mulig å kontrollere, og passer sammen med H1. |
| AD-6 | nei | Se H5 og M7. «Kjøres på nytt hver gang en prompt endres» avhenger av hukommelsen. |
| AD-7 | ja | Bortsett fra formatet (M6) og hvordan ønskede nøkkelord tas imot (streng eller liste, og hvem som deler dem opp, L3). |
| AD-8 | ja | `OneToOne` håndhever regelen i databasen. Se M1 og M12. |
| AD-9 | delvis | Bruk av riktig felttype kan sjekkes av en test som går gjennom `apps.get_models()` og feiler på vanlige `TextField`, `JSONField` og `BinaryField` i dokumentmodeller. Feilen ved dekryptering har ikke noe navn (M9b). |
| AD-10 | ja | |
| AD-11 | delvis | Se M2 (passordregler) og L4 (store og små bokstaver i e-post). |
| AD-12 | delvis | Se H2 og M1. |
| AD-13 | delvis | Se H4 og M8. |
| AD-14 | ja | Se M11 (DEBUG). |
| AD-15 | delvis | Regelen mot `|safe` kan sjekkes med grep. NFR-7 mangler (M5). |
| AD-16 | ja | |
| AD-17 | delvis | «Uten nettverk» håndheves ikke. Med `pytest-socket` (`--disable-socket`) feiler en test som prøver å gå på nettet (L5). |
| AD-18 | ja | |

#### M2 (middels): Djangos passordregler bryter med FR-12

- **Hvor:** AD-11 («minste lengde er 8 tegn»), FR-12 («Det er ingen andre passordregler»)
- **Problem:** Et nytt Django-prosjekt har fire regler i `AUTH_PASSWORD_VALIDATORS`: likhet med brukerens opplysninger, vanlige passord, bare tall og minste lengde. Regelen om vanlige passord avviser for eksempel «passord1», og regelen om bare tall avviser «12345678». FR-12 sier at det ikke skal være andre regler.
- **Forslag:** Legg til regelen: «`AUTH_PASSWORD_VALIDATORS` inneholder bare `MinimumLengthValidator` med `min_length=8`.» Alternativt kan gruppa velge å beholde Djangos regler og oppdatere FR-12.

### 1.3 Kan noe under «Utsatt» la to deler spriké?

| Utsatt | Risiko | Kommentar |
|---|---|---|
| Visuelt design og CSS | lav til middels | `base.html` er felles. Uten regler for NFR-7 kan sidene likevel bli ulike i tilgjengelighet (M5). |
| Teksten i promptene | lav | Plasseringen er bestemt. Men signaturen (H1) og formatet på svarene må være bestemt før promptene skrives. |
| Innholdet i `ordliste.json` | **middels** | Formatet er ikke bestemt, selv om §7 sier det (M6). |
| Nøkkelbytte | lav | Hva som skjer når nøkkelen er byttet, er beskrevet som [Forslag] i AD-9. |
| Hosting, HTTPS | lav | |
| Grense for innloggingsforsøk | lav | |
| Glemt passord, historikk | lav | |

Det mangler også noen ting som verken er utsatt eller bestemt: hvor lenge en innlogging varer (Djangos standard er 2 uker; faglærer sa at dette kan vente, så det bør stå i §7), egne feilsider for 404 og 500, og om `LANGUAGE_CODE` er `nb` (L6).

### 1.4 Dekker den alle FR og NFR?

Alle FR-er og NFR-er står under `binds`. Tabellen i §6 har derimot ingen rader for **NFR-3, NFR-4, NFR-7, NFR-8, NFR-9 og NFR-10**. NFR-3 og NFR-4 dekkes i praksis av AD-5, AD-9, AD-10 og AD-15, og NFR-9 av AD-4 og AD-14. NFR-7 har ingen regel (M5), og varselet i NFR-4 har heller ingen regel (M4). Siden sensor ser etter sporbarhet, bør tabellen ha en rad for hvert krav (L7).

Krav som har landet bare delvis:

| Krav | Status | Funn |
|---|---|---|
| FR-1 | delvis | Filtype, 5 MB og `TomPDF` er med. Tegnkoding for TXT og sjekken av filtype mangler (M8). Midlertidig fil på disk (M9). |
| FR-2 | delvis | M12 |
| FR-3 | **mangler** | M3 |
| FR-10 | delvis | H5, M12 |
| FR-11 | **motsies** | H2. Meldingen er bare tatt med ved henvisning («meldingen fra FR-11»). Den bør stå ordrett ett sted, for eksempel i `kjerne/meldinger.py`. |
| FR-12 | **motsies** | M2 |
| FR-17 | delvis | M10 |
| FR-23 | delvis | H4 |
| NFR-4 | delvis | M4 |
| NFR-7 | **mangler** | M5 |
| NFR-8 | delvis | L6 (Djangos egne meldinger kommer på engelsk) |

#### H4 (høy): PDF-eksporten mangler et Unicode-font

- **Hvor:** AD-13 («`fpdf2` … æ, ø og å»), FR-23, SM-7
- **Problem:** Kjernefontene i fpdf2 (Helvetica, Times) støtter bare Latin-1. Æ, ø og å er med, men tegnene KI ofte skriver, er det ikke: tankestrek «–», krøllete anførselstegn «’ “ ”», punkttegn «•» og «…». fpdf2 gir da en feil, og eksporten krasjer for nesten alle ekte brev. Testen i SM-7 kan likevel bestå hvis den bare bruker æ, ø og å. Velger to utviklere ulik løsning (bytte ut tegn eller bruke et font), blir resultatet forskjellig.
- **Forslag:** Legg til regelen: «`eksport/pdf.py` bruker et innebygd TTF-font med åpen lisens (for eksempel DejaVu Sans eller Noto Sans) som ligger i `eksport/fonter/` og legges til med `add_font()`. Kjernefontene brukes ikke.» Testen i SM-7 bør ta med «– ’ • …».

### 1.5 Er hver dimensjon bestemt, utsatt eller et åpent spørsmål?

| Dimensjon | Status | Kommentar |
|---|---|---|
| Rammeverk og paradigme | bestemt | AD-1, AD-2 |
| KI-leverandør og modell | bestemt | AD-4 |
| **Lagring (database)** | **bare i stacktabellen** | H3 |
| Kryptering | bestemt | AD-9. Trusselmodellen er ikke beskrevet (L8). |
| Innlogging og tilgang | bestemt | AD-10, AD-11. Hvor lenge en innlogging varer, er ikke nevnt (§1.3). |
| Datamodell | bestemt | AD-8 |
| PDF inn og ut | bestemt | AD-13, med krav før P2 |
| Konfigurasjon og hemmeligheter | bestemt | AD-14 |
| Grensesnitt | bestemt og utsatt | AD-15 og UX |
| Testing | bestemt | AD-17 |
| Kjøring (hvor) | bestemt | AD-18: bare lokalt |
| **Kjøring (hvordan)** | **delvis** | M11: DEBUG, statiske filer, feilsider |
| Drift og leverandørkonto | åpent spørsmål | §8 punkt 2 (API-kontoen). Bra at det står. |
| Hvem som kjører `lag_lagrede_svar` | åpent (indirekte) | Krever API-nøkkel. Henger sammen med §8 punkt 2. Bør nevnes der. |
| Overvåking og backup | utsatt | §7 |
| Logging | bestemt | §3 |
| Internasjonalisering av Django | ikke nevnt | L6 |

#### H3 (høy): Lagringsvalget er ikke begrunnet i arkitekturen

- **Hvor:** §4 («SQLite | følger med Python»), §5. Begrunnelsen og alternativet som ble valgt bort (PostgreSQL), står bare i `.memlog.md`.
- **Kilde:** Faglærer, tilbakemelding på briefen, kriterium 5: «Begrunn valg av LLM-leverandør, **lagring** og kryptering i arkitekturen.»
- **Problem:** Leverandøren (AD-4) og krypteringen (AD-9) har egne AD-er med begrunnelse og alternativer som ble valgt bort. Lagringen har det ikke, selv om faglærer nevnte den uttrykkelig. Sensor leser spine-dokumentet, ikke beslutningsloggen. Lagringspolicyen (ingen automatisk sletting, bare siste resultat) står i PRD-en, men henger ikke sammen med et lagringsvalg i arkitekturen.
- **Forslag:** Lag en egen AD, for eksempel «AD-19 Lagring: SQLite i én fil». Gjelder: alle modeller. Begrunnelse: følger med Python, ingen server å installere (NFR-1), en lokal app med få brukere. Valgt bort: PostgreSQL (server eller Docker, i strid med NFR-1). Ta med det som følger av valget: låsing ved skriving (M1), sletting (M10), og at `db.sqlite3` holdes utenfor git.

#### M11 (middels): Drift og miljø, med DEBUG og statiske filer

- **Hvor:** AD-14 (`DJANGO_DEBUG`), AD-18, AD-10 («Dokumentinnhold legges aldri … i unntakstekster»)
- **Problem:**
  - Med `DEBUG=False` serverer `runserver` ikke statiske filer. CSS og `skjema.js` forsvinner, og NFR-6 og FR-22 slutter å virke for sensor.
  - Med `DEBUG=True` viser Djangos feilside de lokale variablene ved en feil, også CV-teksten. Det bryter med intensjonen i AD-10.
  - `ALLOWED_HOSTS` er ikke nevnt.
  - Det står ikke hva appen gjør når `DJANGO_SECRET_KEY` mangler: stopper den, som ved `KRYPTERINGSNOKKEL`?
- **Forslag:** Bestem verdiene i `.env.example`, for eksempel `DJANGO_DEBUG=true` for lokal kjøring, og si at dette er et bevisst valg fordi appen aldri kjøres i produksjon (AD-18). Alternativt kan gruppa bruke `DEBUG=False` med `whitenoise` eller `runserver --insecure`. Sett `ALLOWED_HOSTS = ["localhost", "127.0.0.1"]`. Si at en manglende `DJANGO_SECRET_KEY` stopper appen på samme måte som en manglende `KRYPTERINGSNOKKEL`. Legg også til at `lag_env.py` ikke skal overskrive en `.env` som finnes fra før, fordi en ny krypteringsnøkkel gjør alle lagrede dokumenter uleselige (L9).

---

## Del 2 – Avstemming mot kildene

### 2.1 PRD

#### M3 (middels): FR-3-grensene og en grense for CV-teksten

- **Hvor:** FR-3 («under 100 tegn gir en melding, ikke et KI-kall»; «over 15 000 tegn avvises»), §12 (bekreftet av gruppa). Arkitekturen nevner ingen av tallene. AD-15 sier bare at det brukes Django-skjemaer og `maxlength`.
- **Problem:**
  - Grensene ligger i dag i hodet til den som skriver `analyse/forms.py`. Skjemaet, `maxlength`-attributtet og testene bør bruke de samme konstantene.
  - Det står ikke om grensen regnes før eller etter at mellomrom i starten og slutten er fjernet.
  - **Det finnes ingen øvre grense for CV-teksten.** En TXT-fil på 5 MB gir rundt 5 millioner tegn, som sendes til KI. Det sprenger kontekstvinduet og koster mye. Kostnadsgrunnen bak FR-3 gjelder minst like mye for CV-teksten (NFR-9). Det samme gjelder ønskede nøkkelord.
- **Forslag:** Legg konstantene ett sted, for eksempel `kjerne/grenser.py` med `ANNONSE_MIN = 100`, `ANNONSE_MAKS = 15_000`, `CV_FIL_MAKS_BYTE = 5 * 1024 * 1024`, `CV_TEKST_MAKS = …` og `ONSKEDE_NOKKELORD_MAKS = …`. Skjemaer, maler og tester bruker disse. Grensen for CV-teksten er en ny føring som gruppa må bestemme, og den bør også inn i PRD-en (FR-2).

#### M4 (middels): NFR-4-varselet og «KI kan gjøre feil»

- **Hvor:** NFR-4 («Appen forteller brukeren at CV-teksten sendes til en ekstern KI-tjeneste»), addendum til UX («Min konto bør forklare … hva som sendes til KI-tjenesten»), §6 skjermbilde 4, faglærer 4.5 («Resultatsiden viser teksten ‹KI kan gjøre feil – les gjennom før du sender›»)
- **Problem:** AD-5 dekker *hva* som sendes, men ingen AD sier *at* og *hvor* brukeren får beskjed. Faglærers forslag om varselet på resultatsiden er heller ikke med. §8 punkt 1 nevner bare at annonsen er data, ikke instruksjoner, fra 4.5. Disse varslene havner lett mellom UX og koding, og blir glemt.
- **Forslag:** Legg til regelen i AD-15 eller AD-5: «Siden for ny analyse viser, ved «Analyser»-knappen, at CV-teksten og annonsen sendes til Claude API (Anthropic) i KI-modus. Resultatsiden viser «KI kan gjøre feil – les gjennom før du sender». Tekstene ligger i `kjerne/meldinger.py`.» Ta med varselet i §8 punkt 1, siden PRD-en må oppdateres. Faglærers forslag om en egen annonse som tester prompt-injeksjon, er heller ikke med. Det passer naturlig som et fjerde eksempel i evalueringsrapporten (AD-6).

#### M5 (middels): NFR-7 mangler en regel

- **Hvor:** AD-15 nevner NFR-7 under «Gjelder», men regelen inneholder ingenting om tilgjengelighet.
- **Problem:** Etiketter, tastaturbruk, kontrast, alternativtekst og skjermer fra 360 px er krav som går på tvers av alle sidene. Bygger tre personer hver sin side, blir de ulike hvis ikke `base.html` og reglene for skjemaer tar seg av det.
- **Forslag:** Legg til i AD-15:
  - Skjemafelt vises med Djangos `label`.
  - Knapper er `<button>`, ikke `<div>` med klikkhendelser.
  - Kopier-knappen (FR-22) og «Jobber …»-visningen (NFR-6) bruker `aria-live`.
  - `base.html` har `<meta name="viewport">` og `lang="nb"`.
  - Ingen fast bredde over 360 px.

  Detaljene kan vente til UX-steget, men da bør det stå i §7 at NFR-7 bestemmes der.

#### M8 (middels): Innlesing av TXT og sjekk av filtype

- **Hvor:** AD-13 (`les_cv` «sjekker filtype»), FR-1, FR-23 (æ, ø og å)
- **Problem:** Det står ikke om filtypen sjekkes med filendelsen, `content_type` (som nettleseren bestemmer) eller de første bytene i filen (`%PDF-`). Det står heller ikke hvilken tegnkoding TXT-filer leses med. Norske TXT-filer fra Windows er ofte cp1252. Leses de som UTF-8, gir det feil eller ødelagte tegn. To personer (den som lager opplastingen og den som skriver testene) vil løse dette forskjellig.
- **Forslag:** Legg til regelen: «Filtypen avgjøres av filendelsen og kontrolleres mot innholdet (`%PDF-` for PDF). TXT leses som UTF-8 (med eller uten BOM), og hvis det feiler, som cp1252. Andre feil gir `InnlesingFeil`.»

#### M9 (middels): Ukrypterte midlertidige filer og navn på dekrypteringsfeilen

- **Hvor:** AD-9, FR-15
- **Problem:**
  1. Django skriver opplastinger over `FILE_UPLOAD_MAX_MEMORY_SIZE` (2,5 MB som standard) til en midlertidig fil på disk. En CV på mellom 2,5 og 5 MB blir altså liggende ukryptert i den midlertidige mappen en kort stund. Det bryter med intensjonen i FR-15, selv om filen slettes etterpå.
  2. Regelen for et felt som ikke kan dekrypteres, gir ikke feilen noe navn og sier ikke hvor den fanges. Felttypen kaster den når modellen lastes, altså ofte i en tjeneste eller mal. Da blir det fort ulike løsninger, eller en feilside med stacktrace.
- **Forslag:**
  1. Sett `FILE_UPLOAD_MAX_MEMORY_SIZE` til 5 MB, eller bruk bare `MemoryFileUploadHandler`.
  2. Kall feilen for eksempel `DekrypteringFeil` (i `kjerne/kryptering.py`) og si at tjenestene fanger den og sender brukeren til en side som tilbyr sletting.

#### M10 (middels): Slettede data kan ligge igjen i SQLite-filen

- **Hvor:** FR-16 («ingen av brukerens dokumenter i databasen»), FR-17 («ingen data om brukeren i databasen»), SM-9, AD-8, AD-11
- **Problem:** SQLite overskriver ikke slettede rader som standard. Sidene blir merket som ledige. E-posten til en slettet bruker, som ikke er kryptert, kan derfor fortsatt leses i `db.sqlite3` med en hex-editor eller `strings`. Dokumentene er krypterte, så der er risikoen lav. For e-posten bryter dette med FR-17 hvis testen leser filen direkte, slik SM-8 gjør for kryptering. I tillegg ligger øktrader i `django_session` igjen til de utløper.
- **Forslag:** Legg til regelen: «`PRAGMA secure_delete = ON` settes ved oppkobling (via `connection_created`-signalet), og sletting av konto logger brukeren ut og fjerner øktene hennes.» Eventuelt kan `VACUUM` kjøres etter at en konto er slettet. Testen for FR-17 kan søke etter e-posten som bytes i databasefilen.

#### Andre PRD-punkter som mangler eller er uklare

- **FR-11-meldingen:** Står bare som en henvisning. Den bør legges ordrett ett sted (se tabellen i §1.4). UJ-3 sier også at appen forklarer «hvordan en API-nøkkel legges inn». Meldingen kan lenke til README (lav).
- **FR-12 og FR-13:** E-post skal være unik, men det står ikke om `Emma@x.no` og `emma@x.no` er samme konto. Djangos `normalize_email` gjør bare domenet til små bokstaver. Registrering og innlogging kan da behandle store bokstaver ulikt (L4).
- **FR-21:** Den foreslåtte løsningen i AD-7 («ingen KI-forklaring») sier ikke om hele forklaringen skjules, eller bare delen om de ønskede nøkkelordene. Kostnaden er liten, men det bør presiseres (lav).
- **Kostnad i AD-4:** «Under 0,50 kr per kall» stemmer for en vanlig annonse. Med en annonse på 15 000 tegn og en lang CV blir det omtrent 9 000 tegn-tokens inn og 1 500 ut, altså rundt 0,07 USD, eller omtrent 0,7 kr. Dette er Claudes grove overslag og bør kontrolleres. Skriv «rundt 0,3–0,8 kr» eller oppgi hva tallet bygger på (lav).

### 2.2 Addendum

| Punkt i addendumet | Status |
|---|---|
| Leverandør (norsk språk, kostnad, databehandling, forbruksgrense) | Med i AD-4 |
| Nøkkelord med ordliste | Med i AD-7. Formatet mangler (M6) |
| 42 lagrede svar og skript | Med i AD-6. Oppslaget er uspesifisert (H5) |
| Felles grensesnitt for KI-kall | Med i AD-3. Signaturen mangler (H1) |
| Strukturerte svar | Med i AD-4 og §3 |
| PDF testet mot C før resten bygges, brevoppsett med æ, ø og å | Med i AD-13. Font mangler (H4) |
| Hva skjer hvis krypteringsnøkkelen mangler eller byttes | Med i AD-9. Navnet på feilen mangler (M9) |
| UX: avsender før PDF-eksport, «opplysningene lagres ikke» | Delvis. AD-13 sier at avsenderen ikke lagres, men ikke at den aldri sendes til KI. Det følger av hvitelisten i AD-5, men bør nevnes i AD-13 (lav) |
| UX: «Min konto» forklarer lagringspolicyen og hva som sendes til KI | Mangler (M4) |

### 2.3 Faglærers tilbakemelding på PRD-en

| Punkt | Status |
|---|---|
| 4.1 Evaluering i KI-modus og fast format | Delvis. AD-4 og AD-6 tar med evalueringen og formatet. Bestått-kriterier mangler (M7) |
| 4.1 Et svar som ikke kan leses, behandles etter NFR-5 | Med (`KIUgyldigSvar`) |
| 4.2 Kuttrekkefølge | Riktig plassert i §8 som gruppas ansvar |
| 4.3 Resultat i tre deler | Med i AD-8, merket [Forslag] |
| 4.3 Ønskede nøkkelord i testmodus | Med i AD-7, merket [Forslag] |
| 4.4 Fasit med tre lister | Med i AD-17. Formatet mangler (M6) |
| 4.4 Sjekkbart kriterium for brev | Mangler. Kunne vært automatisert i evalueringsrapporten (M7) |
| 4.5 Annonsen er data, ikke instruksjoner | Med i AD-5 |
| 4.5 «KI kan gjøre feil – les gjennom» | Mangler (M4) |
| 4.5 Eksempelannonse som tester injeksjon | Mangler (M4) |
| §6 «Kan vente: hvor lenge en innlogging varer» | Ikke nevnt i §7 (§1.3) |

#### M7 (middels): Evalueringsrapporten mangler kriterier og kan ikke håndheves

- **Hvor:** AD-6 («lager i samme kjøring en evalueringsrapport mot fasit», «Kommandoen kjøres på nytt hver gang en prompt endres»), faglærer 4.1 («0 manglende krav feilmerket som matcher … 0 treff på fasitens liste over forbudte påstander») og 4.4
- **Problem:** Det står ikke hva rapporten måler, eller når en kjøring regnes som bestått. Regelen om å kjøre skriptet på nytt etter en promptendring avhenger av at noen husker det. Det var nettopp faglærers spørsmål 2: «Hvordan vil dere oppdage at en endret prompt gjør KI-svarene dårligere?»
- **Forslag:**
  1. Rapporten måler minst: krav som mangler, men er feilmerket som matcher (må være 0), krav som matcher, men er feilmerket som manglende, treff på listen over krav som mangler i brev og forslag (må være 0), og treff på floskler (må være 0).
  2. Hvert lagret svar har metadata med hash av promptfilen og modell-ID. En vanlig pytest-test sammenligner hashen av `ki/prompter/*` med metadataene og feiler hvis en prompt er endret uten at svarene er laget på nytt. Da håndheves regelen av testene, uten nettverk.

### 2.4 Faglærers tilbakemelding på briefen

| Punkt | Status |
|---|---|
| Begrunn valget av LLM-leverandør | Med i AD-4, med databehandling og interessekonflikt. Bra |
| Begrunn valget av **lagring** | **Mangler** (H3) |
| Begrunn valget av kryptering | Med i AD-9. Det står ikke hva krypteringen beskytter mot (L8) |
| Velg bibliotek for filhåndtering tidlig | Med i AD-13, med krav før P2 |
| Beskriv hvordan nøkkelen konfigureres | Med i AD-14 (`.env.example`, `lag_env.py`) |
| Beskriv hvordan testmodus for sensor fungerer | Med i AD-6 og AD-14. Oppslaget er uspesifisert (H5) |
| `.env.example` for API- og krypteringsnøkler | Med i AD-14 |
| Bare oppdiktede testdata | Med i NFR-4 i PRD-en. Ikke gjentatt i arkitekturen, men `testdata/` er riktig plassert (OK) |
| Teknologivalg ikke mer komplekse enn nødvendig | Godt dekket. Hver AD har en «Valgt bort»-linje, og `technology.md` er vurdert |

---

## Lave funn

- **L1:** AD-2 sier at bare tjenester skriver modeller. Si om `UserCreationForm.save()` og `LoginView` er unntak, eller om registreringen skal gå gjennom `kontoer/tjenester.py`.
- **L2:** En ugyldig API-nøkkel (401) blir `KIUtilgjengelig`. Sensor som legger inn feil nøkkel, bør få meldingen «API-nøkkelen ble avvist» (for eksempel en egen `KIUgyldigNokkel`).
- **L3:** `finn_nokkelord(annonse, onskede)`: si at `onskede` er `list[str]`, og at skjemaet deler opp teksten på komma og linjeskift.
- **L4:** E-post lagres med små bokstaver (`email.strip().lower()`) både ved registrering og innlogging.
- **L5:** AD-17: Bruk `pytest-socket` (`--disable-socket`) for å håndheve «uten nettverk» i NFR-2. `pytest-socket` står ikke i stacken.
- **L6:** NFR-8: Sett `LANGUAGE_CODE = "nb"` og `USE_I18N = True`. Ellers kommer Djangos egne meldinger («This field is required.» og passordmeldinger) på engelsk.
- **L7:** Tabellen i §6 mangler rader for NFR-3, NFR-4, NFR-7, NFR-8, NFR-9 og NFR-10.
- **L8:** AD-9: Skriv én setning om hva krypteringen beskytter mot. Den beskytter databasefilen alene (for eksempel om den kopieres eller sjekkes inn i git ved en feil), men ikke mot noen som har tilgang til maskinen, siden `.env` ligger ved siden av. Faglærer ba om at krypteringen begrunnes.
- **L9:** `lag_env.py` skal ikke overskrive en `.env` som finnes fra før, siden en ny `KRYPTERINGSNOKKEL` gjør alle dokumentene uleselige. `.gitignore` i rotmappen dekker `.env`, men **ikke** `db.sqlite3` ennå. §5 sier at den skal inn.
- **L10:** Mindre ting:
  - `docs/evaluering/` ligger utenfor `app/`, mens alle kommandoer kjøres fra `app/`. Si at stien bygges fra `BASE_DIR.parent`.
  - `[Forslag]`-merket står midt i begrunnelsen i AD-9 og AD-10, så det er uklart hva som er forslaget.
  - «Tilgjengelighet» og «Grensesnittspråk» bør nevnes i §6.

## Det som er bra

- Hver AD har «Hindrer» og «Valgt bort», og interessekonflikten ved leverandørvalget er nevnt. Det er nøyaktig det sensor ser etter i kriterium 1 og 5.
- AD-10 fjerner FR-14-risikoen ved at URL-ene ikke har ID-er. Det er en enkel og sterk løsning.
- AD-4 har `max_retries=0` og en konkret oversettelse av feilmeldingene om forbruksgrensen. Det viser at gruppa har sjekket API-et i stedet for å gjette.
- AD-13 har et «krav før P2» med en reserveløsning, slik at den største tekniske risikoen blir et konkret sjekkpunkt.
- Avviket fra PRD-en (Resultat i tre deler) er åpent merket, og §8 sier at PRD-en må oppdateres. Husk å forklare dette i `docs/endringer/` når PRD-en oppdateres (CLAUDE.md, NFR-10).
