# Oppdatering av product brief etter tilbakemelding

| | |
|---|---|
| **Dato** | 2026-10-10 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `eee64f2`, `5b9f3e1` (revert), `d984277`, samt pull request #1 (`docs/omstrukturer-dokumentasjon`) og #2 (`docs/claude-md`), og branchen `docs/pr-mal` |

## Mål

Innarbeide faglærers tilbakemelding (`docs/tilbakemeldinger/tilbakemelding-product-brief.md`) i product brief, og dokumentere hva som ble endret.

## Viktigste prompts

1. «Kan du se på tilbakemeldingene fra "tilbakemelding-product-brief" og oppdatere vår "product-brief" slik den følger tilbakemeldingen. Etter det vil jeg også at du lager en egen fil som oppsummerer og forklarer hva du har endret på/fikset.»
2. «Ligger den gamle product brief fortsatt der? Eller har du endret den som var der?»
3. «Kan du ta det tilbake slik det var.»
4. «Jeg vil at du skal oppdatere product-brief etter tilbakemeldingene. Vil faglærer at vi oppdaterer product-brief eller lager en ny versjon men fortsatt beholder den gamle?»
5. «Jeg har en PDF-fil som inneholder sensorveiledningen … kan du se over den så du vet hva kriteriene er for innleveringen og hva sensor ser etter?»
6. «Forklar hva du mener med "flytte dokumentene ut av rotmappen".» — deretter «okey gjør det».
7. «Okey så jeg gir deg en oppgave. Du lager i branches og vi sjekker og pusher til main dersom vi liker det.»
8. «Vi har hver Claude for oss selv, hvordan husker du samtaler for hver av oss?» — deretter «ja lag en claude.md».
9. «Skriv innlegg i KI-loggen — dette gjør du automatisk, sant?» — deretter «er dette lurt?» om en sjekkliste i pull requestene, og «okey».

## Hva KI gjorde

- Leste tilbakemeldingen og skrev versjon 2 av product brief: strammet inn V1-omfanget, skrev ti testbare suksesskriterier, la til tre oppdiktede eksempelpar med fasit, gjorde ATS-delen om til en nøkkelordanalyse beregnet i kode, og beskrev en testmodus for sensor.
- Lagde `endringer-product-brief.md` som forklarer hver endring og hvorfor.
- La til lenker til planleggingsdokumentene i README.
- Leste sensorveiledningen for del 1 og foreslo tiltak: KI-logg, branches og pull requests, og ryddigere mappestruktur.
- Flyttet dokumentene ut av rotmappen og opprettet denne loggen.
- Forklarte at Claude-hukommelsen er lokal for hver person, og lagde `CLAUDE.md` med felles regler som alle gruppemedlemmenes Claude leser automatisk.
- Lagde en mal for pull requests (`.github/pull_request_template.md`) med sjekkliste for KI-logg, README og tester, og la inn i `CLAUDE.md` at Claude alltid skal ta med sjekklisten.

## Våre vurderinger og korrigeringer

- **Ny fil eller oppdatere samme fil?** Etter første push var vi usikre på om den gamle briefen var tapt, og ba KI angre (`5b9f3e1`). Vi sjekket så hva faglærer faktisk ba om. Tilbakemeldingen sier: «Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg.» Vi valgte derfor å oppdatere samme fil og la git-historikken ta vare på versjon 1, og la endringene inn igjen (`d984277`). Vi avviste å lagre en kopi som `product-brief-v1.md`, fordi sensorveiledningen trekker for gamle versjoner i rotmappen.
- **Innhold KI har foreslått som vi må bekrefte i gruppa:** de tre eksempelparene med fasit, de ti suksesskriteriene, og at tone er låst til «formell/uformell». Dette er KI sine forslag og er ikke diskutert i gruppa ennå.
- **Arbeidsflyt:** De første endringene ble committet rett på `main`. Etter å ha lest sensorveiledningen bestemte vi at videre arbeid skal gå via branches og pull requests.
- **Sensorveiledningen** holdes utenfor repoet med `.gitignore`, siden den er kursmateriell.
- **Arbeidsdeling med KI:** Vi avtalte at Claude lager branches og pull requests, mens gruppa selv ser over og fletter inn i `main`.
- **Felles regler:** Siden hver av oss har sin egen Claude, ville vi at reglene skulle ligge i repoet (`CLAUDE.md`) i stedet for i hver enkelts lokale Claude-hukommelse.
- **Sjekkliste i pull requests:** Vi spurte om det var lurt før vi sa ja. KI-ens vurdering var at det koster lite og gir en fast rutine, men at avkrysning uten faktisk kontroll er verdiløst, og at listen må være kort. Vi valgte fire punkter. Claude skal ikke krysse av på vegne av gruppa.

## Resultat

- Product brief versjon 2 ligger i `_bmad-output/planning-artifacts/product-brief.md`.
- Endringsforklaringen ligger i `docs/endringer/endringer-product-brief.md`.
- README beskriver mappestrukturen og lenker til alle dokumentene.
- `CLAUDE.md` inneholder felles regler for arbeidsflyt, KI-logg, mappestruktur og personvern.
- Pull requests har en mal med sjekkliste.

**Gjenstår:** gå gjennom eksempelparene og suksesskriteriene i gruppa, lage selve eksempelfilene, og gå videre til PRD med BMAD.
