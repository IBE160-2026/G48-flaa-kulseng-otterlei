# Oppdatering av product brief etter tilbakemelding

| | |
|---|---|
| **Dato** | 2026-10-10 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `eee64f2`, `5b9f3e1` (revert), `d984277`, samt branchen `docs/omstrukturer-dokumentasjon` |

## Mål

Innarbeide faglærers tilbakemelding (`docs/tilbakemeldinger/tilbakemelding-product-brief.md`) i product brief, og dokumentere hva som ble endret.

## Viktigste prompts

1. «Kan du se på tilbakemeldingene fra "tilbakemelding-product-brief" og oppdatere vår "product-brief" slik den følger tilbakemeldingen. Etter det vil jeg også at du lager en egen fil som oppsummerer og forklarer hva du har endret på/fikset.»
2. «Ligger den gamle product brief fortsatt der? Eller har du endret den som var der?»
3. «Kan du ta det tilbake slik det var.»
4. «Jeg vil at du skal oppdatere product-brief etter tilbakemeldingene. Vil faglærer at vi oppdaterer product-brief eller lager en ny versjon men fortsatt beholder den gamle?»
5. «Jeg har en PDF-fil som inneholder sensorveiledningen … kan du se over den så du vet hva kriteriene er for innleveringen og hva sensor ser etter?»
6. «Forklar hva du mener med "flytte dokumentene ut av rotmappen".» — deretter «okey gjør det».

## Hva KI gjorde

- Leste tilbakemeldingen og skrev versjon 2 av product brief: strammet inn V1-omfanget, skrev ti testbare suksesskriterier, la til tre oppdiktede eksempelpar med fasit, gjorde ATS-delen om til en nøkkelordanalyse beregnet i kode, og beskrev en testmodus for sensor.
- Lagde `endringer-product-brief.md` som forklarer hver endring og hvorfor.
- La til lenker til planleggingsdokumentene i README.
- Leste sensorveiledningen for del 1 og foreslo tiltak: KI-logg, branches og pull requests, og ryddigere mappestruktur.
- Flyttet dokumentene ut av rotmappen og opprettet denne loggen.

## Våre vurderinger og korrigeringer

- **Ny fil eller oppdatere samme fil?** Etter første push var vi usikre på om den gamle briefen var tapt, og ba KI angre (`5b9f3e1`). Vi sjekket så hva faglærer faktisk ba om. Tilbakemeldingen sier: «Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg.» Vi valgte derfor å oppdatere samme fil og la git-historikken ta vare på versjon 1, og la endringene inn igjen (`d984277`). Vi avviste å lagre en kopi som `product-brief-v1.md`, fordi sensorveiledningen trekker for gamle versjoner i rotmappen.
- **Innhold KI har foreslått som vi må bekrefte i gruppa:** de tre eksempelparene med fasit, de ti suksesskriteriene, og at tone er låst til «formell/uformell». Dette er KI sine forslag og er ikke diskutert i gruppa ennå.
- **Arbeidsflyt:** De første endringene ble committet rett på `main`. Etter å ha lest sensorveiledningen bestemte vi at videre arbeid skal gå via branches og pull requests.
- **Sensorveiledningen** holdes utenfor repoet med `.gitignore`, siden den er kursmateriell.

## Resultat

- Product brief versjon 2 ligger i `_bmad-output/planning-artifacts/product-brief.md`.
- Endringsforklaringen ligger i `docs/endringer/endringer-product-brief.md`.
- README beskriver mappestrukturen og lenker til alle dokumentene.

**Gjenstår:** gå gjennom eksempelparene og suksesskriteriene i gruppa, lage selve eksempelfilene, og gå videre til PRD med BMAD.
