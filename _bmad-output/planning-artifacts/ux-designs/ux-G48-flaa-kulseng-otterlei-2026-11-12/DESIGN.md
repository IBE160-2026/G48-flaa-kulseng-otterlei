---
name: Søknadshjelpen
description: Visuell identitet for AI CV & Job Application Assistant. Rolig, ryddig og blågrønn, for norske studenter som skal skreddersy en søknad uten å streve. Egen CSS i Django-maler, uten UI-rammeverk.
status: final
updated: 2026-11-12
sources:
  - ../../prd/prd.md
  - ../../prd/addendum.md
  - ../../architecture/architecture-G48-flaa-kulseng-otterlei-2026-11-03/ARCHITECTURE-SPINE.md
colors:
  # Lys modus
  background: '#FFFFFF'
  surface: '#F6F8F8'
  text: '#1F2A2E'
  text-muted: '#5E6B70'
  border: '#DCE3E4'
  field-border: '#7F8C8F'
  accent: '#1F7A75'
  on-accent: '#FFFFFF'
  match: '#23784A'
  match-bg: '#E2F3EA'
  missing: '#9A5800'
  missing-bg: '#FCEFD9'
  danger: '#B3261E'  # Claudes forslag, godtatt av Henrik 2026-11-12
  on-danger: '#FFFFFF'
  info-bg: '#E3F1F0'  # testmodus-banner og personvernmerknad
  # Mørk modus (prefers-color-scheme: dark)
  background-dark: '#121718'
  surface-dark: '#1B2224'
  text-dark: '#E4EBEC'
  text-muted-dark: '#98A6AA'
  border-dark: '#2C3639'
  field-border-dark: '#66757A'
  accent-dark: '#5CC2BB'
  on-accent-dark: '#0E1415'
  match-dark: '#6CC495'
  match-bg-dark: '#18322A'
  missing-dark: '#E3A857'
  missing-bg-dark: '#3A2B13'
  danger-dark: '#F2B8B5'
  on-danger-dark: '#2A0E0C'
  info-bg-dark: '#16302E'
typography:
  # Systemskrift. Ingen fontfiler i repoet.
  # Stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
  # Størrelsene er Claudes forslag, godtatt av Henrik 2026-11-12.
  heading:
    fontSize: 24px
    fontWeight: '650'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  heading-sm:
    fontSize: 18px
    fontWeight: '650'
    lineHeight: '1.3'
  body:
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  small:
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.45'
  label:
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
  tag:
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.3'
  letter:
    # Brevteksten i steg 4
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.65'
rounded:
  sm: 6px
  DEFAULT: 10px
  full: 9999px
spacing:
  # 4-basert skala (Claudes forslag, godtatt av Henrik 2026-11-12)
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
  '7': 48px
  content-max: 720px
  gutter-mobile: 16px
  gutter-desktop: 24px
components:
  button-primary:
    background: '{colors.accent}'
    foreground: '{colors.on-accent}'
    radius: '{rounded.DEFAULT}'
    minHeight: 44px
  button-secondary:
    background: '{colors.background}'
    foreground: '{colors.text}'
    border: '1px solid {colors.field-border}'
    radius: '{rounded.DEFAULT}'
    minHeight: 44px
  button-danger:
    background: '{colors.danger}'
    foreground: '{colors.on-danger}'
    radius: '{rounded.DEFAULT}'
  card:
    background: '{colors.surface}'
    border: '1px solid {colors.border}'
    radius: '{rounded.DEFAULT}'
    padding: '{spacing.4}'
    shadow: 'none'
  input:
    background: '{colors.background}'
    border: '1px solid {colors.field-border}'
    radius: '{rounded.sm}'
    minHeight: 44px
  focus-ring:
    outline: '2px solid {colors.accent}'
    offset: 2px
  progress-step:
    bar-upcoming: '{colors.field-border}'
    bar-done: '{colors.accent}'
    bar-active: '{colors.accent}'
    bar-height: 4px
    bar-height-active: 8px
    label: '{typography.small}'
    label-active-weight: '650'
    minHeight: 44px
  link:
    foreground: '{colors.accent}'
    textDecoration: underline
    underlineOffset: 3px
  button-busy:
    background: '{colors.accent}'
    foreground: '{colors.on-accent}'
    cursor: progress
  ai-label:
    foreground: '{colors.text-muted}'
    border: '1px solid {colors.border}'
    radius: '{rounded.full}'
    typography: '{typography.tag}'
  requirement-match:
    icon: '✓'
    foreground: '{colors.match}'
    background: '{colors.match-bg}'
  requirement-missing:
    icon: '!'
    foreground: '{colors.missing}'
    background: '{colors.missing-bg}'
  keyword-chip:
    radius: '{rounded.full}'
    border: '1px solid {colors.border}'
  keyword-chip-missing:
    border: '1px dashed {colors.missing}'
    foreground: '{colors.missing}'
  test-mode-banner:
    background: '{colors.info-bg}'
    foreground: '{colors.text}'
  done-mark:
    background: '{colors.accent}'
    foreground: '{colors.on-accent}'
    size: 64px
