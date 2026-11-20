# Evaluering av påstander

## 2026-11-20 kl. 14:20 — Ole A. Flaa

### Oppgave
Finne hva Ole kan gjøre mens Haakon lager epics og stories, og deretter løse issue #28: bestemme hvordan evalueringen skiller mellom å nevne og å påstå et krav, også på tvers av språk. Ole ba Claude velge den beste løsningen.

### Plan
- Sjekket `origin/main`, PR-er og issues. Foreslo issue #16 (API-konto), #28 og utkast til prompts.
- Svarte på om API-kontoen må betales nå: det kan vente til ekte KI-kall trengs. La det inn i minnet som en påminnelse.
- Lagde branchen `docs/evaluering-pastander` fra `origin/main`, leste AD-3 – AD-6, AD-17, FR-8, NFR-11, SM-4 og addendumet, og skrev løsningen i to trinn inn i AD-6.

### Resultat
- `a56bf69`: AD-6 (to trinn, kontrollsetninger, rapporten viser kandidatene, valgt bort), AD-17 (test av kandidatsøket), §5, §6 og beslutningsloggen.
- `b730857`: KI-logg `docs/ki-logg/2026-11-20-evaluering-pastander.md` og tabellen.
- PR: https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/33 (Closes #28)

### Åpne punkter
- Haakon og Henrik må godta valget i PR #33. Det følges opp i PR-en.

## 2026-11-20 kl. 14:43 — Ole A. Flaa

### Oppgave
Gruppa valgte regelen i story 5.2 (PR #35) for issue #28. PR #33 skulle gjøres om til en logg over det avviste forslaget, og `vurdering.md` fjernes fra det som gjenstår i PR #34.

### Plan
- Satte `ARCHITECTURE-SPINE.md` tilbake til `origin/main` på `docs/evaluering-pastander`.
- Skrev gruppas valg og begrunnelse (fra Ole: ingen ekstra API-kall, enklere å kode, samme svar hver gang) i beslutningsloggen og KI-logginnlegget.
- Endret tittel og beskrivelse i PR #33, og fjernet «Closes #28».

### Resultat
- PR #33 inneholder nå bare KI-logginnlegget, beslutningsloggen og sesjonsloggen.
- Issue #28 står åpen til story 5.2 er ferdig.

### Åpne punkter
- Ingen.
