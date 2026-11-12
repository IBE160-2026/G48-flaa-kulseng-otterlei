---
name: Søknadshjelpen (plassholder)
status: final
updated: 2026-11-12
sources:
  - ../../product-brief.md
  - ../../prd/prd.md
  - ../../prd/addendum.md
  - ../../prd/tilbakemelding-prd.md
  - ../../architecture/architecture-G48-flaa-kulseng-otterlei-2026-11-03/ARCHITECTURE-SPINE.md
---

# Søknadshjelpen: hvordan appen oppfører seg

_Laget med `bmad-ux` i grundig modus 2026-11-12. Henrik tok valgene, og Claude Code skrev dokumentet. Etter første utkast gikk tre KI-reviewere gjennom dokumentene (sjekkliste, tilgjengelighet og motstander, se [valideringsrapporten](validation-report.md)). Henrik endret deretter veiviseren fra seks til fire steg. Ole og Haakon gikk gjennom dokumentene i PR #15 2026-11-12. Vurderingene deres står under Åpne punkter. Alle beslutningene står med begrunnelse i [beslutningsloggen](.memlog.md). Claudes utfylling var merket «[ANTAKELSE]» i utkastet. Henrik godtok alle punktene 2026-11-12, og merkene er fjernet._

_AD-nummer viser til [arkitekturen](../../architecture/architecture-G48-flaa-kulseng-otterlei-2026-11-03/ARCHITECTURE-SPINE.md) (flettet i PR #13). PRD-en er rettet etter faglærers tilbakemelding i PR #14, og UX-en er sjekket mot den versjonen._

## Foundation

AI CV & Job Application Assistant er en **responsiv nettside** som brukes i nettleseren på både PC og mobil. Det finnes ingen egen mobilapp. Sidene er server-rendrede Django-maler med vanlig JavaScript, uten byggesteg, uten UI-rammeverk og uten ressurser fra nettet (AD-15). [DESIGN.md](DESIGN.md) beskriver hvordan appen ser ut, og dette dokumentet beskriver hvordan den fungerer.

Alt grensesnittet er på norsk (NFR-8). Språkvalget gjelder bare teksten KI skriver, så engelsk KI-tekst mellom norske knapper og overskrifter er tilsiktet.

**Målet for opplevelsen:** Emma skal føle at det er lett å lage søknaden, og at hun ikke må streve for å få den ferdig. Derfor er kjerneflyten en **veiviser med fire steg** som tar én ting om gangen. Høydepunktet er når utkastet er klart og alt hun trenger for å ta det med seg, ligger rett under.

## Information Architecture

Appen har én veiviser og tre sider rundt den. PRD-en (§6) har skjermbildene «Ny analyse» og «Resultat». Her er de erstattet av veiviseren (se [Avvik fra PRD og arkitektur](#avvik-fra-prd-og-arkitektur)).

| Side | Nås fra | Formål | Krav |
|---|---|---|---|
| Registrer | Forsiden for besøkende, lenke fra Logg inn | Lage konto med e-post, passord og avkrysning for personvern | FR-12, NFR-4 |
| Logg inn | Forsiden for besøkende, lenke fra Registrer | Logge inn | FR-13 |
| **Steg 1: CV** | Etter innlogging, «Start ny søknad» | Laste opp eller bekrefte CV, se og rette CV-teksten, eller (i testmodus) velge et eksempelpar | FR-1, FR-2, FR-10 |
| **Steg 2: Annonse og valg** | Steg 1 → Neste | Lime inn stillingsannonsen, velge språk og ønskede nøkkelord, og trykke «Analyser» | FR-3, FR-4, NFR-4 |
| **Steg 3: Analyse** | Steg 2 → Analyser | Gap-analyse og ATS-nøkkelordanalyse, CV-forslag, og valg av svarform og tone før «Lag søknad» | FR-5, FR-18 – FR-21, FR-4 |
| **Steg 4: Søknad** | Steg 3 → Lag søknad | Lese, rette og ta med seg søknadsbrevet eller brevforslagene, eller lage et nytt | FR-6 – FR-8, FR-22, FR-23 |
| Min konto | Topplinjen | Hva som lagres og sendes til KI, slette dokumenter og slette konto | FR-16, FR-17, NFR-4 |

### Hvilket steg brukeren står i

Steget leses av hvilke rader som finnes i databasen (AD-8). Det finnes aldri rester fra en forrige søknad, fordi «Start ny søknad» sletter analysen.

| Data som finnes | Siste steg brukeren kan nå | Etter innlogging havner brukeren i | Steg som er lenker i fremdriftslinjen |
|---|---|---|---|
| Ingen CV | 1 | Steg 1 | ingen |
| CV, ingen `Analyse` | 2 | Steg 1 med «Vil du bruke …?» | 1 |
| `Analyse`, ingen `Brev` | 3 | Steg 3 | 1, 2 |
| `Brev` | 4 | Steg 4 | 1, 2, 3 |

Et steg som ikke kan nås ennå, er ikke en lenke. Hvis noen skriver inn adressen direkte, sendes de til det siste steget de kan nå.

### Felles for alle sider

- **Topplinjen** (etter innlogging): appnavnet til venstre, som lenker til steget brukeren står i. Til høyre står «Min konto» som lenke og «Logg ut» som knapp i et lite skjema (`POST`), stylet som en lenke. Det finnes ingen hamburgermeny.
- **Testmodus-banneret** står øverst på alle sider, også før innlogging, så lenge testmodus er på (FR-9).
- **Sidetittel:** `<title>` er unik for hver side, for eksempel «Steg 3 av 4: Analyse – Søknadshjelpen». Hvis siden har feil, begynner tittelen med «Feil: ».
- **Landemerker:** først en «Hopp til innhold»-lenke, deretter `<header>` (banner og topplinje), `<nav aria-label="Fremdrift">` og `<main>`.

## Voice and Tone

Mikroteksten er **varm og hjelpsom**. Den bruker du-form og er litt oppmuntrende og forklarende, men kort. Appen snakker til en student som har dårlig tid. Tekstene er forslag i den tonen Henrik valgte, og endelig ordlyd settes når sidene lages.

| Gjør | Ikke gjør |
|---|---|
| «Lim inn annonsen, så ser vi hva den ber om.» | «Input stillingsannonse.» |
| «SQL står ikke i CV-en. Har du brukt det, er det lurt å få det med.» | «FEIL: SQL mangler.» |
| «Dette tar vanligvis 10–30 sekunder.» | «Vennligst vent …» |
| «Utkastet er klart. Les gjennom og tilpass det før du sender. Lykke til!» | «Søknaden er klar!» eller «Perfekt brev!» |
| «Vi fikk ikke svar fra KI-tjenesten. CV-en og valgene dine er tatt vare på, så du kan prøve igjen.» | «Error 503» eller «Noe gikk galt.» uten noen vei videre |
| «Feil e-post eller passord.» (samme melding uansett, FR-13) | «Det finnes ingen bruker med denne e-posten.» |
| Knapper med verb: «Analyser», «Lag søknad», «Last ned PDF» | «OK», «Send» eller «Fortsett» når det finnes et tydeligere verb |

**KI sier aldri at den er sikker.** Appen skryter aldri av brevet og sier aldri at det er ferdig til å sendes. Det KI har laget, kalles et *utkast* eller *forslag*. Det koden har telt, kan kalles et *resultat* (SM-C2).

## Component Patterns

Her står hvordan komponentene oppfører seg. Utseendet står i `DESIGN.md` under Components.

| Komponent | Brukes | Regler for oppførsel |
|---|---|---|
| **Fremdriftslinje** | Steg 1–4 | En `<ol>` med fire steg: CV, Annonse og valg, Analyse og Søknad. Stegnavnet vises alltid. På mobil står kortnavnet «Annonse», og det fulle navnet ligger i lenketeksten. Steg brukeren kan gå tilbake til (se tabellen over), er lenker med teksten «Steg 2: Annonse og valg (fullført)». Det aktive steget har `aria-current="step"`. Låste steg er tekst med «(ikke tilgjengelig ennå)» skjult for øyet. Hver lenke er minst 44 px høy. |
| **Tilbake / hovedknapp** | Steg 1–3 | «Tilbake» er en sekundærknapp til venstre, og hovedknappen står til høyre. Hovedknappen har et verb som sier hva som skjer: «Neste», «Analyser» eller «Lag søknad». Det er én hovedknapp per steg. |
| **CV-opplasting** | Steg 1 | Et filfelt (`<input type="file">` med `<label>`) som godtar `.pdf` og `.txt`. Det finnes ingen dra-og-slipp-sone. Fil og størrelse sjekkes i nettleseren og på serveren (NFR-3). Etter opplastingen viser steget CV-teksten i et redigerbart tekstfelt med overskriften «Sjekk at teksten ble riktig» (FR-2). Det er teksten der som analyseres. |
| **Bekreft lagret CV** | Steg 1 når en CV finnes | Overskriften er «Vil du bruke cv.pdf?». CV-teksten vises med en gang og kan rettes. Hovedknappen «Bruk denne og gå videre» går til steg 2, og sekundærknappen er «Last opp ny». Første utkast hadde to klikk her. Henrik godtok å slå dem sammen etter forslag fra review. |
| **Eksempelknapper** | Steg 1, bare i testmodus | «… eller prøv med et eksempel: [A] [B] [C]» står ved opplastingen. Et klikk fyller inn CV-teksten og blir stående i steg 1, slik at sensor ser at teksten er lest riktig, også fra to-kolonne-CV-en C (FR-2, SM-2). Annonsen fylles inn i steg 2. |
| **Annonsefelt** | Steg 2 | Et stort tekstfelt med en teller, «1 234 / 15 000 tegn» (telleren krever JavaScript). Under 100 eller over 15 000 tegn gir en feilmelding ved feltet og ingen KI-kall (FR-3). Ved tilbake fra steg 3 eller 4 er feltet fylt med annonsen fra analysen. |
| **Språk og nøkkelord** | Steg 2 | Språket (norsk/engelsk) er radioknapper i en `fieldset` med `legend`, og norsk er forhåndsvalgt (FR-4). Ønskede nøkkelord er et valgfritt tekstfelt med komma mellom ordene og maks 20 ord (AD-15). |
| **Personvernpåminnelse** | Steg 2, rett over «Analyser» | I KI-modus: «Når du trykker Analyser, sendes CV-teksten og annonsen til KI-tjenesten (Claude fra Anthropic). E-posten din sendes ikke. Les mer om personvern», med lenke til Min konto (NFR-4). I testmodus: «Testmodus: ingenting sendes til KI-tjenesten. Appen bruker lagrede svar.» |
| **Erstatte analysen** | Steg 2, når en analyse finnes | Endringer i annonse, språk eller nøkkelord gjelder først når «Analyser» trykkes. Rett over knappen står da: «Dette erstatter analysen og utkastet du har nå.» Det trengs ingen egen bekreftelse. Unntak: en endret CV-tekst i steg 1 sletter analysen med en gang (AD-8 `lagre_cv_tekst`), og da står det samme varselet over «Bruk denne og gå videre». |
| **KI-varsel** | Steg 3 øverst, og steg 4 over brevet | «KI kan gjøre feil – les gjennom før du sender.» (AD-5) |
| **KI-merke** | Alle kort | Kort med innhold fra KI (gap-analysen, forklaringen, CV-forslagene og brevet) har merket «Laget av KI». Nøkkelordkortet har merket «Telt automatisk». Slik ser Emma hva som er en vurdering og hva som er telt. |
| **Kravliste (gap-analyse)** | Steg 3 | Én rad per krav med ✓ «Matcher» eller ! «Mangler», og en begrunnelse som siterer CV-teksten (FR-5). Krav som matcher, står først. Overskriften oppsummerer: «2 av 4 krav dekket». |
| **Nøkkelordanalyse** | Steg 3 | Måleren viser «7 av 10 funnet», og under den står brikker for nøkkelord som finnes og som mangler. De som mangler, har stiplet kant. Under står `<details>` med «Hva betyr nøkkelordanalysen?», som åpner KI-forklaringen med forslag til omformuleringer (FR-21). Den er lukket som standard. |
| **CV-forslag** | Steg 3, under nøkkelordene | Knappen «Vis forslag til CV-en» henter forslagene (et KI-kall) og viser dem som en liste på samme side (FR-18). Hvert forslag viser til en del av CV-teksten. Krav som mangler, står som spørsmål: «Har du erfaring med SQL? I så fall bør det stå i CV-en.» |
| **Lag søknad** | Steg 3, nederst | Et kort med overskriften «Hvordan vil du ha søknaden?». Svarform er radioknapper med forklaring: «Fullt utkast – du får et brev du kan bygge videre på» og «Kun forslag – du får punkter, og skriver brevet selv». Tone er Formell eller Uformell. Første gang er fullt utkast og formell forhåndsvalgt (FR-4). Senere er verdiene fra det siste brevet valgt (AD-8). Under står hovedknappen «Lag søknad». |
| **Utkastet er klart** | Steg 4, øverst | Et ✓-merke med «Utkastet er klart» og «Les gjennom og tilpass det før du sender. Lykke til!». Ved kun forslag står det «Forslagene er klare» og «Bruk dem når du skriver brevet ditt. Lykke til!». Merket skaleres inn én gang når et nytt utkast er laget, og står stille ellers. |
| **Brev** | Steg 4 | Et redigerbart tekstfelt (`<textarea>`) med `lang` satt etter språket. Fullt utkast vises som avsnitt, kun forslag som en punktliste med «– ». Emma kan rette teksten. Endringene følger med kopiering og nedlasting, men **lagres ikke**. Over feltet står: «Endringene dine lagres ikke. Kopier eller last ned når du er ferdig.» |
| **Kopier** | Steg 4 | «Kopier teksten» kopierer innholdet i tekstfeltet, med endringene. «Kopiert!» meldes i et `aria-live`-område som finnes på siden fra før, og vises i 3 sekunder (FR-22). Knappen legges inn av JavaScript. Uten JavaScript kan teksten markeres og kopieres som vanlig. |
| **Last ned** | Steg 4 | Ved fullt utkast er det et lite skjema med Navn (påkrevd, `autocomplete="name"`), E-post (valgfri, `autocomplete="email"`) og Telefon (valgfri, `autocomplete="tel"`), teksten «Brukes bare i PDF-en og lagres ikke», og knappene «Last ned PDF» og «Last ned Markdown» (FR-23). Den redigerte teksten sendes med i samme `POST`. Ved kun forslag står bare knappene, og forslagene eksporteres som en punktliste. |
| **Lag nytt brev** | Steg 4, under nedlasting | Et sammenleggbart `<details>` med «Vil du ha et annet utkast?». Det inneholder Tone, Svarform og [Lag nytt brev]. Det nye brevet erstatter det gamle, og endringer i tekstfeltet går tapt. Det står rett over knappen. |
| **Start ny søknad** | Steg 4, nederst | Går til en bekreftelse: «Analysen og utkastet slettes. CV-en beholdes.» med [Start ny søknad] og [Avbryt]. Deretter kommer steg 1 med «Vil du bruke cv.pdf?». |
| **Slett-bekreftelse** | Min konto | «Slett mine dokumenter» og «Slett konto» går til en egen bekreftelsesside, «Er du sikker? Dette kan ikke angres», med en rød knapp og [Avbryt] (FR-16, FR-17). Bekreftelsen er en egen side i stedet for et dialogvindu, så den virker uten JavaScript. |
| **Feiloppsummering** | Alle skjemaer | Når et skjema vises på nytt med feil (AD-20), står det en boks øverst i `main` med overskriften «Noe må rettes» og en lenke til hvert felt med feil. Boksen får fokus når siden lastes. KI-feil vises i samme boks. |

## State Patterns

| Tilstand | Hvor | Hva brukeren ser |
|---|---|---|
| **Venter på KI** | «Analyser», «Lag søknad», «Lag nytt brev», «Vis forslag til CV-en» | Knappen får `aria-disabled="true"` (ikke `disabled`, så den beholder fokus) og viser «Jobber …» med en liten indikator. Nye trykk stoppes i JavaScript. Under knappen står «Dette tar vanligvis 10–30 sekunder». Teksten skrives inn i et `aria-live`-område som finnes på siden fra før (NFR-6, AD-12). |
| **KI svarte ikke eller ga feil** | Steg 2 → 3, steg 3 → 4, CV-forslag | Siden vises på nytt med feiloppsummeringen: «Vi fikk ikke svar fra KI-tjenesten. CV-en og valgene dine er tatt vare på, så du kan prøve igjen.» Fokus går til oppsummeringen. Ingenting er overskrevet (NFR-5, AD-12, AD-20). |
| **Forbruksgrensen er nådd** | Samme steder | «KI-tjenesten tar ikke imot flere forespørsler akkurat nå. Prøv igjen senere, eller bruk testmodus.» (NFR-9) |
| **En KI-forespørsel kjører allerede** | Samme steder (en annen fane) | «Du har allerede en forespørsel som jobber. Vent til den er ferdig.» (AD-12) |
| **Forklaringen feilet** | Steg 3 | Gap-analysen og nøkkelordene vises. I stedet for forklaringen står «Forklaringen kunne ikke lages» med [Prøv forklaringen igjen] (AD-8, `ki_status="forklaring_feilet"`). |
| **Egen CV i testmodus** | Steg 3 | Nøkkelordene vises uten forklaring. Der gap-analysen stod, står: «Testmodus: KI-svar finnes bare for eksempelparene. Legg inn en API-nøkkel for å analysere din egen CV.» med lenke til README (FR-11). «Lag søknad» og «Vis forslag til CV-en» er byttet ut med hovedknappen «Prøv eksempel A». |
| **Egne nøkkelord på eksempelpar i testmodus** | Steg 3 | Den lagrede forklaringen vises med merknaden «KI-forklaringen gjelder ikke dine egne nøkkelord i testmodus.» Nøkkelordene telles i kode uansett (AD-7). |
| **Ugyldig fil** | Steg 1 | Feiloppsummering og melding ved feltet: «Bare PDF og TXT kan lastes opp.» eller «Filen er større enn 5 MB.» (FR-1) |
| **PDF uten tekst** | Steg 1 | «Vi fant ingen tekst i PDF-en. Er den skannet? Prøv en PDF laget fra et tekstprogram, eller en TXT-fil.» (FR-1) |
| **Annonsen er for kort eller for lang** | Steg 2 | «Annonsen må ha minst 100 tegn.» eller «Annonsen kan ha maks 15 000 tegn.» (FR-3) |
| **Steg som ikke kan nås** | Direkte adresse | Brukeren sendes til det siste steget hun kan nå (se tabellen under Information Architecture). |
| **Tilbakeknappen i nettleseren** | Alle steg | Hvert steg er en `GET`-side. Alle skjemaer bruker Post/Redirect/Get: et vellykket `POST` sender brukeren videre til adressen for neste steg. Tilbakeknappen viser derfor alltid forrige steg med lagrede verdier og sender aldri et KI-kall på nytt. Unntaket er skjemaer som vises på nytt med feil (AD-20). |
| **Økten har utløpt** | Alle skjemaer | Brukeren sendes til Logg inn med meldingen: «Du ble logget ut. Logg inn igjen. Det du limte inn, ble ikke lagret.» |
| **Feil ved innlogging eller registrering** | Logg inn, Registrer | «Feil e-post eller passord.», «Denne e-posten er allerede registrert.», «Passordet må ha minst 8 tegn.» eller «Du må krysse av for at du har lest om personvern.» (FR-12, FR-13) |
| **Sletting utført** | Min konto, eller Logg inn etter sletting av konto | «Dokumentene dine er slettet.» eller «Kontoen din er slettet.» |

## Interaction Primitives

- **Klikk og trykk** på knapper og lenker. Alle trykkflater er minst 44 × 44 px, også lenkene i topplinjen og i fremdriftslinjen.
- **Tastatur:** Tab følger leserekkefølgen, og Enter sender skjemaet. Det finnes ingen egne hurtigtaster.
- **Én ting om gangen.** Hvert steg er én side med én hovedhandling.
- **Fungerer i hovedsak uten JavaScript.** Alt er vanlige skjemaer med Post/Redirect/Get. JavaScript brukes bare til venteknappen (`skjema.js`, AD-12), kopieringsknappen og annonsetelleren. Uten JavaScript virker resten av appen.
- **Ikke tillatt:** dialogvinduer (popup), uendelig rulling, dra og slipp som eneste måte å laste opp på, og handlinger som bare vises når musepekeren holdes over.

## Accessibility Floor

Målet er WCAG 2.1 AA der det er rimelig (NFR-7). Kontrasten står i `DESIGN.md`, og detaljene står i [tilgjengelighetsreviewen](review-tilgjengelighet.md).

- **Sidestruktur:** hver side har en unik `<title>`, en «Hopp til innhold»-lenke og landemerkene `header`, `nav` og `main`. Hver side har én `h1`, og det er stegtittelen.
- **Skjema:** alle felt har en synlig `<label>`. Radioknapper står i `fieldset` med `legend`. Feltene for navn, e-post, telefon og passord har `autocomplete`. Påkrevde felt er merket i teksten, ikke bare med `*`.
- **Feil:** feilmeldinger står under feltet og er koblet til det med `aria-describedby` og `aria-invalid="true"`. Feiloppsummeringen øverst får fokus. Uten feil går fokus til `h1` når et nytt steg er lastet.
- **Statusmeldinger** («Jobber …», «Kopiert!») skrives inn i et `aria-live="polite"`-område som finnes i HTML-en fra start.
- **Fremdriftslinjen** er en `<nav aria-label="Fremdrift">` med `<ol>`. Hvert steg har et navn som en skjermleser kan lese opp, sammen med status (fullført, aktivt eller ikke tilgjengelig ennå). Strekene er pynt med `aria-hidden`.
- **Farge er aldri eneste kjennetegn:** «Matcher» og «Mangler» har symbol og tekst. Lenker er alltid understreket. Nøkkelord som mangler, har stiplet kant.
- **Språk:** siden har `lang="nb"`. Alle blokker med KI-tekst (gap-analysen, forklaringen, CV-forslagene og brevet) får `lang` etter valgt språk.
- **`<summary>`** bruker den innebygde markøren, ikke tegnet «▸» i teksten.
- **Bevegelse:** animasjonen av ✓-merket slås av ved `prefers-reduced-motion`.
- **Zoom og reflow:** siden virker fra 320 px bredde og med 200 % zoom uten vannrett rulling. Skriftstørrelser oppgis i `rem`. Tekstbeholdere har `min-height`, aldri fast `height` eller `overflow: hidden`.
- **Tvungne farger** (Windows høykontrast): streker, måler og ikoner får en kant under `@media (forced-colors: active)`, og fokus vises med `outline`.

## Responsive & Platform

Det er samme oppsett på alle skjermer: **én midtstilt kolonne på maks 720 px**.

| Bredde | Hva som skjer |
|---|---|
| 320–599 px (mobil) | Sidemarg 16 px. Fremdriftslinjen viser kortnavn. Tilbake og hovedknappen står i én rad, og hovedknappen er bredest. |
| 600 px og bredere (nettbrett og PC) | Sidemarg 24 px. Kolonnen er midtstilt med mer luft rundt. Fremdriftslinjen viser fulle stegnavn. |

Appen er laget for nettleseren. Den lages ikke som installerbar app (PWA) og virker ikke uten nett.

## Testmodus

Testmodus er laget for sensor (UJ-3) og for de automatiske testene.

- Banneret står øverst på **alle** sider: «Testmodus: appen bruker lagrede KI-svar. Prøv eksempel A, B eller C i steg 1.» (FR-9)
- Eksempelknappene står bare i steg 1 (FR-10).
- Personvernpåminnelsen sier at ingenting sendes (se Component Patterns).
- Med eksempelpar går hele veiviseren som vanlig, med lagrede svar.
- Med egen CV kommer brukeren til steg 3, med forklaring og «Prøv eksempel A» (se State Patterns).
- En egen CV erstatter eksempel-CV-en og resultatet (FR-1).

## Personvern i grensesnittet

- **Registrering:** en avkrysning, «Jeg har lest hvordan appen behandler CV-en min», med lenke til en kort forklaring. Kontoen kan ikke lages uten avkrysningen.
- **Steg 2:** en påminnelse rett over «Analyser» (se Component Patterns).
- **Steg 4:** «Brukes bare i PDF-en og lagres ikke» ved avsenderfeltene, og «Endringene dine lagres ikke» ved brevet.
- **Min konto** forklarer med enkle ord:
  - hva som lagres: siste CV, CV-tekst, annonse og resultat, kryptert
  - hvor lenge det lagres: til du sletter det
  - hva som sendes til KI-tjenesten: CV-tekst, annonse og valg, aldri e-post eller passord
  - hvem KI-tjenesten er
  - at du kan slette alt når som helst (NFR-4, PRD §4.5)

## Key Flows

Personene og reisene er de samme som i PRD-en (§2.3).

### UJ-1. Emma tilpasser søknaden til en sommerjobb (kjerneflyten)

_Emma studerer IT. Det er tirsdag kveld, og søknadsfristen for sommerjobben som junior utvikler er i morgen. Hun bruker PC-en sin._

1. Emma registrerer seg med e-post og passord, krysser av for at hun har lest om personvern, og blir logget inn. Hun havner i **steg 1**.
2. Hun laster opp CV-en som PDF. Under «Sjekk at teksten ble riktig» ser hun at alt er med, og trykker **Neste**.
3. **Steg 2:** Hun limer inn annonseteksten. Norsk er allerede valgt. Hun leser påminnelsen om at teksten sendes til KI-tjenesten, og trykker **Analyser**. Knappen viser «Jobber …».
4. **Steg 3:** Øverst står «KI kan gjøre feil – les gjennom før du sender». Overskriften er «2 av 4 krav dekket». Python og Git matcher, med sitater fra CV-en. SQL og førerkort klasse B mangler. Nøkkelordkortet er merket «Telt automatisk», og der mangler også «SQL». Nederst står «Fullt utkast» og «Formell» allerede valgt. Hun trykker **Lag søknad**.
5. **Klimaks, steg 4:** Et ✓ skaleres rolig inn: «Utkastet er klart. Les gjennom og tilpass det før du sender. Lykke til!». Brevet ligger rett under. Det trekker fram Python-prosjektene og sier at hun gjerne vil lære SQL, uten å påstå at hun kan det. Hun leser det og retter en setning om bachelorprosjektet slik hun vil ha den. Så trykker hun **Kopier teksten**, ser «Kopiert!» og limer brevet inn i søknadsskjemaet. Fra innlogging har det tatt fire klikk.

**Avvik:** KI-tjenesten svarer ikke etter «Analyser». Steg 2 vises på nytt med «Vi fikk ikke svar fra KI-tjenesten. CV-en og valgene dine er tatt vare på, så du kan prøve igjen» øverst. Annonsen står fortsatt i feltet. Hun trykker **Analyser** igjen og kommer videre.

### UJ-2. Jonas vil skrive selv, men på engelsk

_Jonas studerer logistikk og søker et graduate-program med engelsk annonse. Han bruker telefonen på bussen. Han har brukt appen før._

1. Jonas logger inn og havner i steg 4 med forrige utkast. Han trykker **Start ny søknad** og bekrefter at analysen og utkastet slettes.
2. **Steg 1:** «Vil du bruke cv-jonas.pdf?» står med CV-teksten under. Han trykker **Bruk denne og gå videre**.
3. **Steg 2:** Han limer inn den engelske annonsen, velger **engelsk** og trykker **Analyser**.
4. **Steg 3:** Gap-analysen er på engelsk. Blant nøkkelordene har «SAP» stiplet kant. Han trykker **Vis forslag til CV-en** og ser hvordan lagerjobben kan beskrives tydeligere. SAP står som et spørsmål: «Have you used SAP?». Nederst velger han **Kun forslag** og **Uformell**, og trykker **Lag søknad**.
5. **Klimaks, steg 4:** «Forslagene er klare. Bruk dem når du skriver brevet ditt.» Han får en punktliste på engelsk der hvert punkt viser til lagerjobben eller studiet. Han trykker **Last ned Markdown** og skriver brevet selv senere.

### UJ-3. Sensor prøver appen uten API-nøkkel

1. Sensor starter appen etter README-en, uten nøkkel. Banneret sier at appen kjører i testmodus.
2. Sensor registrerer en bruker. I **steg 1** trykker sensor på **C**, ser at teksten fra to-kolonne-CV-en er lest riktig, og trykker **Neste**.
3. **Steg 2:** Annonsen er fylt inn. Påminnelsen sier at ingenting sendes i testmodus. Sensor trykker **Analyser**.
4. Sensor går gjennom steg 3 og 4 med lagrede svar, og laster ned PDF-en med en avsender.
5. **Klimaks:** Sensor er kommet til «Utkastet er klart» uten nøkkel, uten kostnad og uten feil (SM-10).
6. Sensor starter en ny søknad og laster opp en egen CV, som erstatter eksempelet. Teksten vises og nøkkelordene telles. I steg 3 forklarer appen at KI-svar bare finnes for eksempelparene, og hvordan en API-nøkkel legges inn. Hovedknappen er nå «Prøv eksempel A» (FR-11).

### UJ-4. Emma sletter dataene sine

1. Søknadsfristen er passert. Emma trykker **Min konto** i topplinjen.
2. Hun leser hva som er lagret, og trykker **Slett mine dokumenter**.
3. Bekreftelsessiden sier: «Er du sikker? CV-en, annonsen og resultatet slettes, og det kan ikke angres.» Hun trykker den røde knappen.
4. **Klimaks:** «Dokumentene dine er slettet.» Neste gang hun logger inn, starter hun i steg 1 uten noen CV.
5. Senere sletter hun hele kontoen på samme måte. Hun blir logget ut, og e-posten kan registreres på nytt (FR-17).

## Kutt i grensesnittet

Gruppas svar på faglærers punkt 4.2 er nødplanen i PRD-en (§8.1). Er ikke kjerneflyten P1–P5 ferdig og testet 2. desember, kuttes i denne rekkefølgen:

1. brevoppsettet i PDF
2. CV-forbedringsforslag (P6)
3. KI-forklaringen i ATS-analysen

Arkitekturen merker i tillegg hash-testen av promptene som mulig kutt (AD-6). Listen under er **kutt i grensesnittet**. Den kommer i tillegg til nødplanen og erstatter den ikke. _Den er et forslag, og gruppa bekrefter den i pull requesten._

**Må være med** (kjerneflyten og det kurset vurderer):

- de fire stegene med lagrede svar i testmodus
- feiltilstandene for KI
- personvernpåminnelsen
- KI-varselet og KI-merkene
- Min konto med sletting
- etiketter, tastatur og kontrast

**Kan kuttes, i denne rekkefølgen, hvis tiden blir knapp:**

1. Animasjonen av ✓-merket. Merket står stille i stedet.
2. Mørk modus. Bare lys modus, men tokenene beholdes.
3. «Prøv forklaringen igjen». Bare meldingen vises.
4. Redigering av brevet. Brevet vises som tekst med «Kopier og tilpass det i ditt eget program».
5. «Lag nytt brev» i steg 4. Brukeren går tilbake til steg 3 i stedet.
6. Annonsetelleren.

## Inspiration & Anti-patterns

- **Ønsket:** Henrik liker apper som er **ryddige, og der det er lett å finne fram**. Det er grunnen til veiviseren, én hovedknapp per steg og én smal kolonne.
- **Valgt bort: seks steg.** Første utkast hadde seks steg (CV, Annonse, Valg, Analyse, Søknad, Ferdig). Reviewerne viste at det ga 8–9 klikk, et steg som ikke lagret noe («Ser bra ut»), og en annonse som måtte lagres i økten, noe AD-10 forbyr. Henrik valgte fire steg.
- **Valgt bort: alt på én side, én side som vokser, og faner på resultatet.** Henrik valgte steg for steg, fordi det gir én ting om gangen og viser hvor langt man har kommet.
- **Valgt bort: designretningen «Stram»** (svart-hvitt med skarpe hjørner). Den virket for streng.
- **Valgt bort: «Søknaden er klar» og «Ser bra ut».** Begge lovet mer enn et KI-utkast kan stå inne for.
- **Avvist: chatbot-stil** (PRD §7). Brukeren skriver ikke til KI, hun fyller ut skjemaer og leser resultater.
- **Avvist: poengsum for sjansen til å få jobben** (PRD §7). Nøkkelordmåleren viser bare en andel.

## Avvik fra PRD og arkitektur

PRD-en ble rettet i PR #14 etter faglærers tilbakemelding. Den samsvarer nå med UX-en på flere punkter:

- tone og svarform velges ved brevet (FR-4)
- et nytt brev overskriver bare brevet
- varselet «KI kan gjøre feil» (NFR-4, §6)
- CV-forbedringene står ved gap-analysen (§6)
- det finnes en nødplan (§8.1)

Disse punktene gjenstår. Claude anbefalte å ta dem i en egen pull request etter at gruppa har godkjent UX-en. Det er gruppa som bestemmer.

**PRD:**

1. **§6 Skjermbilder:** «Ny analyse» er delt i steg 1 (CV) og steg 2 (Annonse og valg). «Resultat» er delt i steg 3 (Analyse, med valg av tone og svarform og CV-forslag) og steg 4 (Søknad, med brevet, kopiering og eksport).
2. **FR-12 Registrere konto:** en ny konsekvens er avkrysningen for personvern.
3. **FR-6 og FR-7:** en ny konsekvens er at brevet kan redigeres før kopiering og eksport, men at endringene ikke lagres.
4. **«Start ny søknad»:** sletter analysen, brevet og CV-forslagene, mens CV-en beholdes. Det er en ny handling i forhold til §3 og FR-16.

**Arkitektur:**

1. **URL-er (§3 Konvensjoner):** veiviseren bruker adressene som finnes. Steg 1 er `/cv/`, steg 2 er `/analyse/` (skjemaet), steg 3 er `/resultat/` og steg 4 er `/resultat/brev/`. «Start ny søknad» trenger et nytt `POST`-endepunkt som sletter `Analyse` og sender brukeren til `/cv/`.
2. **`/resultat/cv-forbedring/`** er et `POST`-endepunkt som sender brukeren tilbake til `/resultat/`.
3. **Steg 2 skal kunne fylles ut på nytt:** ved tilbake fra steg 3 må `/analyse/` vise annonsen, språket og nøkkelordene fra den lagrede `Analyse`.
4. **Ved `lagre_cv_tekst` (AD-8)** vises et varsel i steg 1 før en analyse slettes.
5. **Eksport (`/resultat/brev/eksport/`)** tar imot den redigerte teksten fra skjemaet og bruker den i stedet for `Brev`, uten å lagre den.
6. **Personvernvarselet i AD-5** gjelder i KI-modus. I testmodus står en egen tekst.

## Visuelle referanser

Nøkkelskjermene ligger i `mockups/`. De viser mobilbredde i lys og mørk modus. Dokumentene her går foran mockupene hvis de er uenige.

- [`mockups/key-steg1-testmodus.html`](mockups/key-steg1-testmodus.html): steg 1 med eksempelknapper, og en lagret CV
- [`mockups/key-steg2-annonse.html`](mockups/key-steg2-annonse.html): steg 2 med personvernpåminnelse og ventetilstand
- [`mockups/key-steg3-analyse.html`](mockups/key-steg3-analyse.html): steg 3 med KI-merker, CV-forslag og «Lag søknad» med valg av svarform
- [`mockups/key-steg4-soknad.html`](mockups/key-steg4-soknad.html): steg 4 med «Utkastet er klart», redigerbart brev og nedlasting
- Designretningene: [runde 1](.working/directions-1.html) og [runde 2](.working/directions-2.html). `.working/` er prosesshistorikk og viser hvordan retningen ble valgt. De første mockupene, med seks steg, er slettet. De finnes i git-historikken (commit `28fb5f0`).

## Åpne punkter

- **Appnavn:** «Søknadshjelpen» er en plassholder. Gruppa bestemmer navnet.
- ~~**[ANTAKELSE]-punkter**~~ **Løst 2026-11-12:** Henrik godtok alle Claudes antakelser: farger for fare og info, typografistørrelser, avstander, egen bekreftelsesside for sletting og ordlyden ved forbruksgrensen. Merkene er fjernet. Ole og Haakon kan si fra i PR #15 hvis de er uenige.
- ~~**Gruppas godkjenning**~~ **Løst 2026-11-12:** Ole og Haakon gikk gjennom PR #15. Ole er enig i fire steg og i at «Start ny søknad» sletter analysen. Haakon er enig i det samme, liker stilen «C dempet», synes «Søknadshjelpen» er greit som navn, og godtar alle antakelsene.
