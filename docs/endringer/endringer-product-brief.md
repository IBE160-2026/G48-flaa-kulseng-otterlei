# Endringer i product brief etter tilbakemelding

| | |
|---|---|
| **Gruppe** | G48 – Gutta krutt |
| **Dokument** | [`product-brief.md`](../../_bmad-output/planning-artifacts/product-brief.md) (versjon 1: commit `681c297`) |
| **Tilbakemelding** | [`tilbakemelding-product-brief.md`](../tilbakemeldinger/tilbakemelding-product-brief.md) (commit `f7d871b`) |
| **Dato** | 2026-10-10 |

Dette dokumentet forklarer hva som er endret i product brief etter faglærers tilbakemelding, og hvorfor. Den forrige versjonen kan ses i git-historikken (`git show 681c297:product-brief.md` — briefen lå i rotmappen i versjon 1).

## Kort oppsummert

Faglærer pekte på tre hovedendringer. Alle tre er innarbeidet:

1. **Mindre omfang i V1:** skrivestil-læring er flyttet til Vision, DOC-støtte er fjernet, eksport er begrenset til Markdown og PDF (pluss kopiering), og V1-punktene er rangert.
2. **Konkrete suksesskriterier:** ett samlet kriterium er erstattet med ti testbare kriterier, støttet av tre oppdiktede eksempelpar med fasit.
3. **Kjørbar for sensor:** briefen beskriver nå en testmodus med lagrede LLM-svar, slik at appen kan prøves uten gruppens API-nøkkel.

I tillegg er ATS-delen gjort om til en nøkkelordanalyse beregnet i kode, og det er lagt til føringer for teknologi, hemmeligheter og testdata.

## Endringer, del for del

### 1. Omfang (Scope)

| Før | Etter | Hvorfor |
|---|---|---|
| Valgfri opplasting av tidligere søknader for å lære skrivestil | Flyttet til Vision | Tilbakemeldingen: ekstra arbeid som ikke trengs for kjerneflyten. |
| Opplasting av PDF/DOC/TXT | Opplasting av PDF og TXT | DOC-lesing er mindre vanlig og vanskeligere å få pålitelig. |
| Eksport til PDF, DOC og Markdown | Eksport til Markdown og PDF, pluss kopiering til utklippstavle | Fjerner DOC-eksport, som er et eget delprosjekt. |
| Åtte V1-punkter uten rekkefølge | V1 rangert 1–8: kjerneflyt (1–5) først, deretter CV-forbedringer, ATS og eksport | Faglærer ba om at kjerneflyten blir ferdig og stabil før resten, og at punktene rangeres. |
| «tone/stilnivå (f.eks. formell/uformell)» | To faste toner: formell og uformell | Avgrenser KI-funksjonaliteten, som faglærer vurderte som høy kompleksitet. |
| — | «Utenfor omfang» utvidet med skrivestil og DOC/DOCX | Gjør avgrensningen eksplisitt. |
| Risikoavsnitt om bredde vs. dybde | Oppdatert: forklarer hva som er strammet inn, og navngir de to største gjenværende risikoene (PDF-innlesing og oppdiktet erfaring) med tiltak | Viser at risikoen er håndtert, ikke bare nevnt. |

Executive Summary, The Solution og Vision er oppdatert slik at de stemmer med det nye omfanget.

### 2. Suksesskriterier (Success Criteria)

**Før:** Ett samlet kriterium om en fungerende ende-til-ende-demo.

**Etter:** Ti nummererte, testbare kriterier:

| # | Kriterium | Dekker |
|---|---|---|
| 1 | Kjerneflyt ende-til-ende, både med ekte LLM og i testmodus | Hele flyten |
| 2 | Innlesing av CV, inkludert to-kolonne-PDF | Filhåndtering (høy risiko i tilbakemeldingen) |
| 3 | Gap-analysen finner fasitens manglende krav (f.eks. SQL og førerkort for par A) | Gap-analyse |
| 4 | Søknadsbrevet dikter ikke opp erfaring, sjekket mot sjekkliste | Kvalitetskravet faglærer trakk frem |
| 5 | Valg av utkast/forslag, språk og tone respekteres | Brukervalg |
| 6 | ATS-matchen er deterministisk og har enhetstester mot fasit | ATS |
| 7 | Eksport til Markdown og PDF med korrekte æ/ø/å | Eksport |
| 8 | Tilgangskontroll mellom brukere og kryptert lagring | Sikkerhet |
| 9 | Sletting av dokumenter og konto | Personvern |
| 10 | Appen kan kjøres etter README uten gruppens API-nøkkel | Kjørbarhet for sensor |

