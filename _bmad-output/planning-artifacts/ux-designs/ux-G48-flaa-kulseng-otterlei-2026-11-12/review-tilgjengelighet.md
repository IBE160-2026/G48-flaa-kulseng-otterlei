# Tilgjengelighetsgjennomgang — G48

_Gjennomgang av `DESIGN.md`, `EXPERIENCE.md`, `.memlog.md` og `.working/directions-2.html` (variant «3 — C dempet») mot PRD NFR-7, arkitekturen (AD-12, AD-15) og WCAG 2.1 AA. Skrevet av Claude Code som tilgjengelighets-reviewer 2026-11-12. Alle kontrasttall er regnet ut på nytt med WCAG-formelen for relativ luminans (`python3 -I`). Funnene er forslag. Gruppa avgjør hva som skal rettes._

## Samlet vurdering

Grunnlaget er godt. Fargene består AA for all vanlig tekst i begge moduser. «Matcher» og «Mangler» bruker symbol og tekst, ikke bare farge. Det finnes et eget token for feltkanter (3:1). Appen bruker ingen dialogvinduer og ingen hover-handlinger, og den fungerer uten JavaScript. Accessibility Floor dekker de riktige temaene.

Svakhetene ligger i **hvordan veiviseren oppfører seg med skjermleser og tastatur**, ikke i fargene:

1. Fremdriftslinjen er tegnet som seks streker på 4 px uten stegnavn, men fullførte steg skal være lenker. Slik den er beskrevet, får lenkene ikke noe navn og er for små til å treffe.
2. Ventestatusen og KI-feilen skal meldes med `aria-live`, men begge skjer rundt en vanlig, synkron `POST` (AD-12). Da lastes en ny side, og en `aria-live`-melding som kommer med sideinnlastingen blir som regel ikke lest opp. Feilen må derfor få fokus.
3. Lenker skilles fra brødtekst bare med farge (2,87:1 i lys modus og 1,76:1 i mørk modus mot teksten), noe som strider mot 1.4.1. Dokumentet sier ikke at lenker skal være understreket.

Ingen funn er kritiske, fordi ingen av dem stopper en bruker helt. Alle er enkle å rette i dokumentene før koden skrives. Det meste av rettingen er å legge til presiseringer i Accessibility Floor (se siste funn) og noen rader i kontrasttabellen i `DESIGN.md`.

**Antall funn:** kritisk 0 · høy 5 · middels 12 · lav 12.

**2.2.1 Justerbar tidsbruk gjelder ikke ventetiden.** Ventetiden på opptil 60 sekunder er en ventetid, ikke en tidsgrense som brukeren må rekke å gjøre noe innenfor. 2.2.1 slår bare inn hvis innloggingsøkta kan gå ut mens brukeren skriver (se funn L-11).

## Funn

### Høy

- **[høy] H-1 Fremdriftslinjen har lenker uten navn og trykkflate** (`DESIGN.md` Components › Fremdriftslinje, `EXPERIENCE.md` Component Patterns › Fremdriftslinje og Accessibility Floor; 2.4.4, 4.1.2, 1.3.1, 2.5.3). Linjen er seks streker på 4 px. Bare det aktive steget har et navn («Steg 4 av 6 · Analyse»). Fullførte steg skal likevel være lenker. En lenke på en strek på 4 px har ikke noe tilgjengelig navn, og den er ikke 44 × 44 px, slik Interaction Primitives lover. Det står heller ikke hvordan en skjermleser skal få vite at et steg er fullført eller låst.
  *Retting:* Beskriv markeringen eksakt: `<nav aria-label="Fremdrift"><ol>` med ett `<li>` per steg. Hvert `<li>` har stegnavnet som tekst (synlig fra 600 px og visuelt skjult på mobil). Fullførte steg er `<a href>` med teksten «Steg 2: Annonse (fullført)», det aktive steget er en `<span aria-current="step">`, og låste steg er `<span>` med «(ikke tilgjengelig ennå)». Strekene er `aria-hidden` pynt. Lenkens trykkflate må være minst 44 px høy, for eksempel ved at strek og navn er én lenke med padding. Alternativt: la strekene bare være pynt, og legg «Tilbake til: CV · Annonse · Valg» som vanlige tekstlenker under.

