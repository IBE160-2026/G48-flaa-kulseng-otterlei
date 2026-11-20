## Epic 1: Konto og innlogging

Brukeren kan registrere seg med avkrysning for personvern, logge inn og ut, lese i Min konto hva som lagres og sendes, og slette kontoen. Alt skjer i `kontoer/` (AD-2). Etter Epic 1 kommer brukeren til Min konto etter innlogging. Epic 2 endrer det til steget brukeren står i.

### Story 1.1: Registrere konto

Som student
vil jeg registrere meg med e-post og passord,
slik at CV-en og søknadene mine bare er mine.

**Krav:** FR-12, NFR-3, NFR-4. **UX:** UX-DR26, UX-DR27, UX-DR29, UX-DR34, UX-DR36. **Styres av:** AD-2, AD-5, AD-11, AD-15.

**Akseptansekriterier:**

**Gitt** at jeg ikke er logget inn
**Når** jeg åpner `/registrer/`
**Så** ser jeg feltene E-post og Passord med synlige etiketter og `autocomplete`, og avkrysningen «Jeg har lest hvordan appen behandler CV-en min» med lenke til personvernsiden `/personvern/`

**Gitt** personvernsiden `/personvern/`
**Når** jeg åpner den uten å være logget inn
**Så** forklarer den hva som lagres (siste CV, CV-tekst, annonse og resultat, kryptert), hvor lenge (til jeg sletter det), hva som sendes til KI (CV-tekst, annonse og valg, aldri e-posten og passordet), at CV-teksten sendes med navn og kontaktinformasjon som jeg kan fjerne når jeg retter den, at KI-tjenesten er Claude fra Anthropic, og at jeg kan slette alt når som helst (UX-DR27, AD-5)
**Og** teksten ligger i maldelen `templates/kontoer/personvern.html`, som Min konto også bruker (story 1.3). Den brukes bare av `kontoer`, så den ligger ikke i `templates/felles/` (AD-15)

**Gitt** gyldig e-post, et passord på minst 8 tegn og avkrysning
**Når** jeg trykker «Registrer»
**Så** lages kontoen, og jeg blir logget inn og sendt til Min konto
**Og** e-posten lagres med små bokstaver og uten mellomrom først og sist, og passordet lagres bare som PBKDF2-hash (FR-12, AD-11)

**Gitt** en e-post som allerede er registrert, også med andre store og små bokstaver
**Når** jeg prøver å registrere meg
**Så** får jeg «Denne e-posten er allerede registrert.», og ingen ny konto lages

**Gitt** et passord under 8 tegn, eller manglende avkrysning
**Når** jeg trykker «Registrer»
**Så** får jeg «Passordet må ha minst 8 tegn.» eller «Du må krysse av for at du har lest om personvern.» i feiloppsummeringen og ved feltet
**Og** tekstene ligger i `kjerne/meldinger.py`
**Og** det finnes ingen andre passordregler (FR-12)

**Gitt** testene for storyen
**Når** de kjøres
**Så** dekker de vellykket registrering, dobbel e-post, kort passord, manglende avkrysning og at passordet ikke ligger i klartekst i databasen

### Story 1.2: Logge inn og ut

Som registrert bruker
vil jeg logge inn og ut,
slik at bare jeg kommer til dataene mine.

**Krav:** FR-13, FR-14. **UX:** UX-DR3, UX-DR34, UX-DR35. **Styres av:** AD-10, AD-11, AD-20.

**Akseptansekriterier:**

**Gitt** riktig e-post og passord
**Når** jeg logger inn på `/logg-inn/`
**Så** blir jeg sendt til Min konto, og topplinjen viser «Min konto» og «Logg ut»

**Gitt** feil e-post eller feil passord
**Når** jeg prøver å logge inn
**Så** får jeg «Feil e-post eller passord.» i begge tilfeller (FR-13)
**Og** teksten ligger i `kjerne/meldinger.py`

**Gitt** at jeg er logget inn
**Når** jeg trykker «Logg ut» (et `POST`-skjema i topplinjen)
**Så** blir jeg logget ut og sendt til Logg inn
**Og** trykker jeg tilbakeknappen, ser jeg ingen brukerdata, fordi sidene har `never_cache` (FR-13, AD-10)

