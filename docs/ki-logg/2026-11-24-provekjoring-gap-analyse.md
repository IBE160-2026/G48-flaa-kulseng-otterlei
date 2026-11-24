# Prøvekjøring av gap-analyse-prompten mot Claude

| | |
|---|---|
| **Dato** | 2026-11-23 – 2026-11-24 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5), skillen `claude-api` |
| **Commits / PR** | Branchen `docs/provekjoring-gap-analyse` |

## Mål

Prøve `app/ki/prompter/gap_analyse.md` mot Claude før Epic 4 bygges. Ole venter på at Henrik og Haakon skal gå gjennom pull requestene, og Epic 4 trenger skjelettet fra Epic 0. Prøven skulle vise to ting:
- om prompten gir et svar som stemmer med fasiten
- hva ett kall faktisk koster (issue #39)

## Viktigste prompts

1. «Hva kan jeg gjøre mens jeg venter på at de skal godkjenne pull requestene?»
2. «Ja, prøvekjør»
3. «ta meg gjennom steg for steg hvordan jeg lager .env i worktree mappa, og hva annet jeg må gjøre (API-nøkkel osv)»

## Hva KI gjorde

- Foreslo prøvekjøringen som ett av tre alternativer og anbefalte den.
- Skrev et prøveskript **utenfor repoet**, i et eget Python-miljø med `anthropic` 2.12.0, `pydantic` og `pdfplumber`. Skriptet er ikke appkode og er ikke committet. Det gjør det samme som `ClaudeKlient` skal gjøre etter AD-4:
  - Deler `gap_analyse.md` i system og melding og bytter ut plassholderne.
  - Leser CV-teksten fra `cv.pdf` med pdfplumber og fjerner `<cv>`- og `<annonse>`-taggene fra teksten.
  - Bruker `messages.parse` med en pydantic-modell `GapAnalyse` (`krav`, `status`, `begrunnelse`), `claude-opus-5-5`, `effort: low`, `max_tokens` 16 000, `timeout=60` og `max_retries=0`.
  - Bruker ikke automatisk bytte til en annen modell, fordi AD-4 har valgt det bort.
- Ga Ole en trinnvis veiledning for å lage API-nøkkelen og `.env`. Claude så aldri nøkkelen. Skriptet leser den fra fila uten å skrive den ut.
- Kjørte ett kall for par A på norsk og sjekket svaret mot `fasit.json`. Sjekket også med kode at alle sitatene i begrunnelsene står ordrett i CV-teksten.

## Resultat av kallet

| | |
|---|---|
| Par, språk, effort | A, norsk, `low` |
| Tid | 4,2 sekunder |
| Tokens inn / ut | 2 341 / 312 (tankene er med i «ut») |
| Kostnad | 0,0156 USD (4 USD / 20 USD per million tokens) |
| `stop_reason` | `end_turn` |

| Krav | Status | Fasit |
|---|---|---|
| Python | matcher | matcher |
| SQL | mangler | mangler |
| Git | matcher | matcher |
| Førerkort klasse B | mangler | mangler |

- Kravene kom i samme rekkefølge som i annonsen, med korte navn, slik prompten ber om.
- Alle de fem sitatene i begrunnelsene står ordrett i CV-teksten.
- Prompten ber om sitater «i anførselstegn». Claude brukte "rette" anførselstegn og ikke «sjevroner». Det kan presiseres i prompten hvis gruppa vil.

**Hva det betyr for kostnaden (issue #39):** Ett kall for gap-analysen kostet under 2 cent. Henrik anslo 1–5 USD for en full kjøring av `lag_lagrede_svar` med rundt 45 kall. Brevene er lengre og koster mer per kall, men med dette tallet ser det ut til at en full kjøring havner nederst i det anslaget. Det er bare målt ett kall, så det må bekreftes i evalueringsrapporten (story 4.5 og 5.2).

## Våre vurderinger og korrigeringer

- Ole valgte prøvekjøringen blant de tre alternativene.
- Planen i [innlegget om API-kontoen](2026-11-20-api-konto.md) var å lage API-nøkkelen først når `app/.env` finnes i Epic 0. Ole lagde den nå, til denne prøven. Nøkkelen er knyttet til Default-arbeidsområdet, uten tilgang til Admin API, og utløper etter 30 dager (24. desember 2026). Til Epic 4 og evalueringen lages en ny nøkkel.
- Console spurte hvor koden kjører. Ole valgte «Et annet sted» (API-nøkkel), som Claude anbefalte, fordi appen og sensor skal bruke en nøkkel i `.env`, ikke innloggingsverktøyet `ant`.

## Resultat

- `app/ki/prompter/README.md`: Statusen sier nå at `gap_analyse.md` er prøvd med ett kall.
- Gjenstår:
  - Prøve de andre parene, særlig C (norsk CV og engelsk svar) og D (instruksjoner skjult i annonsen).
  - Prøve de tre andre promptene.
