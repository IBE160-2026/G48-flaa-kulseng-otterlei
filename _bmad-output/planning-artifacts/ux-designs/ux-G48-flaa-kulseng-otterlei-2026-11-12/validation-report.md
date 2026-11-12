# Valideringsrapport — G48 UX

- **DESIGN.md:** `_bmad-output/planning-artifacts/ux-designs/ux-G48-flaa-kulseng-otterlei-2026-11-12/DESIGN.md`
- **EXPERIENCE.md:** `_bmad-output/planning-artifacts/ux-designs/ux-G48-flaa-kulseng-otterlei-2026-11-12/EXPERIENCE.md`
- **Kjørt:** 2026-11-12

## Samlet vurdering

**Tilstrekkelig. Kan brukes etter en runde med rettinger.** Paret er ryddig, kildebundet og ærlig om hva som er antakelser. Alle fire brukerreisene har et klimaks, alle FR-er unntatt to rene backend-krav har et sted i grensesnittet, og kontrasttabellen stemmer når den regnes ut på nytt. Svakhetene ligger i skjøtene: fremdriftslinjen er beskrevet ulikt i de to filene, «Start ny søknad» kolliderer med slettevarselet og fremdriftslinjen, tre konflikter med arkitekturen mangler i «Avvik» (tone og svarform mellom steg 3 og 5, ønskede nøkkelord i testmodus, og når en endret annonse sletter analysen), mange komponenter i EXPERIENCE.md mangler et visuelt motstykke i DESIGN.md, og mockupene av nøkkelskjermene er ikke lenket.

Tilgjengelighets- og motstandergjennomgangen flytter bildet. Motstanderen løfter «Start ny søknad» til kritisk: veiviseren utleder fremdriften av hvilke rader som finnes, og den modellen passer ikke med AD-8 og AD-10. Det rammer særlig tilbakevendende brukere (UJ-2). Seks steg gir åtte til ni handlinger der PRD-en ga omtrent fire, og «Ser bra ut» lagrer ingenting. **Hovedrisikoen er derfor veiviserens tilstandsmodell og antall steg**, ikke enkeltkomponenter. Tilgjengelighetsgjennomgangen finner at fargene holder, men at **skjermleseroppførselen ved sidelast** ikke er beskrevet: med vanlige POST-er (AD-12, AD-20) blir ventestatus og feil i `aria-live` vanligvis ikke lest opp, og fokus til `h1` skjuler at noe gikk galt. Etter sammenslåing av dubletter er det 1 kritisk, 13 høye, 28 middels og 30 lave funn.

## Vurdering per kategori

- 1. Flytdekning — tilstrekkelig
- 2. Tokens — tilstrekkelig
- 3. Komponentdekning — tynn
- 4. Tilstander — tilstrekkelig
- 5. Visuelle referanser — tynn
- 6. Oppblåsing og overspesifisering — sterk
- 7. Arvedisiplin — tilstrekkelig
- 8. Form — tilstrekkelig

## Funn etter alvorlighetsgrad

Dubletter er slått sammen. Der flere gjennomganger fant det samme, står alle i hakeparentesen, og funnet har fått den høyeste alvorlighetsgraden som ble gitt.

### Kritisk (1)

**[Motstander + Rubrikk · 1. Flytdekning]** — «Start ny søknad» gir en tilstand som fremdriftslinjen og sletteregelen ikke kan vise (§ EXPERIENCE.md: Component Patterns «Start ny søknad», «Fremdriftslinje»; State Patterns «Endring som sletter analysen», «Låste steg»; UJ-2 steg 1–2)  
Den gamle `Analyse` og `Brev` finnes fortsatt etter «Start ny søknad» (AD-8). Steg 4–6 vises da som fullførte lenker til forrige jobb, og enhver ny annonse utløser slettevarselet. Den vanlige veien for en tilbakevendende bruker (UJ-2) går derfor gjennom en advarsel om sletting, og etter innlogging havner Jonas i steg 6 for forrige søknad. Rubrikken satte dette til høy, motstanderen til kritisk.  
Retting: Definer «en søknad i arbeid» i stedet for å utlede fremdriften av radene. Enkleste løsning: «Start ny søknad» sletter `Analyse` etter én bekreftelse. Skriv tilstandsregelen som en tabell (ingen CV → 1, CV uten analyse → 1–3, analyse → 4, brev → 5/6), oppdater UJ-2 og ta den med i avvikslisten.  
Funnet av: motstander, rubrikk.

### Høy (13)

**[Rubrikk · 3. Komponentdekning + Tilgjengelighet H-1]** — Fremdriftslinjen er beskrevet ulikt, og lenkene har verken navn eller trykkflate (§ DESIGN.md: Components «Fremdriftslinje»; EXPERIENCE.md: Component Patterns, Accessibility Floor)  
DESIGN.md beskriver seks streker på 4 px, EXPERIENCE.md en `<ol>` der fullførte steg er lenker på minst 44 × 44 px. Bare det aktive steget har et navn, så lenkene får ikke noe tilgjengelig navn, og fullført/låst er ikke beskrevet for skjermleser.  
Retting: Beskriv markeringen eksakt i begge filer: `<nav aria-label="Fremdrift"><ol>` med stegnavn som tekst, `<a>` med «(fullført)», `aria-current="step"` og «(ikke tilgjengelig ennå)». Strekene er `aria-hidden`, og hele cellen er trykkflaten. Lag en mockup.  
Funnet av: rubrikk, tilgjengelighet.

