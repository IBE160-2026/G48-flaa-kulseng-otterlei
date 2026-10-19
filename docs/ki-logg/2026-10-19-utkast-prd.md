# Utkast til PRD med bmad-prd

| | |
|---|---|
| **Dato** | 2026-10-19 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5), BMAD-skillen `bmad-prd` |
| **Commits / PR** | `3112d2a`, pull request #4 (`docs/prd`, utkast) |

## Mål

Finne ut hva som er neste steg i prosessen, og lage første utkast til PRD basert på product brief v2.

## Viktigste prompts

1. «what is the next step in the process?»
2. «kva er bmad-prd og kvifor trenger vi dette?»
3. «ja, lag branchen og start bmad-prd»
4. «gruppa har ikkje diskutert videre etter v2 av brief. Vi vil at appen skal ver en nettside. Vi veit ikkje enda om det vil bli for mykje eller for vanskelig. Du bør gå gjennom "sensorveiliedinga" for å sjå om vi er på rett spor og kva dei neste sega er i prosessen. fristen er om 4-5 veker.»
5. «før eg svarer kva er 1-5 og 6-8»
6. «1. vi vil gjeren ha alle stegene 1-8, 2. innlogging kan ver med passord og email (vi kan legge til glemt passord dersom det ikkje tar for lang tid og vi har tid)kva teker du?, 3. resultat av analysen dei nettopp har kjørt, 4. kva tenker du? er det lurt med etter x antall dager?, 5. usikker, 6. hva mener du?»
7. «vi er enig med det du har kommet med.»
8. «ja, push og lag utkast-PR»

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
- Merket 16 punkter med `[ASSUMPTION]`, der KI har gjettet uten at vi har bestemt det.
- Pushet branchen og lagde en utkast-PR, så hele gruppa kan kommentere på GitHub.

## Våre vurderinger og korrigeringer

**Det vi bestemte selv:**
- Appen skal være en nettside.
- Målet er alle åtte v1-funksjonene fra briefen, ikke bare kjerneflyten (1–5).
- Innlogging med e-post og passord.
- Brukeren ser bare resultatet av analysen hen nettopp kjørte. Det blir ingen historikk.

**Forslag fra KI som vi godtok uten endringer:**
- Dropp «glemt passord» i v1, fordi det krever en e-posttjeneste og sensor ikke kan teste det uten eget oppsett. Vi hadde selv foreslått å ta det med hvis vi fikk tid.
- Ingen automatisk sletting etter et antall dager. Data lagres til brukeren sletter dem, og en ny analyse overskriver den forrige.
- Testmodus med knapper for eksempelpar A, B og C, og en tydelig melding hvis brukeren laster opp sin egen CV i testmodus. Her var vi selv usikre.
- Sjekkpunkt ved slutten av uke 3: er kjerneflyten ikke ferdig, kuttes omfanget bakfra (8, 7, 6).
- PRD-en skrives på norsk (BMAD-oppsettet sa engelsk) og ligger i en fast mappe i stedet for en ny mappe med dato for hver økt.
- Rask modus, der KI skriver utkastet og vi retter etterpå, i stedet for å gå gjennom seksjonene én og én.

**Før vi svarte,** ba vi KI forklare hva punktene 1–5 og 6–8 var, siden spørsmålet viste til nummereringen i briefen.

**Ikke vurdert ennå:** Ingen i gruppa har lest selve PRD-utkastet. De 16 antagelsene og 5 åpne spørsmålene skal gjennomgås av alle tre i PR #4.

## Resultat

- Utkast til PRD i `_bmad-output/planning-artifacts/prd/prd.md`, med addendum og beslutningslogg i samme mappe.
- Utkast-PR #4 er åpnet for gjennomgang.

**Gjenstår:**
- Gruppa leser og kommenterer utkastet i PR #4.
- KI retter utkastet etter kommentarene, sjekker det mot briefen, kjører en gjennomgang og oppdaterer README.
- Lage eksempel-CV-ene og fasiten.
- Gå videre til UX-skisser og arkitektur.
