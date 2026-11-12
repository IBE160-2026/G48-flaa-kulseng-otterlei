---
name: Søknadshjelpen (plassholder)
description: Visuell identitet for AI CV & Job Application Assistant. Rolig, ryddig og blågrønn, for norske studenter som skal skreddersy en søknad uten å streve. Egen CSS i Django-maler, uten UI-rammeverk.
status: draft
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
  danger: '#B3261E'        # [ANTAKELSE] ikke valgt i økta
  on-danger: '#FFFFFF'     # [ANTAKELSE]
  info-bg: '#E3F1F0'       # [ANTAKELSE] testmodus-banner og personvernmerknad
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
  danger-dark: '#F2B8B5'   # [ANTAKELSE]
  on-danger-dark: '#2A0E0C' # [ANTAKELSE]
  info-bg-dark: '#16302E'  # [ANTAKELSE]
typography:
  # Systemskrift. Ingen fontfiler i repoet.
  # Stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
  # Størrelsene er [ANTAKELSE] – ikke diskutert i økta.
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
    # Brevteksten i steg 5 og 6
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.65'
rounded:
  sm: 6px
  DEFAULT: 10px
  full: 9999px
spacing:
  # 4-basert skala [ANTAKELSE]
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
  progress-bar:
    track: '{colors.border}'
    done: '{colors.accent}'
    height: 4px
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

- **Blågrønn aksent (`#1F7A75` lys / `#5CC2BB` mørk)** er appens farge. Den brukes på hovedknapper, fullførte steg i fremdriftslinjen, lenker, fokusring og ✓-merket på «Ferdig». Den brukes ikke på flater eller til dekor.
- **Matcher (`#23784A` på `#E2F3EA`)** brukes bare på krav og nøkkelord som finnes i CV-en.
- **Mangler (`#9A5800` på `#FCEFD9`)** brukes bare på krav og nøkkelord som ikke finnes i CV-en. Fargen er **oransje, ikke rød**. Noe som mangler, er en mulighet, ikke en feil, og rødt er reservert for farlige handlinger.
- **Fare (`#B3261E`)** [ANTAKELSE] brukes bare på «Slett mine dokumenter» og «Slett konto» og på feilmeldinger i skjemaer.
- **Infoflate (`#E3F1F0`)** [ANTAKELSE] brukes på testmodus-banneret og personvernmerknaden. Teksten på infoflaten har alltid fargen `{colors.text}`, aldri aksentfargen, fordi blågrønn på infoflate gir for lav kontrast (4,4:1).
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

Mangler-fargen ble justert fra `#A65F00` (4,3:1) til `#9A5800`, og `field-border` ble lagt til etter sjekken.

## Typography

Appen bruker **systemskrift**: San Francisco på Apple, Segoe UI på Windows og Roboto på Android. Den ser naturlig ut på hver enhet, laster ingen filer og er lett å lese på norsk med æ, ø og å.

Rollene er `heading` (stegtittel, én per side), `heading-sm` (korttitler), `body`, `small` (begrunnelser og hjelpetekst), `label` (feltetiketter), `tag` («Matcher» og «Mangler») og `letter` (brevteksten). Brevet har ekstra linjeavstand, så det er behagelig å lese gjennom i steg 5. Størrelsene er [ANTAKELSE]. Brødtekst er aldri mindre enn 16 px på mobil, slik at iOS ikke zoomer inn i skjemafelt.

## Layout & Spacing

**Én smal midtkolonne på alle skjermer**, maks `{spacing.content-max}` (720 px). Oppsettet er det samme på mobil og PC. PC-en får bare mer luft rundt kolonnen. Det finnes ingen flerkolonne-oppsett. Sidemargen er `{spacing.gutter-mobile}` (16 px) på mobil og `{spacing.gutter-desktop}` (24 px) fra 600 px og oppover. Siden skal virke fra 360 px uten vannrett rulling (NFR-7).

Avstandene følger en 4-basert skala [ANTAKELSE]. Det er 16 px inni kort, 16 px mellom kort og 24–32 px mellom seksjoner. Siden er luftig, men ikke tom.

## Elevation & Depth

**Flatt.** Det finnes ingen skygger. Lag skilles med tynne kantlinjer (`{colors.border}`) og den svake fargeforskjellen mellom `background` og `surface`. Det eneste som «løfter seg», er ✓-merket på «Ferdig», og det gjør det med farge og størrelse, ikke med skygge.

## Shapes

- `{rounded.DEFAULT}` (10 px) brukes på kort og knapper.
- `{rounded.sm}` (6 px) brukes på skjemafelt.
- `{rounded.full}` brukes på nøkkelord-brikker, «Matcher»- og «Mangler»-merker og ✓/!-ikonene.

Middels runde hjørner gjør appen vennlig uten at den blir leken.

## Components

- **Topplinje.** Navnet på appen står til venstre. «Min konto» og «Logg ut» står som tekstlenker til høyre, også på mobil. Linjen har `{colors.surface}` med en kantlinje under.
- **Testmodus-banner.** Det står over topplinjen på alle sider i testmodus (FR-9), med `{colors.info-bg}` og vanlig tekst.
- **Fremdriftslinje.** Seks streker på 4 px. Fullførte steg er `{colors.accent}`, det aktive steget er aksentfargen med 50 % gjennomsiktighet, og kommende steg er `{colors.border}`. Under strekene står «Steg 4 av 6 · Analyse» i `small`.
- **Hovedknapp.** Fylt med aksentfargen og minst 44 px høy. Det er én hovedknapp per steg, nederst til høyre ved siden av «Tilbake».
- **Sekundærknapp.** Hvit med `field-border`.
- **Fareknapp.** Rød fyll. Den brukes bare i bekreftelsen av sletting.
- **Kort.** `surface` med 1 px kantlinje og 10 px hjørner, uten skygge. Korttittelen står i `heading-sm` eller `label`.
- **Kravrad (gap-analyse).** Et rundt ikon på 22 px (✓ eller !), kravet i fet skrift, merket «Matcher» eller «Mangler», og under det begrunnelsen i `small` og `text-muted`. Radene skilles med tynne linjer.
- **Nøkkelord-brikke.** Pilleformet. Nøkkelord som mangler, har stiplet kant og mangler-farge, så forskjellen synes også uten farge.
- **Nøkkelordmåler.** En stolpe på 8 px med andelen funnet i aksentfargen og teksten «7 av 10 funnet» over.
- **Skjemafelt.** 1 px `field-border`, 6 px hjørner og minst 44 px høyde. Etiketten står over feltet. Feilmeldingen står under feltet i fare-farge, med et ikon.
- **Fokusring.** 2 px aksentfarge med 2 px avstand, på alt som kan få fokus.
- **Ferdig-merke.** En sirkel på 64 px i aksentfargen med et hvitt ✓. Den skaleres kort inn (cirka 300 ms) og står stille ved `prefers-reduced-motion`.
- **Brev.** Står i et kort med `letter`-typografi og en varsellinje over: «KI kan gjøre feil – les gjennom før du sender».

Nøkkelskjermene vises i [`.working/directions-2.html`](.working/directions-2.html) (steg 4, «3 – C dempet»). Dokumentet her går foran mockupen hvis de er uenige.

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
