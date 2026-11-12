# Forslag til arbeidsfordeling og fremdriftsplan

| | |
|---|---|
| **Dato** | 2026-11-12 |
| **Hvem** | Ole A. Flaa |
| **Verktøy** | Claude Code (Claude Opus 5.5) |
| **Commits / PR** | Commiten med dette innlegget, pull request på branchen `docs/arbeidsfordeling` |

## Mål

Få et forslag til hvordan de tre i gruppa kan fordele ansvaret, og hvordan vi kommer i gang med resten av prosjektet fram til fristen 15. desember.

## Viktigste prompts

1. «Vi har ett gruppeprosjekt som skal leveres om ca en måned. Vi skal lage AI CV & Job Application Assistant som er beskrevet i vedlagte Prosjektforslag_ Programmering med KI.pdf. Vi er tre på gruppen som trenger hjelp til hvordan vi skal fordele arbeidsoppgavene våre og løse oppgaven med ett mål om å få karakter: A. Vi vil hovedsakelig jobbe i VsCode, med GitHub integrert. Les gjennom alle filer i G48-flaa-kulseng-otterlei repositoriet, samt alle vedlagte filer og fortell meg hvordan vi kan fordele ansvarsområder oss imellom og hvordan vi kan begynne på oppgaven.» Vedlagt var prosjektforslagene, sensorveiledningen for del 1, malen for product brief, et eksempel på en product brief, malen for refleksjonsrapporten og lysbildene om product brief.
2. «Ja, lag PR» (etter at Claude spurte om forslaget skulle legges inn i repoet).

## Hva KI gjorde

- Leste planleggingsdokumentene, tilbakemeldingene, KI-loggen, sesjonsloggen og git-historikken i repoet, og alle vedleggene.
- Pekte på fire risikoer: ingen kode ennå, alle commits er fra én person, tre punkter i den nye PRD-tilbakemeldingen som må avklares før arkitekturen, og at `architecture/technology.md` beskriver et annet prosjekt og er større enn appen vår trenger.
- Foreslo en fordeling: Ole tar arkitektur og KI-laget, Henrik tar UX og frontend, og Haakon tar data, sikkerhet og testgrunnlag. Felles regler for issues, gjennomgang av pull requests og KI-logg.
- Foreslo en ukeplan med fem uker og ingen nye funksjoner fra 10. desember.
- Foreslo at gruppa vurderer en kuttrekkefølge, selv om gruppa tidligere har bestemt at ingenting skal kuttes, fordi faglærer har pekt på det igjen.
- Skrev forslaget inn i `docs/arbeidsfordeling.md`, og la til dokumentet i README.

## Våre vurderinger og korrigeringer

- Ole ba om at forslaget legges inn i repoet som en pull request.
- Resten av gruppa har ikke vurdert forslaget ennå. Fordelingen, ukeplanen og spørsmålet om kuttrekkefølge er Claudes forslag og tas opp i gjennomgangen av pull requesten. Gruppas vurderinger føres inn her etter gjennomgangen.

## Resultat

- Nytt dokument: `docs/arbeidsfordeling.md`.
- README lenker til dokumentet og viser det i mappestrukturen.

**Gjenstår:** Gruppa går gjennom og bekrefter eller endrer forslaget, og avgjør punktene i §5 i dokumentet.
