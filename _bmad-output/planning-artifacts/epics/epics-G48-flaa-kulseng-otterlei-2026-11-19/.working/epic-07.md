## Epic 7: Ta med søknaden ut (P8)

Brukeren kan kopiere søknadsbrevet eller brevforslagene og laste dem ned som Markdown eller PDF. Koden ligger i `eksport/` (`markdown.py`, `pdf.py` og fontene som allerede finnes i `app/eksport/fonter/`), i `static/js/` og i steg 4 (`analyse/`). Den redigerte teksten fra steg 4 lagres aldri (AD-10, AD-22). Brevoppsettet i PDF-en er siste story, fordi det er første kutt i nødplanen (PRD §8.1). Kuttes det, eksporteres brevet som vanlig PDF. Epicet bruker tekstfeltet fra story 5.5. Kuttes 5.5, må kopieringen og eksporten bruke teksten i `Brev` i stedet, og det forklares i `docs/endringer/`.

### Story 7.1: Kopiere teksten

Som student
vil jeg kopiere brevet eller forslagene med én knapp,
slik at jeg kan lime teksten inn i søknadsskjemaet.

**Krav:** FR-22, NFR-7. **UX:** UX-DR22, UX-DR36. **Styres av:** AD-15, AD-17, AD-22.

**Akseptansekriterier:**

**Gitt** at jeg står i steg 4 med JavaScript på
**Når** siden lastes
**Så** legger `static/js/kopier.js` inn knappen «Kopier teksten» ved tekstfeltet med brevet (UX-DR22)
**Og** skriptet er vanlig JavaScript uten byggesteg og uten CDN, og kan brukes på alle tekstfelt med samme `data-`-attributt (AD-15)

**Gitt** at jeg har rettet teksten i feltet
**Når** jeg trykker «Kopier teksten»
**Så** kopieres innholdet i feltet med endringene (FR-22, AD-22)
**Og** «Kopiert!» skrives i et `aria-live`-område som finnes på siden fra start, og forsvinner etter 3 sekunder (UX-DR22)

**Gitt** at nettleseren nekter tilgang til utklippstavlen
**Når** jeg trykker knappen
**Så** markeres teksten i feltet, og `aria-live`-området sier at teksten kan kopieres med Ctrl+C (Cmd+C på Mac)
**Og** tekstene ligger i `kjerne/meldinger.py` og sendes til skriptet som `data-`-attributter fra malen

**Gitt** at JavaScript er av
**Når** steg 4 vises
**Så** finnes ingen kopieringsknapp, og teksten i feltet kan markeres og kopieres som vanlig (UX-DR22)

**Gitt** testene for storyen
**Når** de kjøres
**Så** sjekker en pytest-test at steg 4 har `data-`-attributtet, `aria-live`-området og `kopier.js`
**Og** kopiering, «Kopiert!», nektet utklippstavle og JavaScript av testes for hånd i Chrome og Firefox, og resultatet står i `docs/testplan.md` (AD-17)

### Story 7.2: Laste ned som Markdown

Som student
vil jeg laste ned brevet eller forslagene som en Markdown-fil,
slik at jeg kan jobbe videre med teksten i mitt eget program.

**Krav:** FR-13, FR-23, NFR-3, NFR-4, SM-7. **UX:** UX-DR23, UX-DR29. **Styres av:** AD-2, AD-8, AD-10, AD-13, AD-15, AD-20, AD-22.

**Akseptansekriterier:**

**Gitt** steg 4
**Når** siden vises
**Så** står knappen «Last ned Markdown» i et `POST`-skjema til `/resultat/brev/eksport/` som sender med teksten i tekstfeltet (UX-DR23, AD-13)
**Og** viewet ligger i `eksport/`, fordi avhengigheten går fra `eksport` til `analyse` (AD-2)

**Gitt** den redigerte teksten
**Når** jeg trykker «Last ned Markdown»
**Så** lager `eksport/markdown.py` filen ut fra `Brev.svarform`: ved fullt utkast deles teksten i avsnitt på tomme linjer, og ved kun forslag i punkter på linjeskift, der «– » foran hvert punkt fjernes før punktene skrives som en Markdown-liste (AD-8, AD-22)
**Og** oppdelingen i avsnitt og punkter ligger i én felles funksjon i `eksport/`, som PDF-eksporten i story 7.3 også bruker (DRY)
**Og** filen er UTF-8 med riktige æ, ø og å, og inneholder hele teksten (FR-23, SM-7)
**Og** svaret har `Content-Type: text/markdown; charset=utf-8` og `Content-Disposition: attachment`, med filnavnet `soknadsbrev.md` ved fullt utkast og `brevforslag.md` ved kun forslag. Filnavnet har aldri navn, e-post eller ID (AD-10)

**Gitt** en tekst over `BREV_MAKS` tegn etter at mellomrom først og sist er fjernet
**Når** jeg prøver å laste den ned
**Så** vises steg 4 på nytt med feiloppsummeringen og en melding fra `kjerne/meldinger.py`, og teksten jeg skrev, står fortsatt i feltet (AD-15, AD-20)

**Gitt** en eksport
**Når** den er ferdig
**Så** er den redigerte teksten verken lagret i `Brev`, i økten, i Django-meldinger eller i logger (AD-10, AD-22)
**Og** eksporten sender ingenting til KI-tjenesten (NFR-4)

