# Gjennomgang av spine-paret — G48

_Rubrikk-gjennomgang av `DESIGN.md` og `EXPERIENCE.md` (status draft, 2026-11-12), laget av en KI-reviewer (Claude Code). Kilder: `prd/prd.md`, `prd/addendum.md`, `prd/tilbakemelding-prd.md`, `product-brief.md`, arkitekturen (`ARCHITECTURE-SPINE.md` fra PR #13, lest fra en lokal kopi) og `.memlog.md`. Spørsmålet er om de som bygger videre (arkitektur og stories, mennesker eller KI) kan hente ut det de trenger direkte, om alle henvisninger løser seg, og om alle beslutninger som noe annet bygger på, er tatt. Dokumentene er ikke endret._

## Samlet vurdering

**Middels god (adequate). Kan brukes etter en runde med rettinger.** Paret er ryddig, kildebundet og ærlig om hva som er antakelser. Alle fire brukerreisene har et klimaks, alle FR-er unntatt to rene backend-krav har et sted i grensesnittet, og kontrasttabellen stemmer når den regnes ut på nytt. Svakhetene ligger i skjøtene:

1. **Fremdriftslinjen** er beskrevet ulikt i de to filene (streker på 4 px mot klikkbare steg i en `<ol>`).
2. **«Start ny søknad»** kolliderer med advarselen om at analysen slettes, og med fremdriftslinjen.
3. **Tre konflikter med arkitekturen mangler i «Avvik»:** hvor tone og svarform lagres mellom steg 3 og 5 (AD-8), ønskede nøkkelord i testmodus (AD-7) og når en endret annonse sletter analysen (AD-8).
4. **Mange komponenter i EXPERIENCE.md har ikke noe visuelt motstykke** i DESIGN.md.
5. **Mockupene av nøkkelskjermene** er ikke lenket fra noen av filene.

Ingen funn er kritiske. Fem er høye.

| Kategori | Vurdering |
|---|---|
| 1. Flytdekning | adequate |
| 2. Tokens | adequate |
| 3. Komponentdekning | thin |
| 4. Tilstander | adequate |
| 5. Visuelle referanser | thin |
| 6. Oppblåsing | strong |
| 7. Arvedisiplin | adequate |
| 8. Form | adequate |

## 1. Flytdekning — adequate

UJ-1 – UJ-4 fra PRD §2.3 finnes alle under Key Flows, med samme navn og nummer, nummererte steg og et markert klimaks. UJ-1 har en feilvei.

**FR-dekning:** FR-1 – FR-13 og FR-16 – FR-23 har et sted i IA-tabellen eller i Component Patterns. FR-11 står under State Patterns og Testmodus. FR-8 dekkes indirekte (varselet i steg 5 og UJ-1 steg 6). FR-14 og FR-15 har ikke noe sted i grensesnittet.

**NFR-dekning:** NFR-3 (filsjekk), NFR-4, NFR-5, NFR-6, NFR-7, NFR-8 og NFR-9 er dekket. NFR-1 er dekket gjennom README-lenken i FR-11-meldingen. NFR-2 og NFR-10 er ikke relevante for UX.

### Funn
- **[høy]** UJ-2 og «Start ny søknad» stemmer ikke med «Endring som sletter analysen» (EXPERIENCE.md: Component Patterns «Start ny søknad», State Patterns «Endring som sletter analysen», UJ-2 steg 1–2). «Start ny søknad» beholder den gamle analysen (AD-8). Jonas har brukt appen før, så når han limer inn en ny annonse i steg 2, skal han etter State Patterns få advarselen «Hvis du endrer CV-en eller annonsen … Brevet og forslagene forsvinner». Flyten viser ikke dette. I tillegg viser fremdriftslinjen steg 4–6 som fullførte lenker til den *gamle* analysen mens han er i steg 1–3. *Retting:* Bestem hva «Start ny søknad» gjør med den gamle analysen. Ett alternativ er at advarselen kommer én gang ved «Start ny søknad», og at steg 4–6 da låses. Oppdater UJ-2 og fremdriftsregelen i samsvar med det.
- **[middels]** UJ-2, UJ-3 og UJ-4 har ingen feilvei (Key Flows). Det er enklest å skrive den for UJ-2 (KI-feil ved «Lag søknad» eller «Vis forslag til CV-en», der tilstanden finnes, men ikke er knyttet til en reise) og for UJ-4 («Avbryt» på bekreftelsessiden). *Retting:* Legg til én «Avvik:»-linje per reise.
- **[middels]** Egen CV i testmodus: det er uklart hvilken hovedknapp steg 4 har (State Patterns «Egen CV i testmodus», UJ-3 steg 5). Tilstanden sier «Steg 4, 5 og 6», men også at «steg 5 og 6 kan da ikke fullføres». Skal «Lag søknad» vises, være deaktivert eller byttes ut med «Prøv eksempel A»? *Retting:* Si hva hovedknappen i steg 4 er når `ki_status="ikke_i_testmodus"`, og fjern steg 5 og 6 fra «Hvor» hvis de ikke kan nås.
- **[lav]** UJ-3 og UJ-4 mangler scenelinjen som UJ-1 og UJ-2 har (hvem, når, hvilken enhet). UJ-3 fortsetter også etter klimakset (steg 5). *Retting:* Legg til en kursiv scenelinje, og flytt FR-11-delen til en egen «Deretter:»- eller «Avvik:»-linje.
- **[lav]** FR-14 og FR-15 har ikke noe sted i grensesnittet, og det står ikke at det er med vilje. FR-8 står ikke i IA-tabellen. *Retting:* Skriv én setning om at FR-14 og FR-15 er usynlige i grensesnittet (det finnes ingen ID-er i URL-ene, jf. AD-10), og legg FR-8 til i Krav-kolonnen for steg 5.
- **[lav]** UJ-1 steg 5 sier at Emma «åpner ‹Hva betyr dette?› og ser at ‹SQL› også mangler blant nøkkelordene». Nøkkelordbrikkene står utenfor `<details>` og synes allerede. *Retting:* Skriv om setningen, så det er forklaringen hun åpner.

## 2. Tokens — adequate

Alle `{path.to.token}`-henvisninger i frontmatter og prosa løser seg (colors, rounded, spacing). Alle 17 fargetokener har en `-dark`-variant. Kontrasttabellen er regnet ut på nytt med WCAG-formelen, og alle tallene stemmer når de avrundes til én desimal (for eksempel 14,70 / 14,98, 5,12 / 8,76, 4,73 / 6,52, 4,90 / 6,52, 3,26 / 3,38 og 6,54 / 10,59). Merknaden om at aksent på infoflate gir 4,4:1 stemmer også (4,42).

### Funn
- **[middels]** Komponenter som er beskrevet i prosaen, mangler tokens i `components`: Topplinje, Nøkkelordmåler (8 px, mens `progress-bar` er 4 px), Brev (kort med `letter`-typografi og varsellinje), merkene «Matcher»/«Mangler» (tag-pillen), en deaktivert knapp som viser «Jobber …», et varsel eller en feilboks for KI-feil og feiloppsummeringen, og radioknapp/avkrysning. *Retting:* Legg til `top-bar`, `keyword-meter`, `letter-card`, `tag-match`/`tag-missing`, `button-busy`, `alert` og `checkbox-radio`, med tokenhenvisninger.
- **[middels]** «Les mer»-lenken i personvernpåminnelsen bryter DESIGN.md sin egen regel (Colors: «Infoflate … Teksten på infoflaten har alltid fargen `{colors.text}`»). Personvernpåminnelsen bruker infoflaten (DESIGN.md Colors) og har en lenke (EXPERIENCE.md Component Patterns). En lenke i aksentfarge på `info-bg` gir 4,42:1. *Retting:* Skriv en regel om at lenker på infoflaten har tekstfarge og understrek.
- **[lav]** `typography` har ingen `fontFamily`. Skriftstakken står bare i en YAML-kommentar, så den forsvinner når tokenene hentes ut maskinelt. *Retting:* Legg til `fontFamily` på rollene (eller et felles `body.fontFamily`).
- **[lav]** `button-danger` mangler `minHeight: 44px`, selv om alle trykkflater skal være minst 44 px (EXPERIENCE.md Interaction Primitives). *Retting:* Legg den til.
- **[lav]** Kontrasttabellen mangler to par som noe bygger på: aksent som lenketekst på kort (4,81 lys / 7,60 mørk, består) og det aktive steget i fremdriftslinjen. Aktivt steg (aksent med 50 % gjennomsiktighet) har 2,09:1 mot bakgrunnen og 1,60:1 mot kommende steg i lys modus, så forskjellen synes ikke godt. *Retting:* Ta med begge parene, og si at det aktive steget vises med teksten «Steg N av 6» (eller gi det full aksent med en annen form).

## 3. Komponentdekning — thin

**I DESIGN.md Components (14):** Topplinje, Testmodus-banner, Fremdriftslinje, Hovedknapp, Sekundærknapp, Fareknapp, Kort, Kravrad, Nøkkelord-brikke, Nøkkelordmåler, Skjemafelt, Fokusring, Ferdig-merke, Brev.

**I EXPERIENCE.md Component Patterns (19):** Fremdriftslinje, Tilbake / Neste, CV-opplasting, Bekreft lagret CV, Eksempelknapper, Annonsefelt, Valg, Personvernpåminnelse, Kravliste, Nøkkelordanalyse, Brevvisning, Lag nytt brev, Ferdig-merke, Kopier, PDF-avsender, Last ned Markdown, CV-forbedringer, Start ny søknad, Slett-bekreftelse.

Bare **Fremdriftslinje** og **Ferdig-merke** har samme navn i begge filene.

### Funn
- **[høy]** Fremdriftslinjen beskrives ulikt i de to filene. I DESIGN.md (Components) er den «Seks streker på 4 px … Under strekene står ‹Steg 4 av 6 · Analyse›». I EXPERIENCE.md (Component Patterns og Accessibility Floor) er fullførte steg lenker, linjen er en `<ol>` med `aria-current="step"`, og alle trykkflater skal være minst 44 × 44 px. En strek på 4 px uten tekst kan ikke være en lenke på 44 px, og det er ingen steder beskrevet hvordan stegnavnene ser ut. *Retting:* Beskriv i DESIGN.md hvordan klikkbare steg ser ut (for eksempel en `<ol>` med korte stegnavn eller tall over strekene, der hele cellen er trykkflaten), og lag en mockup av det.
- **[middels]** Navnene er ulike i de to filene, og det finnes ingen oversikt som kobler dem: Kravrad ↔ Kravliste, Brev ↔ Brevvisning, Hovedknapp/Sekundærknapp ↔ Tilbake / Neste. Nøklene i frontmatter er på engelsk (`requirement-match`, `keyword-chip`, `test-mode-banner`, `done-mark`), mens navnene i teksten er på norsk. *Retting:* Bruk samme navn i begge filene, og legg til en kolonne eller parentes med frontmatter-nøkkelen (for eksempel «Kravrad (`requirement-match` / `requirement-missing`)»).
- **[middels]** Disse komponentene i EXPERIENCE.md har ikke noe visuelt motstykke i DESIGN.md: CV-opplasting (filfelt), Bekreft lagret CV, Eksempelknapper, Annonsefelt med teller, Valg (`fieldset` med radioknapper og forklaring), Personvernpåminnelse, Lag nytt brev, Kopier med «Kopiert!», PDF-avsender, Last ned Markdown, CV-forbedringer (listen), Start ny søknad og Slett-bekreftelse. Det gjelder også det visuelle for tilstandene: venteknapp med indikator, KI-feilmelding, feiloppsummering og bekreftelsesmeldinger («Dokumentene dine er slettet»). *Retting:* Legg til korte linjer i DESIGN.md Components. Mange kan vise til en grunnkomponent, for eksempel «Eksempelknapper = Sekundærknapp i rad».
- **[middels]** Steg 6 har fem handlinger (Kopier, Last ned PDF, Last ned Markdown, Vis forslag til CV-en, Start ny søknad), og regelen er «Én hovedknapp per steg» (DESIGN.md Components og Do's and Don'ts, EXPERIENCE.md Tilbake / Neste). Det står ikke hvilken som er hovedknappen. *Retting:* Bestem hovedknappen (sannsynligvis «Kopier teksten») og hvordan de andre ser ut. Gjør det samme for steg 1 med lagret CV («Bruk denne», «Last opp ny» og «Neste»).
- **[lav]** Fareknappen er beskrevet på to måter i DESIGN.md. Colors sier at fare brukes på «‹Slett mine dokumenter› og ‹Slett konto›», mens Components sier «Fareknapp … brukes bare i bekreftelsen av sletting». Det er uklart om knappene på Min konto er røde. *Retting:* Velg én regel, for eksempel sekundærknapp på Min konto og fareknapp på bekreftelsessiden.
- **[lav]** Topplinje, Testmodus-banner, Kort, Skjemafelt og Fokusring står bare i DESIGN.md. Oppførselen deres står spredt i EXPERIENCE.md (i IA, Testmodus og Accessibility Floor), men ikke i Component Patterns. *Retting:* Legg til korte rader med henvisning til der oppførselen står.

## 4. Tilstander — adequate

Venting, KI-feil, forbruksgrense, at en forespørsel allerede kjører, at forklaringen feilet, egen CV i testmodus, filfeil, PDF uten tekst, feil lengde på annonsen, låste steg, innloggingsfeil, sletting utført og «Kopiert!» er dekket. Tilstanden «ingen tilgang» er ikke relevant, fordi URL-ene ikke har ID-er (AD-10), men det står ikke i dokumentet.

### Funn
- **[middels]** Det står ikke hva som skjer når brukeren ikke er innlogget eller økten har gått ut (FR-13: «Sider med brukerdata kan ikke åpnes uten å være innlogget»). Det står heller ikke hvor brukeren havner etter utlogging. *Retting:* Legg til en rad: brukeren sendes til Logg inn med en kort melding og kommer tilbake til steget etterpå. Etter utlogging havner hun på Logg inn.
- **[middels]** Siden for dekrypteringsfeil (AD-9 [Forslag]: «sender brukeren til en side som forklarer at dokumentene ikke kan leses, og tilbyr å slette dem») finnes ikke i UX. *Retting:* Legg den til i State Patterns, med tekst og en knapp til Slett-bekreftelse.
- **[middels]** Valideringstilstander mangler for grenser som arkitekturen allerede har: CV-tekst over 30 000 tegn (AD-15 `CV_TEKST_MAKS`) i steg 1, mer enn 20 ønskede nøkkelord (AD-15 `ONSKEDE_NOKKELORD_MAKS`) i steg 3, og personvernavkrysningen som ikke er krysset av ved registrering. *Retting:* Legg til én rad per grense, med meldingsteksten.
- **[middels]** «Fungerer uten JavaScript» (Interaction Primitives) holder ikke for FR-22. Kopieringsknappen trenger JS, og det står ikke hva som skjer uten. *Retting:* Si at knappen bare vises når JS er på (eller at den markerer teksten), og at brevet ellers kan markeres og kopieres manuelt.
- **[middels]** Annonsetelleren «blir oransje» ved feil lengde (State Patterns «Annonsen er for kort eller for lang»). DESIGN.md sier at mangler-fargen brukes «bare på krav og nøkkelord», og at fare-fargen brukes på «feilmeldinger i skjemaer». *Retting:* Bruk `{colors.danger}` (eller tekstfarge pluss melding) på telleren.
- **[lav]** Mangler: Min konto uten dokumenter (tom tilstand), steg 2 når brukeren kommer tilbake (er annonsen fylt ut?), og venting under opplasting og innlesing av PDF. *Retting:* Legg til korte rader, eller si at de ikke trengs.
- **[lav]** Plasseringen av KI-feil er beskrevet ulikt. State Patterns sier «En melding over knappen», mens Accessibility Floor sier at feil «nevnes i en oppsummering øverst i skjemaet». AD-20 bruker `form.add_error(None, …)` (feil som gjelder hele skjemaet). *Retting:* Velg én plassering for slike feil.

## 5. Visuelle referanser — thin

`.working/` har seks filer: `directions-1.html`, `directions-2.html`, `key-steg1-testmodus.html`, `key-steg3-valg.html`, `key-steg4-analyse.html` og `key-steg5-6.html`. `imports/` er tom, og `mockups/` og `wireframes/` finnes ikke. DESIGN.md lenker bare til `directions-1/2`. EXPERIENCE.md lenker ikke til noen mockup. At spinene går foran ved konflikt, står én gang (DESIGN.md Components, siste avsnitt), og det gjentas i hodet på hver `key-*`-fil. Det er bra.

### Funn
- **[middels]** De fire `key-*.html`-mockupene er ikke lenket fra noen av filene. EXPERIENCE.md Åpne punkter sier fortsatt at «Mockups av nøkkelskjermene er ikke laget ennå», og DESIGN.md peker bare på steg 4 i `directions-2.html`. *Retting:* Lenk hver mockup der den hører hjemme (Component Patterns og Key Flows), oppdater setningen i DESIGN.md Components, og fjern punktet i Åpne punkter.
- **[lav]** Mockupen av steg 3 kaller valget «Språk i brevet», men språket gjelder all KI-tekst, også gap-analysen (FR-5, EXPERIENCE.md Foundation, UJ-2 steg 4). Mockupen har også en annen rekkefølge (svarform først) enn EXPERIENCE.md Valg (språk, tone, svarform). *Retting:* Endre etiketten i mockupen og skriv rekkefølgen inn i spinen. Begrunnelsen i mockupen (at faglærer ba om at svarformen skulle synes) bør stå i spinen.
- **[lav]** Mockupen av steg 6 viser ikke varselet «KI kan gjøre feil», selv om DESIGN.md Brev og EXPERIENCE.md Brevvisning sier at varselet står over brevet i steg 5 *og* 6. *Retting:* Bestem om varselet skal stå i steg 6, og rett enten spinen eller mockupen.
- **[lav]** `imports/` er tom. *Retting:* Slett mappen, eller skriv at den er tom med vilje.

## 6. Oppblåsing og overspesifisering — strong

Lengden er riktig for en app med seks steg og tre andre sider. Detaljene (for eksempel 3 sekunder for «Kopiert!» og `ki_status`) er de som stories trenger.

### Funn
- **[lav]** Seksjonene Testmodus og Personvern i grensesnittet gjentar deler av Component Patterns og State Patterns (FR-11-meldingen og personvernpåminnelsen står to steder). *Retting:* La seksjonene vise til radene i stedet for å gjenta tekst, så teksten bare må endres ett sted.
- **[lav]** I DESIGN.md Brand & Style beskriver tre setninger historikken bak designretningene. Det hører hjemme i `.memlog.md`. *Retting:* Kort ned til retningsnavnet og lenken.

## 7. Arvedisiplin — adequate

UJ-ID-ene, FR-ID-ene og personene er hentet ordrett fra PRD-en. Arkitekturbeslutningene (AD-8, AD-12, AD-15) er sitert riktig. «Avvik fra PRD og arkitektur» fanger de største avvikene, men ikke alle.

### Funn
- **[høy]** Hvor tone og svarform lagres mellom steg 3 og steg 5, er ikke ført opp i «Avvik» (EXPERIENCE.md Valg og Lag nytt brev, mot AD-8: «Tone og svarform finnes bare på `Brev`»). `Analyse` lagrer språk og ønskede nøkkelord, men ikke tone og svarform, og `Brev` finnes ikke før steg 5. `.memlog.md` har dette som «NOTE FOR ARKITEKTUR», men det har ikke kommet med i EXPERIENCE.md. *Retting:* Legg det til som punkt 5 under Arkitektur, for eksempel «tone og svarform lagres på `Analyse` som standard for første `Brev`».
- **[høy]** Ønskede nøkkelord i testmodus står som [ÅPENT] med to alternativer (Testmodus-seksjonen), men arkitekturen har allerede et tredje forslag (AD-7 [Forslag]: «Den lagrede forklaringen vises, men med teksten ‹KI-forklaringen gjelder ikke dine egne nøkkelord i testmodus›»). Konflikten er ikke nevnt. *Retting:* Ta med AD-7-alternativet. Velg ett, eller før punktet opp under «Avvik».
- **[høy]** En endret annonse sletter analysen på et annet tidspunkt i UX enn i arkitekturen (State Patterns «Endring som sletter analysen», Component Patterns «Fremdriftslinje»). I UX slettes analysen når CV-en *eller annonsen* endres. I AD-8 er det bare `lagre_cv_tekst` som sletter `Analyse` med en gang. En ny annonse erstatter analysen først når «Analyser» kjøres. «Avvik» Arkitektur 4 nevner bare CV-en. *Retting:* Bestem regelen for annonsen, og utvid punkt 4 til å gjelde den.
- **[middels]** «Avvik» Arkitektur 1 foreslår å lagre annonsen i Django-sesjonen (kryptert). AD-10 sier at dokumentinnhold «legges aldri i økten», uansett om det er kryptert. *Retting:* Vis til AD-10 i punktet, og vurder heller å lagre annonsen i en utkastrad (for eksempel en `Analyse` uten KI-felt) eller å sende steg 2 og 3 som ett skjema.
- **[middels]** Ordene i grensesnittet er ikke koblet til ordlisten i PRD §3: «Valg» (steg) ↔ **Innstillinger**, «CV-forbedringer» ↔ **CV-forbedringsforslag**, «Nøkkelordanalyse» ↔ **ATS-nøkkelordanalyse**, «Søknad» (steg 5) ↔ **Søknadsbrev**/**Brevforslag**, «Forslagene»/«punktliste» ↔ **Brevforslag**, «Annonse» ↔ **Stillingsannonse**. Det er greit at mikroteksten er kortere, men stories må vite hva som er det samme. *Retting:* Lag en liten tabell som kobler «Ord i grensesnittet» til «Ord i PRD §3», og bruk PRD-ordene i komponentnavn og Krav-kolonner.
- **[middels]** Lenken ved personvernavkrysningen («lenke til en kort forklaring», Personvern i grensesnittet) mangler en side. Min konto krever innlogging, så en besøkende kan ikke åpne den, og IA har ingen offentlig side for dette. Dette er ikke med i «Avvik». *Retting:* Legg til en offentlig side «Slik behandler vi dataene» i IA (og i arkitekturens URL-liste), eller vis teksten på selve registreringssiden.
- **[lav]** Bekreftelsessiden for sletting er en egen side, men arkitekturen har bare `POST /min-konto/slett-dokumenter/` og `/min-konto/slett-konto/` (§3 URL-er). Det trengs to nye GET-sider. *Retting:* Legg det til under «Avvik» Arkitektur.
- **[lav]** IA viser til «Forsiden for besøkende», men den siden er ikke definert, og det står ikke hva topplinjen viser før innlogging. *Retting:* Si at forsiden er Logg inn (eller definer siden).
- **[lav]** (Bare merknad, ikke et brudd.) Kilden `../../architecture/…/ARCHITECTURE-SPINE.md` i frontmatter løser seg først når PR #13 er flettet.

## 8. Form — adequate

Seksjonene i DESIGN.md står i riktig rekkefølge (Brand & Style → Do's and Don'ts). EXPERIENCE.md har alle de påkrevde seksjonene (Foundation, IA, Voice and Tone, Component Patterns, State Patterns, Interaction Primitives, Accessibility Floor, Responsive & Platform, Inspiration & Anti-patterns og Key Flows).

### Funn
- **[lav]** I EXPERIENCE.md står Inspiration & Anti-patterns etter Key Flows. I mønstereksemplene står den før. *Retting:* Flytt den rett etter Responsive & Platform.
- **[lav]** Fire egne seksjoner er lagt til: Testmodus, Personvern i grensesnittet, Avvik fra PRD og arkitektur, og Åpne punkter. Avvik og Åpne punkter har en tydelig funksjon. Testmodus og Personvern har det også (FR-9 – FR-11 og NFR-4 er sentrale for sensor), men de bør vise til andre seksjoner i stedet for å gjenta dem (se 6). *Retting:* Ingen, utover det som står under 6.

## Mekaniske merknader

- **Tokenhenvisninger:** 21 ulike `{…}`-henvisninger, og alle løser seg. Det finnes 17 fargetokener, og alle har en `-dark`-variant.
- **Kontrast (regnet ut på nytt):** Tallene i tabellen stemmer. Nye tall: aksent på kort 4,81 / 7,60, mangler-tekst på kort 5,23 / 7,69, fare-tekst på kort 6,13 / 9,45 og aktivt steg (50 % aksent) mot bakgrunn 2,09 / 3,03.
- **Personvernavkrysningen** har litt ulik ordlyd i `.memlog.md` («jeg har lest hvordan dataene behandles») og EXPERIENCE.md («Jeg har lest hvordan appen behandler CV-en min»). Spinen gjelder, men loggen og spinen bør stemme overens.
- **Antall i Åpne punkter:** «[ANTAKELSE]-punkter» lister seks punkter. Det mangler «ordlyden ved forbruksgrensen» (State Patterns), som også er merket [ANTAKELSE].
- **Frontmatter:** DESIGN.md har `description`, men EXPERIENCE.md har det ikke. Det er greit, men det er ulikt.
- **Kilder:** EXPERIENCE.md har `product-brief.md` og `tilbakemelding-prd.md` som kilder, men DESIGN.md har det ikke. Det er greit, fordi DESIGN.md ikke bruker dem.
