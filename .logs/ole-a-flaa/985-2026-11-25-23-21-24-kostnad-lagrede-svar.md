# Kostnaden for lag_lagrede_svar

## 2026-11-25 kl. 23:21 — Ole A. Flaa

### Oppgave
Ole ba om å ta issue #39: avgjøre hvordan story 4.5 håndterer kostnaden for `lag_lagrede_svar` før Epic 4.

### Plan
- Lese issue #39, målingene fra prøvekjøringene og story 4.5.
- Regne anslaget per operasjon og la Ole velge mellom Henriks tre forslag.
- Ny branch `docs/kostnad-lagrede-svar` fra `origin/main` og skrive valgene inn i `epics.md`.

### Resultat
- Nytt anslag: rundt 44 kall og omtrent 1,0 USD per full kjøring.
- Oles valg: kostnaden i USD i rapporten, `--operasjon <navn>` for delkjøring, ikke batch-API nå.
- Story 4.5 har to nye kriterier, og «Fra de åpne issuene» har et punkt om #39.
- KI-logg: `docs/ki-logg/2026-11-25-kostnad-lagrede-svar.md` og ny rad i tabellen.
- Commit `a5dbbe0`.

### Åpne punkter
- Issue #39 står åpen til den første evalueringsrapporten viser den faktiske kostnaden.
- Kostnaden for `nokkelord_forklaring` er ikke målt. Anslaget antar at den koster det samme som gap-analysen (står i issue #39).