**Gitt** at jeg ikke er logget inn, eller at økten har utløpt
**Når** jeg åpner en side med brukerdata
**Så** blir jeg sendt til Logg inn med «Du ble logget ut. Logg inn igjen. Det du limte inn, ble ikke lagret.» når økten har utløpt (UX-DR34)
**Og** økten regnes som utløpt når nettleseren sender en øktkake (`sessionid`) som ikke lenger er gyldig. Uten øktkake vises ingen melding
**Og** meldingen ligger i `kjerne/meldinger.py`
**Og** alle views med brukerdata har `login_required` og `never_cache` (FR-14, AD-10)

**Gitt** testene for storyen
**Når** de kjøres
**Så** dekker de innlogging, samme melding ved feil e-post og feil passord, at utlogging bare virker med `POST`, og at Min konto ikke kan åpnes uten innlogging
**Og** en test logger inn, sletter økten i databasen, sender et skjema og sjekker at meldingen om utløpt økt vises

### Story 1.3: Min konto med personverninformasjon

Som innlogget bruker
vil jeg lese hva appen lagrer om meg og hva som sendes til KI-tjenesten,
slik at jeg vet hva som skjer med CV-en min.

**Krav:** NFR-4, NFR-8. **UX:** UX-DR27. **Styres av:** AD-5, AD-10.

**Akseptansekriterier:**

**Gitt** at jeg er logget inn
**Når** jeg åpner `/min-konto/`
**Så** ser jeg e-posten min og forklaringen fra maldelen `templates/kontoer/personvern.html` fra story 1.1 (UX-DR27, AD-5)
**Og** teksten skrives ikke på nytt i malen for Min konto

**Gitt** testene for storyen
**Når** de kjøres
**Så** sjekker de at Min konto viser e-posten til den som er logget inn og ikke e-posten til en annen bruker, og at personverntekst fra maldelen vises (AD-10)

### Story 1.4: Slette konto

Som bruker
vil jeg slette kontoen min,
slik at ingenting om meg blir liggende igjen i appen.

**Krav:** FR-17, NFR-2, SM-9. **UX:** UX-DR28, UX-DR34. **Styres av:** AD-8, AD-9, AD-11, AD-17, AD-19, AD-21.

**Akseptansekriterier:**

**Gitt** at jeg er logget inn
**Når** jeg trykker «Slett konto», som legges inn i Min konto som egen handling i denne storyen
**Så** kommer jeg til bekreftelsessiden (`GET` til `/min-konto/slett-konto/`), laget med `templates/felles/bekreftelse.html`, med «Er du sikker? Dette kan ikke angres», en rød knapp og [Avbryt] (FR-17, UX-DR28)
**Og** `GET` sletter ingenting, og en test viser det

**Gitt** bekreftelsessiden
**Når** jeg trykker den røde knappen (`POST` til `/min-konto/slett-konto/`)
**Så** blir jeg logget ut, øktene mine slettes, og `Bruker` slettes, så `CASCADE` tar alt som henger på kontoen (AD-11)
**Og** jeg kommer til Logg inn med meldingen «Kontoen din er slettet.» fra `kjerne/meldinger.py`
**Og** meldingen legges inn etter utloggingen, fordi utloggingen sletter økten der Django lagrer meldingene. En test følger viderekoblingen og sjekker at meldingen vises

**Gitt** at kontoen er slettet
**Når** testen søker etter e-posten som bytes i databasefilen
**Så** finnes den ikke (AD-17, AD-19)
**Og** e-posten kan registreres på nytt (FR-17)

**Gitt** en bruker med en CV som ikke kan dekrypteres
**Når** brukeren sletter kontoen
**Så** virker slettingen uten `Dekrypteringsfeil`, fordi `CASCADE` ikke leser de krypterte feltene, og en test viser det (AD-9)

**Gitt** at jeg trykker [Avbryt]
**Når** jeg kommer tilbake til Min konto
**Så** er ingenting slettet

