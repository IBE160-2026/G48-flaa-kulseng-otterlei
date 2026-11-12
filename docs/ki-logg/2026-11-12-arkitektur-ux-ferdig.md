# Arkitektur og UX gjort ferdig

| | |
|---|---|
| **Dato** | 2026-11-12 |
| **Hvem** | Henrik O. Kulseng |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `7f47bcb`, `65a2318`, `aec1f33`, commiten med dette innlegget, pull request på branchen `docs/arkitektur-ux-ferdig` |

## Mål

Gjøre arkitekturen og UX-en ferdige før epics og stories: bekrefte [Forslag]-punktene i arkitekturen (issue #18), legge UX-avvikene inn i arkitekturen (issue #21) og PRD-en (issue #20), og sette arkitekturen til `final`.

## Viktigste prompts

1. «jeg skal gjøre ferdig arkitekturen og ux-en»
2. Svar på Claudes spørsmål:
   - [Forslag]-punktene: «Jeg godtar alle»
   - Har Haakon bekreftet punktene fra PR #13? «Ja, han er enig»
   - Skal PRD-avvikene med i samme PR? «Ja, samme PR»

## Hva KI gjorde

- Leste åpne issues og fant at UX-en allerede var satt til `final` (issue #22 var gjort), og at arkitekturen sto som `draft` med [Forslag]-merker.
- Fjernet [Forslag]-merkene, satte arkitekturen til `final` og førte inn hvem som bekreftet hva.
- La inn de seks UX-avvikene i arkitekturen: en ny **AD-22 Veiviseren i fire steg**, personvernteksten i testmodus og avkrysningen ved registrering i AD-5, eksport av den redigerte brevteksten i AD-13, og `/ny-soknad/` i URL-listen.
- La inn de fire UX-avvikene i PRD-en (§6, FR-6, FR-7, FR-12, FR-16), markerte §11 som løst og forklarte endringene i `docs/endringer/endringer-prd.md`.
- Markerte avvikslisten i `EXPERIENCE.md` som løst, og oppdaterte beslutningsloggene og README.
- Foreslo selv noen detaljer i AD-22 som ikke sto i UX-en (se under).

## Våre vurderinger og korrigeringer

- Henrik godtok alle gjenstående [Forslag]-punkter, på samme måte som [ANTAKELSE]-punktene i UX-en. Ole og Haakon kan si fra i pull requesten hvis de er uenige.
- Henrik opplyste at Haakon er enig i punktene Ole og Henrik avtalte i PR #13.
- **Må bekreftes av gruppa i pull requesten:** Claudes egne tillegg i AD-22:
  - `analyse.tjenester.siste_steg()` er det eneste stedet som regner ut hvilket steg brukeren kan nå.
  - Steg 2 fyller inn eksempelannonsen når CV-teksten er et eksempelpar. UX-en sier at annonsen fylles inn i steg 2, men ikke hvordan, og annonsen kan ikke legges i økten (AD-10).
  - Den redigerte teksten deles i avsnitt på tomme linjer (fullt utkast) eller i punkter på linjeskift (kun forslag) ved eksport.
  - `dokumenter` ser om en analyse finnes gjennom `cv.analyse`, uten å importere `analyse` (AD-2).

## Resultat

- Arkitekturen er `final`, med AD-22. PRD-en, arkitekturen og UX-en samsvarer.
- Issue #18, #20, #21 og #22 kan lukkes når pull requesten er flettet. Issue #11 (arkitektur og UX-skisser) kan også lukkes.
- Neste steg er epics og stories (`bmad-create-epics-and-stories`).
