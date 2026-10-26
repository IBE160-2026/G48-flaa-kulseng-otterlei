# CLAUDE.md

Felles instruksjoner for Claude Code i G48-prosjektet. Alle tre i gruppa bruker hver sin Claude; denne filen er det som gjør at alle følger de samme reglene. Endringer i filen går via pull request som alt annet.

## Prosjektet

- **Emne:** IBE160 Programmering med KI, Høgskolen i Molde, høst 2026. Gruppe G48 «Gutta krutt»: Ole A. Flaa, Henrik O. Kulseng, Haakon Remen Otterlei.
- **App:** AI CV & Job Application Assistant — se `_bmad-output/planning-artifacts/product-brief.md`.
- **Status:** Planlegging (product brief er ferdig i versjon 2; PRD, arkitektur og stories gjenstår). Ingen kode ennå.
- **Språk:** Skriv dokumentasjon, commit-meldinger og pull requests på norsk bokmål. Svar brukeren på norsk.

Les `README.md` og `docs/ki-logg/README.md` før du gjør endringer, så du kjenner strukturen og hva som er gjort.

## Hva sensor vurderer

Repoet vurderes ved fristen, og sporene av prosessen teller like mye som appen. Del 1 (70 % av karakteren): prosess og KI-styring 30 %, funksjonalitet 20 %, testing og kvalitetssikring 15 %, design 10 %, kodekvalitet 10 %, README og kjørbarhet 10 %, ryddighet i repoet 5 %. Sensor ser spesielt etter:

- planleggingsdokumenter som oppdateres underveis, og kode som kan spores tilbake til krav og stories
- små, jevne commits med beskrivende meldinger, og bruk av branches og pull requests
- lagrede prompts og eksempler på at gruppa har vurdert, rettet eller avvist KI-forslag
- dokumenterte beslutninger med begrunnelse
- at sensor kan kjøre appen kun ved å følge README, uten gruppens nøkler

## Arbeidsflyt med git

- **Aldri commit eller push direkte til `main`.** Start hver oppgave med `git switch main` og `git pull`, og lag en ny branch: `<type>/<kort-beskrivelse>`, f.eks. `docs/prd`, `feature/gap-analyse`, `fix/pdf-innlesing`.
- Lag små commits med beskrivende meldinger på norsk.
- Push branchen og lag en pull request med `gh pr create`. Følg malen i `.github/pull_request_template.md` (Hva, Hvorfor, Hva bør sjekkes, Sjekkliste), og ta alltid med sjekklisten uendret — GitHub legger den ikke inn automatisk når beskrivelsen sendes fra kommandolinjen. Ikke kryss av punkter på vegne av gruppa.
- **Ikke flett pull requests selv.** Gruppa ser over og fletter inn i `main`. Gjør det bare hvis du uttrykkelig blir bedt om det.
- Gi brukeren lenken til pull requesten når du er ferdig.

## KI-logg

Hver økt som fører til endringer i repoet, skal ha et innlegg i `docs/ki-logg/`, etter malen i `docs/ki-logg/README.md`: mål, viktigste prompts, hva KI gjorde, gruppens vurderinger og korrigeringer, og resultat med commits. Legg innlegget i samme pull request som endringene, og legg det til i tabellen i `docs/ki-logg/README.md`.

Skriv bare det som faktisk skjedde. Gruppens vurderinger og begrunnelser skal komme fra gruppa — spør hvis du er usikker, i stedet for å dikte dem opp.

## Mappestruktur

- `_bmad-output/planning-artifacts/` — planleggingsdokumenter fra BMAD (brief, PRD, arkitektur, epics, stories)
- `docs/tilbakemeldinger/` — tilbakemeldinger fra faglærer
- `docs/endringer/` — forklaring av større endringer i planleggingsdokumentene
- `docs/ki-logg/` — KI-logg
- Kode kommer i egen mappe når arkitekturen er bestemt.

**Ingen nye filer i rotmappen** utover det som hører hjemme der (README, CLAUDE.md, .gitignore og konfigurasjon). Når mappestrukturen endres, oppdater oversikten i README.

## Planleggingsdokumenter

- Bruk BMAD-skillene i `.claude/skills/` for planlegging (PRD, arkitektur, epics og stories).
- **Oppdater eksisterende dokumenter i stedet for å lage nye versjoner** (ikke `product-brief-v2.md`). Git-historikken tar vare på gamle versjoner, og sensor vil se hvordan planen utviklet seg.
- Større endringer etter tilbakemelding forklares i `docs/endringer/`.
- Når koden avviker fra planen, oppdater planen eller forklar avviket.

## Personvern og hemmeligheter

- Bruk bare oppdiktede CV-er, søknader og personer som testdata — aldri ekte personopplysninger.
- API-nøkler og andre hemmeligheter skal i `.env` (ignoreres av git). Lag `.env.example` uten ekte verdier.
- Kursmateriell, som sensorveiledningen, skal ikke inn i repoet.

## Samarbeid med gruppa

- Gruppa lærer git og GitHub underveis. Forklar kort og enkelt når nye begreper dukker opp.
- Si tydelig fra om hva som er dine forslag og hva gruppa må bekrefte.

## Sesjonslogg

Når en oppgave eller økt avsluttes, før sluttoppsummeringen, bruk `sesjonslogg`-skillen: dokumenter Oppgave + Plan + Resultat + åpne punkter i `.logs/<bruker>/`, og før åpne punkter i `.logs/<bruker>/issues.md`. Skillen committer loggfila lokalt; push gjør du selv. Gruppens egne regler for commit og språk gjelder foran dette.