**[Rubrikk · 7. Arvedisiplin + Motstander]** — Tone og svarform har ikke noe lagringssted mellom steg 3 og 5 (§ EXPERIENCE.md: Valg, Lag nytt brev; AD-8; .memlog.md linje 16)  
AD-8 sier at tone og svarform bare finnes på `Brev`, som ikke finnes før steg 5. Notatet til arkitekturen i `.memlog.md` kom aldri inn i «Avvik». Uten avklaring løser to utviklere det ulikt.  
Retting: Før det opp som arkitekturavvik nummer 5: `Analyse` får `tone` og `svarform` som startverdier, og `Brev` lagrer det som ble brukt. Alternativt flyttes valgene til steg 5.  
Funnet av: rubrikk, motstander.

**[Rubrikk · 7. Arvedisiplin]** — Ønskede nøkkelord i testmodus overser AD-7 (§ EXPERIENCE.md: Testmodus [ÅPENT]; AD-7)  
UX har to alternativer, men AD-7 [Forslag] har et tredje: den lagrede forklaringen vises med teksten «KI-forklaringen gjelder ikke dine egne nøkkelord i testmodus». Konflikten er ikke nevnt.  
Retting: Ta med AD-7-alternativet. Velg ett, eller før punktet opp under «Avvik».

**[Rubrikk · 7. Arvedisiplin + Motstander]** — Regelen for når endringer sletter analysen avviker fra AD-8 og dekker ikke språk og nøkkelord (§ EXPERIENCE.md: State Patterns «Endring som sletter analysen», Fremdriftslinje; AD-8)  
I UX slettes analysen når CV-en eller annonsen endres, men i AD-8 er det bare `lagre_cv_tekst` som sletter med en gang. «Avvik» punkt 4 nevner bare CV-en. Det står heller ikke hva som skjer når språk eller ønskede nøkkelord endres etter analysen.  
Retting: Endringer i steg 1–3 gjelder først ved nytt «Analyser», med ett varsel der. Unntak: endret CV-tekst sletter analysen med en gang. Utvid avvikspunkt 4.  
Funnet av: rubrikk, motstander.

**[Rubrikk · 7. Arvedisiplin + Motstander]** — Forslaget om å lagre annonsen i økten bryter AD-10 (§ EXPERIENCE.md: Avvik, Arkitektur 1; Eksempelknapper; AD-10)  
AD-10 sier at dokumentinnhold aldri legges i økten, uansett kryptering. `/eksempel/A/` har samme problem. Rubrikken satte dette til middels, motstanderen til høy.  
Retting: Slå sammen steg 2 og 3 til «Annonse og valg», så annonsen følger samme `POST` som analysen. Ellers: send annonsen som skjult felt eller i en utkastrad, og fjern økt-alternativet.  
Funnet av: rubrikk, motstander.

**[Tilgjengelighet H-2]** — Ventestatusen blir ikke lest opp, og fokus kan forsvinne (§ EXPERIENCE.md: Venter på KI, Accessibility Floor; AD-12; WCAG 4.1.3, 2.4.3)  
`aria-live` leses bare hvis området finnes før teksten endres. En knapp med fokus som får `disabled`, mister fokus i flere nettlesere, og verdien sendes ikke med i skjemaet.  
Retting: Tomt `<p role="status">` i malen fra start. `skjema.js` setter `aria-disabled="true"` (ikke `disabled`), stopper dobbel innsending, beholder fokus og skriver «Jobber … Dette tar vanligvis 10–30 sekunder.» i statusområdet.

**[Tilgjengelighet H-3 + Rubrikk · 4. Tilstander]** — Feil etter ny sidelast blir ikke lest opp, og plasseringen av KI-feil er uavklart (§ EXPERIENCE.md: State Patterns «KI svarte ikke», «Feil ved innlogging»; Accessibility Floor; AD-20)  
AD-20 rendrer skjemaet på nytt, så `aria-live` leses vanligvis ikke opp, og fokus går til `h1`. Brukeren hører stegtittelen og vet ikke at noe gikk galt. I tillegg sier State Patterns «over knappen» og Accessibility Floor «oppsummering øverst».  
Retting: Uten feil: fokus til `h1`. Med feil: fokus til én feiloppsummering (`role="alert"`, `tabindex="-1"`) øverst i `<main>`, med lenker til feltene og KI-feil i samme liste. Sidetittelen får «Feil: » foran.  
Funnet av: tilgjengelighet, rubrikk.

**[Tilgjengelighet H-4]** — Lenker skilles fra tekst bare med farge (§ DESIGN.md: Colors «Blågrønn aksent»; WCAG 1.4.1)  
Aksent mot vanlig tekst er 2,87:1 i lys og 1,76:1 i mørk modus, under 3:1. Gjelder «Les mer», README-lenken, lenken ved registrering, «Min konto» og «Logg ut».  
Retting: «Lenker i løpende tekst er alltid understreket. Lenker i topplinjen får understrek ved hover og fokus.»

**[Tilgjengelighet H-5]** — Sidene mangler unik tittel og landemerker (§ EXPERIENCE.md: IA, Accessibility Floor; WCAG 2.4.2, 1.3.1, 2.4.1)  
Det står ingenting om `<title>`, `header`/`nav`/`main` eller «Hopp til innhold». Alle steg bruker samme mal, så titlene blir fort like.  
Retting: `<title>` er «Steg 4 av 6: Analyse – Søknadshjelpen» («Feil: …» ved feil). `base.html` får `<header>`, `<main id="innhold">` og en «Hopp til innhold»-lenke som første element.

