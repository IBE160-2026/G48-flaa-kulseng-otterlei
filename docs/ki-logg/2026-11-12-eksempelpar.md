# Eksempelpar A–D med fasit

| | |
|---|---|
| **Dato** | 2026-11-12, rettelser 2026-11-16 |
| **Hvem** | Haakon Remen Otterlei |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | `caaf91a`, `74301b4`, `7e37e64`, `639a1d2`, `444c287`, `c3dae11`, `4a84a93`, `e8d0fe6` og commiten med dette innlegget, på branchen `docs/eksempelpar`. [Kommentar på PR #25](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/25#issuecomment-6828694095) |

## Mål

- Gå gjennom Henriks PR #25 (arkitektur og UX gjort ferdig) og gi en kommentar.
- Lage eksempelparene A, B og C med fasit (PRD §10, issue #10, frist 18. november), og eksempelpar D med en innebygd instruksjon i annonsen (AD-6).
- Teste at `pdfplumber` klarer CV-en i to kolonner før P2 (AD-13).

## Viktigste prompts

1. «kan du gå gjennom branchen #25. og komme med en kommentar som eg kan gi til henrik» og «ja, eg er enig. legg ut kommentaren»
2. «hva er neste oppgave for meg? stories og epics?» og «ja la oss starte å Eksempelpar»
3. «hva tenkter du er best?» (skript eller Word for PDF-ene)
4. «ja, gå gjennom par A med meg» og «sysnest du den ser bra ut, og følger den krav»
5. «ja, rett begge (kva skjer når du rette dette)»
6. «men hvor og hva mener du eg skal nevne til notatet til ole» og «gjør det som er best» (par D)

## Hva KI gjorde

- **PR #25:** Gikk gjennom diffen og Oles kommentar, sjekket henvisningene og fant i tillegg at NFR-11 manglet i arkitekturen. Skrev en kommentar som Haakon fylte inn svaret sitt i, og la den ut.
- **Eksempelpar A–D:** Laget CV, annonse og `fasit.json` for hvert par etter briefen, PRD §10 og formatet i AD-17. Gikk gjennom A, B og C med Haakon i tre deler: CV, annonse og fasit. Hver del ble sjekket mot kravene i briefen, PRD-en og arkitekturen.
- **`app/testdata/lag_cv_pdf.py`:** Et skript som lager CV-PDF-ene fra `cv_kilde.txt` med `fpdf2` og fonten DejaVu Sans, med fast dato, så samme kilde gir samme PDF på samme maskin. (Rettet 2026-11-16: på Henriks maskin ble filen litt annerledes, men teksten var lik. Se under.) Utvidet med to kolonner for par C.
- **PDF-test mot CV C:** Med standardinnstillinger blander `pdfplumber` de to kolonnene linje for linje. Når mellomrommet mellom kolonnene finnes først, og hver kolonne leses for seg, kommer all teksten ut i riktig rekkefølge. `pdfplumber` kan beholdes, men innlesingen må finne kolonnene selv.
- **Feil KI fant og rettet selv:** Etter å ha sett på PDF-en som bilde: «Sommer 2023» havnet ikke i tidskolonnen, og kulepunktene ble blokkjustert. I testkoden for kolonnene brukte KI feil koordinater for utsnittene i første forsøk.

## Våre vurderinger og korrigeringer

- **Skript i stedet for Word:** Haakon spurte hva som var best, og valgte skriptet etter Claudes anbefaling. Grunnen var at CV-teksten da bare finnes ett sted, og at PDF-ene kan lages på nytt.
- **Par A:** Haakon spurte om CV-en fulgte kravene. Da fant Claude to ting som Haakon ba om å få rettet: annonsen gjelder nå «studenter eller nyutdannede», fordi Emma er ferdig våren 2027, og værvarsel-appen er gjort til bachelorprosjektet hennes, slik UX-en beskriver det. Haakon godtok fasiten, ba om at `andel` ble lagt til, beholdt aliaset «databasespørringer», og ba om at punktet om «nevne» og «påstå» kommer med i pull requesten.
- **Par B:** CV, annonse og fasit godkjent uten endringer. Haakon beholdt `andel` med slingringsmonn i testen, og ba om feltet `tone` i alle fasitene.
- **Par C:** Haakon spurte om CV-en burde være på norsk eller engelsk, og valgte norsk CV etter Claudes anbefaling, fordi det er det vanlige tilfellet for norske studenter. Han ba om at det doble `sprak`-feltet fjernes fra alle fasitene.
- **Par D:** Haakon lot Claude velge («gjør det som er best»). Claude valgte samme CV som A, og at `finn_eksempelpar` bare ser på A–C.
- **Arkitekturen:** Claude foreslo å vente med å oppdatere arkitekturen til PR #25 var flettet, for å unngå konflikter, og Haakon sa ja. #25 ble flettet mens denne pull requesten ble laget, og da førte Claude beslutningene fra økten inn i arkitekturen. Ingen nye valg ble tatt.

## Resultat

- Eksempelpar A–D med fasit ligger i `app/testdata/eksempler/`, og skriptet ligger i `app/testdata/lag_cv_pdf.py`. Fonten ligger i `app/eksport/fonter/`.
- README har fått den nye mappen og en oversikt over eksempelparene.
- Arkitekturen er oppdatert:
  - AD-6: `finn_eksempelpar` ser bare på A–C
  - AD-13: resultatet av PDF-prøven
  - AD-17: fasitformatet
  - §8 punkt 3 er merket som løst
- **Gjenstår:**
  - `ordliste.json` med synonymene parene trenger
  - innlesingen av PDF med kolonner (P1)

## Etter gjennomgangen i PR #26 (2026-11-16)

**Prompts:** «hei kan du sjekke kommentarene til ole og henrik på #26» og «ja, eg er enig i A, gjør alt. Legg også til en kommentar om endringene slik henrik og ole kan sjå over igjen.»

**Funn fra gruppa, og hva som ble gjort:**

| Funn | Fra | Hva som ble gjort |
|---|---|---|
| Fasiten hadde bare ett språk og én tone, men `lag_lagrede_svar` lager åtte brevvarianter per par. Det engelske brevet for A ville strøket på «Skrevet på norsk bokmål». | Ole, Henrik enig | `floskler` har nå én liste per språk. `sprak_og_tone` har kjennetegn for `alle`, `nb`, `en`, `formell`, `uformell`, `fullt_utkast` og `kun_forslag`. Svarform var Claudes tillegg til Oles forslag. AD-17 er oppdatert. |
| Bachelorgraden i par C er ikke fullført, men står som krav som matcher. | Ole, Henrik enig | Kravet har fått en `merknad` om at graden fullføres før programmet starter. |
| AD-5 sier at navn og e-post aldri sendes til KI, men CV-ene inneholder begge. | Ole | Haakon støtter Henriks forslag (løsning A): presisere AD-5 til kontoens e-post og navn, og det samme i NFR-4. Ole tar det i en egen PR. |
| D er en kopi av A og kan bli utdatert. | Ole, Henrik | En test i Epic 0 skal sjekke at CV-ene er like. Lagt inn i issue #29. D har fått samme formatering som A–C. |
| PDF-ene ble ikke like byte for byte på Henriks maskin. | Henrik | Påstanden i skriptet og her er rettet. `fonttools` lagt til i issue #29, så versjonene låses i Epic 0. |

**Hva KI burde sett selv:** Claude laget fasitformatet uten å sjekke det mot de åtte variantene i FR-10 og AD-6, og påsto at PDF-ene alltid blir like uten å ha prøvd på en annen maskin. Begge feilene ble fanget i gjennomgangen. Det viser at gjennomgang av KI-arbeid fungerer.
