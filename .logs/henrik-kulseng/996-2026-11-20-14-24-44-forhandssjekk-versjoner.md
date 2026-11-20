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
- Test av 7.3 med fpdf2 2.9.0 og DejaVu: spesialtegn er OK, 30 000 tegn gir 9 sider, og en emoji fonten mangler, faller bort uten krasj.
- Ingen kode eller planleggingsdokumenter er endret.

### Åpne punkter
- Issue #17: lukkes når første story i Epic 0 har kjørt en test mot Django 6.1. Gruppa avgjør.
- PR #35: Haakon og Ole svarer på forslagene, og Ole bekrefter fordelingen i Epic 5.
- PR #34: Gruppa velger A eller B for hvordan brevet starter og slutter. Ole svarer på forslaget om linjeskift.
- Issue #29: akseptkriteriene for Epic 0 bør teste tekst og ikke bytes. Tekstene om fonttools i `lag_cv_pdf.py` og i issuet bør rettes.
