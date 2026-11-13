# Gjennomgang av PR #26 og #30, og presisering av AD-5

| | |
|---|---|
| **Dato** | 2026-11-12 – 2026-11-13 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `f482982`, `0454187` og commiten med dette innlegget, på branchen `docs/ad5-kontaktinfo` |

## Mål

- Finne ut hva som var neste steg for Ole etter at arkitektur og UX var ferdige.
- Gå gjennom Haakons PR #26 (eksempelpar A–D) og PR #30 (arbeidsfordelingen bekreftet), og skrive kommentarer.
- Rette avviket i AD-5 som gjennomgangen av PR #26 fant.

## Viktigste prompts

1. «Hva er neste steg?» og «OK, Haakon tar seg av epics og stories. Hva kan jeg gjøre?»
2. «Haakon har nå laget PR#26, kan du gå gjennom og gi meg en tilbakemelding på den?» og «skriv kommentaren her»
3. «kan du gjøre det samme for PR#30»
4. «Henrik har skrevet en kommentar til PR#26. Hva må jeg gjøre?» og «Start AD-5-PR-en»

## Hva KI gjorde

- **Neste steg:** Sjekket `main`, åpne PR-er og issues, og foreslo issue #10 (eksempeldata) for Ole. Det viste seg at Haakon allerede hadde laget eksempelparene i PR #26.
- **PR #26:** Leste CV-ene, annonsene og fasitene mot PRD §10, briefen og AD-5, AD-6 og AD-17, og skrev en kommentar med fire punkter:
  1. Fasitens `sprak_og_tone` og `floskler` dekker bare én av åtte brevvarianter.
  2. AD-5 sier at navn og e-post aldri sendes, men CV-teksten inneholder begge.
  3. Bachelorgraden i par C er ikke fullført ennå.
  4. D er en kopi av A.
- **PR #30:** Sjekket sitatene mot PR #6 og #13 og kuttrekkefølgen mot PRD §8.1, og skrev en kommentar med tre små forslag.
- **Henriks svar på PR #26:** Oppsummerte hva Ole måtte gjøre. Påpekte at Henrik og Haakon testet med samme versjon av `fpdf2` (2.9.0), så forskjellen i PDF-filene skyldes trolig noe annet enn versjonen. Det er ikke testet.
- **AD-5:** Presiserte at kontoens e-post og passord og avsenderopplysningene fra PDF-eksporten aldri sendes, men at CV-teksten sendes slik den står, også med navn og kontaktinformasjon. Gjorde den samme presiseringen i NFR-4, i personvernpåminnelsen og «Min konto» i EXPERIENCE.md og i mockupen for steg 2. Førte beslutningen inn i de tre beslutningsloggene og i `docs/endringer/endringer-prd.md`.
- **Ikke sjekket:** Claude kjørte ikke `pdfplumber` mot PDF-ene i PR #26, fordi biblioteket ikke var installert.

## Våre vurderinger og korrigeringer

- **Kommentaren på PR #26:** Ole la den ut. Han tok ikke med Claudes avsnitt om hva som ikke var sjekket, eller avslutningen om «nevne vs. påstå».
- **AD-5:** Henrik svarte i PR #26 at han heller mot å presisere AD-5, fordi CV-en må sendes for at analysen skal fungere, og brukeren laster den opp selv. Ole valgte å lage PR-en med presiseringen.
- **Claudes forslag som gruppa må bekrefte:**
  - Grunnen til å velge bort automatisk fjerning av kontaktinformasjon (står som Claudes vurdering i AD-5).
  - Den nye teksten i personvernpåminnelsen og i «Min konto».
- Haakon har ikke svart på punkt 2 ennå.

## Resultat

- AD-5, NFR-4, EXPERIENCE.md og mockupen for steg 2 sier nå det samme om hva som sendes til KI.
- Kommentarer på PR #26 og #30. PR #30 er flettet.
- **Gjenstår:** Haakon må bekrefte presiseringen. Fasitformatet per språk og tone (punkt 1 i PR #26) må bestemmes før PR #26 flettes.
