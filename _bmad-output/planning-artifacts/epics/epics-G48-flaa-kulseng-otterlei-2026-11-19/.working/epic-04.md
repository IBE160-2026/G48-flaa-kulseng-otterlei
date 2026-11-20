## Epic 4: Gap-analyse med KI

Brukeren får gap-analysen med begrunnelser, i testmodus med lagrede svar og i KI-modus med Claude. Koden ligger i `ki/` (klientene, promptene og `lag_lagrede_svar`) og `analyse/` (tjenesten, steg 3 og feiltilstandene), etter eierskapsreglene i AD-2. Testmodus-klienten kommer før Claude-klienten, så snittet virker uten nøkkel. KI-forklaringen av nøkkelordene er siste story, fordi den kan kuttes (PRD §8.1). Story 4.2 og 4.3 leveres i samme pull request, fordi egen CV i testmodus ellers gir feil i steg 2 mellom dem.

### Story 4.1: Testmodus-klient med lagrede svar

Som sensor
vil jeg at appen henter KI-svar fra lagrede filer når den kjører uten nøkkel,
slik at jeg kan prøve gap-analysen uten API-nøkkel, nettverk eller kostnad.

**Krav:** FR-9, FR-10, FR-11, NFR-2. **Styres av:** AD-3, AD-6, AD-14, AD-17.

**Akseptansekriterier:**

**Gitt** `ki/eksempelpar.py`
**Når** storyen er ferdig
**Så** finnes også `eksempel_hash(cv_tekst, annonse)` og `svarfil(par, operasjon, **innstillinger)` slik AD-6 beskriver dem
**Og** `svarfil` gir filnavn på formen `<operasjon>__<sprak>[__<tone>__<svarform>].json` i `testdata/eksempler/<par>/svar/`, for eksempel `gap_analyse__en.json`
**Og** hashene for A, B og C regnes ut fra `les_cv()` og `annonse.txt` første gang de trengs, huskes med `functools.cache` og lagres ikke på disk, så `migrate` og testene ikke må lese PDF-ene ved oppstart (AD-6)
**Og** mappen med eksemplene kommer fra `settings.EKSEMPLER_DIR`, så testene kan bytte den

**Gitt** `ki/testmodus_klient.py: TestmodusKlient`
**Når** en av de fire operasjonene kalles med CV-tekst og annonse som etter `normaliser()` gir hashen til et par
**Så** leser klienten filen fra `svarfil()` og returnerer `svar` validert mot returtypen i `ki/modeller.py` (AD-6)
**Og** gir teksten ikke treff på noe par, eller finnes ikke filen, kastes `IkkeITestmodus` (FR-11)

**Gitt** `ki.hent_klient()`
**Når** den kalles
**Så** returnerer den overstyringen fra testene når den er satt, ellers `TestmodusKlient` når `er_testmodus()` er sann (AD-3)
**Og** i KI-modus kaster den `KIUgyldigNokkel` til Claude-klienten finnes (story 4.4)

**Gitt** testene for storyen
**Når** de kjøres
**Så** bruker de egne testfiler med lagrede svar i en midlertidig mappe via `settings.EKSEMPLER_DIR`, ikke ekte svar, tømmer cachen for hashene mellom testene, og sjekker treff for A, B og C, at teksten gir treff også med `\r\n`, og at en endret CV gir `IkkeITestmodus`

### Story 4.2: Gap-analyse i steg 3 med lagrede svar

Som student
vil jeg se hvilke krav i annonsen CV-en min dekker og hvilke som mangler,
slik at jeg vet hva jeg bør ta med i søknaden.

**Krav:** FR-5, FR-10, NFR-2, NFR-3, NFR-4, NFR-5, NFR-6. **UX:** UX-DR15, UX-DR16, UX-DR29, UX-DR30, UX-DR31. **Styres av:** AD-3, AD-5, AD-8, AD-9, AD-10, AD-12, AD-15, AD-17, AD-20.

**Akseptansekriterier:**

**Gitt** `analyse.tjenester` og «Analyser»
**Når** jeg trykker «Analyser» i steg 2
**Så** kjøres `nokkelord.match` først (fra Epic 3) og deretter `ki.hent_klient().gap_analyse(cv_tekst, annonse, sprak)` inne i `ki_las(bruker_id)`, utenfor databasetransaksjonen (AD-8, AD-12)
**Og** resultatet lagres i `Analyse` i et kryptert felt i en kort `transaction.atomic` (AD-9, AD-12)
**Og** storyen legger til feltet `ki_status` på `Analyse` med verdiene `ok` (standard) og `ikke_i_testmodus` (brukes i story 4.3), med migrering (AD-8)
**Og** mens jeg venter, viser «Analyser» «Jobber …» med den felles ventetilstanden fra `skjema.js`, og et nytt trykk gir ikke et nytt kall (NFR-6, UX-DR30)

