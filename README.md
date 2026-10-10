# G48 — Gutta krutt

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Om appen

**AI CV & Job Application Assistant** hjelper norske studenter med å skreddersy jobbsøknader. Studenten laster opp CV-en sin og limer inn en stillingsannonse, og får en gap-analyse av hva som matcher og mangler, et utkast til søknadsbrev eller konkrete forslag, CV-forbedringer og en ATS-nøkkelordanalyse. Se [product brief](_bmad-output/planning-artifacts/product-brief.md) for full beskrivelse.

> Appen er under planlegging. Installasjon, oppstart, konfigurasjon og testing beskrives her når koden er på plass.

## Mappestruktur

```
.
├── _bmad/                         BMAD-rammeverket (planleggingsverktøy)
├── _bmad-output/
│   └── planning-artifacts/        Planleggingsdokumenter fra BMAD (brief, PRD, arkitektur, epics)
├── docs/
│   ├── endringer/                 Forklaring av endringer i planleggingsdokumentene
│   ├── ki-logg/                   Logg over KI-økter: prompts, vurderinger og korrigeringer
│   └── tilbakemeldinger/          Tilbakemeldinger fra faglærer
├── .claude/                       Claude Code-skills
├── CLAUDE.md                      Felles instruksjoner til Claude Code for hele gruppa
└── README.md
```

## Planleggingsdokumenter

- [Product brief](_bmad-output/planning-artifacts/product-brief.md) — produktbeskrivelse (versjon 2)

## Prosessdokumentasjon

- [KI-logg](docs/ki-logg/README.md) — hvordan vi har brukt og styrt KI, økt for økt
- [Tilbakemelding på product brief](docs/tilbakemeldinger/tilbakemelding-product-brief.md) — faglærers vurdering av versjon 1
- [Endringer i product brief](docs/endringer/endringer-product-brief.md) — hva som er endret etter tilbakemeldingen, og hvorfor

## Arbeidsflyt

Endringer gjøres på egne branches og flettes inn i `main` via pull requests. Hver KI-økt som fører til endringer i repoet, dokumenteres i [KI-loggen](docs/ki-logg/README.md).

Alle i gruppa bruker hver sin Claude Code. [`CLAUDE.md`](CLAUDE.md) inneholder de felles reglene som alle Claude-økter leser automatisk, slik at arbeidsflyten blir lik uansett hvem som jobber. Kjør `git pull` på `main` for å få siste versjon.

## Medlemmer

- Ole A Flaa
- Henrik O Kulseng
- Haakon Remen Otterlei
