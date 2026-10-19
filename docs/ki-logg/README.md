# KI-logg

Her dokumenterer vi hvordan vi bruker KI (Claude Code og BMAD) i prosjektet. Hver økt der KI gjør noe som ender i repoet, får ett innlegg. Målet er at man skal kunne følge hva vi ba om, hva KI foreslo, hva vi godtok, endret eller avviste, og hvilke commits det ble til.

## Innlegg

| Dato | Innlegg | Hvem |
|---|---|---|
| 2026-10-10 | [Oppdatering av product brief etter tilbakemelding](2026-10-10-oppdatering-product-brief.md) | Haakon |
| 2026-10-19 | [Utkast til PRD med bmad-prd](2026-10-19-utkast-prd.md) | Haakon |

## Slik skriver du et innlegg

1. Lag en fil som heter `ÅÅÅÅ-MM-DD-kort-beskrivelse.md` i denne mappen.
2. Kopier malen under og fyll den ut. Skriv kort — punktlister er nok.
3. Legg til en linje i tabellen over.
4. Commit innlegget sammen med endringene det beskriver, eller i samme pull request.

## Mal

```markdown
# <Tittel>

| | |
|---|---|
| **Dato** | ÅÅÅÅ-MM-DD |
| **Hvem** | <navn> |
| **Verktøy** | <f.eks. Claude Code (modell), BMAD-skill> |
| **Commits / PR** | <hash-er eller lenke til pull request> |

## Mål
Hva skulle vi oppnå i økten?

## Viktigste prompts
De promptene som styrte arbeidet, ordrett eller nesten ordrett.

## Hva KI gjorde
Kort om hva KI foreslo og laget.

## Våre vurderinger og korrigeringer
Hva vi sjekket, godtok, endret eller avviste — og hvorfor.

## Resultat
Hva ble endret i repoet, og hva gjenstår?
```
