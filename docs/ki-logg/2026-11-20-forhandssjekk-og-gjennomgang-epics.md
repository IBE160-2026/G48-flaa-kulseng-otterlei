# Forhåndssjekk av versjoner og gjennomgang av epics

| | |
|---|---|
| **Dato** | 2026-11-20 |
| **Hvem** | Henrik |
| **Verktøy** | Claude Code (Claude Opus 5.5), BMAD-skillen `bmad-help` |
| **Commits / PR** | Sesjonsloggen på branchen `docs/forhandssjekk-versjoner`. Kommentarer på issue #17 og #29 og på PR #34 og #35 |

## Mål
Haakon lager epics og stories. I mellomtiden ville Henrik finne noe nyttig å gjøre som ikke kolliderer med det arbeidet. Han valgte å sjekke på forhånd at versjonene arkitekturen har valgt, virker sammen (issue #17 og #29). Etterpå gikk han gjennom storyene sine i Haakons PR #35.

## Viktigste prompts
- «help» (`bmad-help`: hvor står vi, og hva er neste steg?)
- «haakon holder på med det nå, hva kan jeg gjøre nå imens?»
- «ja, ta punkt 1» (forhåndssjekken av #17 og #29)
- «gå gjennom storyene mine» (0.3, Epic 5 og Epic 7 i PR #35)
- «skriv et utkast til kommentaren», og deretter «legg den inn»
- «ja, skriv utkast, jeg er enig om flosklene» (kommentar på Oles PR #34 med prompter)

## Hva KI gjorde
- Lagde et midlertidig Python-miljø utenfor repoet med alle versjonene fra arkitekturen §4, og et lite Django 6.1-prosjekt med pytest-django og pytest-socket. Seks tester besto (#17).
- Kjørte `lag_cv_pdf.py` på en kopi av `app/`. Fant at PDF-ene ikke blir like byte for byte selv med fonttools 4.68.0. Fant årsaken ved å prøve 14 versjoner av fonttools og sammenligne PDF-objektene: bare zlib-komprimeringen er ulik (#29).
- Skrev funnene og forslagene som kommentarer i issuene.
- Sammenlignet storyene til Henrik med `DESIGN.md`, `EXPERIENCE.md` og arkitekturen. Prøvde kriteriene i 7.3 med fpdf2 og fant at fpdf2 logger tegn fra brevteksten som fonten mangler, noe som strider mot AD-10.
- Leste `brev.md` i Oles PR #34 opp mot storyene for steg 4 og eksporten. Fant at prompten sier at appen legger til underskrift og kontaktinformasjon, noe den bare gjør i PDF-en (7.4), og at linjeskift inne i et punkt kan bli to punkter i eksporten (7.2). Skrev et utkast til kommentar med to alternativer for hvordan brevet starter og slutter, uten å velge for Henrik.
- Skrev et utkast til kommentar på PR #35 og markerte tre steder der den gjettet hva Henrik mente: å beholde 0.3 samlet, fordelingen i Epic 5 og å godta filnavnene.

## Våre vurderinger og korrigeringer
- **KI rettet seg selv:** Første forsøk på #29 søkte etter `fakta_i_cv` ordrett i PDF-teksten og fant nesten ingen treff, selv i B, som er ren tekst. Faktaene i fasiten er omskrevet, så metoden var feil. Den ble byttet ut med en sjekk av ordene i `cv_kilde.txt`.
- Henrik valgte forhåndssjekken av de fire forslagene KI ga, og ba om å få gå gjennom storyene sine en etter en.
- Henrik leste utkastet til kommentaren på PR #35 og lot den legges inn uendret, som en vanlig kommentar og ikke som en forespørsel om endringer.
- PR #34: Henrik er enig med Ole i at flosklene fra fasiten ikke skal stå i promptene. Han lot kommentaren legges inn uendret, uten å velge mellom alternativ A og B.
- Forslagene i issuene og på PR #34 og #35 er ikke vedtatt. Gruppa må svare på dem.

## Resultat
- Ingen kode eller planleggingsdokumenter er endret. Funnene står i [#17](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/17#issuecomment-7040666585), [#29](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/issues/29#issuecomment-7040667017) [PR #34](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/34#issuecomment-7041672423) og [PR #35](https://github.com/IBE160-2026/G48-flaa-kulseng-otterlei/pull/35#issuecomment-7041179298).
- Sesjonslogg: `.logs/henrik-kulseng/996-2026-11-20-14-24-44-forhandssjekk-versjoner.md`.
- Gjenstår: Gruppa svarer på forslagene i PR #34 og #35, velger A eller B for hvordan brevet starter og slutter, og avgjør issue #16 (API-kontoen), som story 5.7 venter på.
