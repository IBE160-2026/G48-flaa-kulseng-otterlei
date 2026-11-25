# Forslag til evalueringsregel for issue #28 (avvist)

| | |
|---|---|
| **Dato** | 2026-11-20 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `a56bf69` (forslaget i AD-6, senere fjernet), `b730857` og commiten med denne rettelsen, på branchen `docs/evaluering-pastander`, [PR #33](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/33) (issue #28) |

## Mål

Bestemme hvordan evalueringskjøringen (AD-6, NFR-11) skal telle påstander i brev, brevforslag og CV-forbedring, før Haakon skriver storyene for evalueringen. Issue #28 viste to problemer: «Jeg vil gjerne lære SQL» er riktig for par A, men inneholder ordet SQL, og i par C er fasiten på norsk mens brevet er på engelsk.

## Viktigste prompts

1. «Haakon jobber med epics og stories nå. Hva kan jeg gjøre?»
2. «ok la oss gjøre issue #28, velg den løsningen som er best for oppgaven»

## Hva KI gjorde

- Leste AD-3 – AD-6, AD-17, FR-8, NFR-11, SM-4, PRD-addendumet og fasiten for par A.
- Vurderte fem løsninger: bare tekstsøk, bare manuell gjennomgang, at brevet selv lister påstandene sine, KI-vurdering alene, og tekstsøk og KI-vurdering i to trinn.
- Valgte to trinn og skrev det inn i AD-6 (fjernet igjen etter gruppas valg, se under):
  - Tekstsøk etter krav og alias fra `krav_mangler` finner kandidatsetningene.
  - Én KI-vurdering per svar avgjør om kandidatene er påstått, og lister utsagn uten dekning i `fakta_i_cv`, uansett språk.
  - Kontrollsetninger med kjent svar sjekker at vurderingen er til å stole på. Bommer den, er kjøringen ikke bestått.
  - Rapporten viser alle kandidatene, så gruppa kan overprøve dem.
- La til en enhetstest av kandidatsøket i AD-17, `ki/evaluering.py` og `kontrollsetninger.json` i strukturen, og påstander som ikke står i `fakta_i_cv` (FR-8) i listen over hva rapporten måler.
- Pekte selv på svakheten: Claude vurderer svar fra Claude og kan ta feil på samme måte. Det er grunnen til kontrollsetningene og til at alle kandidatene vises.

## Våre vurderinger og korrigeringer

- Ole ba Claude velge den løsningen som passer best for oppgaven. Løsningen var derfor Claudes valg.
- **Gruppa avviste forslaget** etter at Haakon hadde godkjent en annen regel i story 5.2, som Claude foreslo i gjennomgangen av storyene (PR #35): en fast liste med uttrykk som «lære», «ønsker å» og «eager to». En setning med et slikt uttrykk regnes som «vil lære», og ellers som en mulig påstand som gruppa sjekker for hånd. Fakta-sjekken merkes som manuell når brevet er på et annet språk enn fasiten. Claude sammenlignet de to reglene for Ole og pekte på at «Jeg kan SQL og ønsker å lære mer» ikke blir telt som en påstand med listen.
- **Svakheten fanges opp likevel** av den manuelle kontrollen i story 5.2, der alle setninger som nevner et krav som mangler, listes i rapporten, også de som har et «vil lære»-uttrykk. Henrik og Haakon ba om at dette står her, så det ikke ser ut som om gruppa godtok hullet (kommentarer på PR #33, issue #42).
- **Begrunnelsen til gruppa:** regelen i 5.2 gir ingen ekstra API-kall, er enklere å kode, og gir samme svar hver gang.

## Resultat

- AD-6 og AD-17 er ikke endret. Forslaget og avvisningen står i beslutningsloggen for arkitekturen og her.
- Regelen fra story 5.2 og 6.1 bygges med Epic 5 og 6, og issue #28 lukkes når story 5.2 er ferdig.
