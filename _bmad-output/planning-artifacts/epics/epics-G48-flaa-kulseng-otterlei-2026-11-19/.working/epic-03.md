## Epic 3: Annonse og nøkkelordanalyse (steg 2 og 3)

Brukeren kan lime inn annonsen, velge språk og egne nøkkelord, trykke «Analyser» og se hvilke nøkkelord som finnes og mangler. Alt i Epic 3 virker uten KI, også med egen CV i testmodus. Koden ligger i `nokkelord/` (ren Python, AD-7) `analyse/` (modellen `Analyse`, tjenesten og stegene 2 og 3) og `ki/eksempelpar.py` (`finn_eksempelpar`, story 3.2). «Analyser» kjører i Epic 3 bare det første steget i AD-8 (`nokkelord.match`). Gap-analysen og KI-forklaringen legges til i Epic 4.

### Story 3.1: Finne og matche nøkkelord i kode

Som student
vil jeg at appen finner nøkkelordene i annonsen og sjekker dem mot CV-en min på samme måte hver gang,
slik at jeg kan stole på at resultatet ikke er tilfeldig.

**Krav:** FR-19, FR-20, NFR-2, SM-6. **Styres av:** AD-2, AD-7, AD-16, AD-17.

**Akseptansekriterier:**

**Gitt** `nokkelord/modeller.py`
**Når** jeg ser på den
**Så** bruker pakken pydantic-modellene `Nokkelord` og `Nokkelordresultat` fra story 0.4, der resultatet har `funnet`, `mangler` og `andel` (en `float` fra 0 til 1)
**Og** pakken `nokkelord/` importerer ikke Django (AD-2)

**Gitt** `finn_nokkelord(annonse, onskede: list[str]) -> list[Nokkelord]`
**Når** den får en annonse
**Så** finner den nøkkelordene fra `nokkelord/ordliste.json` (grunnform og synonymer) og tar med de ønskede nøkkelordene (FR-19)
**Og** den matcher på hele ord med `(?<!\w)` før og `(?!\w)` etter skrivemåten, så C#, C++, .NET og «Bachelor's» virker, og mellomrom i en skrivemåte med flere ord matcher `\s+` (AD-7)
**Og** et treff som ligger inni et lengre treff fra et annet nøkkelord, droppes, så «førerkort klasse B» bare gir klasse B, mens «Vi krever førerkort» gir det generelle nøkkelordet
**Og** et ønsket nøkkelord som er lik en grunnform eller et synonym i ordlisten, uansett store og små bokstaver, blir det nøkkelordet fra ordlisten og kommer bare med én gang
**Og** et nøkkelord med `"skiller_store_og_sma": true` matches med nøyaktige store og små bokstaver bare for grunnformen, så «react quickly», «excel at» og «a word of advice» ikke gir treff, mens synonymer som «regneark» og «microsoft word» gjør det (FR-20)

**Gitt** `match(cv_tekst, nokkelord) -> Nokkelordresultat`
**Når** den sjekker CV-teksten
**Så** ignoreres store og små bokstaver alltid, også for nøkkelord med `skiller_store_og_sma`, og det holder at én skrivemåte finnes i CV-teksten (FR-20, AD-7)
**Og** krever annonsen «førerkort», og CV-en sier «Førerkort klasse B», regnes førerkort som funnet
**Og** gir annonsen ingen nøkkelord, er `andel` 0.0, og `funnet` og `mangler` er tomme

**Gitt** samme inndata to ganger
**Når** funksjonene kjøres
**Så** er utdata like, og listene er sortert med `key=str.casefold` (FR-19, FR-20)

**Gitt** eksempelpar A, B og C, lest gjennom `ki.eksempelpar.hent_eksempelpar()` og `dokumenter.pdf_innlesing.les_cv()`
**Når** enhetstestene kjører `finn_nokkelord` og `match`
**Så** stemmer `i_annonsen`, `funnet` og `mangler` med `nokkelord` i fasiten som mengder, og `andel` stemmer med `pytest.approx(..., abs=0.001)` (for A: Git og Python funnet, SQL og førerkort klasse B mangler, andel 0,5) (SM-6, AD-17)
**Og** testene bruker ikke databasen og ikke nettverket

