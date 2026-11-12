# Endringer i PRD etter tilbakemelding

| | |
|---|---|
| **Gruppe** | G48 – Gutta krutt |
| **Dokument** | [`prd.md`](../../_bmad-output/planning-artifacts/prd/prd.md) (versjonen faglærer vurderte: commit `07a17f3`) |
| **Tilbakemelding** | [`tilbakemelding-prd.md`](../../_bmad-output/planning-artifacts/prd/tilbakemelding-prd.md) (commit `9217294`) |
| **Dato** | 2026-11-12 |
| **Status** | Godkjent av alle tre i gruppa uten endringer i pull request #14 (2026-11-12) |

Dette dokumentet forklarer hva som er endret i PRD-en etter faglærers tilbakemelding 2026-11-12, og hvorfor. Den forrige versjonen kan ses med `git show 07a17f3:_bmad-output/planning-artifacts/prd/prd.md`. Beslutningene står også i [beslutningsloggen](../../_bmad-output/planning-artifacts/prd/.memlog.md).

## Kort oppsummert

Faglærer pekte på fem forbedringer (4.1–4.5), der tre måtte avklares før UX, arkitektur og epics. Alle fem er innarbeidet:

1. **KI-kvaliteten testes nå mot ekte svar.** Det nye kravet NFR-11 sier at eksempelparene kjøres i KI-modus og sammenlignes med fasiten i en rapport.
2. **Det finnes en nødplan.** Målet er fortsatt alle åtte funksjonene, men har vi ikke kjerneflyten klar 2. desember, kuttes det i en fast rekkefølge.
3. **Resultatet er tre deler.** Analysen, brevet og CV-forbedringsforslagene lagres hver for seg. Tone og svarform velges ved brevet.
4. **Fasiten gjør «ingen oppdiktede påstander» sjekkbart**, med en liste over fakta i CV-en. Haakon lager den innen 18. november.
5. **Annonsen er data, ikke instruksjoner**, og brukeren får beskjed om å lese gjennom KI-teksten.

## Endringer, punkt for punkt

### 4.1 KI-kvaliteten ble bare testet mot lagrede svar (høy)

| Før | Etter | Hvem bestemte |
|---|---|---|
| Testene leser lagrede svar. FR-8 og SM-4 sjekkes manuelt, uten fast rutine. | **NFR-11:** Eksempelparene kjøres i KI-modus hver gang de lagrede svarene lages, og alltid før innlevering. Rapporten i `docs/evaluering/` skal vise 0 feilmerkede krav, 0 påståtte krav som mangler og 0 floskler, og svartid. SM-3 og SM-4 måles i denne kjøringen. | Claudes forslag, bygget på faglærers eksempel og AD-6 i arkitekturen |
| Fast format på gap-analysen sto bare i addendumet. | **FR-5:** KI-svaret har et fast format. Et svar som ikke følger formatet, er en feil etter NFR-5. | Claudes forslag, bygget på faglærers eksempel og AD-4 |

**Hvorfor:** Faglærer påpekte at de automatiske testene tester skriptet og visningen, ikke promptene. Evalueringskjøringen svarer også på refleksjonsspørsmål 2: en endret prompt som gjør svarene dårligere, blir oppdaget i rapporten, og promptene rettes før svarene tas i bruk.

### 4.2 Alle åtte funksjoner, uten kuttplan (høy)

| Før | Etter | Hvem bestemte |
|---|---|---|
| «Gruppa planlegger ikke å kutte noen av dem, fordi gruppa mener det er god nok tid.» | **§8.1 Nødplan:** Målet er fortsatt alle åtte. Sjekkpunkt 2. desember: P1–P5 ferdig og testet. Holder det ikke, kuttes (1) brevoppsettet i PDF, (2) CV-forbedringsforslag (P6), (3) KI-forklaringen i ATS-analysen. | Haakon i økten, etter at Claude sammenlignet tre rekkefølger. Rekkefølgen er faglærers forslag. |

**Hvorfor:** Faglærer pekte på tidsrisikoen for andre gang, etter at gruppa fjernet sjekkpunktet 2026-10-19. Nødplanen endrer ikke målet. Den gjør bare et eventuelt kutt til en beslutning tatt på forhånd. Rekkefølgen kutter først det som tar mye tid og gir lite (brevoppsett i PDF), og beholder nøkkelordanalysen i kode, som er den mest testbare delen av appen.

### 4.3 Uklar modell for Analyse, Resultat og lagring (medium)

