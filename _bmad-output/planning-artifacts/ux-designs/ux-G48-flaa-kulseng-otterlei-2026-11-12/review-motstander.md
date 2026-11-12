# Motstandergjennomgang — G48 UX

_Gjennomgått 2026-11-12 av en KI-kontrollør (Claude Code) med oppdrag om å finne svakheter. Grunnlaget er `DESIGN.md`, `EXPERIENCE.md` og `.memlog.md`, sammenholdt med PRD-en, faglærers tilbakemelding på PRD-en, product brief og arkitekturutkastet (ARCHITECTURE-SPINE, AD-5, AD-8, AD-10, AD-12, AD-15 og §3). Funnene er forslag. Gruppa avgjør hva som rettes._

## Samlet vurdering

UX-en er gjennomarbeidet. Den har tydelige tilstander, en god tilgjengelighetsdel og en ærlig liste over avvik. Den svake delen er **veiviserens tilstandsmodell**. Seks steg med låste steg, «hvor langt har brukeren kommet» og en annonse som må lagres før analysen, passer dårlig med AD-8, der det bare finnes én `Analyse` som overskrives, og med AD-10, der dokumentinnhold aldri skal ligge i økten. Det rammer særlig tilbakevendende brukere, som er UJ-2. Veiviseren gjør også flyten lengre enn PRD-ens to skjermbilder, og et av stegene («Ser bra ut») lagrer ingenting. Samtidig legger UX-en til arbeid (bekreftelser, låsing, animasjon, mørk modus, avkrysning) uten å si hva som kan kuttes. Faglærer etterlyste nettopp det i punkt 4.2. Kjernen i kurset er KI-kontroll, og der sier UX-en for mye: «Søknaden er klar» og «Ser bra ut» lover mer enn appen kan stå inne for, og varselet om KI-feil står bare ved brevet.

**Antall funn:** 1 kritisk, 6 høy, 7 middels, 6 lav.

## Funn

- **[kritisk]** «Start ny søknad» gir en tilstand modellen ikke kan vise (EXPERIENCE.md: Component Patterns «Start ny søknad», «Fremdriftslinje», State Patterns «Endring som sletter analysen» og «Låste steg», og «Hvor brukeren havner etter innlogging»; Avvik, arkitektur punkt 3).
  *Hvorfor det betyr noe:* Etter «Start ny søknad» står brukeren i steg 1, men den gamle `Analyse` og det gamle `Brev` finnes fortsatt (AD-8). Hvis fremdriften leses av hvilke rader som finnes, slik avvikspunkt 3 foreslår, vises steg 4–6 som fullførte lenker til **forrige jobb**. Et klikk på «Analyse» viser da gap-analysen for feil annonse. Steg 2 kan enten være fylt med den gamle annonsen eller være tomt, men det står ikke hvilket. Uansett vil enhver ny annonse utløse varselet «Brevet og forslagene forsvinner. [Endre likevel]». Det betyr at **den vanlige veien for en tilbakevendende bruker (UJ-2) går gjennom en advarsel om sletting**. Etter innlogging sendes Jonas til «det siste steget hun har nådd», altså steg 6 for den forrige søknaden. Det finnes heller ingen rad som viser at brukeren er i steg 2 eller 3, fordi annonsen ikke er lagret før «Analyser».
  *Retting:* Definer «en søknad i arbeid» i stedet for å utlede fremdriften av radene. Den enkleste løsningen som passer AD-8: «Start ny søknad» sletter `Analyse` (med en bekreftelse på Ferdig-siden, ikke i steg 2). Da er tilstanden alltid entydig: ingen CV → steg 1, CV uten analyse → steg 1–3, analyse → 4, brev → 5/6. Skriv regelen som en tabell i EXPERIENCE.md og ta den med i avvikslisten til arkitekturen. Ellers må fremdriftslinjen vise de gamle stegene som «forrige søknad», og det koster mer.