---

## Brand & Style

Appen skal få Emma til å føle at **det er lett å lage søknaden, og at hun ikke må streve for å få den ferdig**. Uttrykket er rolig, ryddig og litt mer seriøst enn vennlig. Det er en hjelper hun kan stole på, ikke en leken app. Henrik plasserte appen på 2 av 5 på alle tre skalaene: seriøs ↔ vennlig, luftig ↔ kompakt og nøytral ↔ fargerik.

Retningen heter **«C dempet»** og ble valgt i andre runde blant designretningene ([runde 1](.working/directions-1.html), [runde 2](.working/directions-2.html)). Den har den blågrønne fargen fra «Mykt kort», men flate flater med tynne kantlinjer, som i «Rolig blå». Retningen «Stram» (svart-hvitt med skarpe hjørner) ble avvist.

Appen bygges med Django-maler og egen CSS i `static/css/`, uten UI-rammeverk og uten ressurser fra nettet (arkitekturen, AD-15). Alle verdiene her blir CSS-variabler på `:root`.

## Colors

Det finnes én aksentfarge og to statusfarger. Resten er nøytralt.

- **Blågrønn aksent (`#1F7A75` lys / `#5CC2BB` mørk)** er appens farge. Den brukes på hovedknapper, fullførte steg i fremdriftslinjen, lenker, fokusring og ✓-merket når utkastet er klart (steg 4). Den brukes ikke på flater eller til dekor.
- **Matcher (`#23784A` på `#E2F3EA`)** brukes bare på krav og nøkkelord som finnes i CV-en.
- **Mangler (`#9A5800` på `#FCEFD9`)** brukes bare på krav og nøkkelord som ikke finnes i CV-en. Fargen er **oransje, ikke rød**. Noe som mangler, er en mulighet, ikke en feil, og rødt er reservert for farlige handlinger.
- **Fare (`#B3261E`)** brukes bare på «Slett mine dokumenter» og «Slett konto» og på feilmeldinger i skjemaer.
- **Infoflate (`#E3F1F0`)** brukes på testmodus-banneret og personvernmerknaden. Teksten på infoflaten har alltid fargen `{colors.text}`, aldri aksentfargen, fordi blågrønn på infoflate gir for lav kontrast (4,4:1).
- **Nøytrale:** `background` og `surface` (kortene) har nesten samme farge. Det er `border` som skiller dem. `field-border` er en mørkere kant som bare brukes på skjemafelt og sekundærknapper. Den må ha 3:1 mot bakgrunnen (WCAG 1.4.11).

**Mørk modus** følger enheten (`prefers-color-scheme`), og det finnes ingen bryter. Hvert token har en `-dark`-variant.

**Kontrast, sjekket 2026-11-12 (WCAG 2.1 AA):**

| Par | Lys | Mørk |
|---|---|---|
| Tekst på bakgrunn | 14,7 | 15,0 |
| Dempet tekst på kort | 5,2 | 6,4 |
| Tekst på aksentknapp | 5,1 | 8,8 |
| Matcher-tekst på matcher-flate | 4,7 | 6,5 |
| Mangler-tekst på mangler-flate | 4,9 | 6,5 |
| Feltkant mot kort | 3,3 | 3,4 |
| Fare-tekst på bakgrunn | 6,5 | 10,6 |
| Tekst og lenker på infoflate | 12,7 | 11,6 |
| Aksent (lenke, fokusring) på bakgrunn | 5,1 | 8,5 |
| Aksent (lenke, fokusring) på kort | 4,8 | 7,6 |
| Mangler-tekst i brikke på hvit | 5,6 | 6,5 |
| Kommende steg i fremdriftslinjen (`field-border`) | 3,5 | 3,8 |