**[Motstander]** — Veiviseren gir mange klikk, og «Ser bra ut» er et tomt steg (§ EXPERIENCE.md: IA, Tilbake/Neste, UJ-1, UJ-2; Avvik arkitektur 3)  
En ny bruker trenger åtte handlinger og sju sidelastinger fra innlogging til kopiert brev, en tilbakevendende bruker ni. PRD §6 ga omtrent fire. «Ser bra ut» lagrer ingenting, og «Bruk denne» + «Neste» er to klikk for én bekreftelse. Målet «ikke må streve» trekker i motsatt retning.  
Retting: Slå sammen steg 5 og 6, slå sammen steg 2 og 3, og vis CV-teksten direkte i steg 1. Da blir det fire steg (CV, Annonse og valg, Analyse, Søknad) og omtrent fem handlinger.

**[Motstander]** — UX-en legger til omfang uten kuttrekkefølge (§ EXPERIENCE.md og DESIGN.md; faglærers punkt 4.2)  
Seks maler og views, låste steg, bekreftelsesflyt, egen registrering (mot unntaket i AD-2), «Prøv forklaringen igjen», «Lag nytt brev», animasjon og full mørk modus med 15 ekstra tokens. Faglærer etterlyste en kuttplan, og UX-en gjør planen større uten å svare på det. Sensor vil se om gruppa prioriterer.  
Retting: Legg til seksjonen «Minste versjon og kuttrekkefølge» med *må*/*kan* per komponent. Forslag: animasjon → mørk modus → «Prøv forklaringen igjen» → låste steg → CV-forbedringer.

**[Motstander]** — Varselet om KI-feil står bare ved brevet, og KI-innhold og kode-innhold ser like ut (§ EXPERIENCE.md: Brevvisning, Kravliste, Nøkkelordanalyse, CV-forbedringer; DESIGN.md: Brev; AD-5)  
AD-5 krever varselet på alle sider med KI-tekst. Gap-analysen, forklaringen og CV-forbedringene har det ikke, og avviket er ikke listet. I steg 4 står KI sin vurdering og den sikre nøkkelordtellingen side om side i samme visuelle språk, så brukeren ser ikke hva som er påstand og hva som er telling.  
Retting: Merkelapp «Laget av KI» på KI-kort og «Telt automatisk» på nøkkelordkortet. Vis varselet øverst i steg 4 og ved CV-forbedringene, eller skriv inn avviket fra AD-5 med begrunnelse.

**[Motstander]** — «Søknaden er klar» og «Ser bra ut» lover for mye (§ EXPERIENCE.md: Ferdig-merke, Tilbake/Neste, UJ-1 trinn 6–7, Voice and Tone)  
Teksten sier at appen aldri skryter av brevet, men legger «Ser bra ut» i munnen på Emma og gir et stort ✓ med «Søknaden er klar». Det er et KI-utkast som kan inneholde feil. Sensor som ser etter KI-kontroll, vil lese dette som at «les gjennom» er gjort til et klikk.  
Retting: Bytt «Ser bra ut» med «Ta med brevet» (eller fjern steget) og «Søknaden er klar» med «Utkastet er klart». La Emma rette en setning i UJ-1 trinn 7.

### Middels (28)

**[Rubrikk · 1. Flytdekning]** — UJ-2, UJ-3 og UJ-4 har ingen feilvei (§ EXPERIENCE.md: Key Flows)  
Bare UJ-1 har en feilvei. Det er enklest å skrive for UJ-2 (KI-feil ved «Lag søknad» eller «Vis forslag til CV-en») og UJ-4 («Avbryt» på bekreftelsessiden).  
Retting: Legg til én «Avvik:»-linje per reise.

**[Rubrikk · 1. Flytdekning + Motstander]** — Testmodus: egen CV gir en blindvei, og eksempelknappen hopper over CV-teksten (§ EXPERIENCE.md: State Patterns «Egen CV i testmodus», Eksempelknapper, UJ-3 trinn 2 og 5)  
Det står ikke hva hovedknappen i steg 4 er når steg 5 og 6 ikke kan nås. Opplasting av egen CV sletter demoen (FR-1) uten at UJ-3 sier det, og eksempelknappen hopper til steg 3, så sensor ikke ser at CV C leses riktig (FR-2, SM-2).  
Retting: «Prøv eksempel A» som hovedknapp ved egen CV i testmodus, og fjern steg 5 og 6 fra «Hvor». La eksempelknappen vise CV-teksten. Nevn i UJ-3 at egen CV erstatter eksempelet.  
Funnet av: rubrikk, motstander.

**[Rubrikk · 2. Tokens]** — Komponenter i prosaen mangler tokens i `components` (§ DESIGN.md: frontmatter `components`)  
Topplinje, Nøkkelordmåler (8 px mot 4 px på `progress-bar`), Brev, merkene «Matcher»/«Mangler», knapp som viser «Jobber …», varsel/feilboks og radioknapp/avkrysning har ikke tokens.  
Retting: Legg til `top-bar`, `keyword-meter`, `letter-card`, `tag-match`/`tag-missing`, `button-busy`, `alert` og `checkbox-radio` med tokenhenvisninger.

**[Rubrikk · 2. Tokens + Tilgjengelighet M-2]** — «Les mer» på infoflaten har for lav kontrast og bryter DESIGN.md sin egen regel (§ DESIGN.md: Colors «Infoflate»; EXPERIENCE.md: Personvernpåminnelse)  
Lenke i aksentfarge på `info-bg` gir 4,42:1 i lys modus (WCAG 1.4.3), og DESIGN.md sier at tekst på infoflaten alltid har `{colors.text}`.  
Retting: «Lenker på infoflaten har fargen `text` og understrek» (12,67:1).  
Funnet av: rubrikk, tilgjengelighet.

**[Rubrikk · 2. Tokens + Tilgjengelighet M-1 + Motstander]** — Fremdriftslinjens steg har for lav kontrast, og kontrasttabellen mangler par (§ DESIGN.md: Colors (kontrasttabellen), Components «Fremdriftslinje»)  
Aktivt steg (aksent 50 %) har 2,09:1 mot bakgrunnen og 1,60:1 mot kommende steg i lys modus, og kommende steg har 1,30:1 (WCAG 1.4.11). Tabellen mangler også lenke på kort og flere andre par, og sier ikke hvordan den er sjekket. Rubrikken og motstanderen satte dette til lav, tilgjengelighet til middels.  
Retting: Full aksent og tykkere strek eller kant på aktivt steg, `field-border` på kommende steg. Legg til de manglende parene og nevn verktøyet.  
Funnet av: rubrikk, tilgjengelighet, motstander.

**[Rubrikk · 3. Komponentdekning]** — Komponentnavnene er ulike i de to filene (§ DESIGN.md: Components; EXPERIENCE.md: Component Patterns)  
Kravrad ↔ Kravliste, Brev ↔ Brevvisning, Hovedknapp/Sekundærknapp ↔ Tilbake / Neste. Frontmatter-nøklene er engelske og teksten norsk. Bare Fremdriftslinje og Ferdig-merke har samme navn begge steder.  
Retting: Bruk samme navn i begge filene, med frontmatter-nøkkelen i parentes, for eksempel «Kravrad (`requirement-match` / `requirement-missing`)».

**[Rubrikk · 3. Komponentdekning]** — Mange komponenter i EXPERIENCE.md mangler visuelt motstykke (§ DESIGN.md: Components)  
CV-opplasting, Bekreft lagret CV, Eksempelknapper, Annonsefelt med teller, Valg, Personvernpåminnelse, Lag nytt brev, Kopier, PDF-avsender, Last ned Markdown, CV-forbedringer, Start ny søknad og Slett-bekreftelse. Det samme gjelder venteknapp, KI-feilmelding, feiloppsummering og bekreftelsesmeldinger.  
Retting: Legg til korte linjer i DESIGN.md Components. Mange kan vise til en grunnkomponent, for eksempel «Eksempelknapper = Sekundærknapp i rad».

**[Rubrikk · 3. Komponentdekning]** — Steg 6 har fem handlinger, men ingen er utpekt som hovedknapp (§ DESIGN.md: Components, Do's and Don'ts; EXPERIENCE.md: Tilbake / Neste)  
Regelen er én hovedknapp per steg. Det samme gjelder steg 1 med lagret CV («Bruk denne», «Last opp ny» og «Neste»).  
Retting: Bestem hovedknappen (sannsynligvis «Kopier teksten») og hvordan de andre ser ut, også for steg 1.

**[Rubrikk · 4. Tilstander + Motstander + Tilgjengelighet L-11]** — Utløpt økt og utlogging er ikke beskrevet (§ EXPERIENCE.md: State Patterns; FR-13)  
Det står ikke hva som skjer når brukeren ikke er innlogget, eller hvor hun havner etter utlogging. Går økta ut midt i en innsending, forsvinner det som var limt inn. Risikoen er liten med Djangos standard på to uker.  
Retting: En rad i State Patterns: brukeren sendes til Logg inn med «Økten er utløpt – logg inn igjen. Det du limte inn, er ikke lagret.», og kommer tilbake til steget. Ikke korte ned `SESSION_COOKIE_AGE`.  
Funnet av: rubrikk, motstander, tilgjengelighet.

**[Rubrikk · 4. Tilstander]** — Siden for dekrypteringsfeil mangler (§ EXPERIENCE.md: State Patterns; AD-9)  
AD-9 [Forslag] sender brukeren til en side som forklarer at dokumentene ikke kan leses, og tilbyr sletting. UX har ikke den siden.  
Retting: Legg den til i State Patterns, med tekst og en knapp til Slett-bekreftelse.

**[Rubrikk · 4. Tilstander]** — Valideringstilstander mangler for kjente grenser (§ EXPERIENCE.md: State Patterns; AD-15)  
CV-tekst over 30 000 tegn (`CV_TEKST_MAKS`), mer enn 20 ønskede nøkkelord (`ONSKEDE_NOKKELORD_MAKS`) og personvernavkrysning som ikke er krysset av.  
Retting: Legg til én rad per grense, med meldingsteksten.

**[Rubrikk · 4. Tilstander + Motstander + Tilgjengelighet L-4]** — «Fungerer uten JavaScript» stemmer ikke for kopiering (§ EXPERIENCE.md: Interaction Primitives, Kopier)  
Kopiering til utklippstavlen (FR-22) krever JavaScript, så uten står det en knapp som ikke gjør noe. Det står heller ikke hva som skjer hvis utklippstavlen er blokkert.  
Retting: Knappen settes inn av skriptet (statusområdet finnes fra start), brevet kan ellers markeres og kopieres manuelt, og feilmeldingen er «Kunne ikke kopiere. Merk teksten og kopier selv.»  
Funnet av: rubrikk, motstander, tilgjengelighet.

**[Rubrikk · 4. Tilstander + Tilgjengelighet M-9]** — Annonsetelleren viser feil bare med oransje og kan støye i skjermleser (§ EXPERIENCE.md: Annonsefelt, State Patterns «Annonsen er for kort eller for lang»; DESIGN.md: Colors)  
Oransje er reservert for krav og nøkkelord, farge alene skiller ikke tilstanden (WCAG 1.4.1), og `aria-live` vil lese ved hvert tastetrykk.  
Retting: Bruk `{colors.danger}` eller tekstfarge pluss tekst («– minst 100 tegn»), koble telleren med `aria-describedby` og annonser bare når grensen krysses.  
Funnet av: rubrikk, tilgjengelighet.

**[Rubrikk · 5. Visuelle referanser + Motstander]** — Mockupene av nøkkelskjermene er ikke lenket, og spinen sier at de ikke finnes (§ DESIGN.md: Components; EXPERIENCE.md: Åpne punkter; `.working/key-*.html`)  
Rubrikken fant fire `key-*.html` i `.working/` som ingen av filene lenker til. EXPERIENCE.md sier fortsatt at de ikke er laget, og motstanderen fant bare steg 4.  
Retting: Lenk hver mockup der den hører hjemme, og fjern punktet i Åpne punkter. Lag eller oppdater mockupene når antall steg er avklart.  
Funnet av: rubrikk, motstander.

**[Rubrikk · 7. Arvedisiplin]** — Ordene i grensesnittet er ikke koblet til ordlisten i PRD §3 (§ EXPERIENCE.md: Component Patterns, IA; PRD §3)  
Valg ↔ Innstillinger, CV-forbedringer ↔ CV-forbedringsforslag, Nøkkelordanalyse ↔ ATS-nøkkelordanalyse, Søknad ↔ Søknadsbrev/Brevforslag, Annonse ↔ Stillingsannonse.  
Retting: Lag en liten tabell «Ord i grensesnittet» ↔ «Ord i PRD §3», og bruk PRD-ordene i komponentnavn og Krav-kolonner.

**[Rubrikk · 7. Arvedisiplin]** — Personvernlenken ved registrering mangler en side (§ EXPERIENCE.md: Personvern i grensesnittet, IA)  
Min konto krever innlogging, og IA har ingen offentlig side for forklaringen. Dette er ikke med i «Avvik».  
Retting: Legg til en offentlig side «Slik behandler vi dataene» i IA og i arkitekturens URL-liste, eller vis teksten på registreringssiden.

**[Tilgjengelighet M-3]** — Deaktivert knapp og «Jobber …» har ingen farger (§ DESIGN.md: Components; EXPERIENCE.md: Venter på KI; WCAG 1.4.3)  
Den deaktiverte knappen bærer statusteksten. Vanlig `opacity: .5` gir 2,09:1.  
Retting: Legg til `button-primary-busy` med samme farger som hovedknappen, `cursor: progress` og en `aria-hidden` indikator. Ingen opasitet på teksten.

**[Tilgjengelighet M-4]** — `autocomplete` mangler på personopplysningsfelt (§ EXPERIENCE.md: PDF-avsender, registrering; WCAG 1.3.5)  
E-post, passord, navn og telefon har et formål som kan bestemmes maskinelt.  
Retting: Angi `autocomplete` per felt (`email`, `new-password`, `current-password`, `name`, `tel`) og `off` på CV-tekst, annonse og nøkkelord.

**[Tilgjengelighet M-5]** — Nøkkelord-brikkene skiller funnet og mangler bare visuelt (§ DESIGN.md: Nøkkelord-brikke; EXPERIENCE.md: Nøkkelordanalyse; WCAG 1.3.1, 1.4.1)  
Stiplet kant og oransje farge høres ikke av skjermleser. Den heltrukne kanten har bare 1,22:1 mot kortet.  
Retting: To lister med underoverskriftene «Funnet (7)» og «Mangler (3)», eller visuelt skjult tekst «mangler» i hver brikke.

**[Tilgjengelighet M-6 + Motstander]** — Bare brevkortet får `lang="en"` (§ EXPERIENCE.md: Accessibility Floor; UJ-2 trinn 4 og 6)  
Gap-analysen, forklaringen, brevforslagene og CV-forbedringene er også på engelsk, men leses med norsk uttale (WCAG 3.1.2). Blandingen av norske merkelapper og engelsk KI-tekst er ikke beskrevet.  
Retting: Alle KI-blokker får `lang` etter `Analyse.sprak`. Én setning sier at blandingen er tilsiktet (NFR-8).  
Funnet av: tilgjengelighet, motstander.

**[Tilgjengelighet M-7]** — Reflow er satt til 360 px, men WCAG krever 320 px (§ DESIGN.md: Layout; EXPERIENCE.md: Accessibility Floor, Responsive; WCAG 1.4.10)  
To knapper side om side og lange ord fra brukeren kan gi vannrett rulling.  
Retting: «Virker fra 320 px». Knappene brytes under 360 px med hovedknappen øverst. `overflow-wrap: anywhere` og `white-space: pre-wrap` på brev og CV-tekst.

**[Tilgjengelighet M-8]** — Filopplastingen er ikke beskrevet for tastatur og skjermleser (§ EXPERIENCE.md: CV-opplasting, Ugyldig fil; WCAG 2.1.1, 3.3.2, 4.1.2)  
Et `input` skjult med `display:none` forsvinner fra tastaturet. Kravene (PDF eller TXT, maks 5 MB) står bare i feilmeldingene.  
Retting: Vanlig `<input type="file">` med synlig etikett og hjelpetekst via `aria-describedby`, visuelt skjult (ikke `display:none`) ved styling. Fokus til «Sjekk at teksten ble riktig» etter opplasting.

**[Tilgjengelighet M-10]** — Eksempelknappene heter bare «A», «B» og «C» (§ EXPERIENCE.md: Eksempelknapper, Testmodus; WCAG 2.4.6, 2.5.3)  
Skjermleseren sier «A, knapp». Det står ikke at et klikk hopper over steg 2.  
Retting: Synlig tekst «Eksempel A: junior utvikler» og hjelpeteksten «Fyller inn CV og annonse og går til steg 3.»

**[Tilgjengelighet M-11]** — Ferdig-steget mangler regler for fokus og animasjon (§ EXPERIENCE.md: Ferdig-merke, Accessibility Floor; WCAG 1.1.1, 2.3.3)  
✓ leses som «hake» før overskriften, og det står ikke om spinneren stopper ved `prefers-reduced-motion`.  
Retting: ✓ er `aria-hidden`, «Søknaden er klar» er `h1` og får fokus, og spinneren erstattes av statisk tekst ved redusert bevegelse.

**[Tilgjengelighet M-12]** — Feltkrav står bare i feilmeldingene (§ EXPERIENCE.md: Feil ved innlogging/registrering, PDF-avsender, Valg; WCAG 3.3.2)  
Passordkravet og nøkkelordreglene (komma, maks 20) vises først ved feil. Påkrevde og valgfrie felt er ikke merket.  
Retting: Krav som hjelpetekst under etiketten via `aria-describedby`, «(valgfri)» i etiketten og `required` på påkrevde felt.

**[Motstander]** — Tilbakeknappen i nettleseren kan sende «Analyser» på nytt (§ EXPERIENCE.md: Interaction Primitives; AD-10 `never_cache`)  
Er steg 4 svaret på en `POST`, kan tilbake og frem gi et nytt betalt KI-kall som overskriver analysen. Låsen i AD-12 hjelper bare mot samtidige kall.  
Retting: Hvert steg er en `GET`-side, og alle skjemaer bruker Post/Redirect/Get, unntatt når skjemaet vises på nytt med feil (AD-20).

**[Motstander]** — CV-forbedringer er låst bak brevet (§ EXPERIENCE.md: CV-forbedringer, UJ-2 trinn 6; PRD §4.2)  
Forbedringene avhenger av analysen, ikke brevet. En student som bare vil forbedre CV-en, må betale for et brev hun ikke trenger, og ved et KI-brudd i steg 5 kommer hun aldri dit.  
Retting: Flytt «Vis forslag til CV-en» til steg 4 under gap-analysen.

**[Motstander]** — Det er ikke avgjort om brevet kan redigeres før det kopieres (§ EXPERIENCE.md: Brevvisning, Kopier, PDF-avsender)  
En feil påstand må rettes i et annet program, og PDF-en inneholder feilen. Redigering viser kontroll, men reiser spørsmål om lagring og eksport.  
Retting: Ta en uttrykkelig beslutning. Forslag for v1: ingen redigering, med teksten «Kopier brevet og tilpass det i ditt eget program», ført i beslutningsloggen.

### Lav (30)

**[Rubrikk · 1. Flytdekning]** — UJ-3 og UJ-4 mangler scenelinje (§ EXPERIENCE.md: Key Flows UJ-3, UJ-4)  
UJ-1 og UJ-2 har en scenelinje (hvem, når, hvilken enhet). UJ-3 fortsetter også etter klimakset.  
Retting: Legg til en kursiv scenelinje, og flytt FR-11-delen til en egen «Deretter:»- eller «Avvik:»-linje.

**[Rubrikk · 1. Flytdekning]** — FR-14 og FR-15 har ikke noe sted i grensesnittet (§ EXPERIENCE.md: IA-tabellen)  
Det står ikke at det er med vilje. FR-8 mangler også i IA-tabellen.  
Retting: Skriv én setning om at FR-14 og FR-15 er usynlige i grensesnittet (AD-10), og legg FR-8 til i Krav-kolonnen for steg 5.

**[Rubrikk · 1. Flytdekning]** — UJ-1 steg 5 beskriver nøkkelordbrikkene feil (§ EXPERIENCE.md: UJ-1 steg 5)  
Emma «åpner ‹Hva betyr dette?›» og ser at «SQL» mangler, men brikkene står utenfor `<details>` og synes allerede.  
Retting: Skriv om setningen, så det er forklaringen hun åpner.

**[Rubrikk · 2. Tokens]** — `typography` har ingen `fontFamily` (§ DESIGN.md: frontmatter `typography`)  
Skriftstakken står bare i en YAML-kommentar og forsvinner når tokenene hentes ut maskinelt.  
Retting: Legg til `fontFamily` på rollene, eller et felles `body.fontFamily`.

**[Rubrikk · 2. Tokens]** — `button-danger` mangler `minHeight: 44px` (§ DESIGN.md: frontmatter `components`)  
Alle trykkflater skal være minst 44 px (EXPERIENCE.md Interaction Primitives).  
Retting: Legg den til.

**[Rubrikk · 3. Komponentdekning]** — Fareknappen er beskrevet på to måter (§ DESIGN.md: Colors og Components)  
Colors sier at fare brukes på «Slett mine dokumenter» og «Slett konto», mens Components sier at den bare brukes i bekreftelsen.  
Retting: Velg én regel, for eksempel sekundærknapp på Min konto og fareknapp på bekreftelsessiden.

**[Rubrikk · 3. Komponentdekning]** — Fem komponenter står bare i DESIGN.md (§ EXPERIENCE.md: Component Patterns)  
Topplinje, Testmodus-banner, Kort, Skjemafelt og Fokusring har oppførselen spredt i IA, Testmodus og Accessibility Floor.  
Retting: Legg til korte rader i Component Patterns med henvisning til der oppførselen står.

**[Rubrikk · 4. Tilstander]** — Noen tilstander mangler (§ EXPERIENCE.md: State Patterns)  
Min konto uten dokumenter, steg 2 når brukeren kommer tilbake, og venting under opplasting og innlesing av PDF.  
Retting: Legg til korte rader, eller si at de ikke trengs.

**[Rubrikk · 5. Visuelle referanser]** — Mockupen av steg 3 avviker fra spinen (§ `.working/key-steg3-valg.html`; EXPERIENCE.md: Valg)  
Etiketten «Språk i brevet» er for snever, fordi språket gjelder all KI-tekst. Rekkefølgen er også ulik (svarform først).  
Retting: Endre etiketten, skriv rekkefølgen inn i spinen, og ta med begrunnelsen fra mockupen (faglærer ba om at svarformen skulle synes).

**[Rubrikk · 5. Visuelle referanser]** — Mockupen av steg 6 mangler KI-varselet (§ `.working/key-steg5-6.html`; DESIGN.md: Brev; EXPERIENCE.md: Brevvisning)  
Spinen sier at varselet står over brevet i steg 5 og 6.  
Retting: Bestem om varselet skal stå i steg 6, og rett spinen eller mockupen.

**[Rubrikk · 5. Visuelle referanser]** — `imports/` er tom (§ `imports/`)  
Mappen har ingen filer.  
Retting: Slett mappen, eller skriv at den er tom med vilje.

**[Rubrikk · 6. Oppblåsing og overspesifisering]** — Testmodus og Personvern gjentar tekst (§ EXPERIENCE.md: Testmodus, Personvern i grensesnittet)  
FR-11-meldingen og personvernpåminnelsen står to steder.  
Retting: La seksjonene vise til radene, så teksten bare må endres ett sted.

**[Rubrikk · 6. Oppblåsing og overspesifisering]** — Historikk i Brand & Style (§ DESIGN.md: Brand & Style)  
Tre setninger om historikken bak designretningene hører hjemme i `.memlog.md`.  
Retting: Kort ned til retningsnavnet og lenken.

**[Rubrikk · 7. Arvedisiplin]** — Bekreftelsessiden for sletting trenger nye GET-sider (§ EXPERIENCE.md: Slett-bekreftelse; arkitektur §3)  
Arkitekturen har bare `POST /min-konto/slett-dokumenter/` og `/min-konto/slett-konto/`.  
Retting: Legg det til under «Avvik» Arkitektur.

**[Rubrikk · 7. Arvedisiplin]** — «Forsiden for besøkende» er ikke definert (§ EXPERIENCE.md: IA)  
Det står heller ikke hva topplinjen viser før innlogging.  
Retting: Si at forsiden er Logg inn, eller definer siden.

**[Rubrikk · 7. Arvedisiplin + Motstander]** — Arkitekturkilden finnes ikke før PR #13 er flettet (§ frontmatter `sources` i DESIGN.md og EXPERIENCE.md)  
`ARCHITECTURE-SPINE.md` ligger i PR #13. Flettes UX-en først, peker kilden på ingenting.  
Retting: Flett arkitekturen før UX-en, eller skriv i pull requesten at UX-en avhenger av PR #13.  
Funnet av: rubrikk, motstander.

**[Rubrikk · 8. Form]** — Inspiration & Anti-patterns står etter Key Flows (§ EXPERIENCE.md)  
I mønstereksemplene står seksjonen før Key Flows.  
Retting: Flytt den rett etter Responsive & Platform.

**[Rubrikk · 8. Form]** — Fire egne seksjoner er lagt til (§ EXPERIENCE.md: Testmodus, Personvern i grensesnittet, Avvik, Åpne punkter)  
Alle har en tydelig funksjon, men Testmodus og Personvern bør vise til andre seksjoner i stedet for å gjenta dem.  
Retting: Ingen, utover det som står under 6.

**[Tilgjengelighet L-1]** — Manuell ▸ i `<summary>` (§ EXPERIENCE.md: Nøkkelordanalyse; WCAG 1.3.1)  
Skjermleseren leser «svart trekant som peker mot høyre».  
Retting: Bruk den innebygde markøren eller CSS `::before`, og skriv «Hva betyr nøkkelordanalysen?».

**[Tilgjengelighet L-2]** — Ikonene ✓ og ! leses dobbelt (§ DESIGN.md: Kravrad; WCAG 1.1.1)  
Skjermleseren leser «hake, Python, Matcher».  
Retting: Ikonene er `aria-hidden`, kravlisten er en `<ul>`, og «2 av 4 krav dekket» står i overskriften.

**[Tilgjengelighet L-3]** — Nøkkelordmåleren er pynt, men det står ikke (§ DESIGN.md: Nøkkelordmåler; WCAG 1.1.1, 1.4.11)  
Sporet har 1,22:1 mot kortet. Teksten «7 av 10 funnet» bærer informasjonen.  
Retting: `aria-hidden` eller `<meter>`, og `field-border` på sporet hvis grafikken skal kunne leses.

**[Tilgjengelighet L-5]** — Lenke inne i avkrysningsetiketten (§ EXPERIENCE.md: Personvern i grensesnittet; WCAG 2.5.3, 3.3.2)  
Trykk på lenken kan krysse av, og lenken er vanskelig å treffe på mobil.  
Retting: Legg lenken som egen tekst under avkrysningen, koblet med `aria-describedby`.

**[Tilgjengelighet L-6]** — Låste steg sender videre uten forklaring (§ EXPERIENCE.md: Låste steg; WCAG 3.3.1)  
En bruker som følger et bokmerke, får ikke vite hvorfor hun havnet et annet sted.  
Retting: Vis en melding: «Steg 5 er ikke tilgjengelig ennå. Du er tilbake i steg 3.»

**[Tilgjengelighet L-7]** — «10–30 sekunder» passer ikke med 60 sekunder (§ EXPERIENCE.md: Venter på KI; AD-4)  
Etter 30 sekunder ser det ut som om appen har hengt seg opp.  
Retting: Oppdater statusområdet etter 30 sekunder: «Det tar litt lenger tid enn vanlig. Vent litt til.»

**[Tilgjengelighet L-8]** — Tekststørrelser i px og faste høyder (§ DESIGN.md: typography, Components; WCAG 1.4.4, 1.4.12)  
px følger ikke brukerens standard skriftstørrelse, og faste høyder kan klippe tekst.  
Retting: CSS i `rem`, `min-height` i stedet for `height`, og aldri `overflow: hidden` på tekstbeholdere.

**[Tilgjengelighet L-9]** — Tvungne farger (Windows høykontrast) er ikke nevnt (§ DESIGN.md: Colors; WCAG 1.4.11)  
Fremdriftslinjen, måleren og ikonsirklene forsvinner med `forced-colors: active`.  
Retting: Kant (`1px solid CanvasText`) under `forced-colors`, og fokusring med `outline`, ikke `box-shadow`.

**[Tilgjengelighet L-10]** — Topplinjens lenker og «Logg ut» (§ DESIGN.md: Topplinje; WCAG 2.5.5 (AAA), 4.1.2)  
Små tekstlenker når ikke 44 px, og «Logg ut» må være en `POST` i Django 5.  
Retting: Padding til 44 px høyde, og «Logg ut» som `<button>` i et skjema, stylet som lenke.

**[Tilgjengelighet L-12]** — Mockupen bruker gammel mangler-farge og mindre tekst (§ `.working/directions-2.html`, variant 3)  
`--miss:#A65F00` (4,34:1) og 12 px tekst, mens DESIGN.md har 14 px.  
Retting: Merk mockupen som utdatert på disse punktene, eller oppdater den.

**[Motstander]** — Personvernpåminnelsen er feil i testmodus (§ EXPERIENCE.md: Personvernpåminnelse; AD-5)  
Påminnelsen sier at teksten sendes til KI-tjenesten, men i testmodus sendes ingenting (FR-9).  
Retting: I testmodus: «Testmodus: ingenting sendes til KI-tjenesten. Appen bruker lagrede svar.»

**[Motstander]** — Beslutningene er tilskrevet én person (§ EXPERIENCE.md, DESIGN.md, .memlog.md)  
«Henrik valgte» står gjennom hele dokumentet. Sensor vurderer gruppens prosess, og det finnes ikke spor av at Ole og Haakon har vurdert valgene.  
Retting: Når PR-en er gjennomgått: en linje i hvert dokument om at gruppa har godtatt eller endret valgene, med dato.

## Mekaniske merknader

- Tokenhenvisninger: 21 ulike `{…}`-henvisninger, og alle løser seg. 17 fargetokener, alle med `-dark`-variant.
- Kontrast (regnet ut på nytt): tallene i tabellen stemmer. Nye tall: aksent på kort 4,81 / 7,60, mangler-tekst på kort 5,23 / 7,69, fare-tekst på kort 6,13 / 9,45, aktivt steg (50 % aksent) mot bakgrunn 2,09 / 3,03.
- Personvernavkrysningen har litt ulik ordlyd i `.memlog.md` og EXPERIENCE.md. Spinen gjelder, men de bør stemme overens.
- «[ANTAKELSE]-punkter» i Åpne punkter lister seks punkter, men mangler «ordlyden ved forbruksgrensen».
- DESIGN.md har `description` i frontmatter, EXPERIENCE.md har det ikke.
- EXPERIENCE.md har `product-brief.md` og `tilbakemelding-prd.md` som kilder, DESIGN.md har det ikke. Det er greit, fordi DESIGN.md ikke bruker dem.

## Gjennomgangsfiler

- `review-rubric.md`
- `review-tilgjengelighet.md`
- `review-motstander.md`