- **[høy]** Forslaget om å lagre annonsen i økten bryter AD-10 (EXPERIENCE.md, Avvik, arkitektur punkt 1, og Eksempelknapper som «hopper til steg 3»).
  *Hvorfor det betyr noe:* AD-10 sier rett ut: «Dokumentinnhold … legges aldri i økten.» Økter lagres ukryptert, så forslaget bryter FR-15. UX-en nevner økten som det første alternativet og sier at annonsen «også [må] krypteres der», men nevner ikke at AD-10 forbyr det. Samme problem gjelder `/eksempel/A/`, som må ha annonsen et sted når den hopper til steg 3. Hvis annonsen sendes videre som skjult felt, må hver side i steg 3 bære annonsen, og «Tilbake» til steg 2 må også sende den.
  *Retting:* Slå sammen steg 2 og 3 til **ett steg, «Annonse og valg»**, med «Analyser» nederst. Da følger annonsen samme `POST` som analysen, slik `/analyse/` i arkitekturen allerede er laget for, og veiviseren får fem steg. Personvernpåminnelsen står fortsatt rett over «Analyser». Hvis gruppa vil beholde seks steg, skriv at annonsen sendes som skjult felt (ikke økt), og fjern økt-alternativet fra avvikslisten.

- **[høy]** Veiviseren gir mange klikk, og «Ser bra ut» er et tomt steg (EXPERIENCE.md: Information Architecture, Tilbake/Neste, UJ-1 og UJ-2; Avvik, arkitektur punkt 3).
  *Hvorfor det betyr noe:* Fra innlogging til kopiert brev trenger en ny bruker åtte handlinger og sju sidelastinger: velg fil → last opp → Neste → lim inn + Neste → Analyser → Lag søknad → Ser bra ut → Kopier. En tilbakevendende bruker lander på det gamle steg 6 og trenger ni handlinger: Start ny søknad → Bruk denne → Neste → (Endre likevel) → Neste → Analyser → Lag søknad → Ser bra ut → Kopier. PRD §6 ga omtrent fire. «Ser bra ut» lagrer ingenting, som avvikspunkt 3 selv innrømmer, og gir bare et klikk mellom å lese brevet og ta det med seg. «Bruk denne» viser teksten og krever så «Neste», altså to klikk for én bekreftelse. Målet «ikke må streve» trekker i motsatt retning.
  *Retting:* (1) Slå sammen steg 5 og 6: Kopier og eksport står under brevet, og ✓-merket vises over brevet når det er laget. (2) Slå sammen steg 2 og 3 (se forrige funn). (3) Vis CV-teksten direkte i steg 1 når en CV finnes, med «Last opp ny» som sekundærknapp. Da blir det fire steg (CV, Annonse og valg, Analyse, Søknad) og omtrent fem handlinger. Klimakset kan ligge i siste steg uansett.

- **[høy]** UX-en legger til omfang uten kuttrekkefølge (hele EXPERIENCE.md og DESIGN.md; faglærers 4.2).
  *Hvorfor det betyr noe:* Utover PRD-en krever UX-en blant annet seks maler og views, låste steg med omdirigering, en bekreftelsesflyt før sletting av analysen (uten dialogvindu, altså en ekstra side eller tilstand), avkrysning ved registrering (et eget skjema i stedet for Djangos standard, i strid med unntaket i AD-2), «Prøv forklaringen igjen», «Lag nytt brev» i steg 5, animasjon og full mørk modus med 15 ekstra tokens. Faglærer pekte på at planen mangler en kuttplan, og UX-en gjør planen større uten å svare på det. Sensor vil se om gruppa prioriterer.
  *Retting:* Legg til en kort seksjon, «Minste versjon og kuttrekkefølge», som merker hver komponent som *må* eller *kan*. Forslag til rekkefølge for kutt: animasjon → mørk modus (bare lys, behold tokenene) → «Prøv forklaringen igjen» (vis bare meldingen) → låste steg (alle steg er lenker, og siden viser «Kjør analysen først») → CV-forbedringer (P6). Hvis veiviseren slås sammen til fire steg, kuttes mye av dette uansett.