- **[høy] H-2 Ventestatusen blir ikke lest opp, og fokus kan forsvinne** (`EXPERIENCE.md` State Patterns › Venter på KI, Accessibility Floor; AD-12; 4.1.3, 2.4.3). `skjema.js` skal deaktivere knappen og vise «Jobber …» med `aria-live` ved innsending. Det er tre problemer: (a) Et `aria-live`-område leses bare opp hvis det finnes i DOM-en *før* teksten endres. (b) Når knappen som har fokus får `disabled`, mister den fokus i flere nettlesere, og skjermleserbrukeren mister stedet sitt. (c) En `disabled`-knapp sendes ikke med i skjemaet, så hvis viewet leser `name`/`value` fra knappen, forsvinner verdien.
  *Retting:* Skriv i Accessibility Floor: «Hver side med KI-knapp har et tomt `<p role="status" id="ki-status">` i malen fra start. Ved innsending setter `skjema.js` `aria-disabled="true"` på knappen (ikke `disabled`), stopper flere innsendinger med en variabel, beholder fokus på knappen og skriver ‹Jobber … Dette tar vanligvis 10–30 sekunder.› i statusområdet.» Teksten «Dette tar vanligvis 10–30 sekunder» bør stå i statusområdet, ikke bare som synlig tekst under knappen.

- **[høy] H-3 Feil som vises etter at siden lastes på nytt, blir ikke lest opp** (`EXPERIENCE.md` State Patterns › KI svarte ikke, Feil ved innlogging; Accessibility Floor; AD-20; 3.3.1, 4.1.3, 2.4.3). AD-20 viser feil ved å rendre skjemaet på nytt med status 200. Det er en ny side. En `aria-live`-melding i den nye siden blir vanligvis ikke lest opp, og Accessibility Floor sier samtidig at fokus alltid skal gå til `h1`. Da hører skjermleserbrukeren stegtittelen og vet ikke at noe gikk galt.
  *Retting:* Del regelen i to: «Uten feil går fokus til `h1` (med `tabindex="-1"`). Med feil går fokus til feiloppsummeringen.» Beskriv feiloppsummeringen: `<div role="alert" tabindex="-1">` øverst i `<main>`, med overskriften «Noe må rettes» og en liste med lenker (`href="#id_felt"`) til hvert felt med feil. KI-feil og feil uten felt (`form.add_error(None, …)`) står i den samme oppsummeringen. Sidetittelen får forstavelsen «Feil: ». Uten JavaScript er `autofocus` ikke mulig på en `div`, så noter at fokusflyttingen gjøres i `skjema.js`, og at oppsummeringen øverst er reserveløsningen uten JavaScript.

- **[høy] H-4 Lenker skilles fra tekst bare med farge** (`DESIGN.md` Colors › Blågrønn aksent; 1.4.1). Aksentfargen brukes på lenker, men kontrasten mot vanlig tekst er bare 2,87:1 i lys modus og 1,76:1 i mørk modus. WCAG krever 3:1 mot omkringliggende tekst *og* en ekstra markering ved fokus/hover hvis lenken bare skilles med farge. Dette gjelder «Les mer» i personvernpåminnelsen, lenken til README (FR-11), lenken ved registreringen og «Min konto» og «Logg ut».
  *Retting:* Legg til i `DESIGN.md`: «Lenker i løpende tekst er alltid understreket. Lenker i topplinjen kan stå uten understrek fordi de står alene, men får understrek ved hover og fokus.»

- **[høy] H-5 Hver side mangler en unik sidetittel og landemerker** (`EXPERIENCE.md` Information Architecture, Accessibility Floor; 2.4.2, 1.3.1, 2.4.1). Det står ikke noe om `<title>`. I en veiviser der alle steg ligger under samme mal, er det fort gjort å få samme tittel på alle sider. Da hører en skjermleserbruker ikke hvilket steg som er lastet. Det står heller ikke noe om `header`, `nav`, `main` eller en «Hopp til innhold»-lenke, og testmodus-banneret og topplinjen står foran innholdet på hver side.
  *Retting:* Legg til: «`<title>` er ‹Steg 4 av 6: Analyse – Søknadshjelpen› (‹Feil: …› når skjemaet har feil). `base.html` har `<header>` (banner og topplinje), `<main id="innhold">` og en ‹Hopp til innhold›-lenke som første element, synlig ved fokus.»

### Middels

