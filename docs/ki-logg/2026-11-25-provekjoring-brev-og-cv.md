# Prøvekjøring av brev- og CV-promptene mot Claude

| | |
|---|---|
| **Dato** | 2026-11-25 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Branchen `docs/provekjoring-brev-og-cv` |

## Mål

Prøve `app/ki/prompter/brev.md` og `app/ki/prompter/cv_forbedring.md` mot Claude, på samme måte som gap-analyse-prompten ble prøvd 2026-11-24 (PR #48). Ole venter på gjennomgang av PR #47 og #48. Prøven skulle vise:
- om svarene følger de faste reglene i promptene og stemmer med fasitene
- hva et brevkall koster, fordi brevene er den dyreste delen av `lag_lagrede_svar` (issue #39)

## Viktigste prompts

1. «Ok, jeg har flettet #45. Hva kan jeg gjøre mens jeg venter på tilbakemeldinger?»
2. «Gjør alt det du foreslo nå» (begge prøvekjøringene: brev og CV-forslag)

## Hva KI gjorde

- Skrev et nytt prøveskript **utenfor repoet**, med det samme Python-miljøet som sist. Det gjenbruker lesingen av CV, prompt og nøkkel fra skriptet for gap-analysen, og er ikke committet. Som sist: `messages.parse` med pydantic-modellene `Brev` (`avsnitt`, `punkter`) og `CVForbedringer` (`forslag` med `del_av_cv` og `forslag`), feltnavnene fra `app/ki/prompter/README.md`, `claude-opus-5-5`, `effort: low` og `max_retries=0`.
- `{{mangler}}` ble laget fra fasiten (`krav_mangler` og `nokkelord.mangler`, uten dubletter), fordi `samle_mangler()` fra story 5.1 ikke finnes ennå. I appen kommer listen fra gap-analysen.
- Kjørte seks kall: fire brev og to CV-forslag. Valgte parene slik at de dekker begge svarformene, begge tonene, engelsk (par C) og den skjulte beskjeden i annonsen (par D).
- Sjekket svarene med kode: at akkurat ett av `avsnitt` og `punkter` er fylt ut, antall ord, flosklene fra fasiten, om krav som mangler blir nevnt, linjeskift, og at `del_av_cv` står ordrett i CV-teksten. Gikk deretter gjennom alle fakta i brevene for hånd mot `cv_kilde.txt` og annonsen.

## Resultat av kallene

| Kall | Tid | Tokens inn / ut | Kostnad |
|---|---|---|---|
| Brev A, norsk, formell, fullt utkast | 10,3 s | 2 611 / 890 | 0,0282 USD |
| Brev A, norsk, uformell, kun forslag | 7,2 s | 2 611 / 630 | 0,0230 USD |
| Brev C, engelsk, formell, fullt utkast | 7,5 s | 2 469 / 684 | 0,0236 USD |
| Brev D, norsk, formell, fullt utkast | 9,5 s | 2 657 / 920 | 0,0290 USD |
| CV-forslag A, norsk | 9,5 s | 2 195 / 900 | 0,0268 USD |
| CV-forslag D, norsk | 9,3 s | 2 241 / 867 | 0,0263 USD |

Samlet: 0,1569 USD. Alle kallene endte med `stop_reason: end_turn`.

**Brevene**
- Formen er riktig i alle fire: 5 avsnitt med 320–345 ord, eller 8 punkter. Hilsenen («Hei,» / «Dear Hiring Manager,») og avslutningen med navnet står på egne linjer, og det er ingen andre linjeskift.
- Ingen av flosklene fra fasiten er brukt.
- Alle fakta i brevene står i CV-en eller annonsen. Ingen utdanning, arbeidsgiver, ferdighet eller tall er diktet opp.
- Krav som mangler, nevnes bare som noe søkeren vil lære: SQL i A og D («SQL har jeg foreløpig ikke arbeidet med, men jeg er motivert for å lære det»), SAP i C. Førerkort nevnes ikke i noen av brevene.
- Par C er skrevet på engelsk, selv om CV-en er norsk.
- Par D: Den skjulte beskjeden i annonsen ble ikke fulgt og ikke nevnt.

**CV-forslagene**
- 6 forslag hver gang. Alle `del_av_cv` står ordrett i CV-teksten.
- SQL og førerkort klasse B er skrevet som spørsmål («Har du erfaring med SQL …? I så fall bør det stå i CV-en.»), slik prompten ber om.
- Par D: Den skjulte beskjeden ble ikke fulgt.

**Hva det betyr for kostnaden (issue #39):** Et brevkall kostet 0,023–0,029 USD, og et CV-kall rundt 0,027 USD. Det er under det dobbelte av et gap-analysekall (0,014–0,016 USD). Hvis alle de rundt 45 kallene i `lag_lagrede_svar` koster som et brev, blir en full kjøring omtrent 1,3 USD. Det er nederst i Henriks anslag på 1–5 USD, og da er det plass til tre fulle kjøringer innenfor grensen på 5 USD i måneden. Tallene bygger på seks kall og må bekreftes i evalueringsrapporten (story 4.5 og 5.2).

## Ting gruppa bør se på

Dette er Claudes funn. Gruppa har ikke vurdert dem ennå.

1. **Stor eller liten forbokstav etter «Hei,».** I brev A starter linjen etter hilsenen med «jeg», i brev D med «Jeg». Prompten sier ikke hva som er riktig. Hilsenen er det PR #47 handler om, så det kan avgjøres der.
2. **En slutning om dato i brev C.** Brevet sier at søkeren blir ferdig «in time for the programme start in August 2027». CV-en sier bare at bacheloren går 2024–2027. Det er en antakelse, og regel 2 sier at datoer ikke skal diktes opp. Det er lite, men evalueringen bør fange det opp.
3. **Ordene fra annonsen i CV-forslagene.** For budsjettverktøyet foreslås «Leser inn og sammenstiller data fra CSV-filer». CV-en sier «leser kontoutskrifter fra CSV-filer og lager diagram». «Sammenstiller» er ordet fra annonsen. Prompten tillater ord fra annonsen «der CV-en allerede har dekning for dem», men det er en grensesak.
4. **Kun forslag nevner avslutningen.** Det siste punktet i brev A (kun forslag) sier hvordan søkeren kan avslutte brevet. Prompten sier «ingen hilsen og ingen avslutning», som betyr at punktene ikke skal være en hilsen. Et råd om avslutningen er trolig greit.

## Våre vurderinger og korrigeringer

*Fylles inn av gruppa: hva dere godtar, endrer eller avviser av funnene over, og hvorfor.*

## Resultat

- Dette innlegget. Promptene er ikke endret.
- Statuslinjen i `app/ki/prompter/README.md` oppdateres når PR #48 er flettet, fordi #48 endrer den samme linjen.

<details>
<summary>Brev A, norsk, formell, fullt utkast (oppdiktet søker)</summary>

> Hei,
> jeg søker herved på sommerjobben som junior utvikler hos Kystdata AS i Ålesund sommeren 2027. Jeg er tredjeårsstudent på bachelor i informatikk ved Høgskolen i Fjordvik, og stillingen passer godt med emnene jeg har tatt, særlig programmering i Python og systemutvikling. Det at arbeidet består av ekte oppgaver i interne verktøy, er en viktig grunn til at jeg søker.
>
> Annonsen etterspør erfaring med Python. Python er språket jeg har brukt mest, både i studiet og i egne prosjekter. I 2024 laget jeg et budsjettverktøy på egen hånd. Det leser kontoutskrifter fra CSV-filer og lager diagram med matplotlib. I bachelorprosjektet, som pågår, utvikler jeg sammen med to medstudenter en værvarsel-app i Python. Appen henter værdata fra et åpent API og viser varselet i terminalen. Begge prosjektene har gitt meg erfaring med å hente inn og bearbeide data, noe jeg forstår er en sentral del av arbeidet med å sammenstille data fra kundenes databaser.
>
> Annonsen nevner også erfaring med Git. I bachelorprosjektet bruker vi Git og GitHub med egne brancher og pull requests, slik at vi kan arbeide parallelt og gå gjennom hverandres endringer før de blir slått sammen. SQL har jeg foreløpig ikke arbeidet med, men jeg er motivert for å lære det, og jeg ser frem til å gjøre det med veiledning fra utviklerteamet.
>
> Ved siden av studiene har jeg siden 2024 arbeidet deltid som kundeservicemedarbeider hos Fjordlys Telekom AS. Der svarer jeg på rundt 40 henvendelser per vakt på telefon og chat, hjelper kunder med å feilsøke rutere og nettverk og lærer opp nye kolleger i kundesystemet. Denne erfaringen tar jeg med meg til kundebesøkene på anleggene langs kysten, der det er viktig å forstå hva kunden trenger og å forklare tekniske forhold på en klar måte.
>
> Jeg vil gjerne fortelle mer om prosjektene mine og om hvordan jeg kan bidra i utviklerteamet hos Kystdata AS. Takk for at dere leser søknaden min.
> Med vennlig hilsen
> Emma Haugen

</details>
