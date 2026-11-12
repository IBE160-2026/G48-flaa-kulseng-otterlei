# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G48 – G48-flaa-kulseng-otterlei |
| **PRD vurdert** | `_bmad-output/planning-artifacts/prd/prd.md` (status `final`, sist endret 2026-11-03, commit 07a17f3) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en sterk PRD: tydelig tese, 23 nummererte FR-er med testbare konsekvenser, eksempeldata med fasit, en fungerende testmodus og suksesskriterier med motkriterier. Hovedrisikoen er ikke dokumentet, men planen bak det. KI-kvaliteten (gap-analyse, «ingen oppdiktede påstander») kan i praksis bare testes mot lagrede svar, og alle åtte funksjoner skal ferdig på ca. fem uker uten kuttplan.

## 2. Dette fungerer godt

- **KI-kontroll er tenkt inn fra start.** §1: «Nøkkelordanalysen beregnes i kode, så den gir samme svar hver gang og kan testes mot fasit.» Dermed finnes en deterministisk del som kan enhetstestes (FR-20), og KI brukes bare der det trengs. SM-C1 («SM-4 går foran SM-6») viser at dere har tenkt på hva som ikke skal optimaliseres.
- **FR-ene er skrevet som testtilfeller.** FR-3 («under 100 tegn gir en melding, ikke et KI-kall»; «over 15 000 tegn avvises») og FR-5 (par A: «SQL» og «førerkort klasse B» mangler, «Python» og «Git» matcher) kan overføres rett til stories og tester. Grensen på 15 000 tegn er også et kostnadstiltak.
- **Testmodus, kostnad og feil er egne krav.** FR-9–FR-11, NFR-5 (60 sekunder, «CV og innstillinger beholdes») og NFR-9 gir sensor en kjørbar vei uten nøkkel. §8.2 begrunner hvert utelatte punkt.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | god | Beslutninger og begrunnelser er synlige (§8.2, §12), men valget «alle åtte funksjoner skal med» mangler en avveining. |
| Substans | sterk | Ingen pynte-personas eller boilerplate. NFR-ene har konkrete grenser (5 MB, 8 tegn, 60 s, 360 px). |
| Strategisk sammenheng | sterk | Tesen er «brukeren styrer KI, og alt bygger på CV-en». Funksjonene og SM-ene følger den. |
| Testbarhet | god | Deterministiske deler er sterke. KI-delene kontrolleres manuelt, med enkelte vage formuleringer. |
| Scope og avgrensning | god | Ikke-mål og utenfor v1 er eksplisitte. Omfanget er stort for tre personer og fem uker. |
| Brukbarhet for neste fase | god | IDer er sammenhengende. Datamodellen rundt «Analyse/Resultat» er uklar. |
| Formtilpasning | sterk | Fire reiser, ordliste og SM-er passer en webapp med innlogging. |

## 4. Viktigste forbedringer

### 4.1 KI-kvaliteten testes bare mot lagrede svar
- **Alvorlighet:** høy
- **Hvor:** §5 NFR-2 («De kjører i testmodus, uten nettverk og uten API-nøkkel»), §4.3 FR-8 («Sjekken gjøres manuelt»), §9 SM-3/SM-4
- **Problem og hvorfor det betyr noe:** De automatiske testene kjører mot lagrede svar, så de tester skriptet og visningen, ikke promptene. Ingenting sier hvordan dere vet at den ekte KI-en gir riktig gap-analyse eller unngår oppdiktede påstander, og heller ikke hva som skjer når svaret er usikkert. Det er kjernen i «kontroll på KI-ens arbeid» fra briefen.
- **Forslag:** Legg til en FR eller NFR om en evalueringskjøring i KI-modus. Eksempel: «Før hver release kjøres skriptet fra FR-10 i KI-modus. Resultatet sammenlignes med fasit og dokumenteres i `docs/`. Gap-analysen skal ha 0 manglende krav feilmerket som matcher for hvert par, og 0 treff på fasitens liste over forbudte påstander.» Legg også til et krav om at KI-svar fra gap-analysen kommer i et fast format (det står i addendumet, men ikke som krav), og at et svar som ikke kan leses, behandles etter NFR-5.

### 4.2 Alle åtte funksjoner på fem uker, uten kuttplan
- **Alvorlighet:** høy
- **Hvor:** §8.1 «gruppa planlegger ikke å kutte noen av dem, fordi gruppa mener det er god nok tid»
- **Problem og hvorfor det betyr noe:** Fristen er 15. desember. Arkitektur, UX, epics og all kode gjenstår. Scopet inneholder innlogging, kryptert lagring, PDF-innlesing av kolonner, PDF-eksport med brevoppsett, 42 lagrede svar og tre fasitsett. Briefens tilbakemelding pekte på tid og omfang som risiko. Prioriteringen P1–P8 finnes, men ikke hva som kuttes først.
- **Forslag:** Legg til en kuttrekkefølge og et sjekkpunkt, for eksempel: «Hvis kjerneflyten (P1–P5) ikke er ferdig og testet innen [dato], kuttes først PDF-brevoppsettet i FR-23, deretter FR-18, deretter lagrede svar for tone (FR-10).» Det gjør tidsrisikoen til en beslutning i stedet for en forhåpning.