**Gitt** at jeg ikke er logget inn, eller ikke har noe `Brev`
**Når** noen sender `POST` til `/resultat/brev/eksport/`
**Så** sendes jeg til Logg inn eller til det siste steget jeg kan nå (FR-13, AD-22)

**Gitt** testene for storyen
**Når** de kjøres
**Så** sjekker de hele teksten, æ, ø og å, avsnitt ved fullt utkast og punkter uten doble «– » ved kun forslag

### Story 7.3: Laste ned som PDF

Som student
vil jeg laste ned brevet eller forslagene som PDF,
slik at jeg har en ferdig fil jeg kan lese gjennom eller skrive ut.

**Krav:** FR-23, NFR-1, NFR-4, SM-7. **UX:** UX-DR23. **Styres av:** AD-10, AD-13, AD-18, AD-22.

**Akseptansekriterier:**

**Gitt** steg 4
**Når** siden vises
**Så** står «Last ned PDF» ved siden av «Last ned Markdown» i det samme skjemaet (UX-DR23)

**Gitt** den redigerte teksten
**Når** jeg trykker «Last ned PDF»
**Så** lager `eksport/pdf.py` en PDF med `fpdf2` og fonten DejaVu Sans fra `eksport/fonter/`, uten systembiblioteker (AD-13, NFR-1)
**Og** fullt utkast blir avsnitt, og kun forslag blir en punktliste uten brevoppsett (FR-23)
**Og** filen heter `soknadsbrev.pdf` eller `brevforslag.pdf`, etter samme regel som i story 7.2
**Og** oppdeling i avsnitt og punkter, fjerning av «– » og grensen `BREV_MAKS` gjøres på samme måte som i Markdown-eksporten, uten kopiert kode (AD-22)

**Gitt** en tekst med æ, ø, å, tankestrek «–», typografiske anførselstegn og kulepunkter «•»
**Når** den eksporteres til PDF
**Så** krasjer ikke eksporten, og en test som leser PDF-en med `pdfplumber` finner hele teksten med riktige tegn (FR-23, SM-7, AD-13)
**Og** loggeren `fpdf.output` er dempet, fordi `fpdf2` ellers logger tegn fonten mangler, og det er tegn fra brevteksten. En test viser at eksporten ikke logger noe (AD-10)
**Og** en tekst nær `BREV_MAKS` gir flere sider med hele teksten
**Og** en tekst med en emoji gir en PDF uten krasj. Tegn fonten mangler, kan falle bort, men resten av teksten er med

**Gitt** en eksport
**Når** den er ferdig
**Så** er ingenting lagret, og ingenting er sendt til KI-tjenesten (AD-10, NFR-4)

### Story 7.4: Brevoppsett med dato og avsender i PDF-en

Som student
vil jeg at PDF-en av søknadsbrevet har dato og avsender øverst,
slik at den ser ut som et ordentlig brev.

**Krav:** FR-23, NFR-4, NFR-7, SM-7. **UX:** UX-DR23, UX-DR29, UX-DR36. **Styres av:** AD-5, AD-10, AD-13, AD-14, AD-15, AD-20.

Storyen er første kutt i nødplanen (PRD §8.1). Uten den virker eksporten fra story 7.3 som før.

**Akseptansekriterier:**

**Gitt** steg 4 med fullt utkast
**Når** siden vises
**Så** står feltene Navn (påkrevd), E-post (valgfri) og Telefon (valgfri) over nedlastingsknappene, med synlige etiketter og `autocomplete="name"`, `"email"` og `"tel"` (UX-DR23, UX-DR36)
**Og** under feltene står «Brukes bare i PDF-en og lagres ikke»
**Og** feltene har `maxlength` fra `AVSENDER_MAKS` (100) i `kjerne/grenser.py`, og E-post valideres som e-postadresse når den er fylt ut (AD-15)
**Og** ved kun forslag vises ingen avsenderfelt (FR-23)

**Gitt** et navn, og eventuelt e-post og telefon
**Når** jeg trykker «Last ned PDF»
**Så** har PDF-en avsenderen øverst og eksportdatoen skrevet på valgt språk, for eksempel «19. november 2026» på norsk og «19 November 2026» på engelsk, med månedsnavn skrevet inn i koden og dagens dato i `Europe/Oslo` (FR-23, AD-13, AD-14)

**Gitt** at Navn mangler ved fullt utkast
**Når** jeg trykker «Last ned PDF»
**Så** vises steg 4 på nytt med feiloppsummeringen og feilen ved feltet, og teksten i brevfeltet og det jeg har skrevet i avsenderfeltene, står fortsatt der (UX-DR29, AD-20)
**Og** «Last ned Markdown» virker uten navn, og knappen har `formnovalidate`, så `required` på Navn ikke stopper den i nettleseren
**Og** Markdown-filen har aldri avsender, selv om avsenderfeltene sendes med i det samme skjemaet, og en test viser det (AD-10)

**Gitt** en eksport med avsender
**Når** den er ferdig
**Så** er navn, e-post og telefon verken lagret, lagt i økten, logget eller sendt til KI-tjenesten (FR-23, AD-5, AD-10)
**Og** en test sjekker at avsenderen ikke finnes i databasen etter eksporten

**Gitt** testene for storyen
**Når** de kjøres
**Så** finner de dato og avsender i PDF-en med `pdfplumber` for både norsk og engelsk, og ingen avsender i en PDF av brevforslag
**Og** de dekker et navn over `AVSENDER_MAKS` og en ugyldig e-post