- **[høy]** Tone og svarform har ikke noe sted å bo mellom steg 3 og steg 5, og avviket er ikke tatt med (EXPERIENCE.md: Valg, Lag nytt brev; .memlog.md, linje 16).
  *Hvorfor det betyr noe:* AD-8 sier at tone og svarform **bare** finnes på `Brev`, og at brevskjemaet bruker FR-4-standardene første gang. UX-en lar brukeren velge dem i steg 3, før det finnes et `Brev`, og sier at «Lag nytt brev» er «forhåndsvalgt [med] det som ble valgt i steg 3 … (AD-8)». Det motsier AD-8 og er ikke dekket av henvisningen. Beslutningsloggen har en «NOTE FOR ARKITEKTUR» om akkurat dette, men den kom aldri inn i «Avvik fra PRD og arkitektur». Uten en avklaring vil to utviklere løse det ulikt: den ene legger feltene på `Analyse`, den andre bruker skjulte felt.
  *Retting:* Ta det med som arkitekturavvik nummer 5. Enkleste løsning: `Analyse` får `tone` og `svarform` som startverdier (ikke dokumentinnhold, så de trenger ikke kryptering), og `Brev` lagrer det som faktisk ble brukt. Alternativt flyttes tone og svarform til steg 5 og fjernes fra steg 3, slik AD-8 forutsetter. Det er færre valg før analysen og passer «én ting om gangen».

- **[høy]** Varselet om at KI kan ta feil står bare ved brevet, og KI-innhold og kode-innhold ser like ut (EXPERIENCE.md: Brevvisning, Kravliste, Nøkkelordanalyse, CV-forbedringer; DESIGN.md, Brev).
  *Hvorfor det betyr noe:* AD-5 sier: «Alle sider med KI-tekst viser ‹KI kan gjøre feil – les gjennom før du sender›.» I UX-en står varselet bare på brevkortet i steg 5 og 6. Gap-analysen i steg 4 er KI sin vurdering, «Hva betyr dette?» er KI-tekst, og CV-forbedringene er KI-tekst. Ingen av dem har varselet. Avviket er heller ikke listet. Viktigere for kurset: PRD-en og briefen legger vekt på at nøkkelordene **beregnes i kode** og at gap-analysen **vurderes av KI**. I steg 4 står de ved siden av hverandre med samme visuelle språk («2 av 4 krav dekket», «7 av 10 funnet»). Brukeren får ingen hjelp til å se at «Matcher» i kravlisten er KI sin påstand, mens tellingen av nøkkelord er sikker.
  *Retting:* Gi hvert KI-kort en liten fast merkelapp, «Laget av KI», og gi nøkkelordkortet merkelappen «Telt automatisk» (DESIGN.md får en komponent til). Vis varselet én gang øverst i steg 4 og ved CV-forbedringene, eller skriv inn i avvikslisten at AD-5 snevres inn til brevet, med begrunnelse.

- **[høy]** «Søknaden er klar» og «Ser bra ut» lover for mye (EXPERIENCE.md: Ferdig-merke, Tilbake/Neste, UJ-1 trinn 6–7, Voice and Tone).
  *Hvorfor det betyr noe:* Teksten sier selv: «Appen skryter aldri av brevet … Kontrollen ligger hos Emma (SM-C2).» Likevel får Emma en hovedknapp med ordene «Ser bra ut», som appen legger i munnen hennes, og deretter et stort ✓ med «Søknaden er klar». Det er et utkast fra KI som kan inneholde feil, og UJ-1 beskriver at Emma «ikke har måttet styre med noe» og lukker fanen. Sensor som ser etter KI-kontroll, vil lese dette som at appen gjør «les gjennom» til et klikk. Ved «kun forslag» er «Forslagene er klare» som klimaks svakt, fordi Jonas ennå ikke har skrevet brevet.
  *Retting:* Bytt «Ser bra ut» med et verb som beskriver handlingen, for eksempel «Ta med brevet» (eller fjern steget, se over). Bytt «Søknaden er klar» med «Utkastet er klart», med undertekst om at brevet bør leses og tilpasses før det sendes. Skriv om UJ-1 trinn 7 slik at Emma retter en setning før hun sender. Det viser kontrollen i stedet for å påstå den.

