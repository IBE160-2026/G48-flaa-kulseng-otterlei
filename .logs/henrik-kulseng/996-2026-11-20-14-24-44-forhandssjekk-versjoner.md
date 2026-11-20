# Forhåndssjekk av versjoner og gjennomgang av epics

## 2026-11-20 kl. 14:24 — Henrik Kulseng

### Oppgave
Haakon lager epics og stories. I mellomtiden ville Henrik sjekke på forhånd at versjonene arkitekturen har valgt, virker sammen (issue #17 og #29), så Epic 0 ikke får overraskelser. Deretter ba han om å få gå gjennom storyene sine i Haakons PR #35 (epics og stories): 0.3, Epic 5 og Epic 7.

### Plan
- Midlertidig Python-miljø i scratchpad, utenfor repoet, med alle låste versjoner fra arkitekturen §4.
- Lite Django 6.1-prosjekt med egen brukermodell og pytest, pytest-django og `--disable-socket` (#17).
- Kjøre `lag_cv_pdf.py` på en kopi av `app/` og lese PDF-ene med pdfplumber (#29).
- Skrive funnene som kommentarer i issuene. Repoet endres ikke, bortsett fra denne loggen.
- PR #35: lese storyene mot `DESIGN.md`, `EXPERIENCE.md` og arkitekturen, prøve kriteriene i 7.3 med fpdf2 i testmiljøet, og skrive et utkast til kommentar som Henrik godkjente før det ble lagt inn.

### Resultat
- Alle versjonene i §4 installeres sammen uten konflikter (Python 3.12.7). pytest-django 4.14.0 er fortsatt nyeste på PyPI.
- **#17:** Seks pytest-django-tester mot Django 6.1.3 besto, også med `-W error::DeprecationWarning`: innlogging med `client`, `transaction=True`, `django_user_model`, `settings`, blokkert databasetilgang og blokkert nettverk. Forslag: behold pytest (AD-17). [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/17#issuecomment-7040666585).
- **#29:** Skriptet kjører for A, C og D. pdfplumber henter ut alle ordene fra `cv_kilde.txt` (A 174/174, C 135/135, D 174/174), og A og D er like. PDF-ene blir likevel **ikke** like byte for byte med fonttools 4.68.0. De 14 siste versjonene av fonttools ga samme fil. Innholdet i alle PDF-objektene er identisk når det pakkes ut, så forskjellen ligger bare i zlib-komprimeringen, som følger Python-bygget og ikke kan låses i `requirements.txt`. Forslag: test teksten, ikke bytene. [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/29#issuecomment-7040667017).
- Korrigering underveis: Første forsøk søkte etter `fakta_i_cv` ordrett i PDF-teksten og fant få treff, selv i B, som er ren tekst. Faktaene er omskrevet, så metoden var feil. Den ble byttet ut med en sjekk på ord mot `cv_kilde.txt`.
- **PR #35:** [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/35#issuecomment-7041179298) lagt inn etter at Henrik godkjente utkastet. Forslagene:
  - 0.1: `lag_cv_pdf.py` kjører uten ekstra installasjon (#29).
  - 0.3: Mobil og zoom sjekkes manuelt i `docs/testplan.md`. «10–30 sekunder» og indikatoren mangler.
  - Epic 5: Ole tar 5.1–5.2 og Henrik 5.3–5.7. 5.7 venter på #16. 5.3 bør deles, og «Jobber …» flyttes.
  - Epic 7: fpdf2 logger tegn som mangler i fonten, med tegn fra brevteksten (strider mot AD-10), og Markdown-eksporten bør aldri ha avsender. Henrik godtar filnavnene og meldingen om utklippstavlen.
- **PR #34 (Oles prompter):** [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/34#issuecomment-7041672423) om `brev.md`, sett fra steg 4 og eksporten. Henrik er enig i at flosklene fra fasiten ikke skal stå i promptene. Prompten sier at appen legger til underskrift og kontaktinformasjon, men det gjør den bare i PDF-en (7.4). Gruppa må velge mellom A («Med vennlig hilsen» og navnet fra CV-en) og B (ingen hilsen). Linjeskift inne i et punkt kan bli to punkter i eksporten (7.2).
- **PR #35 godkjent** av Henrik etter at Claude sjekket at alle rettelsene står i 1d70108 og 5667df9, også i `.working/`. Henrik godtok at 5.3 er delt i motsatt rekkefølge (5.3 Vise søknaden, 5.4 Be om søknad), slik at hver del kan testes alene.
- **PR #33 (Oles avviste evalueringsforslag):** Henrik står bak gruppas begrunnelse. [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/33) med forslag om å skrive i KI-loggen at svakheten «Jeg kan SQL og ønsker å lære mer» fanges opp av den manuelle kontrollen i 5.2. Ikke godkjent ennå.
- **PR #38 (Oles API-konto, issue #16 lukket):** [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/38#issuecomment-7042064098) med et grovt kostnadsanslag: rundt 45 kall i `lag_lagrede_svar`, og med prisene for `claude-opus-5-5` ($4 / $20 per million tokens) omtrent 1–5 USD per full kjøring, fordi tankene betales som utdata. Grensen på 5 USD i måneden kan derfor bli for liten. Forslag: les tokenbruken i den første rapporten, lag bare på nytt det som er endret, og vurder batch-API-et.
- Test av 7.3 med fpdf2 2.9.0 og DejaVu: spesialtegn er OK, 30 000 tegn gir 9 sider, og en emoji fonten mangler, faller bort uten krasj.
- Ingen kode eller planleggingsdokumenter er endret.

### Åpne punkter
- Issue #17: lukkes når første story i Epic 0 har kjørt en test mot Django 6.1. Gruppa avgjør.
- PR #33: Ole legger inn setningen om den manuelle kontrollen og løser konflikten. Henrik godkjenner etterpå.
- Henrik takker ja til invitasjonen til organisasjonen i Claude Console (gjøres i nettleseren).
- Fordelingen i Epic 5 (Ole 5.1–5.2, Henrik 5.3–5.8) føres inn i issue #36 når Ole har sagt ja.
- PR #34: Gruppa velger A eller B for hvordan brevet starter og slutter. Ole svarer på forslaget om linjeskift.
- Issue #29: akseptkriteriene for Epic 0 bør teste tekst og ikke bytes. Tekstene om fonttools i `lag_cv_pdf.py` og i issuet bør rettes.

## 2026-11-20 kl. 15:43 — Henrik Kulseng

### Oppgave
Henrik spurte hva neste steg er. Deretter ba han om å få de to logg-commitene på `docs/forhandssjekk-versjoner` inn i en ny PR. De kom til etter at PR #37 var flettet.

### Plan
- Sjekke åpne PR-er, issues, sesjonslogger og hvor langt planleggingen har kommet, og foreslå neste steg.
- Kontrollere at branchen kan flettes uten konflikt, og lage en PR med malen.
- Sjekke om de åpne punktene i loggen fortsatt gjelder.

### Resultat
- Foreslo neste steg i denne rekkefølgen: (1) PR for loggene og invitasjonen i Claude Console, (2) sprint planning, (3) Epic 0 med Haakon (#17, #29), (4) ting som venter på andre.
- [PR #40](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/40) for `aeedf1e` og `16ce40c`. `git merge-tree` viste ingen konflikt med `main`. Loggene er ikke skrevet om i ettertid. PR-beskrivelsen sier hvilke punkter som er løst siden.
- Status på punktene fra forrige seksjon: PR #33 og #35 er flettet, og issue #16 og #36 er lukket. PR #34 er avgjort: Ole valgte alternativ A i `0486320`. PR #33 ble flettet uten setningen om den manuelle kontrollen i 5.2 og uten Haakons presisering (issue #42).
- Kommentar på PR #40: «Gjenstår» i KI-logginnlegget nevnte fortsatt PR #35 og issue #16 som åpne. Den som så over PR-en, mente det ikke trengte å rettes, med henvisning til PR-beskrivelsen. Claude pekte på at begge var avgjort allerede da linjen ble skrevet, og Henrik valgte å rette den (`f2dd7f5`). Svar lagt inn på PR #40.

### Åpne punkter
- Issue #42: KI-logginnlegget for PR #33 mangler setningen om den manuelle kontrollen og Haakons presisering.
- Issue #43: Sprint planning før Epic 0. Henrik og Haakon fordeler storyene i Epic 0 først.
- Henrik takker ja til invitasjonen til organisasjonen i Claude Console (personlig, ingen issue).
- Issue #17 og #29 gjelder fortsatt (Epic 0).
