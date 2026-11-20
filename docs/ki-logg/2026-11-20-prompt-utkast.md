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
- **Gjenstår:** prøve promptene på eksempelparene og å rette feltnavnene når `ki/modeller.py` lages i Epic 0.

## Rettelser etter gjennomgangen av PR #35 (2026-11-20)

**Prompts:** «* at feltnavnene i ki/modeller.py passer med promptutkastene i #34 […] Kan du sjekke dette for meg?» og «Ja, rett #34»

Claude sammenlignet promptene med storyene for KI-laget i PR #35 (epics og stories) og fant to avvik i sine egne utkast:

| Avvik | Story i #35 | Hva som ble gjort |
|---|---|---|
| `del_av_cv` kunne være navnet på en del eller et sitat i anførselstegn, men evalueringen sjekker at utdraget finnes ordrett i CV-teksten | 6.1 | Prompten krever nå et ordrett utdrag uten anførselstegn |
| `mangler` het «krav som mangler i gap-analysen», men lages med `samle_mangler()`, som også tar med nøkkelord som mangler | 5.1 | Overskriften i brev og CV-forbedring og regel 3 i alle fire promptene sier nå «krav og nøkkelord som mangler» |

README for mappen viser nå at feltnavnene er sjekket mot #35, og at `svarform` i `Brev` forutsettes satt av koden.
