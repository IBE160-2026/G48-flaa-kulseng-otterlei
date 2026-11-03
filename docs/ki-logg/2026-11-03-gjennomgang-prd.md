# Ny gjennomgang av PRD før arkitekturen

| | |
|---|---|
| **Dato** | 2026-11-03 |
| **Hvem** | Haakon Remen Otterlei (gjennomgangen ble gjort av hele gruppa) |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `5b1397a`, `eda72f8`, commiten med dette innlegget og rettingen etter godkjenningen, pull request #5 (`docs/prd-gjennomgang`) |

## Mål

Gå gjennom PRD-en en gang til før vi starter på arkitekturen, og rette det som er utdatert eller uklart.

## Viktigste prompts

1. «før vi fortsetter vil vi i gruppen gå gjennom prd»
2. «1. VI har fått vete at firsten er 15 desember. 2. hva mener du er best her? 3. brev oppsett med dato og avsender. 4. ja omformuler denne slik du mener er best. 5. Er prd-en ferdig for nå?»

## Hva KI gjorde

- Leste PRD-en og addendumet og pekte på fem punkter vi kunne ta med i gjennomgangen:
  1. Fristen (ca. 16.–23. november) så stram ut, med arkitektur, UX, stories og all koden igjen.
  2. Addendumet regnet med 24 lagrede brev, men gap-analysen, CV-forbedringsforslagene og KI-forklaringen skal også skrives på valgt språk og trenger lagrede svar.
  3. Åpent spørsmål 4 (brevoppsett i PDF-eksporten) handler om hva vi ønsker, og kunne avgjøres av oss med en gang.
  4. FR-15 sa «ingen av disse» uten å si hva «disse» var.
  5. `CLAUDE.md` sa fortsatt at PRD-en gjensto.
- Anbefalte (punkt 2) at søknadsbrev og brevforslag lagres for alle 8 kombinasjoner av språk, tone og svarform, mens gap-analyse, CV-forbedringsforslag og KI-forklaring bare lagres per språk, fordi tone og svarform bare gjelder brevet. Det gir 42 lagrede svar, laget med samme skript.
- Foreslo detaljene i brevoppsettet: avsenderen skrives inn av brukeren før PDF-eksporten og lagres ikke, datoen er eksportdatoen, og brevforslag får ikke brevoppsett fordi de er en punktliste.
- Oppdaterte PRD-en (§8.1, FR-10, FR-15, FR-23, SM-7, §11, §12), addendumet, beslutningsloggen og statusen i `CLAUDE.md`.

## Våre vurderinger og korrigeringer

- **Frist:** Vi har fått beskjed om at fristen er 15. desember, ikke i november. Det er derfor ikke behov for å vurdere kutt.
- **Lagrede svar:** Vi ba KI om en anbefaling. Forslaget er ført inn i PRD-en og merket som «må bekreftes» i §12.
- **Brevoppsett:** Vi bestemte at PDF-eksporten skal ha brevoppsett med dato og avsender. Hvordan avsenderen legges inn, er KI-ens forslag og må bekreftes.
- **FR-15:** Vi ba KI omformulere kravet slik den mente var best.
- **Godkjenning:** Alle tre gikk hver for seg gjennom endringene i PR #5 og godkjente KI-ens forslag uten endringer. Henrik og Ole kommenterte i PR-en («sett over, ser bra ut» og «Ser bra ut»).

## Resultat

- PRD-en, addendumet og beslutningsloggen er oppdatert. Åpent spørsmål 4 er avklart og fjernet.
- `CLAUDE.md` har riktig status og frist.

**Gjenstår:**
- Arkitektur (`bmad-architecture`), som skal svare på åpne spørsmål 1–3. En annen i gruppa tar den.
- UX-skisser (`bmad-ux`).
- Eksempel-CV-er og annonser med fasit.