- **[middels] M-1 Det aktive steget og kommende steg har for lav ikke-tekst-kontrast** (`DESIGN.md` Components › Fremdriftslinje; 1.4.11, 1.4.1). Aksentfargen med 50 % gjennomsiktighet blir `#8FBCBA` på hvit (2,09:1 mot bakgrunnen, 1,60:1 mot kommende steg, 2,46:1 mot fullførte steg). Kommende steg i `border` har 1,30:1 mot bakgrunnen og er nesten usynlige. I mørk modus er det aktive steget 3,03:1 mot bakgrunnen, men bare 2,08:1 mot kommende steg. Forskjellen mellom de tre tilstandene vises altså bare med svake fargeforskjeller. Teksten «Steg 4 av 6» redder forståelsen, så det er ikke et sikkert brudd, men grafikken alene oppfyller ikke 1.4.11.
  *Retting:* La det aktive steget være full aksentfarge og høyere (for eksempel 8 px mot 4 px), eller gi det en kant. Gi kommende steg `field-border` (3,47:1 / 3,78:1) i stedet for `border`. Legg linjen inn i kontrasttabellen.

- **[middels] M-2 Lenken i personvernpåminnelsen har for lav kontrast på infoflaten** (`DESIGN.md` Colors › Infoflate; `EXPERIENCE.md` Component Patterns › Personvernpåminnelse; 1.4.3). Dokumentet sier selv at blågrønn på infoflate er 4,4:1 (beregnet 4,42:1). Men «Les mer» er en lenke i påminnelsen, og lenker har aksentfargen. Merknaden ligger på infoflaten. Det er i lys modus et brudd på 1.4.3 (mørk modus: 6,61:1, greit).
  *Retting:* Skriv: «Lenker på infoflaten har fargen `text` og understrek.» Tekstfarge på infoflate gir 12,67:1.

- **[middels] M-3 Deaktivert knapp og «Jobber …» har ingen farger** (`DESIGN.md` Components; `EXPERIENCE.md` State Patterns › Venter på KI; 1.4.3). Deaktiverte kontroller er unntatt fra kontrastkravet, men her er den deaktiverte knappen også bæreren av statusmeldingen «Jobber …». Hvis utvikleren bruker vanlig `opacity: .5`, gir det 2,09:1 i lys modus. Det er for lavt for en tekst brukeren skal lese.
  *Retting:* Legg til `button-primary-busy` i `DESIGN.md`: samme fyll og tekstfarge som hovedknappen (5,12:1 / 8,76:1), `cursor: progress` og en indikator. Unngå opasitet på teksten. Indikatoren er `aria-hidden`.

- **[middels] M-4 `autocomplete` mangler på personopplysningsfelt** (`EXPERIENCE.md` Component Patterns › PDF-avsender; Key Flows UJ-1 registrering; 1.3.5). E-post, passord, navn og telefon er felt der formålet kan bestemmes maskinelt.
  *Retting:* Skriv i Accessibility Floor: Registrer: `autocomplete="email"` og `"new-password"`. Logg inn: `"email"` (eller `"username"`) og `"current-password"`. PDF-avsender: `"name"`, `"email"` og `"tel"` med `type="email"` og `type="tel"`. CV-tekst, annonse og nøkkelord får `autocomplete="off"`.

- **[middels] M-5 Nøkkelord-brikkene skiller funnet og mangler bare visuelt** (`DESIGN.md` Components › Nøkkelord-brikke; `EXPERIENCE.md` Nøkkelordanalyse; 1.3.1, 1.4.1). Stiplet kant og oransje farge sees ikke av skjermleser, så alle brikkene leses som en lang ordrekke. I tillegg er den heltrukne kanten på funnede brikker 1,22:1 mot kortet, så forskjellen mellom heltrukket og stiplet er svak også for seende.
  *Retting:* Del brikkene i to lister med egne underoverskrifter, «Funnet (7)» og «Mangler (3)». Da er forskjellen også tekst. Alternativt: visuelt skjult tekst «mangler» i hver manglende brikke.

