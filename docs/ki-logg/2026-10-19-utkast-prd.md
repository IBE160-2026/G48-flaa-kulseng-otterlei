# PRD med bmad-prd

| | |
|---|---|
| **Dato** | 2026-10-19 – 2026-10-22 |
| **Hvem** | Haakon Remen Otterlei (gjennomgangen av utkastet ble gjort av hele gruppa) |
| **Verktøy** | Claude Code (Claude Opus 5.5), BMAD-skillen `bmad-prd` |
| **Commits / PR** | `3112d2a`, `cca35c8`, `e1999c5`, `b024148`, `de693e9`, `c8b6551`, `01c78cc` og commiten med dette innlegget, pull request #4 (`docs/prd`) |

## Mål

Finne ut hva som er neste steg i prosessen, og lage PRD-en basert på product brief v2.

## Viktigste prompts

**Økt 1 (19. oktober): utkast**

1. «what is the next step in the process?»
2. «kva er bmad-prd og kvifor trenger vi dette?»
3. «ja, lag branchen og start bmad-prd»
4. «gruppa har ikkje diskutert videre etter v2 av brief. Vi vil at appen skal ver en nettside. Vi veit ikkje enda om det vil bli for mykje eller for vanskelig. Du bør gå gjennom "sensorveiliedinga" for å sjå om vi er på rett spor og kva dei neste sega er i prosessen. fristen er om 4-5 veker.»
5. «før eg svarer kva er 1-5 og 6-8»
6. «1. vi vil gjeren ha alle stegene 1-8, 2. innlogging kan ver med passord og email (vi kan legge til glemt passord dersom det ikkje tar for lang tid og vi har tid)kva teker du?, 3. resultat av analysen dei nettopp har kjørt, 4. kva tenker du? er det lurt med etter x antall dager?, 5. usikker, 6. hva mener du?»
7. «vi er enig med det du har kommet med.»
8. «ja, push og lag utkast-PR»

**Gjennomgang i PR #4 (19. oktober)**

9. Samlet kommentar i PR #4: «Vi har gått gjennom alle antagelsene fra KI og er enig i alle.»
10. «rett opp A,B,C først. A. ja, B: Vi mener at det er tilpasset for norske, C: ja.»

**Økt 2 (22. oktober): rettinger**

11. «endre dette inni prd.md: Vi må få med alle punkta.» (om sjekkpunktet for å kutte funksjoner)
12. «Begrunnlese: Vi føler vi har god nok tid til å fullføre»

## Hva KI gjorde

- Sjekket status i repoet og pekte på PRD som neste steg i BMAD-flyten (brief → PRD → arkitektur → epics og stories).
- Forklarte hva en PRD er, hvordan den skiller seg fra briefen, og hvorfor sensor trenger nummererte krav for å spore koden tilbake til planen.
- Leste sensorveiledningen for del 1 og sammenlignet den med repoet. KI fant tre svakheter:
  - Det finnes ingen kode ennå, og fristen er om 4–5 uker. Sensorveiledningen nevner «hele koden i noen få commits rett før fristen» som et varseltegn.
  - Alle commits i repoet er Haakons.
  - Det finnes ingen UX-skisser, som kriterium 4 ser etter.
- Foreslo en ukeplan for resten av semesteret og et sjekkpunkt for å kutte omfang.
- Stilte seks avklaringsspørsmål og ga egne anbefalinger der vi spurte hva KI mente.
- Skrev første utkast til PRD i rask modus: 4 brukerreiser, ordliste, 23 funksjonelle krav og 10 ikke-funksjonelle krav, alle nummerert. Skrev også et addendum med notater til arkitektur og UX, og førte en beslutningslogg (`.memlog.md`).
- Merket 16 punkter med `[ASSUMPTION]`, der KI hadde gjettet uten at vi hadde bestemt det.
- Pushet branchen og lagde en utkast-PR, så hele gruppa kunne kommentere på GitHub.
- Etter gjennomgangen: erstattet `[ASSUMPTION]`-merkene med vanlig tekst og samlet dem i §12 som «Antagelser bekreftet av gruppa».
- Sammenlignet PRD-en med briefen og faglærers tilbakemelding, og vurderte den etter BMADs kvalitetskriterier for PRD-er. KI la fram tre funn vi måtte ta stilling til (A–C), og fire småfeil den rettet selv:
  - NFR-1 manglet at README skal forklare kjøring med egen API-nøkkel.
  - «Dokumenter» og «KI-tjenesten» manglet i ordlisten.
  - FR-6 sa ikke hvordan tonen sjekkes.
  - §4.2 viste feil til P6–P8.
