# PRD rettet etter faglærers tilbakemelding

| | |
|---|---|
| **Dato** | 2026-11-12 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5), `bmad-prd` (oppdatering) |
| **Commits / PR** | Branch `docs/prd-tilbakemelding`, se pull requesten |

## Mål

Rette PRD-en etter faglærers tilbakemelding fra 2026-11-12 ([tilbakemelding-prd.md](../../_bmad-output/planning-artifacts/prd/tilbakemelding-prd.md)), særlig de tre punktene som må avklares før UX, arkitektur og epics: evalueringskjøring (4.1), kuttrekkefølge (4.2) og modellen for Resultat (4.3).

## Viktigste prompts

1. «hvordan ligger vi an? kva har vi fått gjort og hva står igjen» (Claude foreslo PRD-rettingen som neste steg for Haakon)
2. «ja, start på PRD-rettingen»
3. «hva er forskjellen på kuttrekkefølgene»
4. «faglærers forslag, og 2. desember»

I tillegg svarte Haakon på fire spørsmål i en dialog med faste svaralternativer (se under).

## Hva KI gjorde

- Leste PRD-en, beslutningsloggen, tilbakemeldingen og arkitekturen i PR #13, som ikke er flettet ennå, men som allerede foreslår svar på 4.1, 4.3 og 4.5 (AD-4 – AD-8, AD-15).
- Pekte på at faglærers punkt 4.2 (kuttrekkefølge) er i strid med gruppas beslutning fra 2026-10-19 om ingen kuttplan, og lot gruppa avgjøre det.
- Stilte spørsmål om det som måtte avgjøres av gruppa, med en anbefaling for hvert:
  - nødplan eller ingen kuttplan
  - hvor tone og svarform velges
  - ønskede nøkkelord på eksempelpar i testmodus
  - ansvarlig og dato for fasiten
- Forklarte forskjellen på tre mulige kuttrekkefølger (faglærers forslag, bakfra etter prioritet, og PDF først) og anbefalte faglærers forslag.
- Skrev egne forslag til 4.1, 4.4 og 4.5, bygget på faglærers formuleringer og arkitekturen:
  - nytt krav NFR-11 om evalueringskjøring
  - fast format i FR-5
  - fasit med en liste over fakta i CV-en
  - annonsen er data og ikke instruksjoner
  - varselet «KI kan gjøre feil»
- Oppdaterte PRD-en, addendumet og beslutningsloggen, og skrev [docs/endringer/endringer-prd.md](../endringer/endringer-prd.md).

## Våre vurderinger og korrigeringer

- **Kuttplan (4.2):** Haakon valgte en nødplan, så målet om alle åtte funksjonene står, men med et sjekkpunkt og en kuttrekkefølge. Han ba om en forklaring på forskjellen mellom rekkefølgene før han valgte. Han valgte faglærers rekkefølge og sjekkpunktet 2. desember. Dette endrer gruppas beslutning fra 2026-10-19.
- **Resultat (4.3):** Haakon valgte tre deler, med tone og svarform valgt ved brevet (Claudes anbefaling).
- **Nøkkelord i testmodus (issue #9):** Haakon valgte at egne nøkkelord tas med i matchen, med en merknad på den lagrede forklaringen (Claudes anbefaling).
- **Fasit (4.4):** Haakon tar ansvaret og lager den innen 18. november.
- **4.1, 4.4 og 4.5 for øvrig:** Dette er Claudes forslag, og de er ikke vurdert av gruppa ennå. De er merket i PRD-ens §12.
- Valgene over ble gjort av Haakon i økten. Henrik og Ole må se over og bekrefte dem i pull requesten. _Gruppa fyller inn her hva som ble godkjent, rettet eller avvist._

## Resultat

- PRD-en (§3, UJ-1, UJ-2, FR-2 – FR-10, NFR-3, NFR-4, ny NFR-11, §6, §8.1, SM-3, SM-4, §10 – §12), addendumet og beslutningsloggen er oppdatert.
- Nytt dokument: [docs/endringer/endringer-prd.md](../endringer/endringer-prd.md).

**Gjenstår:**
- Gruppa bekrefter endringene i pull requesten.
- Eksempelpar A–C med fasit innen 18. november (Haakon), pluss eksempelannonsen med innebygd instruksjon.
- Refleksjonsspørsmålene i tilbakemeldingens §7 besvares i refleksjonsrapporten.
- Arkitekturen (PR #13) sjekkes mot PRD-en når begge er flettet.