- **[middels] M-6 `lang="en"` gjelder bare brevkortet** (`EXPERIENCE.md` Accessibility Floor; UJ-2; 3.1.2). UJ-2 sier at gap-analysen også er på engelsk, og det samme gjelder KI-forklaringen, brevforslagene og CV-forbedringene. Med bare `lang="nb"` leser skjermleseren engelske begrunnelser med norsk uttale.
  *Retting:* «Alle blokker med KI-tekst (begrunnelser, forklaring, brev, brevforslag, CV-forslag) får `lang` etter språket som ble valgt i steg 3 (`nb` eller `en`), tatt fra lagret valg, ikke gjettet fra teksten. Merkelapper som ‹Matcher› og ‹Mangler› er fortsatt norske.»

- **[middels] M-7 Reflow er satt til 360 px, men WCAG krever 320 px** (`DESIGN.md` Layout; `EXPERIENCE.md` Accessibility Floor og Responsive; 1.4.10). 1.4.10 krever at innholdet virker på 320 CSS-piksler (400 % zoom på 1280 px) uten vannrett rulling. Med 16 px sidemarger og to knapper ved siden av hverandre, for eksempel «Tilbake» og «Lag søknad →», blir det trangt. Lange ord fra brukeren (URL-er i CV-en, lange nøkkelord, e-postadresser) kan også presse siden ut.
  *Retting:* Skriv «virker fra 320 px» (360 px fra PRD-en er fortsatt målet for vanlig visning). Legg til: knappene brytes til hver sin linje under 360 px, med hovedknappen øverst. `overflow-wrap: anywhere` på brev, CV-tekst og brikker. Brev og CV-tekst vises med `white-space: pre-wrap`, ikke `<pre>`.

- **[middels] M-8 Filopplastingen er ikke beskrevet for tastatur og skjermleser** (`EXPERIENCE.md` Component Patterns › CV-opplasting, State Patterns › Ugyldig fil; 2.1.1, 3.3.2, 4.1.2). Det står ikke om feltet er et vanlig `<input type="file">` eller en egendefinert knapp. Et vanlig mønster er å skjule `input` med `display:none` og style en `label`, men da forsvinner feltet fra tastaturet og skjermleseren. Kravene (PDF eller TXT, maks 5 MB) står bare i feilmeldingene, ikke før opplastingen.
  *Retting:* «Bruk vanlig `<input type="file" accept=".pdf,.txt,application/pdf,text/plain">` med synlig `<label>` (‹Last opp CV-en›) og hjelpetekst ‹PDF eller TXT, maks 5 MB› koblet med `aria-describedby`. Skjules feltet visuelt for styling, skal det være visuelt skjult (ikke `display:none`) og vise fokusringen på etiketten.» Etter opplastingen går fokus til «Sjekk at teksten ble riktig».

- **[middels] M-9 Tegntelleren kan støye eller vises bare med farge** (`EXPERIENCE.md` Component Patterns › Annonsefelt, State Patterns › Annonsen er for kort; 1.4.1, 4.1.3). Telleren skal bli oransje ved feil. Farge alene skiller ikke tilstanden. Står telleren i et `aria-live`-område, leses den opp ved hvert tastetrykk. Oransje (`missing`) brukes også her, selv om `DESIGN.md` sier at oransje bare er for krav og nøkkelord som mangler.
  *Retting:* Koble telleren til feltet med `aria-describedby`, men ikke med `aria-live`. Legg til tekst når grensen brytes («– minst 100 tegn»). Annonsér i et statusområde bare når grensen krysses. Avklar om fargen skal være `missing` eller `danger`, og oppdater `DESIGN.md`.

- **[middels] M-10 Eksempelknappene heter bare «A», «B» og «C»** (`EXPERIENCE.md` Component Patterns › Eksempelknapper, Testmodus; 2.4.6, 2.5.3). En skjermleser sier «A, knapp», og det er det sensor hører. Det står heller ikke at et klikk hopper over steg 2.
  *Retting:* Synlig tekst «Eksempel A: junior utvikler» (eller tilsvarende) og en hjelpetekst: «Fyller inn CV og annonse og går til steg 3.»

- **[middels] M-11 Ferdig-steget mangler beskrivelse av fokus og animasjon** (`EXPERIENCE.md` Ferdig-merke, Accessibility Floor; 1.1.1, 2.3.3). ✓-merket er pynt, men det står ikke at det skal være `aria-hidden`. Ellers leser skjermleseren «hake» før «Søknaden er klar». Det står heller ikke om «liten indikator» i venteknappen (en spinner) skal stoppe ved `prefers-reduced-motion`.
  *Retting:* «✓-merket er `aria-hidden="true"`. ‹Søknaden er klar› er `h1` og får fokus. Spinneren i venteknappen erstattes av statisk tekst ved `prefers-reduced-motion: reduce`.»

