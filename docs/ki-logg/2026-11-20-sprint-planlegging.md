# Sprint-planlegging og sjekk av at planen er klar

| | |
|---|---|
| **Dato** | 2026-11-20 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5), BMAD-skillen `bmad-sprint-planning` |
| **Commits / PR** | Commitene på branchen `docs/sprint-planlegging` |

## Mål

Sjekke at planleggingen er klar for koding, og lage sprintstatusen som alle bruker til å følge storyene fra Epic 0 og ut. Ole har ansvaret for sprintplanen.

## Viktigste prompts

1. «Hva er neste steg?» (etter at alle åpne PR-er var flettet)
2. «Yes i have the responisbility for the sprint plan, lets make that now»

## Hva KI gjorde

- Kjørte sjekken i `bmad-sprint-planning`: kan en utvikler bygge storyene uten å måtte finne på beslutninger som ikke står noe sted?
  - Alle 23 FR, 11 NFR og 36 UX-krav (UX-DR1 – UX-DR36) i kravoversikten finnes i minst én story.
  - Alle stories og alle epics er godkjent av Haakon i `gjennomgang.md`.
  - De åpne spørsmålene i PRD §11 og punktene i §8 i arkitekturen er løst.
  - Resultat: **PASS**, med to små merknader (se under).
- Lagde `_bmad-output/implementation-artifacts/sprint-status.yaml` med skriptet i skillen: 8 epics og 36 stories med status `backlog`, og en valgfri retrospektiv per epic. Skriptet ga ingen advarsler, og filen ble validert.
- Oppdaterte mappestrukturen i README og `CLAUDE.md`, og statuslinjen i `CLAUDE.md`.

## Våre vurderinger og korrigeringer

- **To merknader fra sjekken.** Ole valgte å nevne dem i pull requesten i stedet for å endre storyene:
  1. `docs/testplan.md` lages ikke av noen story. Story 0.3 er den første som skriver i den.
  2. Story 0.1 lager `app/`, og der ligger allerede promptutkastene i `app/ki/prompter/` (PR #34). De må ikke overskrives.
- **Nøkler med æ, ø og å.** Skriptet lager nøklene fra overskriftene, for eksempel `2-4-prøve-med-eksempel-a-b-eller-c`, og det har ingen innstilling for nøkler uten disse bokstavene. Claude foreslo å beholde dem, fordi git takler slike filnavn og gruppa velger navnene på branchene selv. Ole godtok forslaget.
- **Rettelse av et KI-forslag.** Claude sa tidligere i økten at issue #28 kunne lukkes når #33 var flettet. Det stemmer ikke: #28 er et krav til evalueringen i story 5.2, og det er ikke bygget ennå. Issuen står åpen.

## Resultat

- `sprint-status.yaml` finnes og viser alle 36 storyene i byggerekkefølge.
- **Gjenstår:** Epic 0 (eiere Henrik og Haakon). Hver story bygges med `bmad-build`, og statusen oppdateres i `sprint-status.yaml` underveis.
