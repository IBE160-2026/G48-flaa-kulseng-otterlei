# Prøvekjøring av brev- og CV-promptene

## 2026-11-25 kl. 17:51 — Ole A. Flaa

### Oppgave
Rydde i de åpne PR-ene (#44, #45, #47, #48), og deretter prøvekjøre `brev.md` og `cv_forbedring.md` mot Claude mens Ole venter på gjennomgang. Prøvekjøringen skulle vise om svarene følger reglene, og hva et brevkall koster (issue #39).

### Plan
- Prøveflette alle fire PR-ene i en midlertidig worktree for å finne konflikter.
- Rette like løpenumre i sesjonsloggene på #47 og #48.
- Løse konflikten i `docs/ki-logg/README.md` på #47 og #48 etter at Ole hadde flettet #44.
- Ny branch `docs/provekjoring-brev-og-cv` fra `main`. Prøveskript utenfor repoet, som gjenbruker skriptet for gap-analysen. Seks kall: brev A (formell utkast og uformell forslag), C (engelsk) og D (skjult beskjed), og CV-forslag for A og D.

### Resultat
- Løpenumrene er rettet: #47 `a230fd7` (991 → 990) og #48 `d327b82` (990 → 989).
- Etter #44: `main` er flettet inn i #47 (`564be38`) og #48 (`c6c59c9`). Ole flettet #44 og #45 selv. #47 og #48 venter på gjennomgang, fordi ingen andre har sett på dem.
- Prøvekjøringen: Alle seks svarene fulgte de faste reglene. Ingen oppdiktede fakta, ingen påstand om SQL, SAP eller førerkort, den skjulte beskjeden i D ble ikke fulgt, og alle `del_av_cv` står ordrett i CV-en. Et brevkall kostet 0,023–0,029 USD. Til sammen kostet de seks kallene 0,1569 USD.
- KI-logg `docs/ki-logg/2026-11-25-provekjoring-brev-og-cv.md` og raden i tabellen: `a7d478b`. Promptene er ikke endret.
- Kostnadstallene er lagt som kommentar i issue #39.

### Åpne punkter
- Issue #49: Gruppa må vurdere de fire funnene (forbokstav etter «Hei,», slutningen om dato i brev C, «sammenstiller» i CV-forslaget, avslutningen i kun forslag). Statuslinjen i `app/ki/prompter/README.md` skal også oppdateres etter #48. Seksjonen «Våre vurderinger» i KI-loggen må fylles inn av gruppa.
- #48 får en liten konflikt i `docs/ki-logg/README.md` når #47 er flettet. Det samme gjelder denne PR-en.

## 2026-11-25 kl. 18:16 — Ole A. Flaa

### Oppgave
Lage et utkast til «Våre vurderinger og korrigeringer» i KI-loggen, og gi Ole valg der han må ta stilling.

### Plan
- Ett spørsmål per funn, med Claudes anbefaling først. Skrive vurderingene ut fra Oles svar.

### Resultat
- Ole valgte den anbefalte løsningen på alle fire funnene: stor forbokstav etter «Hei,» i `brev.md` (f1c303f), slutningen om dato tas i evalueringen (kommentar i issue #28), og «sammenstiller» og rådet om avslutningen godtas.
- Vurderingene står i KI-loggen (77d440b), og PR #50 er oppdatert. Begrunnelsene er de Claude ga i alternativene, og Ole valgte dem.
- Kommentar i issue #49 om hva som er avgjort.

### Åpne punkter
- Issue #49: Henrik eller Haakon må bekrefte vurderingene i PR #50. Statuslinjen i `app/ki/prompter/README.md` oppdateres etter #48.