| Før | Etter | Hvem bestemte |
|---|---|---|
| «Resultat» var alt en analyse gir, men brev og CV-forbedring ble laget med egne knapper. Det var uklart hva som ble overskrevet. | **§3:** Resultatet er tre deler som lagres og overskrives hver for seg. Et nytt brev overskriver bare brevet. En ny analyse eller endret CV-tekst (FR-2) sletter alle tre. | Haakon i økten (Claudes anbefaling, som AD-8) |
| Alle innstillinger ble valgt før «Analyser». | **FR-4, UJ-1, UJ-2, §6:** Språk og ønskede nøkkelord velges før «Analyser». Tone og svarform velges når brukeren ber om brev. | Haakon i økten (Claudes anbefaling) |
| Ønskede nøkkelord på eksempelpar ga en lagret KI-forklaring som ikke passet. | **FR-10:** Nøkkelordene tas med i matchen i kode, og den lagrede forklaringen vises med teksten «KI-forklaringen gjelder ikke dine egne nøkkelord i testmodus». | Haakon i økten (Claudes anbefaling, som AD-7). Løser issue #9. |

**Hvorfor:** Modellen styrer databasen og testene av sletting (FR-16), og faglærer ba om at den avklares før arkitekturen. Når tone velges ved brevet, kan brukeren bytte tone uten å kjøre gap-analysen på nytt. Det sparer et KI-kall.

### 4.4 Vage ledd i «ingen oppdiktede påstander» og fasiten (medium)

| Før | Etter | Hvem bestemte |
|---|---|---|
| FR-6: hvert avsnitt «viser til noe konkret fra CV-teksten». | **FR-6, FR-7:** Hvert avsnitt eller forslag inneholder et krav fra annonsen eller et punkt fra fasitens liste over fakta i CV-en. | Claudes forslag, bygget på faglærers formulering |
| FR-8: sjekkes manuelt etter en sjekkliste. | **FR-8:** Brevet nevner ingenting utenfor listen over fakta i CV-en og påstår ingen krav som mangler. Sjekkes i evalueringskjøringen. | Claudes forslag, bygget på faglærers formulering |
| Fasiten var beskrevet med henvisning til briefen, uten ansvarlig eller dato. | **§3, §10:** Fasiten har tre lister (fakta i CV-en, krav som matcher og mangler, sjekkliste for brevet) og nøkkelordene. Haakon lager den innen 18. november. | Listene: Claudes forslag etter faglærer. Ansvarlig og dato: Haakon i økten. |

**Hvorfor:** «Viser til noe konkret» er en skjønnsvurdering, så to i gruppa kunne vurdert det samme brevet forskjellig. Med en liste over fakta kan alle sjekke på samme måte, og deler av sjekken kan gjøres automatisk.

### 4.5 Annonsetekst og brukerens tillit til KI-svar (lav)

| Før | Etter | Hvem bestemte |
|---|---|---|
| NFR-3 dekket XSS, men ikke instruksjoner i annonsen. | **NFR-3:** Systemprompten sier at CV-tekst og annonse er data, ikke instruksjoner. **NFR-11 og §10:** Testes med en eksempelannonse med en innebygd instruksjon. | Claudes forslag, bygget på faglærers forslag og AD-5 og AD-6 |
| Ingen beskjed om å lese gjennom. | **NFR-4, §6:** Sider med KI-tekst viser «KI kan gjøre feil – les gjennom før du sender». | Faglærers forslag (som AD-5) |

### Øvrige endringer

- **FR-2:** En CV-tekst over 30 000 tegn avvises, slik AD-15 i arkitekturen foreslår. Dette er Claudes forslag.
- **FR-2, FR-3, FR-9:** Viser nå hvilken brukerreise de realiserer. Det var et mekanisk funn i tilbakemeldingen.
- **§11:** Viser til at arkitekturen i pull request #13 foreslår svar på de åpne spørsmålene.
- **§12:** Har en ny del som skiller mellom det Haakon valgte i økten og det som er Claudes forslag.
- **Addendum:** Fast format er nå et krav, og det er lagt til notater om evalueringskjøringen og resultat i tre deler.

## Endringer etter UX-en (2026-11-12)

Dette er ikke en endring etter faglærers tilbakemelding, men står her for å samle endringene i PRD-en. UX-en (pull request #15) gjorde om skjermbildene til en veiviser i fire steg, og det ga fire avvik fra PRD-en. Henrik valgte dem i UX-økten, og Ole og Haakon godkjente dem i pull request #15.

| Før | Etter |
|---|---|
| §6: skjermbildene «Ny analyse» og «Resultat» | Veiviser i fire steg: CV, Annonse og valg, Analyse, Søknad |
| FR-12: e-post og passord | I tillegg en avkrysning for personvern |
| FR-6, FR-7: brevet vises | Brevet kan rettes før kopiering og eksport, men endringene lagres ikke |
| FR-16: «Slett mine dokumenter» | I tillegg «Start ny søknad», som sletter resultatet og beholder CV-en |

## Hva som gjenstår

- **Eksempelparene med fasit** skal lages innen 18. november (Haakon), sammen med eksempelannonsen med innebygd instruksjon.
- **Refleksjonsspørsmålene** i tilbakemeldingens §7 er ikke besvart i PRD-en. De passer bedre i refleksjonsrapporten.
- ~~**Arkitekturen (PR #13)** bør sjekkes mot PRD-en når begge er flettet.~~ **Løst 2026-11-12:** Arkitekturen er sjekket og oppdatert etter UX-en (AD-22), og er satt til `final`.
