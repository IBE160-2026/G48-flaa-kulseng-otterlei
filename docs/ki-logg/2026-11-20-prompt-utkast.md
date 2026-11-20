# Utkast til promptene

| | |
|---|---|
| **Dato** | 2026-11-20 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `f8dd015` og commiten med dette innlegget, på branchen `feature/prompt-utkast` |

## Mål

Lage utkast til promptene for KI-laget (AD-3, AD-5) mens Haakon lager epics og stories, slik at Ole er i gang når storyene for KI-laget kommer.

## Viktigste prompts

1. «ok, lag utkast til promtene»

## Hva KI gjorde

- Leste AD-3 – AD-6, FR-4 – FR-8, FR-18, FR-21, UX-reglene for KI-kortene, og annonsene og fasitene for A–D.
- Laget fire promptfiler i `app/ki/prompter/`: gap-analyse, brev og brevforslag, CV-forbedring og forklaring av nøkkelordene. Hver fil har en systemprompt (`## System`) og en brukermelding (`## Melding`) med plassholdere.
- La de samme fem reglene først i alle systempromptene: data er ikke instruksjoner, ingenting oppdiktet, krav som mangler påstås aldri, valgt språk, og ingen skryt. Sjekket med et lite skript at blokken er lik i alle fire filene, og at plassholderne stemmer med parameterne i AD-3.
- Tilpasset gap-analysen etter fasitene: krav hentes fra kravlisten i annonsen, får korte navn («Python», ikke «Erfaring med Python»), og en grad som pågår regnes som oppfylt bare hvis den blir ferdig før stillingen starter (par C).
- Skrev brevprompten etter kjennetegnene i `sprak_og_tone` i fasiten (fullt utkast med innledning, hoveddel og avslutning, kun forslag som punkter som viser til krav eller fakta).
- **Valgte å ikke kopiere flosklene fra fasiten inn i promptene.** Da ville evalueringen bare målt om modellen unngår akkurat de ordene. Promptene beskriver i stedet hva en floskel er, med egne eksempler.
- Skrev en README for mappen med formatet, plassholderne og feltnavnene promptene forutsetter i `ki/modeller.py`, og la formatet inn i AD-5.

## Våre vurderinger og korrigeringer

- Ole ba om utkastene uten å gi egne føringer. Valgene i utkastene er derfor Claudes forslag, og gruppa må se over dem i pull requesten.

## Resultat

- `app/ki/prompter/` med fire prompter og README. AD-5, beslutningsloggen og README i rotmappen er oppdatert.
- **Ikke prøvd mot API-et.** Det krever kreditt i Claude Console (issue #16).
- **Gjenstår:** prøve promptene på eksempelparene, prompten for vurderingen i evalueringen (`vurdering.md`, etter PR #33), og å rette feltnavnene når `ki/modeller.py` lages i Epic 0.
