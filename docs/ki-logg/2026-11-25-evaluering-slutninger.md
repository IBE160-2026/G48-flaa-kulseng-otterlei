# Evalueringen i story 5.2 flagger slutninger som ikke står i CV-en (issue #28)

| | |
|---|---|
| **Dato** | 2026-11-25 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Commitene på branchen `docs/evaluering-slutninger` |

## Mål

Ta issue #28 mens gruppa ser over de åpne PR-ene.

## Viktigste prompts

1. «Ta issue #28»

## Hva KI gjorde

- Leste issue #28 med kommentarene, story 5.2 i `epics.md` og KI-logginnlegget fra prøvekjøringen av brevpromptene (PR #50).
- Fant at story 5.2 allerede løser det issuen opprinnelig handlet om. Det skiller mellom å nevne og å påstå et krav med en fast liste over «vil lære»-uttrykk og manuell bekreftelse, og det har en manuell fakta-sjekk når brevet og CV-en er på ulike språk. Haakon skrev 2026-11-20 at issuen lukkes når story 5.2 er bygget.
- Det som manglet, var Oles beslutning fra prøvekjøringen 2026-11-25: Evalueringen skal flagge slutninger som ikke står i CV-en, som datoen i brev C. Claude Code la til en avkrysning per avsnitt eller punkt i brevdelen av evalueringsrapporten, med eksemplet fra brev C.
- Satte først FR-7 som kravreferanse, men rettet den til FR-8 (ingen oppdiktede påstander) etter å ha lest kravene på nytt.

## Våre vurderinger og korrigeringer

- Beslutningen om å flagge slutninger i evalueringen, og ikke endre prompten, tok Ole 2026-11-25 (KI-logg `2026-11-25-provekjoring-brev-og-cv.md`, PR #50).
- Hvordan beslutningen er skrevet inn i story 5.2, er Claude Codes forslag. Gruppa må bekrefte det i pull requesten.

## Resultat

- `epics.md`, story 5.2: ny avkrysning for «ingen slutning som ikke står i CV-en eller annonsen» per avsnitt eller punkt.
- Issue #28 holdes åpen og lukkes når story 5.2 er bygget, slik Haakon skrev.