- **[middels]** Tilbakeknappen i nettleseren kan sende «Analyser» på nytt (EXPERIENCE.md: Interaction Primitives «vanlige skjemaer med POST»; AD-10 `never_cache`).
  *Hvorfor det betyr noe:* Hvis steg 4 er svaret på en `POST`, får brukeren «Send skjemaet på nytt?» ved tilbake og frem igjen. Med `never_cache` kan det gi et nytt betalt KI-kall og overskrive analysen. UX-en sier ingenting om dette, og låsen i AD-12 hjelper bare mot samtidige kall.
  *Retting:* Skriv inn som regel: hvert steg er en `GET`-side, og alle skjemaer bruker Post/Redirect/Get (et vellykket `POST` sender videre til neste stegs adresse). Unntaket er når skjemaet vises på nytt med feil (AD-20). Si at tilbakeknappen alltid viser siden for forrige steg med lagrede verdier.

- **[middels]** Endring av språk eller nøkkelord etter analysen er ikke dekket, og annonseendring er feil knyttet til AD-8 (EXPERIENCE.md: Fremdriftslinje, State Patterns «Endring som sletter analysen»).
  *Hvorfor det betyr noe:* Gap-analysen og forklaringen avhenger av språket, og nøkkelordresultatet avhenger av ønskede nøkkelord. Hvis brukeren går tilbake til steg 3 og bytter til engelsk, står det ikke om analysen slettes, blir stående (feil språk) eller kjøres på nytt. «Lag nytt brev» tilbyr ikke språk, så den eneste veien er tilbake. I tillegg står det at endret annonse «slettes analysen (AD-8)», men AD-8 nevner bare CV-tekst. Annonsen ligger *på* `Analyse` og blir bare erstattet ved en ny analyse.
  *Retting:* Regel: alle endringer i steg 1–3 gjelder først når «Analyser» trykkes på nytt, og varselet vises ved «Analyser» («Dette erstatter analysen og brevet»), ikke ved hvert felt. Det gir én bekreftelse i stedet for flere og passer AD-8 slik den er. Unntak: endret CV-tekst sletter analysen med en gang (`lagre_cv_tekst`).

- **[middels]** Testmodus: eksempelknappen hopper over CV-teksten, og egen CV fører til en blindvei (EXPERIENCE.md: Eksempelknapper, «Egen CV i testmodus», UJ-3 trinn 2 og 5).
  *Hvorfor det betyr noe:* (1) Når eksempelet hopper rett til steg 3, ser ikke sensor CV-teksten. Da vises ikke det viktigste PRD-en sier om risiko, at to-kolonne-CV-en C leses riktig (FR-2, SM-2). (2) Med egen CV kan steg 5 og 6 aldri nås, men det står ikke om «Lag søknad» vises og gir en feil, eller om knappen skjules. (3) I UJ-3 trinn 5 laster sensor opp en egen CV. Etter FR-1 sletter det CV A og hele resultatet, så demoen forsvinner og må kjøres på nytt. Det står ikke i reisen.
  *Retting:* La eksempelknappen fylle inn og gå til steg 1 med CV-teksten synlig («Sjekk at teksten ble riktig»), eller vise den i et `<details>` i steg 3. Ved egen CV i testmodus: erstatt «Lag søknad» med «Prøv eksempel A» som hovedknapp. Legg en setning i UJ-3 om at egen CV erstatter eksempelet.

- **[middels]** CV-forbedringer er låst bak brevet (EXPERIENCE.md: CV-forbedringer i steg 6, UJ-2 trinn 6; PRD §4.2).
  *Hvorfor det betyr noe:* PRD-en har egne knapper slik at P6 «kan bygges uavhengig av resten». CV-forbedringene avhenger av analysen, ikke av brevet. I veiviseren må brukeren likevel lage et brev og trykke «Ser bra ut» for å se dem. En student som bare vil forbedre CV-en, betaler for et brev hun ikke trenger, og ved et KI-brudd i steg 5 kommer hun aldri dit. Det er også et nytt KI-kall på 10–30 sekunder *etter* klimakset «alt er gjort».
  *Retting:* Flytt «Vis forslag til CV-en» til steg 4 under gap-analysen, der de manglende kravene allerede står. Det passer også arkitekturens `/resultat/`, og avvikspunkt 2 for arkitekturen faller bort.