Kontrasten er regnet ut med WCAG-formelen for relativ luminans i et lite Python-skript, og kontrollert på nytt av tilgjengelighetsreviewen ([review-tilgjengelighet.md](review-tilgjengelighet.md)). Mangler-fargen ble justert fra `#A65F00` (4,3:1) til `#9A5800`, og `field-border` ble lagt til etter første sjekk.

**Lenker er alltid understreket.** Aksentfargen har bare 2,9:1 mot vanlig tekst (1,8:1 i mørk modus), så farge alene kan ikke skille lenker fra teksten (WCAG 1.4.1). På infoflaten har lenker tekstfarge og understrek, aldri aksentfarge.

**Tvungne farger** (`forced-colors: active`): strekene i fremdriftslinjen, nøkkelordmåleren og ikonsirklene får `border: 1px solid CanvasText`, og fokus vises med `outline`, ikke `box-shadow`.

## Typography

Appen bruker **systemskrift**: San Francisco på Apple, Segoe UI på Windows og Roboto på Android. Den ser naturlig ut på hver enhet, laster ingen filer og er lett å lese på norsk med æ, ø og å.

Rollene er `heading` (stegtittel, én per side), `heading-sm` (korttitler), `body`, `small` (begrunnelser og hjelpetekst), `label` (feltetiketter), `tag` («Matcher» og «Mangler») og `letter` (brevteksten). Brevet har ekstra linjeavstand, så det er behagelig å lese gjennom og rette i steg 4. Størrelsene er Claudes forslag, og Henrik godtok dem 2026-11-12. Tokenene er oppgitt i px for lesbarhetens skyld, men skrives i `rem` i CSS (16 px = 1 rem), slik at brukerens egen standard skriftstørrelse følges. Tekst i skjemafelt er aldri mindre enn 16 px, slik at iOS ikke zoomer inn.

## Layout & Spacing

**Én smal midtkolonne på alle skjermer**, maks `{spacing.content-max}` (720 px). Oppsettet er det samme på mobil og PC. PC-en får bare mer luft rundt kolonnen. Det finnes ingen flerkolonne-oppsett. Sidemargen er `{spacing.gutter-mobile}` (16 px) på mobil og `{spacing.gutter-desktop}` (24 px) fra 600 px og oppover. Siden skal virke fra 360 px uten vannrett rulling (NFR-7).

Avstandene følger en 4-basert skala. Det er 16 px inni kort, 16 px mellom kort og 24–32 px mellom seksjoner. Siden er luftig, men ikke tom.

## Elevation & Depth

**Flatt.** Det finnes ingen skygger. Lag skilles med tynne kantlinjer (`{colors.border}`) og den svake fargeforskjellen mellom `background` og `surface`. Det eneste som «løfter seg», er ✓-merket når utkastet er klart (steg 4), og det gjør det med farge og størrelse, ikke med skygge.

## Shapes

- `{rounded.DEFAULT}` (10 px) brukes på kort og knapper.
- `{rounded.sm}` (6 px) brukes på skjemafelt.
- `{rounded.full}` brukes på nøkkelord-brikker, «Matcher»- og «Mangler»-merker og ✓/!-ikonene.

Middels runde hjørner gjør appen vennlig uten at den blir leken.

## Components

- **Topplinje.** Navnet på appen står til venstre. «Min konto» (lenke) og «Logg ut» (en knapp som ser ut som en lenke) står til høyre, også på mobil. Begge er understreket og har padding som gir minst 44 px trykkflate. Linjen har `{colors.surface}` med en kantlinje under.
- **Testmodus-banner.** Det står over topplinjen på alle sider i testmodus (FR-9), med `{colors.info-bg}` og vanlig tekst.
- **Fremdriftslinje.** Fire like brede celler, én per steg. Hver celle har en strek øverst og stegnavnet under i `small`. Navnet er kort på mobil («CV», «Annonse», «Analyse», «Søknad») og fullt fra 600 px.
  - Fullførte steg: strek i `{colors.accent}` og navnet som understreket lenke.
  - Aktivt steg: strek i `{colors.accent}` på 8 px og navnet i halvfet skrift.
  - Kommende steg: strek i `{colors.field-border}` og navnet i `{colors.text-muted}`.
  - Hele cellen er trykkflaten og er minst 44 px høy.
  - Statusen vises med tykkelse og skriftvekt i tillegg til farge, ikke med gjennomsiktighet.