- **[middels] M-12 Feltkrav og hjelpetekst står bare i feilmeldingene** (`EXPERIENCE.md` State Patterns › Feil ved innlogging/registrering, PDF-avsender, Valg › nøkkelord; 3.3.2). «Passordet må ha minst 8 tegn» kommer først når det er feil. Nøkkelordfeltet har regler (komma, maks 20 ord) som ikke står ved feltet. Det står ikke hvordan påkrevde og valgfrie felt merkes.
  *Retting:* «Krav står som hjelpetekst under etiketten før brukeren skriver, koblet med `aria-describedby`. Valgfrie felt merkes ‹(valgfri)› i etiketten. Påkrevde felt har `required`.»

### Lav

- **[lav] L-1 Manuell ▸ i `<summary>`** (`EXPERIENCE.md` Nøkkelordanalyse; 1.3.1). «▸ Hva betyr dette?» får skjermleseren til å lese «svart trekant som peker mot høyre». `<summary>` har allerede en markør. *Retting:* Bruk den innebygde markøren, eller lag pilen i CSS (`::before`). Gi teksten mer sammenheng: «Hva betyr nøkkelordanalysen?»

- **[lav] L-2 Ikonene ✓ og ! leses dobbelt** (`DESIGN.md` Kravrad; 1.1.1). Skjermleseren leser «hake, Python, Matcher». *Retting:* Ikonene er `aria-hidden`. Kravlisten er en `<ul>` med ett `<li>` per krav, og «2 av 4 krav dekket» står i overskriften.

- **[lav] L-3 Nøkkelordmåleren er bare pynt, men det står ikke** (`DESIGN.md` Nøkkelordmåler; 1.1.1, 1.4.11). Sporet (`border`) har 1,22:1 mot kortet, så lengden er vanskelig å se. Teksten «7 av 10 funnet» bærer informasjonen. *Retting:* Måleren er `aria-hidden`, eller bruk `<meter>`. Gi sporet `field-border` hvis andelen skal kunne leses av grafikken.

- **[lav] L-4 Kopier-knappen mangler regler uten JavaScript og ved feil** (`EXPERIENCE.md` Kopier, Interaction Primitives; 4.1.3). Uten JavaScript virker knappen ikke, men den vises likevel. Det står ikke hva som skjer hvis utklippstavlen er blokkert. *Retting:* Knappen settes inn av JavaScript (eller er `hidden` til JavaScript er lastet). Statusområdet (`role="status"`) finnes i malen fra start. Ved feil: «Kunne ikke kopiere. Merk teksten og kopier selv.» Gi knappen et presist navn: «Kopier søknadsbrevet».

- **[lav] L-5 Lenken i avkrysningsetiketten** (`EXPERIENCE.md` Personvern i grensesnittet › Registrering; 2.5.3, 3.3.2). En lenke inne i `<label>` gjør at trykk på lenken også kan krysse av, og den er vanskelig å treffe på mobil. *Retting:* Legg lenken som egen tekst under avkrysningen og koble den med `aria-describedby`.

- **[lav] L-6 Låste steg sender brukeren videre uten forklaring** (`EXPERIENCE.md` State Patterns › Låste steg; 3.3.1). En bruker som følger et bokmerke, havner et annet sted uten å få vite hvorfor. *Retting:* Vis en Django-melding etter omdirigeringen: «Steg 5 er ikke tilgjengelig ennå. Du er tilbake i steg 3.»

- **[lav] L-7 Forventningen «10–30 sekunder» passer ikke med 60 sekunder** (`EXPERIENCE.md` State Patterns › Venter på KI; AD-4; 3.3.x, kognitiv tilgjengelighet). Etter 30 sekunder ser det ut som om appen har hengt seg opp. *Retting:* `skjema.js` oppdaterer statusområdet etter 30 sekunder: «Det tar litt lenger tid enn vanlig. Vent litt til.»

