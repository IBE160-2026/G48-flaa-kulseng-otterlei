# Addendum til PRD

Notater fra PRD-arbeidet som ikke er krav, men som arkitekturen og UX-arbeidet bør ta med seg. Se [PRD](prd.md).

## Til arkitekturen

- **KI-leverandør (åpent spørsmål 1):** Kriteriene fra briefen er kvalitet på norsk tekst, kostnad og hvordan leverandøren behandler data som sendes til API-et. Det må være mulig å sette en forbruksgrense (NFR-9).
- **Nøkkelord (åpent spørsmål 2):** Gruppa har bestemt at nøkkelordene finnes i kode. Det kan for eksempel gjøres med en ordliste over vanlige ferdigheter, verktøy og sertifikater pluss brukerens egne nøkkelord. Da blir FR-19 og FR-20 fullt testbare mot fasiten.
- **Lagrede svar (FR-10):** Søknadsbrev og brevforslag trengs for alle 8 kombinasjoner av innstillinger per eksempelpar (24 til sammen). Gap-analyse, CV-forbedringsforslag og KI-forklaring for nøkkelordene trengs per språk (18 til sammen). Det blir 42 lagrede svar. Et lite skript som kjører eksempelparene i KI-modus og lagrer svarene som filer i testdata-mappen. Skriptet kjøres på nytt når promptene endres, så de lagrede svarene ikke blir utdaterte.
- **Felles grensesnitt for KI-kall:** Testmodus (FR-9) og KI-modus bør bruke samme grensesnitt i koden, så resten av appen ikke vet hvilken modus den kjører i. Det gjør det også enkelt å teste feilhåndteringen i NFR-5.
- **Strukturerte KI-svar:** Gap-analysen (FR-5) skal komme tilbake i et fast format (f.eks. JSON med krav, status og begrunnelse), så appen kan vise den og testene kan sjekke den. Etter faglærers tilbakemelding 2026-11-12 er dette et krav i FR-5.
- **Evalueringskjøring (NFR-11):** Det er naturlig at skriptet som lager de lagrede svarene, også skriver evalueringsrapporten, så de alltid lages sammen (slik AD-6 i arkitekturen foreslår). Påstander om krav som mangler, og floskler, kan telles med tekstsøk mot fasitens lister. Det som ikke kan telles automatisk, sjekkes manuelt og føres i samme rapport.
- **Resultat i tre deler (§3):** Analysen, brevet og CV-forbedringsforslagene lagres hver for seg. En ny analyse eller endret CV-tekst sletter alle tre, mens et nytt brev bare overskriver brevet. Se AD-8 i arkitekturen.
- **PDF (åpent spørsmål 3):** Bibliotek for innlesing og eksport velges tidlig og testes mot eksempel-CV C (to kolonner) før resten av flyten bygges. PDF-eksporten skal ha brevoppsett med dato og avsender (FR-23), så biblioteket må kunne lage et enkelt brevoppsett med æ, ø og å.
- **Kryptering (FR-15):** Krypteringsnøkkelen settes med en miljøvariabel. Arkitekturen bør beskrive hva som skjer hvis nøkkelen mangler eller byttes.

## Til UX

- Gap-analysen og valget mellom «fullt utkast» og «kun forslag» er det faglærer ba om at UX-skissene viser (tilbakemeldingen på briefen, kriterium 4).
- Testmodus må synes på alle sider (FR-9), og meldingen ved egen CV i testmodus (FR-11) må forklare hva brukeren kan gjøre.
- Før PDF-eksport av søknadsbrevet må brukeren kunne skrive inn avsender (navn, eventuelt e-post og telefon), og det bør stå at opplysningene ikke lagres (FR-23).
- Sletting må bekreftes (FR-16, FR-17), og «Min konto» bør forklare lagringspolicyen og hva som sendes til KI-tjenesten (NFR-4).
