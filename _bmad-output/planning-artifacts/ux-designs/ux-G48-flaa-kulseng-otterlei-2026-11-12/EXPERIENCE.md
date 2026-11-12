---
name: Søknadshjelpen (plassholder)
status: draft
updated: 2026-11-12
sources:
  - ../../product-brief.md
  - ../../prd/prd.md
  - ../../prd/addendum.md
  - ../../prd/tilbakemelding-prd.md
  - ../../architecture/architecture-G48-flaa-kulseng-otterlei-2026-11-03/ARCHITECTURE-SPINE.md
---

# Søknadshjelpen: hvordan appen oppfører seg

_Laget med `bmad-ux` i grundig modus 2026-11-12. Henrik tok valgene, og Claude Code skrev dokumentet. Alle beslutningene står med begrunnelse i [beslutningsloggen](.memlog.md). Punkter merket **[ANTAKELSE]** er Claudes utfylling og er ikke bekreftet. Gruppa må gå gjennom dem i pull requesten._

## Foundation

AI CV & Job Application Assistant er en **responsiv nettside** som brukes i nettleseren på både PC og mobil. Det finnes ingen egen mobilapp. Sidene er server-rendrede Django-maler med vanlig JavaScript, uten byggesteg og uten ressurser fra nettet (arkitekturen, AD-15). Appen bruker ikke noe UI-rammeverk. [DESIGN.md](DESIGN.md) beskriver hvordan appen ser ut, og dette dokumentet beskriver hvordan den fungerer.

Alt brukeren ser, er på norsk (NFR-8). Språkvalget i steg 3 gjelder bare teksten KI skriver.

**Målet for opplevelsen:** Emma skal føle at det er lett å lage søknaden, og at hun ikke må streve for å få den ferdig. Derfor er kjerneflyten en **veiviser med seks steg** som tar én ting om gangen. Høydepunktet er steg 6, når søknaden er ferdig og alt er gjort.

## Information Architecture

