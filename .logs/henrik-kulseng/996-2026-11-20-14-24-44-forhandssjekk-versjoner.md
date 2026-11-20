# Forhåndssjekk av versjoner til Epic 0

## 2026-11-20 kl. 14:24 — Henrik Kulseng

### Oppgave
Haakon lager epics og stories. I mellomtiden ville Henrik sjekke på forhånd at versjonene arkitekturen har valgt, virker sammen (issue #17 og #29), så Epic 0 ikke får overraskelser.

### Plan
- Midlertidig Python-miljø i scratchpad, utenfor repoet, med alle låste versjoner fra arkitekturen §4.
- Lite Django 6.1-prosjekt med egen brukermodell og pytest, pytest-django og `--disable-socket` (#17).
- Kjøre `lag_cv_pdf.py` på en kopi av `app/` og lese PDF-ene med pdfplumber (#29).
- Skrive funnene som kommentarer i issuene. Repoet endres ikke, bortsett fra denne loggen.

### Resultat
- Alle versjonene i §4 installeres sammen uten konflikter (Python 3.12.7). pytest-django 4.14.0 er fortsatt nyeste på PyPI.
- **#17:** Seks pytest-django-tester mot Django 6.1.3 besto, også med `-W error::DeprecationWarning`: innlogging med `client`, `transaction=True`, `django_user_model`, `settings`, blokkert databasetilgang og blokkert nettverk. Forslag: behold pytest (AD-17). [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/17#issuecomment-7040666585).
- **#29:** Skriptet kjører for A, C og D. pdfplumber henter ut alle ordene fra `cv_kilde.txt` (A 174/174, C 135/135, D 174/174), og A og D er like. PDF-ene blir likevel **ikke** like byte for byte med fonttools 4.68.0. De 14 siste versjonene av fonttools ga samme fil. Innholdet i alle PDF-objektene er identisk når det pakkes ut, så forskjellen ligger bare i zlib-komprimeringen, som følger Python-bygget og ikke kan låses i `requirements.txt`. Forslag: test teksten, ikke bytene. [Kommentar](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/29#issuecomment-7040667017).
- Korrigering underveis: Første forsøk søkte etter `fakta_i_cv` ordrett i PDF-teksten og fant få treff, selv i B, som er ren tekst. Faktaene er omskrevet, så metoden var feil. Den ble byttet ut med en sjekk på ord mot `cv_kilde.txt`.
- Ingen kode eller planleggingsdokumenter er endret.

### Åpne punkter
- Issue #17: lukkes når første story i Epic 0 har kjørt en test mot Django 6.1. Gruppa avgjør.
- Issue #29: akseptkriteriene for Epic 0 bør teste tekst og ikke bytes. Tekstene om fonttools i `lag_cv_pdf.py` og i issuet bør rettes.