**Gitt** testene for reglene i AD-7
**Når** de kjøres
**Så** dekker de minst hele ord, `\s+` over linjeskift, lengste treff vinner, `skiller_store_og_sma` i annonse og CV, ønskede nøkkelord som ikke står i ordlisten, ønskede nøkkelord som allerede står i ordlisten, og en annonse uten nøkkelord

### Story 3.2: Lime inn annonsen og velge språk og nøkkelord (steg 2)

Som student
vil jeg lime inn stillingsannonsen og velge språk og egne nøkkelord,
slik at analysen gjelder akkurat den stillingen jeg søker.

**Krav:** FR-3, FR-4, NFR-3, NFR-4, NFR-7, NFR-8. **UX:** UX-DR7, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR29, UX-DR33, UX-DR35, UX-DR36. **Styres av:** AD-5, AD-6, AD-7, AD-8, AD-10, AD-15, AD-16, AD-20, AD-22.

**Akseptansekriterier:**

**Gitt** at jeg har en CV
**Når** jeg trykker «Bruk denne og gå videre» i steg 1
**Så** kommer jeg til `/analyse/` i stedet for tilbake til steg 1, slik Epic 2 gjorde midlertidig (AD-22)
**Og** uten CV sender `/analyse/` meg til steg 1 (`siste_steg`)

**Gitt** steg 2
**Når** siden vises
**Så** ser jeg fremdriftslinjen med steg 2 aktivt, et stort annonsefelt med etikett, språk som radioknapper i en `fieldset` med `legend` (norsk forhåndsvalgt), og et valgfritt felt for ønskede nøkkelord med komma mellom ordene (FR-4, UX-DR13)
**Og** feltene har `required` og `maxlength` fra `kjerne/grenser.py`, og valgene kommer fra `kjerne/valg.py` (AD-15, AD-16)

**Gitt** et felles skript for tegnteller i `static/js/`
**Når** jeg skriver i annonsefeltet
**Så** vises «1 234 / 15 000 tegn» under feltet, og uten JavaScript virker skjemaet likevel (UX-DR12, UX-DR36)

**Gitt** en annonse som er tom, under `ANNONSE_MIN` (100) eller over `ANNONSE_MAKS` (15 000) tegn etter at mellomrom først og sist er fjernet
**Når** jeg trykker «Analyser»
**Så** vises steg 2 på nytt med feiloppsummeringen og «Annonsen må ha minst 100 tegn.» eller «Annonsen kan ha maks 15 000 tegn.» ved feltet, teksten jeg skrev, står fortsatt i feltet, og ingen analyse kjøres (FR-3, UX-DR33, AD-20)

**Gitt** ønskede nøkkelord
**Når** skjemaet valideres
**Så** deles de opp på komma og linjeskift, tomme fjernes, duplikater fjernes uansett store og små bokstaver, og flere enn `ONSKEDE_NOKKELORD_MAKS` (20) gir en melding ved feltet (AD-7, AD-15)

**Gitt** at appen kjører i KI-modus
**Når** steg 2 vises
**Så** står personvernpåminnelsen fra UX-DR14 rett over «Analyser», med lenke til Min konto (NFR-4, AD-5)
**Og** i testmodus står i stedet «Testmodus: ingenting sendes til KI-tjenesten. Appen bruker lagrede svar.»
**Og** tekstene ligger i `kjerne/meldinger.py`

**Gitt** at det finnes en lagret `Analyse`
**Når** steg 2 vises
**Så** er annonsen, språket og de ønskede nøkkelordene fylt inn fra den, og «Dette erstatter analysen og utkastet du har nå.» står over «Analyser» (UX-DR11, UX-DR12, AD-22)

**Gitt** at det ikke finnes en `Analyse`, og at CV-teksten er teksten til et eksempelpar
**Når** steg 2 vises
**Så** er annonsen til paret fylt inn, funnet med `ki.eksempelpar.finn_eksempelpar(cv_tekst)`, som sammenligner `normaliser(cv_tekst)` med referanseteksten til A, B og C og gir `None` ellers (AD-6, AD-22)
**Og** en test sjekker at par D aldri gir treff, og at en endret CV-tekst gir `None`

