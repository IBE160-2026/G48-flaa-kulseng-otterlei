# Eksempelpar A–D med fasit

| | |
|---|---|
| **Dato** | 2026-11-12 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `caaf91a`, `74301b4`, `7e37e64`, `639a1d2`, `444c287`, `c3dae11`, `4a84a93`, `e8d0fe6` og commiten med dette innlegget, på branchen `docs/eksempelpar`. [Kommentar på PR #25](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/25#issuecomment-6828694095) |

## Mål

- Gå gjennom Henriks PR #25 (arkitektur og UX gjort ferdig) og gi en kommentar.
- Lage eksempelparene A, B og C med fasit (PRD §10, issue #10, frist 18. november), og eksempelpar D med en innebygd instruksjon i annonsen (AD-6).
- Teste at `pdfplumber` klarer CV-en i to kolonner før P2 (AD-13).

## Viktigste prompts

1. «kan du gå gjennom branchen #25. og komme med en kommentar som eg kan gi til henrik» og «ja, eg er enig. legg ut kommentaren»
2. «hva er neste oppgave for meg? stories og epics?» og «ja la oss starte å Eksempelpar»
3. «hva tenkter du er best?» (skript eller Word for PDF-ene)
4. «ja, gå gjennom par A med meg» og «sysnest du den ser bra ut, og følger den krav»
5. «ja, rett begge (kva skjer når du rette dette)»
6. «men hvor og hva mener du eg skal nevne til notatet til ole» og «gjør det som er best» (par D)

## Hva KI gjorde

- **PR #25:** Gikk gjennom diffen og Oles kommentar, sjekket henvisningene og fant i tillegg at NFR-11 manglet i arkitekturen. Skrev en kommentar som Haakon fylte inn svaret sitt i, og la den ut.
- **Eksempelpar A–D:** Laget CV, annonse og `fasit.json` for hvert par etter briefen, PRD §10 og formatet i AD-17. Gikk gjennom A, B og C med Haakon i tre deler: CV, annonse og fasit. Hver del ble sjekket mot kravene i briefen, PRD-en og arkitekturen.
- **`app/testdata/lag_cv_pdf.py`:** Et skript som lager CV-PDF-ene fra `cv_kilde.txt` med `fpdf2` og fonten DejaVu Sans, med fast dato, så samme kilde alltid gir samme PDF. Utvidet med to kolonner for par C.
- **PDF-test mot CV C:** Med standardinnstillinger blander `pdfplumber` de to kolonnene linje for linje. Når mellomrommet mellom kolonnene finnes først, og hver kolonne leses for seg, kommer all teksten ut i riktig rekkefølge. `pdfplumber` kan beholdes, men innlesingen må finne kolonnene selv.
- **Feil KI fant og rettet selv:** Etter å ha sett på PDF-en som bilde: «Sommer 2023» havnet ikke i tidskolonnen, og kulepunktene ble blokkjustert. I testkoden for kolonnene brukte KI feil koordinater for utsnittene i første forsøk.

## Våre vurderinger og korrigeringer

- **Skript i stedet for Word:** Haakon spurte hva som var best, og valgte skriptet etter Claudes anbefaling. Grunnen var at CV-teksten da bare finnes ett sted, og at PDF-ene kan lages på nytt.
- **Par A:** Haakon spurte om CV-en fulgte kravene. Da fant Claude to ting som Haakon ba om å få rettet: annonsen gjelder nå «studenter eller nyutdannede», fordi Emma er ferdig våren 2027, og værvarsel-appen er gjort til bachelorprosjektet hennes, slik UX-en beskriver det. Haakon godtok fasiten, ba om at `andel` ble lagt til, beholdt aliaset «databasespørringer», og ba om at punktet om «nevne» og «påstå» kommer med i pull requesten.
- **Par B:** CV, annonse og fasit godkjent uten endringer. Haakon beholdt `andel` med slingringsmonn i testen, og ba om feltet `tone` i alle fasitene.
- **Par C:** Haakon spurte om CV-en burde være på norsk eller engelsk, og valgte norsk CV etter Claudes anbefaling, fordi det er det vanlige tilfellet for norske studenter. Han ba om at det doble `sprak`-feltet fjernes fra alle fasitene.
- **Par D:** Haakon lot Claude velge («gjør det som er best»). Claude valgte samme CV som A, og at `finn_eksempelpar` bare ser på A–C.
- **Arkitekturen:** Fasitformatet har nå detaljer som ikke står i AD-17. Arkitekturen oppdateres ikke i denne pull requesten, fordi PR #25 endrer samme dokument. Det gjøres etter at #25 er flettet.

## Resultat

- Eksempelpar A–D med fasit ligger i `app/testdata/eksempler/`, og skriptet ligger i `app/testdata/lag_cv_pdf.py`. Fonten ligger i `app/eksport/fonter/`.
- README har fått den nye mappen og en oversikt over eksempelparene.
- **Gjenstår:**
  - legge fasitformatet inn i AD-17 og merke punkt 3 i arkitekturens §8 som løst, etter at PR #25 er flettet
  - `ordliste.json` med synonymene parene trenger
  - innlesingen av PDF med kolonner (P1)
