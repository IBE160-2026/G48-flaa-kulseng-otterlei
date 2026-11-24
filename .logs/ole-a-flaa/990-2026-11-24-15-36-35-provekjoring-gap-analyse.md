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
