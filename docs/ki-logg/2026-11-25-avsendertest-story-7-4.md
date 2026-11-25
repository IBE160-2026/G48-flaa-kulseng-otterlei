# Avsendertesten i story 7.4 tar hensyn til navnet i brevet (issue #46)

| | |
|---|---|
| **Dato** | 2026-11-25 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Commitene på branchen `docs/avsendertest-story-7-4` |

## Mål

Løse issue #46: Gruppa har valgt alternativ A for brevet, så navnet fra CV-en står under avslutningen i brevteksten. Testene i story 7.4 for at avsenderen aldri havner i Markdown-filen, må tåle det.

## Viktigste prompts

1. «Er det noe jeg kan gjøre mens jeg venter?»
2. «Ta issue #46»

## Hva KI gjorde

- Leste issue #46, story 7.4 i `epics.md` og brevprompten i `app/ki/prompter/brev.md`.
- Fant at problemet gjelder to kriterier, ikke bare det issuen nevner: testen for at Markdown-filen ikke har avsender, og testen for at avsenderen ikke finnes i databasen etter eksporten. Navnet fra CV-en står allerede i databasen, både i CV-en og i `Brev`.
- Issuen ga to løsninger: egne testverdier for avsenderen, eller å sjekke at hele avsenderblokken mangler. Claude Code valgte egne testverdier, fordi den samme løsningen dekker begge kriteriene og er enkel å skrive som test.
- La til ett kriterium under Markdown-kriteriet og en presisering i databasekriteriet i story 7.4.

## Våre vurderinger og korrigeringer

- Ole valgte å ta issue #46 nå, mens gruppa ser over de åpne PR-ene.
- Valget av egne testverdier er Claude Codes forslag. Henrik eier story 7.4 og må bekrefte det i pull requesten.

## Resultat

- `epics.md`, story 7.4: Testene bruker et navn, en e-post og et telefonnummer som verken står i CV-en eller i brevteksten, og sjekker at akkurat disse verdiene mangler i Markdown-filen og i databasen.
- Issue #46 lukkes når pull requesten er flettet.
