# Hvordan evalueringen skiller mellom å nevne og å påstå et krav

| | |
|---|---|
| **Dato** | 2026-11-20 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `a56bf69` og commiten med dette innlegget, på branchen `docs/evaluering-pastander` (issue #28) |

## Mål

Bestemme hvordan evalueringskjøringen (AD-6, NFR-11) skal telle påstander i brev, brevforslag og CV-forbedring, før Haakon skriver storyene for evalueringen. Issue #28 viste to problemer: «Jeg vil gjerne lære SQL» er riktig for par A, men inneholder ordet SQL, og i par C er fasiten på norsk mens brevet er på engelsk.

## Viktigste prompts

1. «Haakon jobber med epics og stories nå. Hva kan jeg gjøre?»
2. «ok la oss gjøre issue #28, velg den løsningen som er best for oppgaven»

## Hva KI gjorde

- Leste AD-3 – AD-6, AD-17, FR-8, NFR-11, SM-4, PRD-addendumet og fasiten for par A.
- Vurderte fem løsninger: bare tekstsøk, bare manuell gjennomgang, at brevet selv lister påstandene sine, KI-vurdering alene, og tekstsøk og KI-vurdering i to trinn.
- Valgte to trinn og skrev det inn i AD-6:
  - Tekstsøk etter krav og alias fra `krav_mangler` finner kandidatsetningene.
  - Én KI-vurdering per svar avgjør om kandidatene er påstått, og lister utsagn uten dekning i `fakta_i_cv`, uansett språk.
  - Kontrollsetninger med kjent svar sjekker at vurderingen er til å stole på. Bommer den, er kjøringen ikke bestått.
  - Rapporten viser alle kandidatene, så gruppa kan overprøve dem.
- La til en enhetstest av kandidatsøket i AD-17, `ki/evaluering.py` og `kontrollsetninger.json` i strukturen, og påstander som ikke står i `fakta_i_cv` (FR-8) i listen over hva rapporten måler.
- Pekte selv på svakheten: Claude vurderer svar fra Claude og kan ta feil på samme måte. Det er grunnen til kontrollsetningene og til at alle kandidatene vises.

## Våre vurderinger og korrigeringer

- Ole ba Claude velge den løsningen som passer best for oppgaven. Løsningen er derfor Claudes valg, og Haakon og Henrik må godta den i pull requesten.

## Resultat

- AD-6 og AD-17 er oppdatert, og beslutningsloggen for arkitekturen har fått valget.
- **Gjenstår:** `ki/evaluering.py`, `ki/prompter/vurdering.md` og `kontrollsetninger.json` lages med storyen for evalueringen. Vurderingen gir rundt 30 ekstra API-kall per kjøring, og kostnaden må måles.
