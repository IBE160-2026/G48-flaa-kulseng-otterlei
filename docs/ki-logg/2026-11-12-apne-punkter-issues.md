# Åpne punkter som GitHub Issues

| | |
|---|---|
| **Dato** | 2026-11-12 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Commiten med dette innlegget, pull request på branchen `docs/apne-punkter-issues`, Issue #7–#11 |

## Mål

Flytte åpne punkter fra `issues.md`-filene i `.logs/` til GitHub Issues, slik foreleseren gjør i sitt eksempelprosjekt (beergame).

## Viktigste prompts

1. «Jeg har veldig lite erfaring med å jobbe med denne typen oppgave, Claude og GitHub. […] Foreleseren jobber også med sitt eget prosjekt "beergame" som finnes i GitHub under mappen IBE160-2026. Dette er prosjektet han bruker for å lære oss hvordan vi skal jobbe. Prosjektet hans er helt annerledes fra vår oppgave, men du kan eventuelt bruke inspirasjon herfra for å løse utfordringer på samme måte som han.»
2. «Ja, lag PR» (etter at Claude foreslo å føre åpne punkter som GitHub Issues, slik beergame gjør).

## Hva KI gjorde

- Leste `CLAUDE.md` og sesjonsloggene i beergame-repoet. Der føres åpne punkter som GitHub Issues med etiketten `agent`, og `issues.md` er utfaset.
- Foreslo samme ordning for oss, fordi sensor ser etter issues i historikken, og fordi alle i gruppa da ser åpne punkter på ett sted i stedet for i hver sin fil.
- Opprettet etiketten `agent` og Issue #7–#11 med de åpne punktene fra sesjonsloggene til Haakon og Ole.
- Endret avsnittet om sesjonslogg i `CLAUDE.md`, og la til en lenke til issuene i README.

## Våre vurderinger og korrigeringer

- Ole ba om endringen etter forslaget fra Claude.
- Resten av gruppa har ikke vurdert endringen ennå. Den tas opp i gjennomgangen av pull requesten, og gruppas vurderinger føres inn her etterpå.
- Claude tok ikke med punktet om git-oppsett fra Oles sesjonslogg som issue, fordi det er personlig oppsett og ikke noe som gjenstår i prosjektet.

## Resultat

- `CLAUDE.md` sier at åpne punkter føres som GitHub Issues med etiketten `agent`.
- README lenker til issuene.
- Issue #7–#11 er opprettet.

**Gjenstår:** Gruppa bekrefter endringen. Haakon markerer `.logs/haakon-ro/issues.md` som historikk, siden punktene hans nå ligger i Issue #9–#11.