- Vasket språket, satte PRD-en til `final` og la til lenker i README.

## Våre vurderinger og korrigeringer

**Det vi bestemte selv:**
- Appen skal være en nettside.
- Målet er alle åtte v1-funksjonene fra briefen, ikke bare kjerneflyten (1–5).
- Innlogging med e-post og passord.
- Brukeren ser bare resultatet av analysen hen nettopp kjørte. Det blir ingen historikk.

**Forslag fra KI som vi godtok:**
- Dropp «glemt passord» i v1, fordi det krever en e-posttjeneste og sensor ikke kan teste det uten eget oppsett. Vi hadde selv foreslått å ta det med hvis vi fikk tid.
- Ingen automatisk sletting etter et antall dager. Data lagres til brukeren sletter dem, og en ny analyse overskriver den forrige.
- Testmodus med knapper for eksempelpar A, B og C, og en tydelig melding hvis brukeren laster opp sin egen CV i testmodus. Her var vi selv usikre.
- PRD-en skrives på norsk (BMAD-oppsettet sa engelsk) og ligger i en fast mappe i stedet for en ny mappe med dato for hver økt.
- Rask modus, der KI skriver utkastet og vi retter etterpå, i stedet for å gå gjennom seksjonene én og én.

**Før vi svarte,** ba vi KI forklare hva punktene 1–5 og 6–8 var, siden spørsmålet viste til nummereringen i briefen.

**Gjennomgang av utkastet:** Alle tre i gruppa leste PRD-utkastet. Haakon ga tilbakemeldingen på vegne av gruppa i PR #4. Vi godtok alle de 16 antagelsene uten endringer.

**Funnene A–C fra KI-ens kontroll:**
- **A. Floskler:** KI påpekte at briefen beskriver floskler som et problem, men at PRD-en ikke stilte krav om det. Vi sa ja til KI-ens forslag om at hvert avsnitt i brevet skal vise til noe konkret, og at fasiten skal ha 3–5 floskler brevet ikke skal bruke.
- **B. «Tilpasset det norske arbeidsmarkedet»:** KI spurte om dette betydde særnorske krav, f.eks. et eget brevoppsett. Vi presiserte at det betyr at appen er laget for norske studenter. Det kom ingen nye krav.
- **C. Byggerekkefølge:** Vi sa ja til at prioriteringen bare sier hva som er viktigst, ikke hva som bygges først, så en enkel innlogging kan komme tidlig i stories.

**Det vi avviste:**
- **Sjekkpunktet for å kutte funksjoner.** KI hadde foreslått å kutte P8, P7 og P6 hvis kjerneflyten ikke var ferdig etter uke 3. Vi godtok det først, men endret mening og fjernet det: «Vi må få med alle punkta.» Begrunnelse: «Vi føler vi har god nok tid til å fullføre.»

**Å starte på nytt:** Haakon vurderte å slette branchen og begynne PRD-en på nytt. KI frarådet det, fordi committene da ikke kommer inn i `main` og ikke vises i historikken sensor ser på. Vi valgte å rette PRD-en i stedet.

**Småfeilene** KI rettet selv, hadde vi ingen innvendinger mot.

## Resultat

- Ferdig PRD i `_bmad-output/planning-artifacts/prd/prd.md`, med addendum og beslutningslogg i samme mappe.
- README lenker til PRD-en, addendumet og beslutningsloggen.
- PR #4 er klar til å merges når sjekklisten er gått gjennom.

**Gjenstår:**
- Arkitektur (`bmad-architecture`), som også skal svare på de åpne spørsmålene i PRD-ens §11.
- UX-skisser (`bmad-ux`).
- Eksempel-CV-er og annonser med fasit.