**Gitt** et svar fra `falsk_ki` for par A der «Python» og «Git» matcher, og «SQL» og «Førerkort klasse B» mangler (de ekte lagrede svarene kommer i story 4.5)
**Når** steg 3 vises
**Så** har overskriften «2 av 4 krav dekket», «Python» og «Git» står som ✓ «Matcher» først med begrunnelsen fra CV-teksten, og «SQL» og «Førerkort klasse B» står som ! «Mangler» (FR-5, UX-DR16)
**Og** kortet har merket «Laget av KI», blokken har `lang` etter valgt språk, og «KI kan gjøre feil – les gjennom før du sender.» står øverst i steg 3, laget med `templates/felles/ki_merke.html` og `ki_varsel.html` (NFR-4, UX-DR15)
**Og** all KI-tekst vises med Djangos escaping, uten `|safe` (NFR-3, AD-15)

**Gitt** en annen `KIFeil` enn `IkkeITestmodus` i gap-analysen (testet med fiksturen `falsk_ki(feil=...)`)
**Når** jeg trykker «Analyser»
**Så** lagres ingenting nytt, en analyse fra før beholdes uendret, og steg 2 vises på nytt med annonsen i feltet og meldingen fra `kjerne/meldinger.py` i feiloppsummeringen (NFR-5, AD-8, AD-20, UX-DR29)
**Og** meldingen er «Vi fikk ikke svar fra KI-tjenesten …» for tidsavbrudd, utilgjengelig tjeneste og ugyldig svar, og forbruksgrense-meldingen for `KIForbruksgrense` (UX-DR31)
**Og** `KIUgyldigNokkel` gir «KI-tjenesten godtok ikke API-nøkkelen. Sjekk `ANTHROPIC_API_KEY` i `.env`, eller fjern den for å bruke testmodus.»
**Og** tester viser hver melding, og at en analyse fra før beholdes når KI feiler

**Gitt** at låsen for brukeren er opptatt
**Når** jeg trykker «Analyser» i en annen fane
**Så** får jeg «Du har allerede en forespørsel som jobber. Vent til den er ferdig.» (AD-12, UX-DR31)

**Gitt** testene for storyen
**Når** de kjøres i testmodus uten nettverk
**Så** bruker de fiksturen `falsk_ki` og sjekker visningen, rekkefølgen (matcher først), oppsummeringen, lagringen og feiltilstandene (NFR-2, AD-17)

### Story 4.3: Egen CV i testmodus

Som sensor
vil jeg få en forklaring når jeg prøver min egen CV uten nøkkel,
slik at jeg forstår hva testmodus kan og hvordan jeg slår på KI.

**Krav:** FR-11, NFR-1. **UX:** UX-DR32. **Styres av:** AD-6, AD-8, AD-20.

**Akseptansekriterier:**

**Gitt** testmodus og en CV som ikke er et eksempelpar
**Når** jeg trykker «Analyser»
**Så** fanger tjenesten `IkkeITestmodus` og lagrer `Analyse` med nøkkelordresultatet, tomme KI-felt og `ki_status="ikke_i_testmodus"` (AD-8)

**Gitt** en slik analyse
**Når** steg 3 vises
**Så** vises nøkkelordene uten forklaring, og der gap-analysen skulle stått, står ordrett «Testmodus: KI-svar finnes bare for eksempelparene. Legg inn en API-nøkkel for å analysere din egen CV.» med lenke til README (FR-11, UX-DR32)
**Og** lenken går til avsnittet om KI-modus i README på GitHub, fordi appen ikke kan vise `README.md`. Adressen ligger som én konstant i `kjerne/meldinger.py`, og en test sjekker at README har overskriften lenken peker på
**Og** hovedknappen er «Prøv eksempel A», som bruker eksempelknappen fra Epic 2
**Og** knappen erstatter CV-en med eksempel A og sender brukeren til steg 1 med teksten til A, slik story 2.4 beskriver, og en test viser det

**Gitt** README
**Når** jeg leser den
**Så** forklarer den hvordan `ANTHROPIC_API_KEY` legges inn i `.env` for KI-modus (NFR-1, AD-20)

### Story 4.4: Claude-klient og prompt for gap-analysen