- **[middels]** Det er ikke avgjort om brevet kan redigeres før det kopieres (EXPERIENCE.md: Brevvisning, Kopier, PDF-avsender).
  *Hvorfor det betyr noe:* Brevet vises som avsnitt i et kort og kopieres eller eksporteres som det er. En bruker som ser én feil påstand, må kopiere til et annet program for å rette den, og PDF-en vil da inneholde feilen. Kurset handler om at brukeren styrer KI. Et redigerbart felt viser det tydelig, men gir mer arbeid: lagres endringen i `Brev`? Overskrives den av «Lag nytt brev»? Hvilken versjon eksporteres?
  *Retting:* Ta en uttrykkelig beslutning. Forslag for v1: ingen redigering i appen, med teksten «Kopier brevet og tilpass det i ditt eget program». Marker valget som et bevisst avvik fra «kontroll» i beslutningsloggen. Hvis gruppa vil ha redigering: et `<textarea>` som sendes med eksport-`POST`, og som ikke lagres. Det er billig og passer AD-10.

- **[middels]** «Fungerer uten JavaScript» stemmer ikke for kopiering (EXPERIENCE.md: Interaction Primitives, Kopier).
  *Hvorfor det betyr noe:* Kopiering til utklippstavlen (FR-22) krever JavaScript. Uten JavaScript står det en knapp som ikke gjør noe. Sensor som tester påstanden, finner et brudd.
  *Retting:* Skriv at knappen bare vises når JavaScript kjører (legges inn av skriptet), og at brevet uten JavaScript kan markeres og kopieres manuelt. Ellers bør påstanden svekkes til «fungerer i hovedsak uten JavaScript».

- **[middels]** Engelsk KI-tekst er bare merket på brevkortet (EXPERIENCE.md: Accessibility Floor siste punkt, UJ-2 trinn 4 og 6).
  *Hvorfor det betyr noe:* Ved engelsk er gap-analysen, begrunnelsene, forklaringen og CV-forbedringene også på engelsk. Bare brevkortet får `lang="en"`, så skjermlesere leser resten med norsk uttale. Overskrifter som «2 av 4 krav dekket», og merkene «Matcher» og «Mangler», står på norsk mellom engelske krav. Det er riktig etter NFR-8, men blandingen er ikke beskrevet. I UJ-2 skrives et spørsmål som «Have you used SAP?» ved siden av norske knapper.
  *Retting:* Regel: alle blokker med KI-tekst får `lang` etter `Analyse.sprak`. Legg til én setning om at grensesnittet er norsk, KI-teksten er på valgt språk, og at blandingen er tilsiktet (NFR-8).

- **[lav]** Personvernpåminnelsen er feil i testmodus (EXPERIENCE.md: Personvernpåminnelse).
  *Hvorfor det betyr noe:* «sendes CV-teksten og annonsen til KI-tjenesten» stemmer ikke i testmodus, der ingenting sendes (FR-9). AD-5 sier at påminnelsen gjelder «når appen kjører i KI-modus».
  *Retting:* I testmodus: «Testmodus: ingenting sendes til KI-tjenesten. Appen bruker lagrede svar.»

- **[lav]** Utløpt økt eller utlogging midt i en innsending kan gjøre at brukeren mister annonsen (State Patterns).
  *Hvorfor det betyr noe:* `login_required` på en `POST` sender brukeren til innlogging, og det hun limte inn, forsvinner. Det samme skjer hvis hun logger ut i en annen fane mens «Analyser» kjører. Risikoen er liten med Djangos standard på to uker, men tilstanden er ikke nevnt. To faner på ulike steg kan også vise et utdatert brev etter at den andre fanen har kjørt en ny analyse.
  *Retting:* En linje i State Patterns: «Økten er utløpt – logg inn igjen. Det du limte inn, er ikke lagret.» Det er godt nok for v1.