- **[lav] L-8 Tekststørrelser i px og faste høyder** (`DESIGN.md` typography, Components; 1.4.4, 1.4.12). Med px følger teksten nettleserzoom, men ikke brukerens valg av standard skriftstørrelse. Faste høyder på brikker, ikoner (22 px) og knapper kan klippe tekst når linjeavstand eller bokstavavstand økes. *Retting:* Skriv CSS-verdiene i `rem`, bruk `min-height` (som allerede er valgt for knapper og felt) og aldri `height` eller `overflow: hidden` på tekstbeholdere.

- **[lav] L-9 Tvungne farger (Windows høykontrast) er ikke nevnt** (`DESIGN.md` Colors; 1.4.11). Fremdriftslinjen, måleren og ikonsirklene er bakgrunnsfarger og forsvinner med `forced-colors: active`. *Retting:* En kort regel: under `@media (forced-colors: active)` får strekene og måleren en kant (`border: 1px solid CanvasText`), og fokusringen bruker `outline` (ikke `box-shadow`).

- **[lav] L-10 Topplinjens lenker og «Logg ut»** (`DESIGN.md` Topplinje; 2.5.5 (AAA), 4.1.2). Tekstlenker med 13–14 px skrift når ikke 44 px. «Logg ut» må være en `POST` i Django 5, altså en knapp som ser ut som en lenke. *Retting:* Gi lenkene padding til 44 px høyde, og skriv at «Logg ut» er en `<button>` i et skjema, stylet som lenke.

- **[lav] L-11 Øktutløp mens brukeren skriver** (2.2.1). Hvis Django-økta går ut mens Emma redigerer CV-teksten eller annonsen, mister hun teksten ved innsending. Standard i Django er to uker, så risikoen er liten. *Retting:* Ikke korte ned `SESSION_COOKIE_AGE`, og skriv dette i arkitekturen eller her.

- **[lav] L-12 Mockupen bruker gammel mangler-farge og mindre tekst** (`.working/directions-2.html`, variant 3). Variant 3 har `--miss:#A65F00` (4,34:1 på mangler-flaten), og stegteksten og begrunnelsene er 12 px, mens `DESIGN.md` sier `small` = 14 px. `DESIGN.md` går foran, men en utvikler som kopierer fra mockupen, får feil verdier. *Retting:* Merk mockupen som utdatert på disse punktene, eller oppdater den når nøkkelskjermene lages.

### Hva Accessibility Floor bør inneholde i tillegg

Accessibility Floor er det en utvikler (eller en annen Claude) bygger etter. Disse punktene mangler og bør stå der i en kort liste, med henvisning til funnene over:

1. Unik `<title>` per side og per steg, med «Feil: » ved feil (H-5).
2. Landemerker `header`, `nav`, `main` og «Hopp til innhold» (H-5).
3. Eksakt markering av fremdriftslinjen med navn, «fullført», `aria-current` og «ikke tilgjengelig ennå» (H-1).
4. Fokusregel: `h1` uten feil, feiloppsummering med feil (H-3).
5. Statusområder (`role="status"`) finnes i malen fra start. `aria-disabled`, ikke `disabled`, på knappen som jobber (H-2).
6. Feiloppsummering med lenker til feltene (H-3).
7. Lenker i løpende tekst er understreket (H-4).
8. `autocomplete` per felt (M-4).
9. `lang` på alle KI-blokker (M-6).
10. Krav i hjelpetekst før feil, og merking av valgfrie felt (M-12).
11. Pyntegrafikk (`✓`, `!`, måler, streker) er `aria-hidden` (L-2, L-3, M-11).
12. 320 px reflow, `rem`, ingen faste høyder (M-7, L-8).
13. Hvordan gruppa sjekker dette: for eksempel tastaturtest av hele UJ-1 og UJ-3, VoiceOver eller NVDA på steg 3–6, og axe eller Lighthouse i nettleseren. Det gir sensor spor av kvalitetssikringen (testing og kvalitetssikring er 15 % av karakteren).

## Kontrasttabell (beregnet)

Regnet ut med WCAG 2.1-formelen for relativ luminans. Krav: 4,5:1 for vanlig tekst, 3:1 for stor tekst og for grafikk og kontrollkanter (1.4.11), 3:1 mellom lenke og tekst rundt (1.4.1, hvis lenken ikke er understreket).

