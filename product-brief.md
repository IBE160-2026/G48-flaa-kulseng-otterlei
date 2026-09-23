# Product Brief: AI CV & Job Application Assistant

**Gutta krutt** — IBE160 Programmering med KI, Høgskolen i Molde, høst 2026
Team: Ole A. Flaa, Henrik O. Kulseng, Haakon Remen Otterlei
Vanskelighetsgrad (fra emnets idéliste): 🟠 Middels

## Executive Summary

AI CV & Job Application Assistant er et verktøy som hjelper studenter med å lage skreddersydde jobbsøknader basert på egen CV og en konkret stillingsannonse. Verktøyet leser CV-en og annonsen, identifiserer hvilke kvalifikasjoner som matcher og hvilke som mangler (gap-analyse), og genererer — etter brukerens eget valg — enten et komplett utkast til søknadsbrev eller konkrete forbedringsforslag studenten selv skriver inn. I tillegg gir det CV-forbedringsforslag og ATS-optimaliseringstips, og eksporterer resultatet i flere filformater. Prosjektet bruker ekte kall til en språkmodell (LLM-API), og gir dermed gruppa en praktisk erfaring med hvordan AI faktisk brukes i rekruttering — samtidig som verktøyet er nyttig for målgruppen selv: norske studenter som søker sommerjobb, deltidsjobb eller sin første heltidsstilling.

## The Problem

Å skrive en god, skreddersydd søknad for hver enkelt stilling er tidkrevende. Mange studenter ender opp med å (a) sende samme generiske brev til alle stillinger, eller (b) bruke generiske AI-chatboter som produserer søknader fulle av floskler rekrutterere i dag kjenner igjen umiddelbart. Samtidig vet mange studenter for lite om hvordan automatiserte rekrutteringssystemer (ATS) faktisk filtrerer søknader, og får avslag uten å forstå hvorfor — de mangler innsikt i hvilke konkrete kvalifikasjoner som faktisk mangler for en gitt stilling.

## The Solution

Studenten laster opp CV (PDF/DOC/TXT), limer inn teksten fra en konkret stillingsannonse, og kan valgfritt laste opp tidligere søknader slik at verktøyet lærer brukerens egen skrivestil. Brukeren angir også ønskede nøkkelord, samt språk (norsk/engelsk) og tone/stilnivå (f.eks. formell/uformell). Verktøyet:

1. Kjører en gap-analyse: sammenligner CV mot annonsens krav og viser konkret hva som matcher og hva som mangler.
2. Genererer — etter brukerens valg — et fullt utkast til søknadsbrev i valgt språk og stil (informert av tidligere søknader), eller kun konkrete forslag/forbedringspunkter studenten selv skriver inn.
3. Gir CV-forbedringsforslag basert på annonsen.
4. Gir ATS-optimaliseringstips (nøkkelord, formatering) for å øke sjansen for å komme gjennom automatiske filtre.

Resultatet kan lastes ned i flere formater (PDF, DOC, Markdown).

## What Makes This Different

Vi er ærlige på at hver enkelt del av dette allerede finnes hos etablerte aktører: Jobscan og lignende dekker ATS-scoring, Rezi/Kickresume/Enhancv dekker AI-generert søknadsbrev, og LinkedIns eget "Apply Assistant" tilbyr lignende funksjonalitet direkte i søkeflyten. Vi bygger ingen unik teknologi.

Vårt bidrag er (a) å samle gap-analyse, brevgenerering, CV-forbedring og ATS-tips i én sammenhengende flyt tilpasset norske studenter og det norske arbeidsmarkedet, og (b) å la brukeren selv styre hvor mye AI skal generere versus foreslå — i stedet for å tvinge et ferdig, generisk brev på studenten. Vi legger også vekt på at forslagene skal bygge på det som faktisk står i CV-en og ikke dikte opp erfaring — et kjent problem hos flere konkurrerende verktøy.

## Who This Serves

Primær målgruppe: norske studenter, uavhengig av studieretning, som søker sommerjobb, deltidsjobb eller sin første heltidsstilling etter studiene. De har typisk en CV, men mangler tid, erfaring eller innsikt til å skreddersy hver søknad godt, og vet ofte ikke hvorfor de siles ut av automatiske systemer.

## Success Criteria

Prosjektet er en suksess når vi har en fungerende end-to-end demo hvor en reell CV og en reell stillingsannonse kan lastes inn, og verktøyet — via ekte LLM-API-kall — leverer alle fire kjernefunksjoner (gap-analyse, søknadsbrev/forslag, CV-forbedringsforslag, ATS-tips) i en sammenhengende brukerflyt, med eksport til minst to filformater.

## Scope

**I V1:**

- Opplasting av CV (PDF/DOC/TXT) og innliming av stillingsannonsetekst
- Valgfri opplasting av tidligere søknader, brukt til å lære brukerens skrivestil
- Gap-analyse mot annonsen
- Søknadsbrev-generering med brukervalg mellom fullt utkast og forslag/punkter, samt valg av språk (norsk/engelsk) og tone/stilnivå
- CV-forbedringsforslag
- ATS-optimaliseringstips
- Eksport i flere formater (PDF, DOC, Markdown)
- Innlogging og kryptert lagring av personopplysninger/dokumenter (reell implementasjon, ikke forenklet)

**Utenfor omfang (V1):**

- Automatisk innhenting av stillingsannonser fra eksterne plattformer (f.eks. Finn.no, LinkedIn) — brukeren limer inn annonseteksten selv
- Støtte for andre språk enn norsk og engelsk
- Betalings-/kjøpsfunksjonalitet
- Automatisk innsending av søknader ("auto-apply")

**Risiko å være bevisst på:** Gruppa har valgt bred dekning av alle fire funksjoner fremfor å gå smalt og dypt på én. Det gir en mer komplett demo, men betyr at hver enkelt funksjon sannsynligvis blir enklere implementert enn om vi hadde valgt ett fokusområde. Dette er en bevisst avveining gitt tidsrammen på ett semester og en gruppe på tre.

## Sikkerhet og personvern

Verktøyet håndterer personopplysninger og personlige dokumenter (CV, søknadsbrev), og krever derfor ordentlig innlogging og kryptert lagring — ikke en forenklet skoleversjon. Dette inkluderer sikker autentisering, kryptering av lagrede dokumenter, og en tydelig policy for hvor lenge data lagres og hvordan de kan slettes. Siden prosjektet bruker en ekstern LLM-API, må gruppa også ta stilling til hva som faktisk sendes til API-leverandøren, og sikre at dette er i tråd med god personvernpraksis.

## Vision

Om konseptet videreutvikles utover kurset, kan det vokse fra et generelt studentverktøy til noe tilpasset spesifikt for norske høgskoler/universiteter — for eksempel integrert med karriereveiledning ved Høgskolen i Molde, eller utvidet med tilbakemelding fra faktiske rekrutterere. For kursets del er målet et solid, fungerende verktøy som viser hvordan AI kan brukes ansvarlig og presist i en rekrutteringskontekst.
