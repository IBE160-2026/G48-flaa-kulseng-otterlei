# Forhåndssjekk av versjoner og gjennomgang av epics

| | |
|---|---|
| **Dato** | 2026-11-20 |
| **Hvem** | Henrik |
| **Verktøy** | Claude Code (Claude Opus 5.5), BMAD-skillen `bmad-help` |
| **Commits / PR** | Sesjonsloggen på branchen `docs/forhandssjekk-versjoner`. Kommentarer på issue #17 og #29 og på PR #33, #34, #35 og #38 |

## Mål
Haakon lager epics og stories. I mellomtiden ville Henrik finne noe nyttig å gjøre som ikke kolliderer med det arbeidet. Han valgte å sjekke på forhånd at versjonene arkitekturen har valgt, virker sammen (issue #17 og #29). Etterpå gikk han gjennom storyene sine i Haakons PR #35.

## Viktigste prompts
- «help» (`bmad-help`: hvor står vi, og hva er neste steg?)
- «haakon holder på med det nå, hva kan jeg gjøre nå imens?»
- «ja, ta punkt 1» (forhåndssjekken av #17 og #29)
- «gå gjennom storyene mine» (0.3, Epic 5 og Epic 7 i PR #35)
- «skriv et utkast til kommentaren», og deretter «legg den inn»
- «ja, skriv utkast, jeg er enig om flosklene» (kommentar på Oles PR #34 med prompter)
- «ja, jeg står bak begrunnelsen, skriv utkast og godkjenn #35» (PR #33 og #35)
- «ja, skriv en kort kommentar på #38» (kostnadsanslag for API-kontoen)

## Hva KI gjorde
- Lagde et midlertidig Python-miljø utenfor repoet med alle versjonene fra arkitekturen §4, og et lite Django 6.1-prosjekt med pytest-django og pytest-socket. Seks tester besto (#17).
- Kjørte `lag_cv_pdf.py` på en kopi av `app/`. Fant at PDF-ene ikke blir like byte for byte selv med fonttools 4.68.0. Fant årsaken ved å prøve 14 versjoner av fonttools og sammenligne PDF-objektene: bare zlib-komprimeringen er ulik (#29).
- Skrev funnene og forslagene som kommentarer i issuene.
- Sammenlignet storyene til Henrik med `DESIGN.md`, `EXPERIENCE.md` og arkitekturen. Prøvde kriteriene i 7.3 med fpdf2 og fant at fpdf2 logger tegn fra brevteksten som fonten mangler, noe som strider mot AD-10.
- Leste `brev.md` i Oles PR #34 opp mot storyene for steg 4 og eksporten. Fant at prompten sier at appen legger til underskrift og kontaktinformasjon, noe den bare gjør i PDF-en (7.4), og at linjeskift inne i et punkt kan bli to punkter i eksporten (7.2). Skrev et utkast til kommentar med to alternativer for hvordan brevet starter og slutter, uten å velge for Henrik.
- Sjekket at Haakons rettelser i PR #35 faktisk står i `epics.md` og `.working/`. Leste Oles PR #33 og fant at KI-logginnlegget nevner en svakhet i den valgte regelen («Jeg kan SQL og ønsker å lære mer» telles ikke som påstand), men ikke at den manuelle kontrollen i 5.2 fanger den opp.
- Anslo kostnaden av `lag_lagrede_svar` for Oles PR #38 ut fra prisene for `claude-opus-5-5` og antall lagrede svar i AD-6: omtrent 1–5 USD per full kjøring. Anslaget er grovt, fordi tokenbruken til tankene er ukjent.
- Skrev et utkast til kommentar på PR #35 og markerte tre steder der den gjettet hva Henrik mente: å beholde 0.3 samlet, fordelingen i Epic 5 og å godta filnavnene.

## Våre vurderinger og korrigeringer
- **KI rettet seg selv:** Første forsøk på #29 søkte etter `fakta_i_cv` ordrett i PDF-teksten og fant nesten ingen treff, selv i B, som er ren tekst. Faktaene i fasiten er omskrevet, så metoden var feil. Den ble byttet ut med en sjekk av ordene i `cv_kilde.txt`.
- Henrik valgte forhåndssjekken av de fire forslagene KI ga, og ba om å få gå gjennom storyene sine en etter en.
- Henrik leste utkastet til kommentaren på PR #35 og lot den legges inn uendret, som en vanlig kommentar og ikke som en forespørsel om endringer.
- PR #34: Henrik er enig med Ole i at flosklene fra fasiten ikke skal stå i promptene. Han lot kommentaren legges inn uendret, uten å velge mellom alternativ A og B.
- PR #35: Henrik godtok at Haakon delte 5.3 i motsatt rekkefølge av forslaget hans, fordi hver del da kan testes alene, og godkjente PR-en.
- PR #33: Henrik står bak gruppas begrunnelse for å avvise Claudes forslag til evalueringsregel (ingen ekstra API-kall, enklere å kode, samme svar hver gang).
- Forslagene i issuene og på PR #33 og #34 er ikke vedtatt. Gruppa må svare på dem.

## Resultat
- Ingen kode eller planleggingsdokumenter er endret. Funnene står i [#17](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/17#issuecomment-7040666585), [#29](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/29#issuecomment-7040667017), [PR #34](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/34#issuecomment-7041672423) og [PR #35](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/35#issuecomment-7041179298).
- Sesjonslogg: `.logs/henrik-kulseng/996-2026-11-20-14-24-44-forhandssjekk-versjoner.md`.
- Gjenstår: Gruppa avgjør om grensen på 5 USD skal økes når den første evalueringsrapporten viser faktisk tokenbruk (PR #38). Gruppa velger A eller B for hvordan brevet starter og slutter (PR #34).