- **Hovedknapp.** Fylt med aksentfargen og minst 44 px høy. Det er én hovedknapp per steg, nederst til høyre ved siden av «Tilbake». **Mens den venter** («Jobber …») beholder den fargene sine, viser en liten roterende indikator og får markøren `progress`. Den blir ikke dempet, slik at teksten fortsatt er lesbar.
- **Lenke.** Aksentfarge, alltid understreket, med 3 px avstand til streken.
- **KI-merke.** En liten pille øverst til høyre i et kort, i `tag`-typografi, dempet tekst og med tynn kant: «Laget av KI» på kort med KI-tekst, og «Telt automatisk» på nøkkelordkortet. Den skal synes uten å konkurrere med innholdet.
- **KI-varsel.** En linje med ⚠ og `{colors.missing-bg}` som bakgrunn, og teksten i `{colors.text}`. Den står øverst i steg 3 og over brevet i steg 4.
- **Sekundærknapp.** Hvit med `field-border`.
- **Fareknapp.** Rød fyll. Den brukes bare i bekreftelsen av sletting.
- **Kort.** `surface` med 1 px kantlinje og 10 px hjørner, uten skygge. Korttittelen står i `heading-sm` eller `label`.
- **Kravrad (gap-analyse).** Et rundt ikon på 22 px (✓ eller !), kravet i fet skrift, merket «Matcher» eller «Mangler», og under det begrunnelsen i `small` og `text-muted`. Radene skilles med tynne linjer.
- **Nøkkelord-brikke.** Pilleformet. Nøkkelord som mangler, har stiplet kant og mangler-farge, så forskjellen synes også uten farge.
- **Nøkkelordmåler.** En stolpe på 8 px med andelen funnet i aksentfargen og teksten «7 av 10 funnet» over.
- **Skjemafelt.** 1 px `field-border`, 6 px hjørner og minst 44 px høyde. Etiketten står over feltet. Feilmeldingen står under feltet i fare-farge, med et ikon.
- **Fokusring.** 2 px aksentfarge med 2 px avstand, på alt som kan få fokus.
- **Utkast-merke.** En sirkel på 64 px i aksentfargen med et hvitt ✓, og «Utkastet er klart» i `heading` under. Den skaleres kort inn (cirka 300 ms) og står stille ved `prefers-reduced-motion`.
- **Brev.** Et redigerbart tekstfelt med `letter`-typografi, `field-border`, 6 px hjørner og høyde som passer brevet (minst 16 linjer). KI-varselet står over feltet.

Nøkkelskjermene ligger i [`mockups/`](mockups/): [steg 1](mockups/key-steg1-testmodus.html), [steg 2](mockups/key-steg2-annonse.html), [steg 3](mockups/key-steg3-analyse.html) og [steg 4](mockups/key-steg4-soknad.html). Dokumentet her går foran mockupene hvis de er uenige.

## Do's and Don'ts

| Gjør | Ikke gjør |
|---|---|
| Bruk aksentfargen bare til handling, fremdrift og «ferdig» | Bruke aksentfargen på store flater eller til dekor |
| Vis «Matcher» og «Mangler» med symbol **og** tekst | Bruke bare farge til å skille dem |
| Bruk oransje for det som mangler | Bruke rødt for det som mangler (rødt er for sletting og feil) |
| Skill lag med kantlinjer | Bruke skygger |
| Hold én midtkolonne på maks 720 px | Bruke flerkolonne-oppsett på PC |
| Bruk systemskrift | Laste skrift eller ikoner fra nettet |
| Ha én hovedknapp per steg | Ha flere fylte knapper som konkurrerer |
| Understrek alle lenker | Skille lenker fra tekst bare med farge |
| Merk det KI har laget («Laget av KI») | La KI-tekst og tellinger fra koden se like sikre ut |
| Vis status med form og tekst i tillegg til farge | Bruke gjennomsiktighet som eneste statusmarkering |