Appen har én veiviser og tre sider rundt den. PRD-en (§6) deler den opp i «Ny analyse» og «Resultat», men her er de to skjermbildene erstattet med veiviseren (se [Avvik fra PRD og arkitektur](#avvik-fra-prd-og-arkitektur)).

| Side | Nås fra | Formål | Krav |
|---|---|---|---|
| Registrer | Forsiden for besøkende, lenke fra Logg inn | Lage konto med e-post, passord og en avkrysning for personvern | FR-12, NFR-4 |
| Logg inn | Forsiden for besøkende, lenke fra Registrer | Logge inn | FR-13 |
| **Veiviser, steg 1: CV** | Etter innlogging, «Start ny søknad» | Laste opp eller bekrefte CV, se og rette CV-teksten, eller (i testmodus) velge et eksempelpar | FR-1, FR-2, FR-10 |
| **Steg 2: Annonse** | Steg 1 → Neste | Lime inn stillingsannonsen | FR-3 |
| **Steg 3: Valg** | Steg 2 → Neste | Velge språk, tone og svarform, skrive inn ønskede nøkkelord, se personvernpåminnelsen og trykke «Analyser» | FR-4, NFR-4 |
| **Steg 4: Analyse** | Steg 3 → Analyser | Gap-analyse og ATS-nøkkelordanalyse, med forklaringen sammenlagt | FR-5, FR-19 – FR-21 |
| **Steg 5: Søknad** | Steg 4 → Lag søknad | Lese og godkjenne søknadsbrevet eller brevforslagene, og eventuelt lage et nytt med en annen tone eller svarform | FR-6 – FR-8 |
| **Steg 6: Ferdig** | Steg 5 → Ser bra ut | Kopiere og eksportere, se CV-forbedringer og starte en ny søknad | FR-18, FR-22, FR-23 |
| Min konto | Topplinjen | Hva som lagres og sendes til KI, slette dokumenter og slette konto | FR-16, FR-17, NFR-4 |

**Topplinjen** (på alle sider etter innlogging) har appnavnet til venstre, som lenker til gjeldende steg i veiviseren. Til høyre står «Min konto» og «Logg ut» som tekstlenker, også på mobil. Det finnes ingen hamburgermeny.

**Testmodus-banneret** står øverst på alle sider, også før innlogging, så lenge testmodus er på (FR-9).

**Hvor brukeren havner etter innlogging** [ANTAKELSE]: Har hun ikke noen analyse, kommer hun til steg 1. Har hun en lagret analyse, kommer hun til det siste steget hun har nådd, slik at Emma kan fortsette der hun slapp.

## Voice and Tone

Mikroteksten er **varm og hjelpsom**. Den bruker du-form og er litt oppmuntrende og forklarende, men kort. Appen snakker til en student som har dårlig tid, ikke til en ekspert. Tekstene i tabellen er forslag i den tonen Henrik valgte. Endelig ordlyd bestemmes når sidene lages.

| Gjør | Ikke gjør |
|---|---|
| «Lim inn annonsen, så ser vi hva den ber om.» | «Input stillingsannonse.» |
| «SQL står ikke i CV-en. Har du brukt det, er det lurt å få det med.» | «FEIL: SQL mangler.» |
| «Dette tar vanligvis 10–30 sekunder.» | «Vennligst vent …» |
| «KI kan gjøre feil – les gjennom før du sender.» | Ikke si noe om at KI kan ta feil. |
| «Søknaden er klar. Lykke til med søknaden!» | «🎉🎉 Supert!!! Du er rå!» |
| «Vi fikk ikke svar fra KI-tjenesten. CV-en og valgene dine er tatt vare på, så du kan prøve igjen.» | «Error 503» eller «Noe gikk galt.» uten noen vei videre |
| «Feil e-post eller passord.» (samme melding uansett, FR-13) | «Det finnes ingen bruker med denne e-posten.» |
| Knapper med verb: «Analyser», «Lag søknad», «Last ned PDF» | Knapper som «OK», «Send» eller «Fortsett» når det finnes et tydeligere verb |

Appen skryter aldri av brevet. Den sier ikke at brevet er «perfekt» eller «sterkt». Kontrollen ligger hos Emma (SM-C2).

## Component Patterns

Her står hvordan komponentene oppfører seg. Utseendet står i `DESIGN.md` under Components.

| Komponent | Brukes | Regler for oppførsel |
|---|---|---|
| **Fremdriftslinje** | Steg 1–6 | Viser seks steg og teksten «Steg N av 6 · Navn». **Fullførte steg er lenker** du kan hoppe tilbake til. Kommende steg er låst. Endrer brukeren CV-en eller annonsen i et tidligere steg, slettes analysen (AD-8), og steg 4–6 blir låst igjen. Appen sier fra om dette før endringen lagres (se State Patterns). |
| **Tilbake / Neste** | Steg 1–5 | «Tilbake» er en sekundærknapp til venstre, og hovedknappen står til høyre. Hovedknappen har et verb som sier hva som skjer: «Neste», «Analyser», «Lag søknad» eller «Ser bra ut». Det er én hovedknapp per steg. |
| **CV-opplasting** | Steg 1 | Et filfelt som godtar `.pdf` og `.txt`. Fil og størrelse sjekkes i nettleseren og på serveren (NFR-3). Etter opplastingen viser steget CV-teksten i et redigerbart tekstfelt med overskriften «Sjekk at teksten ble riktig» (FR-2). Endringer der er det som analyseres. |
| **Bekreft lagret CV** | Steg 1 når en CV finnes | «Vil du bruke cv.pdf?» med [Bruk denne] og [Last opp ny]. «Bruk denne» viser CV-teksten slik at den kan rettes, og så kommer «Neste». |
| **Eksempelknapper** | Steg 1, bare i testmodus | «… eller prøv med et eksempel: [A] [B] [C]» står ved opplastingen. Et klikk fyller inn CV-tekst og annonse og hopper til steg 3 (FR-10). |
| **Annonsefelt** | Steg 2 | Et stort tekstfelt med en teller, «1 234 / 15 000 tegn». Under 100 eller over 15 000 tegn gir en melding ved feltet og ingen KI-kall (FR-3). |
| **Valg** | Steg 3, og deler av det i steg 5 | Språk, tone og svarform er radioknapper i grupper (`fieldset` med `legend`). Forhåndsvalgt er norsk, formell og fullt utkast (FR-4). **Svarform** har en forklaring på hvert valg: «Fullt utkast – du får et ferdig brev du kan bygge videre på» og «Kun forslag – du får punkter, og skriver brevet selv». Ønskede nøkkelord er et valgfritt tekstfelt med komma mellom ordene og maks 20 ord (AD-15). |
| **Personvernpåminnelse** | Steg 3, rett over «Analyser» | «Når du trykker Analyser, sendes CV-teksten og annonsen til KI-tjenesten (Claude fra Anthropic). E-posten din sendes ikke. Les mer» – lenken går til Min konto (NFR-4). |
| **Kravliste (gap-analyse)** | Steg 4 | Én rad per krav med ✓ «Matcher» eller ! «Mangler», og en begrunnelse som siterer CV-teksten (FR-5). Krav som matcher, står først. Overskriften oppsummerer: «2 av 4 krav dekket». |
| **Nøkkelordanalyse** | Steg 4 | En måler som viser «7 av 10 funnet» og brikker for nøkkelord som finnes og som mangler (de som mangler, har stiplet kant). Under står `<details>` med «▸ Hva betyr dette?», som åpner KI-forklaringen med forslag til omformuleringer (FR-21). Den er lukket som standard og trenger ikke JavaScript. |
| **Brevvisning** | Steg 5 og 6 | Fullt utkast vises som avsnitt i et kort, og kun forslag som en punktliste. Over brevet står varselet «KI kan gjøre feil – les gjennom før du sender». |
| **Lag nytt brev** | Steg 5, under brevet | En linje med Tone [Formell/Uformell], Svarform [Fullt utkast/Kun forslag] og [Lag nytt brev]. Forhåndsvalgt er det som ble valgt i steg 3, eller verdiene fra det siste brevet (AD-8). Det nye brevet erstatter det gamle. |
| **Ferdig-merke** | Steg 6 | Et stort ✓ med «Søknaden er klar» (eller «Forslagene er klare» ved kun forslag) og «Lykke til med søknaden!». En kort animasjon spilles én gang. |
| **Kopier** | Steg 6 | «Kopier teksten» kopierer brevet eller punktlisten. Bekreftelsen «Kopiert!» meldes med `aria-live` og vises i 3 sekunder (FR-22). |
| **PDF-avsender** | Steg 6, bare ved fullt utkast | Et lite skjema rett over «Last ned PDF» med Navn (påkrevd), E-post (valgfri) og Telefon (valgfri), og teksten «Brukes bare i PDF-en og lagres ikke» (FR-23). Ved kun forslag står «Last ned PDF» uten skjemaet, og forslagene eksporteres som en punktliste. |
| **Last ned Markdown** | Steg 6 | En sekundærknapp ved siden av PDF-knappen (FR-23). |
| **CV-forbedringer** | Steg 6 | Knappen «Vis forslag til CV-en» henter forslagene (et KI-kall) og viser dem som en liste under brevet, på samme side (FR-18). Hvert forslag viser til en del av CV-teksten. Krav som mangler, står som spørsmål: «Har du erfaring med SQL? I så fall bør det stå i CV-en.» |
| **Start ny søknad** | Steg 6 | Går til steg 1 med «Vil du bruke cv.pdf?». Den gamle analysen beholdes til en ny analyse kjøres (AD-8). |
| **Slett-bekreftelse** | Min konto | «Slett mine dokumenter» og «Slett konto» går til en egen bekreftelsesside, «Er du sikker? Dette kan ikke angres», med en rød knapp og [Avbryt] (FR-16, FR-17). [ANTAKELSE: egen side i stedet for et dialogvindu, så det virker uten JavaScript.] |

## State Patterns

| Tilstand | Hvor | Hva brukeren ser |
|---|---|---|
| **Venter på KI** | «Analyser», «Lag søknad», «Lag nytt brev», «Vis forslag til CV-en» | Knappen deaktiveres og viser «Jobber …» med en liten indikator. Under knappen står «Dette tar vanligvis 10–30 sekunder». Statusen meldes med `aria-live`. Et dobbeltklikk gir ikke to kall (NFR-6, AD-12). |
| **KI svarte ikke eller ga feil** | Steg 3 → 4, steg 4 → 5, steg 6 | En melding over knappen: «Vi fikk ikke svar fra KI-tjenesten. CV-en og valgene dine er tatt vare på, så du kan prøve igjen.» Knappen blir aktiv igjen. Ingenting er overskrevet (NFR-5, AD-12). |
| **Forbruksgrensen er nådd** | Samme steder | «KI-tjenesten tar ikke imot flere forespørsler akkurat nå. Prøv igjen senere, eller bruk testmodus.» (NFR-9) [ANTAKELSE: ordlyden] |
| **En KI-forespørsel kjører allerede** | Samme steder (en annen fane) | «Du har allerede en forespørsel som jobber. Vent til den er ferdig.» (AD-12) |
| **Forklaringen feilet** | Steg 4 | Gap-analysen og nøkkelordene vises som vanlig. I stedet for «Hva betyr dette?» står «Forklaringen kunne ikke lages» med [Prøv forklaringen igjen] (AD-8, `ki_status="forklaring_feilet"`). |
| **Egen CV i testmodus** | Steg 4, 5 og 6 | Nøkkelordene vises uten forklaring. Der gap-analysen, brevet eller CV-forbedringene skulle stått, står: «Testmodus: KI-svar finnes bare for eksempelparene. Legg inn en API-nøkkel for å analysere din egen CV.» med en lenke til README (FR-11). Steg 5 og 6 kan da ikke fullføres, og appen foreslår å prøve eksempel A. |
| **Ugyldig fil** | Steg 1 | Ved feltet: «Bare PDF og TXT kan lastes opp.» eller «Filen er større enn 5 MB.» (FR-1) |
| **PDF uten tekst** | Steg 1 | «Vi fant ingen tekst i PDF-en. Er den skannet? Prøv en PDF laget fra et tekstprogram, eller en TXT-fil.» (FR-1) |
| **Annonsen er for kort eller for lang** | Steg 2 | Ved feltet: «Annonsen må ha minst 100 tegn.» eller «Annonsen kan ha maks 15 000 tegn.» Telleren blir oransje (FR-3). |
| **Endring som sletter analysen** | Steg 1 og 2 når en analyse finnes | Før lagring: «Hvis du endrer CV-en eller annonsen, må du analysere på nytt. Brevet og forslagene forsvinner.» med [Endre likevel] og [Avbryt]. [ANTAKELSE: formen, enten en egen melding på siden eller et bekreftelsessteg.] |
| **Låste steg** | Fremdriftslinjen | Kommende steg er ikke lenker. Prøver noen å gå rett til adressen, sendes de til det siste steget de har nådd. |
| **Feil ved innlogging eller registrering** | Logg inn, Registrer | «Feil e-post eller passord.» eller «Denne e-posten er allerede registrert.» eller «Passordet må ha minst 8 tegn.» (FR-12, FR-13) |
| **Sletting utført** | Min konto, eller Logg inn etter sletting av konto | «Dokumentene dine er slettet.» eller «Kontoen din er slettet.» |
| **Kopiert** | Steg 6 | «Kopiert!» ved knappen i 3 sekunder (FR-22). |

## Interaction Primitives

- **Klikk og trykk** på knapper og lenker. Alle trykkflater er minst 44 × 44 px.
- **Tastatur:** Tab følger leserekkefølgen, og Enter sender skjemaet. Det finnes ingen egne hurtigtaster.
- **Én ting om gangen.** Hvert steg er én side med én hovedhandling.
- **Fungerer uten JavaScript.** Alt er vanlige skjemaer med `POST`. JavaScript brukes bare til venteknappen (`skjema.js`, AD-12), kopieringsknappen og telleren i annonsefeltet. Uten JavaScript virker appen fortsatt, bare uten disse hjelpemidlene.
- **Ikke tillatt:** dialogvinduer (popup), uendelig rulling, dra og slipp som eneste måte å laste opp på, og handlinger som bare vises når musepekeren holdes over.

## Accessibility Floor

Målet er WCAG 2.1 AA der det er rimelig (NFR-7). Kontrasten står i `DESIGN.md`.

- Alle skjemafelt har en synlig `<label>`. Radioknapper står i `fieldset` med `legend`.
- Feilmeldinger står under feltet, er koblet til feltet med `aria-describedby` og nevnes i en oppsummering øverst i skjemaet når det sendes inn med feil.
- Fremdriftslinjen er en `<ol>` med `aria-current="step"` på det aktive steget. Teksten «Steg 4 av 6 · Analyse» kan leses av skjermleser.
- «Jobber …», «Kopiert!» og statusen for KI-feil meldes med `aria-live="polite"`.
- «Matcher» og «Mangler» vises med både symbol og tekst, ikke bare med farge.
- Fokusringen er alltid synlig. Etter at et steg er lastet, går fokus til overskriften (`h1`) i steget.
- Animasjonen i steg 6 slås av ved `prefers-reduced-motion`.
- Siden virker fra 360 px bredde og med 200 % zoom uten vannrett rulling.
- `lang="nb"` står på siden. KI-tekst på engelsk får `lang="en"` på brevkortet.

## Responsive & Platform

Det er samme oppsett på alle skjermer: **én midtstilt kolonne på maks 720 px**.

| Bredde | Hva som skjer |
|---|---|
| 360–599 px (mobil) | Sidemarg 16 px. Tilbake og Neste står i én rad, og hovedknappen er bredest. |
| 600 px og bredere (nettbrett og PC) | Sidemarg 24 px. Kolonnen er midtstilt med mer luft rundt. |

Appen er laget for nettleseren. Den lages ikke som installerbar app (PWA) og virker ikke uten nett.

## Testmodus

Testmodus er laget for sensor (UJ-3) og for de automatiske testene.

- Banneret står øverst på **alle** sider: «Testmodus: appen bruker lagrede KI-svar. Prøv eksempel A, B eller C i steg 1.» (FR-9)
- Eksempelknappene står bare i steg 1 (FR-10).
- Med eksempelpar går hele veiviseren som vanlig, med lagrede svar.
- Med egen CV: se tilstanden «Egen CV i testmodus».
- **Ønskede nøkkelord på eksempelpar** [ÅPENT]: Faglærer (tilbakemeldingen på PRD-en, 4.3) påpekte at lagrede forklaringer ikke dekker egne nøkkelord. Gruppa må velge om feltet skal være deaktivert for eksempelpar, eller om forklaringen skal skjules når feltet er fylt ut.

## Personvern i grensesnittet

- **Registrering:** en avkrysning, «Jeg har lest hvordan appen behandler CV-en min», med lenke til en kort forklaring. Kontoen kan ikke lages uten avkrysningen.
- **Steg 3:** en påminnelse rett over «Analyser» (se Component Patterns).
- **Steg 6:** «Brukes bare i PDF-en og lagres ikke» ved avsenderfeltene.
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
2. Hun laster opp CV-en som PDF. Under «Sjekk at teksten ble riktig» ser hun teksten appen fant, og hun ser at alt er med. Hun trykker **Neste**.
3. **Steg 2:** Hun limer inn annonseteksten. Telleren viser 2 310 tegn. Hun trykker **Neste**.
4. **Steg 3:** Norsk, formell og fullt utkast er allerede valgt. Hun leser påminnelsen om at teksten sendes til KI-tjenesten, og trykker **Analyser**. Knappen viser «Jobber …».
5. **Steg 4:** «2 av 4 krav dekket». Python og Git matcher, med sitater fra CV-en. SQL og førerkort klasse B mangler. Hun åpner «Hva betyr dette?» og ser at «SQL» også mangler blant nøkkelordene. Hun trykker **Lag søknad**.
6. **Steg 5:** Brevet trekker fram Python-prosjektene og sier at hun gjerne vil lære SQL, uten å påstå at hun kan det. Hun leser gjennom det, slik varselet ber om, og trykker **Ser bra ut**.
7. **Klimaks, steg 6:** Et stort ✓ skaleres rolig inn: «Søknaden er klar. Lykke til med søknaden!». Brevet ligger rett under. Emma trykker **Kopier teksten**, ser «Kopiert!» og limer brevet inn i søknadsskjemaet. Hun har ikke måttet styre med noe. Hun lukker fanen og legger seg.

**Avvik:** KI-tjenesten svarer ikke i steg 4. Emma ser «Vi fikk ikke svar fra KI-tjenesten. CV-en og valgene dine er tatt vare på, så du kan prøve igjen», trykker **Analyser** igjen og kommer videre. Hun trenger ikke laste opp CV-en på nytt.

### UJ-2. Jonas vil skrive selv, men på engelsk

_Jonas studerer logistikk og søker et graduate-program med engelsk annonse. Han bruker telefonen på bussen. Han har brukt appen før._

1. Jonas logger inn og trykker «Start ny søknad». **Steg 1** spør «Vil du bruke cv-jonas.pdf?», og han trykker **Bruk denne** og deretter **Neste**.
2. **Steg 2:** Han limer inn den engelske annonsen.
3. **Steg 3:** Han velger engelsk, uformell og **kun forslag**. Forklaringen under, «du får punkter, og skriver brevet selv», er akkurat det han vil ha. Han trykker **Analyser**.
4. **Steg 4:** Gap-analysen er på engelsk. Blant nøkkelordene har «SAP» stiplet kant og står som manglende.
5. **Steg 5:** Han får en punktliste på engelsk der hvert punkt viser til lagerjobben eller studiet. Han trykker **Ser bra ut**.
6. **Klimaks, steg 6:** «Forslagene er klare.» Han trykker **Vis forslag til CV-en** og ser hvordan lagerjobben kan beskrives tydeligere. SAP står som et spørsmål, «Have you used SAP?». Han trykker **Last ned Markdown** og skriver brevet selv senere.

### UJ-3. Sensor prøver appen uten API-nøkkel

1. Sensor starter appen etter README-en, uten nøkkel. Det blågrønne banneret sier at appen kjører i testmodus.
2. Sensor registrerer en bruker. I **steg 1** trykker sensor på **A**, og CV-en og annonsen fylles inn. Veiviseren hopper til **steg 3**.
3. Sensor trykker **Analyser** og går gjennom steg 4, 5 og 6 med lagrede svar. Sensor laster også ned PDF-en med en avsender.
4. **Klimaks:** Sensor er kommet til «Søknaden er klar» uten nøkkel, uten kostnad og uten feil (SM-10).
5. Sensor starter en ny søknad og laster opp en egen CV. Teksten vises og nøkkelordene telles, men steg 4 forklarer at KI-svar bare finnes for eksempelparene, og hvordan en API-nøkkel legges inn (FR-11).

### UJ-4. Emma sletter dataene sine

1. Søknadsfristen er passert. Emma trykker **Min konto** i topplinjen.
2. Hun leser hva som er lagret, og trykker **Slett mine dokumenter**.
3. Bekreftelsessiden sier: «Er du sikker? CV-en, annonsen og resultatet slettes, og det kan ikke angres.» Hun trykker den røde knappen.
4. **Klimaks:** «Dokumentene dine er slettet.» Neste gang hun logger inn, starter hun i steg 1 uten noen CV.
5. Senere sletter hun hele kontoen på samme måte. Hun blir logget ut, og e-posten kan registreres på nytt (FR-17).

## Inspiration & Anti-patterns

- **Ønsket:** Henrik liker apper som er **ryddige, og der det er lett å finne fram**. Det er grunnen til veiviseren, én hovedknapp per steg og én smal kolonne.
- **Valgt bort: alt på én side og én side som vokser.** Henrik valgte steg for steg, fordi det gir én ting om gangen og viser hvor langt man har kommet.
- **Valgt bort: faner på resultatet.** Henrik valgte egne steg, slik at det blir en tydelig vei til «Ferdig».
- **Avvist: designretningen «Stram»** (svart-hvitt med skarpe hjørner). Den virket for streng.
- **Avvist: chatbot-stil.** Appen er ingen chatbot (PRD §7). Brukeren skriver ikke til KI, hun fyller ut skjemaer og leser resultater.
- **Avvist: poengsum for sjansen til å få jobben** (PRD §7). Nøkkelordmåleren viser bare en andel, ikke en karakter.

## Avvik fra PRD og arkitektur

Disse punktene må inn i PRD-en og arkitekturen når de oppdateres. Claude anbefalte å gjøre det i en egen pull request etter at gruppa har godkjent UX-en, sammen med rettingene etter faglærers tilbakemelding. Det er gruppa som bestemmer.

**PRD:**
1. **§6 Skjermbilder:** «Ny analyse» og «Resultat» er erstattet av en veiviser med seks steg (CV, Annonse, Valg, Analyse, Søknad, Ferdig). Registrer/Logg inn og Min konto er som før.
2. **FR-12 Registrere konto:** en ny konsekvens er avkrysningen for personvern. Kontoen kan ikke lages uten den.
3. **§4.6 FR-18:** CV-forbedringer vises på Ferdig-steget og har ingen egen side.
4. **FR-4:** tone og svarform velges i steg 3, men kan endres i steg 5 med «Lag nytt brev».
5. **Faglærers punkt 4.5:** varselet «KI kan gjøre feil – les gjennom før du sender» er tatt med i steg 5. Det bør bli en konsekvens under FR-6 og FR-7.

**Arkitektur:**
1. **URL-er (§3 Konvensjoner):** Veiviseren trenger én adresse per steg. Steg 2 (annonse) og steg 3 (valg) er egne sider, mens arkitekturen har én `/analyse/`. Annonsen må derfor lagres midlertidig mellom steg 2 og steg 3, før analysen kjøres. Det kan for eksempel gjøres i Django-sesjonen, men da må annonsen også krypteres der, eller så må steg 2 og 3 sendes som ett skjema. Arkitekturen må avgjøre det.
2. **`/resultat/cv-forbedring/`** kan beholdes som POST-endepunkt, men skal sende brukeren tilbake til steg 6, ikke vise en egen side.
3. **Hvor langt brukeren har kommet:** Fremdriftslinjen må vite hvilke steg som er fullført. Det kan leses av hvilke rader som finnes (`CV`, `Analyse`, `Brev`), men det krever en regel for når steg 6 regnes som nådd («Ser bra ut» lagrer ikke noe ennå).
4. **Bekreftelse før en endring sletter analysen** (State Patterns) må passe med `lagre_cv_tekst` i AD-8.

## Åpne punkter

- **Appnavn:** «Søknadshjelpen» er en plassholder. Gruppa bestemmer navnet.
- **Ønskede nøkkelord i testmodus** (se Testmodus).
- **[ANTAKELSE]-punkter** i dette dokumentet og i `DESIGN.md`: farger for fare og info, typografistørrelser, avstander, hvor brukeren havner etter innlogging, egen bekreftelsesside for sletting, og formen på advarselen før en endring sletter analysen.
- **Mockups av nøkkelskjermene** er ikke laget ennå, bare steg 4 i designretningene.
