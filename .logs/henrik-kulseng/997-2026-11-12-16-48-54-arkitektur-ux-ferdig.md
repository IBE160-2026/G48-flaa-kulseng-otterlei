# Arkitektur og UX gjort ferdig

## 2026-11-12 kl. 16:48 — Henrik Kulseng

### Oppgave
Henrik ville gjøre ferdig arkitekturen og UX-en, så planleggingen er klar for epics og stories.

### Plan
- Sjekket åpne issues: UX-en var allerede `final` (#22), arkitekturen sto som `draft` med [Forslag]-merker (#18), og UX-avvikene gjensto i arkitekturen (#21) og PRD-en (#20).
- Spurte Henrik: han godtok alle gjenstående [Forslag]-punkter, opplyste at Haakon er enig i punktene fra PR #13, og ville ha PRD-avvikene med i samme PR.
- Branch `docs/arkitektur-ux-ferdig`. Bygger videre på [UX-loggen](998-2026-11-12-15-09-51-ux.md) og [arkitekturloggen](999-2026-11-12-13-16-04-arkitektur.md).

### Resultat
- `7f47bcb` Arkitekturen: merkene fjernet, `status: final`, ny AD-22 (veiviseren i fire steg), tillegg i AD-5 (personvern i testmodus, avkrysning ved registrering) og AD-13 (eksport av redigert tekst), `/ny-soknad/` i §3, §6–§8 oppdatert, beslutningsloggen oppdatert.
- `65a2318` PRD-en: §6 veiviser i fire steg, FR-6/FR-7 redigerbart brev som ikke lagres, FR-12 avkrysning for personvern, FR-16 «Start ny søknad», §11 markert som løst, ny del i §12. Forklart i `docs/endringer/endringer-prd.md`.
- `aec1f33` EXPERIENCE.md: avvikslisten markert som løst. README: AD-1 – AD-22.
- KI-logginnlegg `docs/ki-logg/2026-11-12-arkitektur-ux-ferdig.md`.
- Issue #22 lukket (var allerede gjort i PR #15). #11, #18, #20 og #21 lukkes av pull requesten når den flettes.

### Åpne punkter
- Issue #24: gruppa må bekrefte Claudes egne tillegg i AD-22.
