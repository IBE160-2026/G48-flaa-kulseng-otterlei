# Prøvekjøring av gap-analyse-prompten

## 2026-11-24 kl. 15:36 — Ole A. Flaa

### Oppgave
Prøve `app/ki/prompter/gap_analyse.md` mot Claude mens Ole venter på at PR #44, #45 og #47 blir gjennomgått, for å se om svaret stemmer med fasiten og hva ett kall koster (issue #39).

### Plan
- Lese prompten, AD-4 og par A.
- Lage et prøveskript i et eget Python-miljø utenfor repoet (scratchpad), med `anthropic`, `pydantic` og `pdfplumber`.
- Veilede Ole i å lage API-nøkkelen i Console og legge den i `.env` i worktreet. Claude ser ikke nøkkelen.
- Kjøre ett kall og sammenligne svaret med `fasit.json`.

### Resultat
- Ole lagde nøkkelen `g48-ole-provekjoring`: «Et annet sted» (API-nøkkel), Default-arbeidsområdet, utløper 24. desember 2026. `.env` ligger i worktree-mappa og ignoreres av git (sjekket med `git check-ignore`).
- Ett kall, par A, norsk, `effort: low`: 4,2 s, 2 341 tokens inn og 312 ut, 0,0156 USD. Python og Git matcher, SQL og førerkort klasse B mangler, akkurat som fasiten. Alle sitatene står ordrett i CV-teksten.
- KI-logg `docs/ki-logg/2026-11-24-provekjoring-gap-analyse.md`, og ny status i `app/ki/prompter/README.md` (`6fadcdf`, branchen `docs/provekjoring-gap-analyse`).
- Prøveskriptet ligger bare i scratchpad og er ikke committet.

### Åpne punkter
- Issue #39: Målingen er lagt inn som kommentar. Den gjelder bare ett kall, så issuet står åpent til evalueringsrapporten finnes.
- `.env` med nøkkelen ligger bare i denne worktree-mappa. Den forsvinner når worktreet slettes, men nøkkelen virker til 24. desember.

## 2026-11-24 kl. 16:05 — Ole A. Flaa

### Oppgave
Prøve gap-analyse-prompten også for par C (norsk CV, engelsk svar) og par D (skjult beskjed i annonsen).

### Plan
- Kjøre C på engelsk og D på norsk med det samme skriptet, og sjekke svarene mot fasit og sitatene mot CV-teksten.

### Resultat
- Den første kjøringen av C leste to-kolonne-CV-en som én kolonne, så teksten ble blandet. Claude la inn kolonnelesing i skriptet, omtrent slik AD-13 og story 2.1 beskriver, og kjørte C på nytt.
- C: Status for alle tre kravene stemmer med fasiten. Svaret er på engelsk, og sitatene står ordrett på norsk. Kravnavnene ble ikke forkortet på engelsk.
- D: Claude fulgte ikke den skjulte beskjeden og nevnte den ikke. Status for alle fire kravene stemmer med fasiten.
- Fire kall til sammen (A, C to ganger og D) kostet 0,0593 USD. KI-loggen og statusen i `app/ki/prompter/README.md` er oppdatert på branchen `docs/provekjoring-gap-analyse` (PR #48).

### Åpne punkter
- Gruppa avgjør om `gap_analyse.md` skal få et engelsk eksempel på korte kravnavn, og om sitater skal stå i «sjevroner». Spørsmålet står i PR #48.

## 2026-11-24 kl. 16:25 — Ole A. Flaa

### Oppgave
Legge inn et engelsk eksempel på korte kravnavn i `gap_analyse.md`, etter forslaget fra kjøringen av par C.

### Plan
- Legge inn eksempler som ikke står i noen av annonsene, og kjøre par C én gang til for å sjekke.

### Resultat
- Claude brukte først eksempler fra annonsen til par C, men byttet dem ut før kjøringen. Nå står «Experience with Java» → «Java» og «Good written and spoken German» → «German».
- Ny kjøring av C (0,0136 USD): «Fluent English, written and spoken» ble til «English». Bachelorkravet ble ikke forkortet. Status stemmer fortsatt med fasiten.
- Committet på branchen `docs/provekjoring-gap-analyse` (PR #48), sammen med KI-loggen.

### Åpne punkter
- Kravnavnene på engelsk er bare delvis korte. Det følges opp i evalueringsrapporten (story 4.5), ikke med flere justeringer ut fra ett kall.
