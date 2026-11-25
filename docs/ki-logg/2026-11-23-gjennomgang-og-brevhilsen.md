# Gjennomgang av PR #40 og #41, og hilsenen i brevet

| | |
|---|---|
| **Dato** | 2026-11-20 – 2026-11-23 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Godkjenning av PR #40 og #41, fletting av PR #41 (`43b12df`), fletting av `main` inn i PR #44 og branchen `docs/brev-hilsen` |

## Mål

Finne ut hva som er neste steg etter sprint-planleggingen, gå gjennom pull requestene fra Henrik og Haakon, og få avgjort hvordan søknadsbrevet starter og slutter (A eller B fra Henriks kommentar på PR #34).

## Viktigste prompts

1. «Hva er neste steg?»
2. «Har jeg noen Pull requests fra de andre jeg må sjekke og godkjenne? Kan du isåfall gjøre det for meg»
3. «flett Haakons #PR41, jeg skal purre på gruppa, og vi velger alternativ A for brevet»

## Hva KI gjorde

- Listet opp de åpne pull requestene og issuene. I det første svaret sa Claude at alle de fire åpne pull requestene var Oles, og at Ole skulle starte Epic 0. Begge deler var feil. #40 er Henriks og #41 er Haakons, og ifølge `docs/arbeidsfordeling.md` eier Henrik og Haakon Epic 0. Claude rettet dette selv i de neste svarene.
- Leste endringene i #40 og #41 og godkjente begge i Oles navn, med kommentarer merket «Skrevet med Claude Code». På #40 påpekte Claude at «Gjenstår» fortsatt nevnte PR #35 og issue #16. Henrik rettet det før han flettet.
- Flettet PR #41 på Oles beskjed. Deretter flettet Claude `main` inn i `docs/sprint-planlegging` (PR #44) og løste konflikten i statuslinja i `CLAUDE.md`. Den nye linja har både eierne og PR #35 fra #41 og sprintstatusen fra #44.
- Fant ut at alternativ A allerede står i `app/ki/prompter/brev.md`, fordi Ole valgte det i PR #34. Claude endret derfor ikke prompten, og la bare bekreftelsen inn i innlegget om promptene.

## Våre vurderinger og korrigeringer

- Ole ba Claude sjekke og godkjenne pull requestene fra de andre, og ba Claude flette #41.
- Gruppa velger alternativ A: hilsen og avslutning med navnet fra CV-en står i brevteksten, ikke bare i PDF-en.

## Resultat

- PR #41 er flettet, og PR #44 kan flettes uten konflikt.
- Valget av A er dokumentert i [innlegget om promptene](2026-11-20-prompt-utkast.md).
- Gjenstår: Henrik og Haakon går gjennom PR #44 og #45.