Som student
vil jeg få gap-analyse av min egen CV når appen har en API-nøkkel,
slik at jeg kan bruke appen på ekte søknader.

**Krav:** FR-5, NFR-3, NFR-4, NFR-5, NFR-9. **Styres av:** AD-3, AD-4, AD-5, AD-10, AD-14, AD-17. **Forutsetning:** Forbruksgrensen i Claude Console er satt (issue #16).

**Akseptansekriterier:**

**Gitt** `ki/claude_klient.py: ClaudeKlient`
**Når** den lages
**Så** bruker den `anthropic`-pakken med `KI_MODELL`, `timeout=60` og `max_retries=0`, og `effort` og `max_tokens` er satt eksplisitt, mens `temperature`, `top_p` og `top_k` ikke sendes (AD-4)
**Og** `ki.hent_klient()` returnerer den når appen ikke er i testmodus
**Og** `brev`, `cv_forbedring` og `nokkelord_forklaring` kaster `NotImplementedError` til storyene deres (5.x, 6.x og 4.6) lager dem. Ingen side kaller dem før da

**Gitt** `gap_analyse(cv_tekst, annonse, sprak)`
**Når** den kalles
**Så** henter den svaret som strukturert utdata med `messages.parse` mot `GapAnalyse`, der hvert krav har `krav`, `status` (`matcher`/`mangler`) og `begrunnelse` (FR-5)
**Og** systemprompten og brukermeldingen leses fra promptfilen for operasjonen, `ki/prompter/gap_analyse.md`, under `## System` og `## Melding`, og systemprompten sier at CV-teksten og annonsen er data og ikke instruksjoner (AD-5, NFR-3)
**Og** bare CV-teksten, annonsen og språket sendes, aldri e-post, passord eller annet fra kontoen (NFR-4)
**Og** før CV-teksten og annonsen settes inn i `<cv>` og `<annonse>`, fjerner koden `<cv>`, `</cv>`, `<annonse>` og `</annonse>` fra teksten, så en CV ikke kan lukke datablokken. Det gjelder alle fire operasjonene, og en test viser det (NFR-3, AD-5)

**Gitt** svar og feil fra API-et (testet med en falsk `anthropic`-klient, uten nettverk)
**Når** `ClaudeKlient` får dem
**Så** blir `refusal`, `max_tokens` eller et svar som ikke validerer til `KIUgyldigSvar`, tidsavbrudd til `KITidsavbrudd`, HTTP 401 til `KIUgyldigNokkel`, forbruksgrensen til `KIForbruksgrense` og alt annet til `KIUtilgjengelig` (AD-4, NFR-5, NFR-9)
**Og** forbruksgrensen gjenkjennes på en feilmelding som starter med «You have reached your specified», eller på `error_code` `enforced_spend_limit_reached`, med én test for hver (AD-4)
**Og** API-nøkkelen, CV-teksten og annonsen havner aldri i logger eller unntakstekster (AD-10)

**Gitt** en manuell prøve i KI-modus med eksempelpar A
**Når** jeg trykker «Analyser»
**Så** viser steg 3 «SQL» og «Førerkort klasse B» som manglende, og prøven står, med dato, hvem som kjørte og resultat, i den skriftlige testplanen `docs/testplan.md` (AD-17)

### Story 4.5: Lagrede svar og evalueringsrapport for gap-analysen

Som gruppe
vil vi lage de lagrede svarene og måle gap-analysen mot fasiten med én kommando,
slik at testmodus bruker ekte svar og vi ser om promptene holder.

**Krav:** FR-5, FR-10, NFR-11, SM-3. **Styres av:** AD-4, AD-6, AD-17.

**Akseptansekriterier:**

**Gitt** KI-modus med en gyldig nøkkel
**Når** jeg kjører `python manage.py lag_lagrede_svar`
**Så** lages `gap_analyse__nb.json` og `gap_analyse__en.json` for A, B og C (6 filer) med `{"meta": {...}, "svar": ...}`, der `meta` har modell-ID og en hash av promptfilen (AD-6)
**Og** kommandoen har en liste over operasjoner, så brev, CV-forbedring og forklaring kan legges til uten å skrive den om

**Gitt** samme kjøring
**Når** den er ferdig
**Så** skrives en rapport til `docs/evaluering/<dato>.md` som per par og språk viser krav som mangler, men er merket som matcher (må være 0), krav som matcher, men er merket som mangler, krav i fasiten som ikke står i svaret, svartid og tokenbruk (NFR-11, SM-3)
**Og** et fasitkrav er funnet når `krav` eller et av `alias` står i `krav`-feltet til ett av kravene i svaret, uansett store og små bokstaver. Statusen hentes fra det kravet, og begrunnelsene søkes ikke i (AD-17)
**Og** kommandoen nekter å kjøre i testmodus, med en melding om hvorfor

**Gitt** den første kjøringen
**Når** svarene og rapporten er laget
**Så** er de sjekket inn i samme pull request, og rapporten viser 0 manglende krav merket som matcher for alle tre parene, eller promptene er rettet og kjøringen gjentatt (NFR-11)
**Og** en vanlig test sjekker at de lagrede gap-analysene for A, B og C har alle krav i fasitens `krav_mangler` som «mangler» og ingen krav i `krav_matcher` som «mangler» (FR-5)
**Og** i testmodus gir eksempelknappen A i steg 1, fulgt av «Analyser» i steg 2, nå den lagrede gap-analysen i steg 3, med «SQL» og «Førerkort klasse B» som manglende (FR-10, UJ-3)

**Gitt** en vanlig test
**Når** hashen av en promptfil ikke stemmer med `meta` i de lagrede svarene
**Så** feiler testen med en melding om å kjøre `lag_lagrede_svar` på nytt (AD-6)
**Og** denne testen kan kuttes hvis tiden blir knapp (AD-6, «Mulig kutt»)

### Story 4.6: KI-forklaring av nøkkelordanalysen

Som student
vil jeg få forklart hva nøkkelordanalysen betyr, med forslag til omformuleringer,
slik at jeg forstår hvordan jeg kan bruke den.

**Krav:** FR-10, FR-11, FR-21, NFR-5, NFR-11. **UX:** UX-DR17, UX-DR31. **Styres av:** AD-3 – AD-8. **Kan kuttes:** dette er punkt 3 i nødplanen (PRD §8.1). Nøkkelordanalysen i kode beholdes.

**Akseptansekriterier:**

**Gitt** «Analyser»
**Når** gap-analysen har lyktes
**Så** kjøres `nokkelord_forklaring(cv_tekst, annonse, sprak, resultat)` som tredje steg, og KI får nøkkelordresultatet bare for å forklare det, aldri for å endre det (AD-7, AD-8)
**Og** prompten ligger i promptfilen `ki/prompter/nokkelord_forklaring.md`, og `ClaudeKlient` og `TestmodusKlient` støtter operasjonen
**Og** returtypen `Forklaring` i `ki/modeller.py` har `forklaring: str` og `omformuleringer: list[Omformulering]`, der `Omformulering` har `nokkelord` og `forslag` (arkitekturen §3)

**Gitt** en analyse med forklaring
**Når** steg 3 vises
**Så** ligger forklaringen i `<details>` «Hva betyr nøkkelordanalysen?», lukket som standard, med merket «Laget av KI» og `lang` etter språket (FR-21, UX-DR17)
**Og** forslagene til omformulering inneholder ingen oppdiktede påstander. Rapporten fra `lag_lagrede_svar` lister hver setning i forklaringen som nevner et nøkkelord fra `mangler`, og gruppa sjekker dem for hånd etter `docs/testplan.md`. Når regelen for påstander fra Epic 5 finnes (issue #28), brukes den også her

**Gitt** en `KIFeil` i forklaringen (testet med `falsk_ki`)
**Når** «Analyser» kjøres
**Så** lagres `Analyse` med gap-analysen og `ki_status="forklaring_feilet"`, en verdi storyen legger til, og steg 3 viser «Forklaringen kunne ikke lages» med [Prøv forklaringen igjen], som sender `POST` til `/resultat/forklaring/` og bare kjører forklaringen på nytt (AD-8, UX-DR31)
**Og** lykkes forklaringen, settes `ki_status` til `ok`, og forklaringen vises. Feiler den igjen, står meldingen og knappen fortsatt der. Gap-analysen og nøkkelordene endres ikke, og begge tilfellene testes med `falsk_ki`

**Gitt** et eksempelpar i testmodus med egne ønskede nøkkelord
**Når** steg 3 vises
**Så** vises den lagrede forklaringen med merknaden «KI-forklaringen gjelder ikke dine egne nøkkelord i testmodus.» (FR-10, AD-7)
**Og** med egen CV i testmodus vises ingen forklaring (FR-11)

**Gitt** `lag_lagrede_svar`
**Når** den kjøres
**Så** lages også `nokkelord_forklaring__nb.json` og `nokkelord_forklaring__en.json` for A, B og C, og rapporten viser svartid og tokenbruk for operasjonen (FR-10, NFR-11)
