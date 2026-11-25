# Kostnaden for lag_lagrede_svar i story 4.5 (issue #39)

| | |
|---|---|
| **Dato** | 2026-11-25 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Commitene på branchen `docs/kostnad-lagrede-svar` |

## Mål

Ta issue #39 mens gruppa ser over de åpne PR-ene: avgjøre hvordan story 4.5 skal håndtere kostnaden for `lag_lagrede_svar` før Epic 4.

## Viktigste prompts

1. «Ta issue #39»

## Hva KI gjorde

- Leste issue #39 med Henriks tre forslag og Oles målinger 2026-11-24 og 2026-11-25, og story 4.5.
- Regnet anslaget på nytt per operasjon i stedet for å regne alle kallene som brev:

  | Operasjon | Kall | Pris per kall (målt) | Sum |
  |---|---|---|---|
  | `gap_analyse` (A, B, C × 2 språk) | 6 | 0,014–0,016 USD | ca. 0,09 USD |
  | `nokkelord_forklaring` (A, B, C × 2 språk) | 6 | ikke målt, antatt som gap-analysen | ca. 0,09 USD |
  | `brev` (A, B, C × 8 kombinasjoner) | 24 | 0,023–0,029 USD | ca. 0,62 USD |
  | `cv_forbedring` (A, B, C × 2 språk) | 6 | ca. 0,027 USD | ca. 0,16 USD |
  | Par D (gap-analyse og brev) | 2 | | ca. 0,04 USD |
  | **Totalt** | **ca. 44** | | **ca. 1,0 USD** |

  Det er under anslaget på 1,3 USD fra prøvekjøringen, som regnet alle kallene som brev.
- Spurte Ole om de tre valgene i issuen, med en anbefaling til hvert.
- Skrev valgene inn i story 4.5 og i listen over åpne issues i `epics.md`.

## Våre vurderinger og korrigeringer

Ole valgte alle tre anbefalingene:

1. **Kostnaden i USD i rapporten: ja.** Rapporten regner ut kostnaden per kall, per operasjon og totalt, så den første rapporten gir den faktiske prisen, slik Henrik foreslo.
2. **Delkjøring: `--operasjon <navn>`.** Henrik foreslo å bare lage på nytt operasjonene der hashen av prompten er endret. Ole valgte i stedet et valg som kjører én operasjon om gangen, fordi rapporten da er fersk for alt som kjøres. Før innlevering kjøres alt.
3. **Batch-API-et: ikke nå.** Med rundt 1 USD per kjøring er det plass til fire–fem kjøringer innenfor grensen på 5 USD i måneden.

## Resultat

- `epics.md`, story 4.5: to nye kriterier, for `--operasjon` og for kostnaden i USD i rapporten.
- `epics.md`, «Fra de åpne issuene»: nytt punkt om #39.
- Issue #39 står åpen til den første rapporten viser den faktiske kostnaden.
