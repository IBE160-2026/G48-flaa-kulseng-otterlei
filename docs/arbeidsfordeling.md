# Arbeidsfordeling og fremdriftsplan

| | |
|---|---|
| **Gruppe** | G48 – Gutta krutt |
| **Dato** | 2026-11-12 |
| **Status** | Forslag fra Claude Code, **bekreftet av gruppa 2026-11-12** (pull request #6 og #13) |
| **Frist** | 15. desember 2026 |

Dette dokumentet fordeler ansvaret for resten av prosjektet mellom de tre i gruppa og setter opp en ukeplan fram til fristen. Forslaget bygger på [product brief](../_bmad-output/planning-artifacts/product-brief.md), [PRD-en](../_bmad-output/planning-artifacts/prd/prd.md), [tilbakemeldingen på PRD-en](../_bmad-output/planning-artifacts/prd/tilbakemelding-prd.md) og sensorveiledningen for del 1. Gruppa går gjennom og retter det i pull requesten før det tas i bruk. Når planen endres underveis, oppdateres dette dokumentet.

**Endret 2026-11-12:** Henrik laget arkitekturen, som her var lagt til Ole. Ole tar i stedet ansvaret for KI-laget (`ki/`) når kodingen starter. Ole og Henrik avtalte det i pull request #13, og Haakon sa seg enig 2026-11-12.

## 1. Status 12. november

**Ferdig:** Product brief (versjon 2) og PRD med 23 FR, 10 NFR og 10 suksesskriterier. KI-logg, beslutningslogg, mal for pull requests og `CLAUDE.md` med felles regler.

**Gjenstår:** Arkitektur, UX, eksempeldata med fasit, epics og stories, all koden, testene, README for kjøring og refleksjonsrapporten.

**Risikoer:**

1. **Ingen kode ennå.** Sensorveiledningen nevner «hele eller nesten hele koden i én eller noen få commits rett før fristen» som et varseltegn. Kode må inn i `main` fra uke 2 og jevnt fram til fristen.
2. **Commit-historikken viser bare én person.** Sensor ser etter at «arbeidet er utført av gruppen over tid». Alle tre skal committe jevnt på egne branches fra nå.
3. **Tilbakemeldingen på PRD-en (12. november) har tre punkter som må avklares før arkitekturen:** modellen for Resultat og lagring (4.3), evalueringskjøring i KI-modus og fast format på KI-svar (4.1), og kuttrekkefølge (4.2).
4. **`architecture/technology.md` beskriver et annet prosjekt** (Pytagoras-nettsiden), og er lagt inn som referanse. Den er mye større enn appen vår trenger. Arkitekturen vår bør hente prinsippet om mock-fallback (som tilsvarer testmodusen i FR-9) og deler av kjernestacken, men ikke Redis, Caddy, Railway, betaling og lignende.

## 2. Ansvarsområder

Hver person eier et område av appen, med både planlegging, kode og tester. Å eie et område betyr å ha ansvaret for at det blir ferdig, ikke å gjøre alt alene.

### Ole A. Flaa — KI-laget

| Fase | Oppgaver | Krav |
|---|---|---|
| Kode | KI-laget (`ki/`, arkitekturen AD-3 – AD-6): felles grensesnitt for KI-modus og testmodus, prompts, gap-analyse, søknadsbrev og brevforslag, CV-forbedringsforslag, KI-forklaring i ATS-analysen | FR-5 – FR-11, FR-18, FR-21, NFR-5, NFR-9 |
| Test | Skript som lager de 42 lagrede svarene, og evalueringskjøring i KI-modus mot fasiten | FR-10, SM-3, SM-4 |

### Henrik O. Kulseng — arkitektur, UX og frontend

| Fase | Oppgaver | Krav |
|---|---|---|
| Planlegging | Arkitektur med `bmad-architecture` (gjort, PR #13): teknologivalg, datamodell, KI-leverandør (åpent spørsmål 1) og formatet på KI-svarene | §11, addendum |
| Planlegging | UX med `bmad-ux`: skisser av de fire skjermbildene, særlig gap-analysen og valget mellom «fullt utkast» og «kun forslag» | §6, addendum |
| Kode | Alle sidene, registrering og innlogging i grensesnittet, testmodus-banner, tilbakemelding mens KI jobber, eksport og kopiering, tilgjengelighet | FR-4, FR-12, FR-13, FR-22, FR-23, NFR-6 – NFR-8 |
| Test | Ende-til-ende-tester av kjerneflyten | SM-1, SM-7 |
| Fast rolle | Eier README og prøvekjøring etter README på en ren maskin | NFR-1, SM-10 |

### Haakon Remen Otterlei — data, sikkerhet og testgrunnlag

| Fase | Oppgaver | Krav |
|---|---|---|
| Planlegging | Eksempelpar A, B og C med fasit (fakta i CV-en, krav som mangler, floskler), retting av PRD-en etter tilbakemeldingen | §10, tilbakemelding 4.1–4.4 |
| Kode | Opplasting og innlesing av CV (PDF-test mot CV C først), stillingsannonse, ATS-nøkkelord i kode, konto, kryptering, tilgangskontroll og sletting | FR-1 – FR-3, FR-14 – FR-17, FR-19, FR-20 |
| Test | Enhetstester for nøkkelord, innlesing, tilgangskontroll, kryptering og sletting | NFR-2, SM-2, SM-6, SM-8, SM-9 |
| Fast rolle | Holder oversikt over prosessdokumentene (KI-logg, endringer, planleggingsdokumenter) | NFR-10 |

### Felles for alle

- **Issue → branch → pull request.** Hver story får et issue på GitHub. Arbeidet gjøres på en egen branch, og pull requesten viser til storyen og FR-ene.
- **Gjennomgang.** Hver pull request godkjennes av én annen i gruppa, med en kommentar om hva som er sjekket. Feil som blir funnet i KI-generert kode, skrives i pull requesten.
- **KI-logg.** Hver skriver innlegg for sine egne økter, og skriver ned med en gang når et KI-forslag blir avvist eller rettet.
- **Små commits** med beskrivende meldinger, helst hver arbeidsdag.
- **Refleksjonsrapporten** skrives sammen i uke 5, med hver sin personlige refleksjon.

## 3. Ukeplan

| Uke | Mål | Ferdig når |
|---|---|---|
| **1** (12.–18. nov) | PRD-en rettes etter tilbakemeldingen. Arkitektur, UX og eksempeldata lages parallelt. Deretter epics og stories (`bmad-create-epics-and-stories`) og `bmad-sprint-planning`. Kodeskjelett med én testkommando og automatisk testkjøring på GitHub. | Planleggingsdokumentene er flettet inn i `main`, og stories finnes som issues |
| **2** (19.–25. nov) | En enkel kjerneflyt i testmodus fra start til slutt: registrere, laste opp CV, lime inn annonse, få gap-analyse og søknadsbrev med lagrede svar | SM-1 i testmodus kan kjøres |
| **3** (26. nov – 2. des) | P1–P5 ferdige og stabile, også i KI-modus, med kryptering og sletting. Arbeidet med P6 og P7 startes | Testene for P1–P5 kjører uten feil |
| **4** (3.–9. des) | P6–P8 ferdige. Evalueringskjøring i KI-modus med resultatet dokumentert. Design og tilgjengelighet pusses | Alle FR-er er implementert |
| **5** (10.–15. des) | Ingen nye funksjoner fra 10. desember. Feilretting, prøvekjøring etter README på en ren maskin, oppdatering av planene der koden avviker, og refleksjonsrapport | Repoet er klart til innlevering |

## 4. Avhengigheter

- Epics og stories bygger på arkitekturen, så arkitekturen bør være ferdig først i uke 1.
- UX og eksempeldata kan lages samtidig med arkitekturen.
- PDF-biblioteket testes mot eksempel-CV C før resten av innlesingen bygges.
- Eksempeldata med fasit må være ferdige før gap-analysen kodes (PRD §10), siden testene og de lagrede svarene bygger på dem.
- Innlogging og kryptering kommer tidlig, fordi det er vanskelig å legge til i etterkant (PRD §8.1).

## 5. Må avgjøres av gruppa

1. ~~Om fordelingen av ansvarsområder passer, eller om noe bør byttes.~~ **Avgjort 2026-11-12:** Fordelingen er bekreftet, med byttet mellom Ole og Henrik over.
2. ~~Hvordan tilbakemeldingene 4.1–4.3 på PRD-en skal løses.~~ **Løst i PR #14 (2026-11-12):** evalueringskjøring i KI-modus (NFR-11) for 4.1, nødplan for 4.2 (se punkt 3) og resultat i tre deler for 4.3. Se [endringer i PRD](endringer/endringer-prd.md).
3. ~~Om det skal skrives ned en kuttrekkefølge til bruk hvis tiden blir knapp.~~ **Løst i PR #14 (2026-11-12):** PRD §8.1 har en nødplan. Målet er fortsatt alle åtte funksjonene. Er ikke P1–P5 ferdige og testet 2. desember, kuttes (1) brevoppsettet i PDF, (2) CV-forbedringsforslag (P6) og (3) KI-forklaringen i ATS-analysen.
4. Om `main` skal kreve én godkjenning før fletting (GitHub → Settings → Branches).
