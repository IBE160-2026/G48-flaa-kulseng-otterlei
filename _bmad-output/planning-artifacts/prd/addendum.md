# Addendum til PRD

Notater fra PRD-arbeidet som ikke er krav, men som arkitekturen og UX-arbeidet bør ta med seg. Se [PRD](prd.md).

## Til arkitekturen

- **KI-leverandør (åpent spørsmål 1):** Kriteriene fra briefen er kvalitet på norsk tekst, kostnad og hvordan leverandøren behandler data som sendes til API-et. Det må være mulig å sette en forbruksgrense (NFR-9).
- **Nøkkelord (åpent spørsmål 2):** Hvis nøkkelordene finnes i kode, kan det for eksempel gjøres med en ordliste over vanlige ferdigheter, verktøy og sertifikater pluss brukerens egne nøkkelord. Da blir FR-19 og FR-20 fullt testbare mot fasiten. Hvis språkmodellen finner dem, bør i hvert fall matchingen (FR-20) skje i kode.
- **Lagrede svar (åpent spørsmål 3):** Et lite skript som kjører eksempelparene i KI-modus og lagrer svarene som filer i testdata-mappen. Skriptet kjøres på nytt når promptene endres, så de lagrede svarene ikke blir utdaterte.
- **Felles grensesnitt for KI-kall:** Testmodus (FR-9) og KI-modus bør bruke samme grensesnitt i koden, så resten av appen ikke vet hvilken modus den kjører i. Det gjør det også enkelt å teste feilhåndteringen i NFR-5.
- **Strukturerte KI-svar:** Gap-analysen (FR-5) bør komme tilbake i et fast format (f.eks. JSON med krav, status og begrunnelse), så appen kan vise den og testene kan sjekke den.
- **PDF (åpent spørsmål 4):** Bibliotek for innlesing og eksport velges tidlig og testes mot eksempel-CV C (to kolonner) før resten av flyten bygges.
- **Kryptering (FR-15):** Krypteringsnøkkelen settes med en miljøvariabel. Arkitekturen bør beskrive hva som skjer hvis nøkkelen mangler eller byttes.

## Til UX

- Gap-analysen og valget mellom «fullt utkast» og «kun forslag» er det faglærer ba om at UX-skissene viser (tilbakemeldingen på briefen, kriterium 4).
- Testmodus må synes på alle sider (FR-9), og meldingen ved egen CV i testmodus (FR-11) må forklare hva brukeren kan gjøre.
- Sletting må bekreftes (FR-16, FR-17), og «Min konto» bør forklare lagringspolicyen og hva som sendes til KI-tjenesten (NFR-4).