- **[lav]** Kildene peker på en fil som ikke finnes på branchen (EXPERIENCE.md og DESIGN.md, `sources` i frontmatter).
  *Hvorfor det betyr noe:* `../../architecture/architecture-G48-…/ARCHITECTURE-SPINE.md` finnes ikke på `docs/ux`. Mappen har bare `technology.md`, og arkitekturen ligger i PR #13. Sensor som følger lenken fra `main`, finner ingenting hvis UX-en flettes først.
  *Retting:* Flett arkitekturen før UX-en, eller skriv i pull requesten at UX-en avhenger av PR #13.

- **[lav]** Kontrasttabellen dekker ikke alle par (DESIGN.md: Colors, Fremdriftslinje).
  *Hvorfor det betyr noe:* Det aktive steget er aksentfarge med 50 % gjennomsiktighet mot `border`. Det er ikke sjekket mot 3:1 (WCAG 1.4.11) og blir trolig for svakt. Lenker i aksentfarge på `surface`, mangler-tekst i brikker på hvit bakgrunn og tekst på infoflaten mangler også i tabellen. «Sjekket 2026-11-12» sier ikke hvordan det ble sjekket.
  *Retting:* Legg til de fire parene og nevn verktøyet. Gi det aktive steget full aksentfarge og skill det fra fullførte steg med tykkelse eller en markør, ikke bare med gjennomsiktighet.

- **[lav]** Beslutningene er tilskrevet én person (EXPERIENCE.md og DESIGN.md, innledning; .memlog.md).
  *Hvorfor det betyr noe:* Det står «Henrik tok valgene» og «Henrik valgte» gjennom hele dokumentet. Det er ærlig, men sensor vurderer gruppens prosess. Uten et spor av at Ole og Haakon har vurdert valgene, ser UX-en ut som én persons smak. CLAUDE.md sier at vurderingene skal komme fra gruppa.
  *Retting:* Når PR-en er gjennomgått, legg til en linje i hvert dokument om at gruppa har gått gjennom og godtatt (eller endret) valgene, med dato. Endringer kan føres i `.memlog.md`.

- **[lav]** Mockupene som ble bestemt, finnes ikke (EXPERIENCE.md: Åpne punkter; .memlog.md, linje 41).
  *Hvorfor det betyr noe:* Loggen sier at det skal lages mockups av steg 1, 3, 4 og 5+6, men bare steg 4 finnes. Flere av funnene over (klikktall, tilstanden ved ny søknad) hadde vært lettere å se i en mockup av steg 1 for en tilbakevendende bruker.
  *Retting:* Lag mockupene etter at strukturen er avklart (antall steg). Ta med steg 1 med en lagret CV og steg 4 med egen CV i testmodus.

## Hva som holder

- **Tilstandene for KI-feil er gode og sporbare.** Venting, tidsavbrudd, forbruksgrense, samtidige kall og «Forklaringen feilet» er knyttet til NFR-5, NFR-6, AD-8 og AD-12, med konkrete meldinger som sier hva som er tatt vare på.
- **Mangler vises i oransje, ikke rødt,** med symbol og tekst. Det er gjennomtenkt både for tilgjengelighet og for tonen («en mulighet, ikke en feil»). Det samme gjelder at CV-forbedringene stiller manglende krav som spørsmål.
- **Tilgjengelighetsdelen er konkret og testbar:** `fieldset`/`legend`, `aria-describedby`, fokus til `h1`, `prefers-reduced-motion`, 360 px og 200 % zoom, og kontrasten er justert etter sjekk (`#A65F00` → `#9A5800`, nytt `field-border`).
- **Avviksseksjonen er ærlig** og gjør den neste PRD-oppdateringen lett. Den bør bare utvides med funnene over (tone og svarform, AD-5 og AD-10).
- **Voice and Tone** har gode og mot-eksempler som utviklerne kan bruke direkte, og regelen om lik melding ved feil innlogging (FR-13) er tatt med.
- **Ikke-mål er respektert:** ingen chatbot og ingen poengsum, og nøkkelordmåleren viser bare en andel.