**Gitt** at skjemaet sendes
**Når** jeg ser på det
**Så** bruker det `POST`, og annonsen havner aldri i økten, i URL-en eller i logger (AD-10)
**Og** et gyldig skjema lagres og analyseres først i story 3.3. I denne storyen testes valideringen på skjemaet i `analyse/forms.py`, og et gyldig skjema blir stående i steg 2

### Story 3.3: Kjøre «Analyser» og se nøkkelordanalysen (steg 3)

Som student
vil jeg trykke «Analyser» og se hvilke nøkkelord fra annonsen som finnes og mangler i CV-en min,
slik at jeg vet hvilke ord jeg bør vurdere å få med.

**Krav:** FR-2, FR-4, FR-11, FR-14, FR-15, FR-19, FR-20, NFR-3, NFR-7, SM-8. **UX:** UX-DR5, UX-DR7, UX-DR17, UX-DR32, UX-DR35, UX-DR36. **Styres av:** AD-2, AD-7, AD-8, AD-9, AD-10, AD-12, AD-20, AD-22.

**Akseptansekriterier:**

**Gitt** modellen `Analyse` i `analyse/models.py`
**Når** migreringen for storyen kjøres
**Så** har `Analyse` feltene for annonse, språk, ønskede nøkkelord og nøkkelordresultat, og alt dokumentinnhold ligger i krypterte felt (FR-15, AD-8, AD-9)
**Og** feltene for gap-analysen, forklaringen og `ki_status` kommer i Epic 4, fordi Epic 3 ikke kaller KI

**Gitt** en gyldig annonse i steg 2
**Når** jeg trykker «Analyser»
**Så** kjører `analyse.tjenester` `nokkelord.finn_nokkelord` og `nokkelord.match` på den lagrede CV-teksten, sletter en eventuell gammel `Analyse` (og med den `Brev` og `CVForbedring` gjennom `CASCADE`) og lagrer den nye i en kort `transaction.atomic` (AD-8, AD-12)
**Og** nøkkelordresultatet lagres med `model_dump(mode="json")` og leses med `model_validate()` (AD-9)
**Og** jeg sendes til `/resultat/` med Post/Redirect/Get, så tilbakeknappen ikke kjører analysen på nytt (UX-DR35)

**Gitt** steg 3
**Når** siden vises
**Så** ser jeg et nøkkelordkort med merket «Telt automatisk», en måler med «7 av 10 funnet» og andelen i aksentfargen, og brikker for nøkkelord som finnes og som mangler, der de som mangler, har stiplet kant (UX-DR17)
**Og** farge er aldri eneste kjennetegn, og nøkkelordene vises med Djangos automatiske escaping (NFR-3, UX-DR36)
**Og** siden har en plass over nøkkelordkortet der gap-analysen kommer i Epic 4
**Og** gir annonsen ingen nøkkelord, viser kortet «Fant ingen kjente nøkkelord i annonsen. Du kan legge til egne nøkkelord i steg 2.» fra `kjerne/meldinger.py`, med lenke til steg 2, i stedet for måleren

**Gitt** at appen kjører i testmodus og jeg har lastet opp en egen CV
**Når** jeg trykker «Analyser»
**Så** vises nøkkelordanalysen fra koden, og ingen KI-kall gjøres (FR-11, UX-DR32)

**Gitt** en lagret `Analyse`
**Når** jeg logger inn på nytt
**Så** havner jeg i steg 3, og fremdriftslinjen har lenker til steg 1 og 2 (`siste_steg` gir 3, UX-DR35)

**Gitt** to testbrukere med hver sin analyse
**Når** bruker 1 åpner `/resultat/`
**Så** ser bruker 1 bare sin egen analyse, og ingen URL inneholder en ID (FR-14, AD-10)

**Gitt** en lagret analyse
**Når** testen leser SQLite-filen direkte
**Så** finnes verken annonsen, de ønskede nøkkelordene eller nøkkelordresultatet i klartekst (FR-15)

**Gitt** at jeg retter CV-teksten i steg 1 etter en analyse
**Når** teksten lagres
**Så** er analysen borte, og `/resultat/` sender meg til steg 2 (FR-2, AD-8)