### 4.3 Uklar modell for Analyse, Resultat og lagring
- **Alvorlighet:** medium
- **Hvor:** §3 «Resultat — det en analyse gir: gap-analyse, søknadsbrev … Bare det siste resultatet lagres» mot §4.2 («Søknadsbrev og CV-forbedringsforslag lages når brukeren ber om dem»)
- **Problem og hvorfor det betyr noe:** Ordlisten sier at en analyse gir alt, men §4.2 sier at «Analyser» bare gir gap-analyse og nøkkelordanalyse. Hva skjer med et lagret brev når brukeren ber om et nytt med annen tone? Overskrives bare brevet, eller hele resultatet? Dette avgjør datamodellen og testene av FR-16. Videre brukes «ønskede nøkkelord» (FR-4) i KI-forklaringen, men de lagrede svarene (FR-10) finnes bare per språk. Egne nøkkelord på eksempelpar gir da en forklaring som ikke passer.
- **Forslag:** Definer «Resultat» som tre deler som lagres og overskrives hver for seg (analyse, brev/forslag, CV-forbedring), og skriv det som en konsekvens under FR-5/FR-6. Si for FR-4 at ønskede nøkkelord i testmodus enten ikke gir KI-forklaring eller er deaktivert på eksempelpar.

### 4.4 Vage ledd i «ingen oppdiktede påstander» og fasiten
- **Alvorlighet:** medium
- **Hvor:** §4.3 FR-6 «Hvert avsnitt … viser til noe konkret fra CV-teksten», FR-7, §10
- **Problem og hvorfor det betyr noe:** «Viser til noe konkret» er en skjønnsvurdering, og to gruppemedlemmer kan sjekke samme brev ulikt. Fasiten er navngitt som grunnlag for FR-5, 6, 8, 18 og 21, men beskrives bare ved henvisning til briefen. Den skal lages «før kodingen av P2 starter», uten ansvarlig eller dato.
- **Forslag:** Gjør kriteriet sjekkbart: «Hvert avsnitt inneholder minst ett krav fra annonsen eller en kvalifikasjon fra fasitens liste over fakta i CV-en. Brevet nevner ingen ferdighet, arbeidsgiver eller utdanning utenfor denne listen.» La fasiten ha tre lister: fakta i CV-en, krav som mangler (må ikke påstås), og floskler. Sett dato og ansvarlig.

### 4.5 Annonsetekst og brukerens tillit til KI-svar
- **Alvorlighet:** lav
- **Hvor:** §5 NFR-3 og NFR-4
- **Problem og hvorfor det betyr noe:** Stillingsannonsen er innlimt tekst som sendes til språkmodellen. NFR-3 dekker XSS, men ikke at annonsen kan inneholde instruksjoner til modellen. Det står heller ikke at brukeren skal få beskjed om å lese gjennom brevet før det brukes.
- **Forslag:** Legg til: «Systemprompten sier at annonsen er data, ikke instruksjoner. Resultatsiden viser teksten ‹KI kan gjøre feil – les gjennom før du sender›.» Dere kan teste dette med en egen eksempelannonse.

## 5. Mekaniske funn

- FR-1–FR-23, UJ-1–UJ-4, SM-1–SM-10, SM-C1–C2 og NFR-1–NFR-10 er sammenhengende, og krysshenvisningene løser seg. Tallet 42 lagrede svar stemmer (24 + 18).
- Glossar: «Resultat» og «Analyse» er i konflikt med §4.2 (se 4.3). «Dokumenter» omfatter stillingsannonsen, mens FR-1 bruker «CV» og «CV-tekst» om ulike ting. Det fungerer, men hold det strengt i stories.
- Ikke alle FR-er sier hvilken UJ de realiserer (f.eks. FR-2, FR-3, FR-9). Det kan sies på funksjonsnivå, men legg det inn der dere lager sporing fra stories.
- Antakelsene står samlet i §12 med henvisning til § og FR, ikke som `[ASSUMPTION]` i teksten. Det fungerer. Alle er bekreftet.

## 6. Før dere går videre

**Må avklares før UX, arkitektur og epics:**
- Modellen for Resultat og lagring (4.3). Den styrer databasen og FR-16.
- KI-evalueringskjøring og format på KI-svar (4.1). Det påvirker arkitekturens KI-grensesnitt.
- Kuttrekkefølge og sjekkpunkt (4.2).
- Åpne spørsmål 1–3 (leverandør, nøkkelordmetode, PDF-bibliotek). De er riktig plassert i arkitekturen, men PDF-testen mot eksempel C bør gjøres først.

**Kan vente:** passordgrenser for utløp av sesjon, hvordan testmodus slås på i konfigurasjonen (FR-9), detaljer om brevoppsettet.

**Oppfølging av briefen: ja.** Skrivestil er flyttet til Vision, DOC er droppet, eksport er begrenset, suksesskriteriene er delt i ti, eksempeldata med fasit er planlagt, testmodus er krav, og nøkkelord beregnes i kode. «Kjørbar for sensor» er løst (NFR-1, SM-10). Tidsrisikoen er fortsatt åpen (4.2).

## 7. Refleksjonsspørsmål

1. Alle 16 antakelser i §12 ble «bekreftet uten endringer». Hvilke av dem sjekket dere mot egne erfaringer, for eksempel 5 MB, 15 000 tegn eller 42 lagrede svar, og hva ville dere ha endret hvis dere hadde jobbet med dem lenger?
2. Hvordan vil dere oppdage at en endret prompt gjør KI-svarene dårligere, når testene bare leser lagrede svar? Hva gjør dere hvis KI-en dikter opp en ferdighet i par B?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