| Par | Lys | Mørk | Krav | Resultat |
|---|---|---|---|---|
| Tekst på bakgrunn | 14,70 | 14,98 | 4,5 | Består |
| Tekst på kort (`surface`) | 13,79 | 13,37 | 4,5 | Består |
| Tekst på infoflate | 12,67 | 11,62 | 4,5 | Består |
| Dempet tekst på bakgrunn | 5,51 | 7,21 | 4,5 | Består |
| Dempet tekst på kort | 5,17 | 6,43 | 4,5 | Består |
| Dempet tekst på infoflate | 4,75 | 5,59 | 4,5 | Består (knapt i lys) |
| Tekst på aksentknapp (`on-accent`/`accent`) | 5,12 | 8,76 | 4,5 | Består |
| Aksent (lenke) på bakgrunn | 5,12 | 8,51 | 4,5 | Består |
| Aksent (lenke) på kort / topplinje | 4,81 | 7,60 | 4,5 | Består |
| **Aksent (lenke) på infoflate** | **4,42** | 6,61 | 4,5 | **Brudd i lys** (M-2) |
| **Aksent (lenke) mot vanlig tekst** | **2,87** | **1,76** | 3,0 | **Brudd begge** uten understrek (H-4) |
| Matcher-tekst på matcher-flate | 4,73 | 6,52 | 4,5 | Består (12 px merke: knapt) |
| Matcher-tekst på kort | 5,11 | 7,66 | 4,5 | Består |
| Mangler-tekst på mangler-flate | 4,90 | 6,52 | 4,5 | Består |
| Mangler-tekst (stiplet brikke) på kort | 5,23 | 7,69 | 4,5 | Består |
| Mangler-tekst (teller) på bakgrunn | 5,57 | 8,61 | 4,5 | Består |
| Stiplet brikkekant (`missing`) mot kort | 5,23 | 7,69 | 3,0 | Består |
| Heltrukket brikkekant (`border`) mot kort | 1,22 | 1,30 | — | Pynt, men svak forskjell (M-5) |
| Fare-tekst på bakgrunn | 6,54 | 10,59 | 4,5 | Består |
| Fare-tekst på kort | 6,13 | 9,45 | 4,5 | Består |
| Tekst på fareknapp | 6,54 | 10,54 | 4,5 | Består |
| Feltkant mot bakgrunn | 3,47 | 3,78 | 3,0 | Består |
| Feltkant mot kort | 3,26 | 3,38 | 3,0 | Består |
| Fokusring (`accent`) mot bakgrunn | 5,12 | 8,51 | 3,0 | Består |
| Fokusring mot kort | 4,81 | 7,60 | 3,0 | Består |
| Fokusring mot infoflate | 4,42 | 6,61 | 3,0 | Består |
| Kantlinje (`border`) mot bakgrunn | 1,30 | 1,46 | — | Pynt. Ikke brukt på kontroller |
| **Kommende steg (`border`) mot bakgrunn** | **1,30** | **1,46** | 3,0 | **Svak** (M-1) |
| **Aktivt steg (aksent 50 %) mot bakgrunn** | **2,09** (`#8FBCBA`) | 3,03 (`#376C6A`) | 3,0 | **Brudd i lys** (M-1) |
| Aktivt steg mot kommende steg | 1,60 | 2,08 | 3,0 | Svak (M-1) |
| Aktivt steg mot fullført steg | 2,46 | 2,81 | 3,0 | Svak (M-1) |
| Fullført steg (`accent`) mot bakgrunn | 5,12 | 8,51 | 3,0 | Består |
| Målerfyll (`accent`) mot spor (`border`) | 3,94 | 5,84 | 3,0 | Består |
| Målerspor (`border`) mot kort | 1,22 | 1,30 | — | Pynt (L-3) |
| Deaktivert hovedknapp med `opacity: .5` (tekst/flate) | 2,09 | 3,06 | — | Unntatt, men «Jobber …» må leses (M-3) |
| Deaktivert hovedknapp med `opacity: .38` | 1,72 | 2,30 | — | Ikke bruk |

Aktivt steg er regnet som aksentfargen blandet 50/50 med bakgrunnen (`#FFFFFF` / `#121718`). Over kortflaten blir tallene nesten de samme (2,03 lys, 2,95 mørk).

**Avvik fra tabellen i `DESIGN.md`:** Tallene i `DESIGN.md` stemmer (avrundet). Tabellen der mangler radene for lenker (mot tekst og på infoflate), fokusringen, fremdriftslinjen, den stiplede brikken og den deaktiverte knappen. Disse bør legges til.