Faglærer ba om 6–10 kriterier som kan bli testtilfeller, og ga to eksempler som begge er tatt inn (kriterium 3 og 4).

### 3. Ny seksjon: Eksempeldata med fasit

Ny tabell med tre oppdiktede eksempelpar (CV + annonse) med forventet match og forventede mangler. Parene er valgt for å dekke ulike risikoer:

- **Par A:** enkel PDF, norsk annonse — grunnleggende kjerneflyt og «ikke dikte opp».
- **Par B:** TXT-fil, uformell tone — den andre filtypen og det andre tonevalget.
- **Par C:** to-kolonne-PDF, engelsk annonse — vanskelig layout og det andre språket.

**Hvorfor:** Faglærer vurderte «kontroll på KI-ens arbeid» og «testbarhet» som risiko, og foreslo eksempel-CV-er og -annonser med fasit. Eksempeldataene brukes både i tester, i manuell kontroll av KI-svar og i testmodusen.

### 4. ATS-delen beregnes i kode

**Før:** «ATS-optimaliseringstips (nøkkelord, formatering)» — ikke spesifisert hvordan.

**Etter:** Nøkkelord-match mellom annonse og CV beregnes i kode. KI brukes bare til å forklare resultatet og foreslå omformuleringer.

**Hvorfor:** Faglærers forslag nr. 2 til justering. Det gir en del av appen som kan testes automatisk med fasit, og som sensor kan kontrollere.

### 5. Ny seksjon: Teknologi, KI-avhengighet og kjørbarhet

Ny seksjon med føringer som arkitekturen skal følge opp:

- **LLM-leverandør** velges og begrunnes i arkitekturen (norsk språkkvalitet, kostnad, databehandling hos leverandør), med forbruksgrense.
- **Testmodus** med lagrede svar når ingen API-nøkkel er satt — sensor kan kjøre kjerneflyten gratis, og testene blir forutsigbare.
- **`.env.example`** for API- og krypteringsnøkler; `.env` sjekkes aldri inn.
- **PDF-bibliotek** velges tidlig og testes mot den vanskelige eksempel-CV-en.
- **Plassering i repoet** for testdata, planleggingsdokumenter og README.

**Hvorfor:** Dekker «Kjørbar for sensor», «Avhengigheter og kostnader» (begge risiko i tilbakemeldingen) og kriteriene 5, 6 og 7 i del 1 av mappen (arkitektur, README/kjørbarhet og ryddighet i repoet).

### 6. Sikkerhet og personvern

Lagt til én setning om at bare oppdiktede CV-er og søknader brukes i utvikling og testing — aldri ekte personopplysninger i repoet. Resten av seksjonen var allerede vurdert som god og er uendret.

### 7. Øvrig

- Versjonsmerknad øverst i briefen som viser til tilbakemeldingen og dette dokumentet.
- README har fått en seksjon som lenker til planleggingsdokumentene, slik faglærer foreslo, så sensor finner dem samlet.
- Delene som fikk «OK» i tilbakemeldingen (The Problem, What Makes This Different, Who This Serves) er beholdt nesten uendret.

## Hva som gjenstår (ikke gjort i denne runden)

Disse punktene fra tilbakemeldingen hører hjemme i senere steg og er bare forberedt i briefen:

- **Lage selve eksempelfilene** (tre CV-er, tre annonser og fullstendig fasit/sjekkliste). Briefen beskriver hva de skal inneholde.
- **Velge LLM-leverandør og bibliotek** for PDF-lesing/-eksport, kryptering og innlogging — gjøres i arkitekturdokumentet.
- **Lage `.env.example`** og beskrive oppsett og testmodus i README — gjøres når koden starter.
- **Skissere skjermbilder** for gap-analysen og valget mellom utkast og forslag — gjøres i UX-steget.
- ~~**Plassering av briefen:** Briefen er beholdt i rotmappen og lenket fra README, i stedet for å flyttes til `_bmad-output/`.~~ _Oppdatert 2026-10-10:_ Briefen er nå flyttet til `_bmad-output/planning-artifacts/`, der BMAD også legger PRD og arkitektur, og øvrige dokumenter er flyttet til `docs/`. Se [KI-loggen for 2026-10-10](../ki-logg/2026-10-10-oppdatering-product-brief.md).
