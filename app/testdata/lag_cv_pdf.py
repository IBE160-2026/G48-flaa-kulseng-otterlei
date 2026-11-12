"""Lager eksempel-CV-ene som PDF fra cv_kilde.txt (PRD §10, AD-6, AD-13).

Kjøres fra mappen app/:

    python testdata/lag_cv_pdf.py A

Skriptet leser testdata/eksempler/<par>/cv_kilde.txt og skriver
testdata/eksempler/<par>/cv.pdf. Teksten finnes bare i cv_kilde.txt, så
PDF-en lages på nytt når CV-en endres.

Krever fpdf2 (pip install fpdf2) til app/requirements.txt finnes.

Formatet på cv_kilde.txt:
- Linje 1 er navnet, linje 2 er tittelen og linje 3 er kontaktinformasjonen.
- En linje med bare store bokstaver er en overskrift, f.eks. «ERFARING».
- En linje som ikke er rykket inn og har to eller flere mellomrom, deles i
  en tidskolonne og en tekstkolonne, f.eks. «2024–nå    Kundeservice ...».
- En innrykket linje fortsetter i tekstkolonnen. Starter linjen (innrykket
  eller ikke) med «- », blir den et kulepunkt.
- En tom linje gir litt luft.
- To kolonner (eksempel C): linjene etter «[VENSTRE]» havner i en smal
  sidekolonne, og linjene etter «[HØYRE]» i hovedkolonnen.
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from fpdf import FPDF

APP_DIR = Path(__file__).resolve().parent.parent
EKSEMPLER = APP_DIR / "testdata" / "eksempler"
FONTER = APP_DIR / "eksport" / "fonter"

# Fast dato gjør at samme kilde alltid gir samme PDF, så git ikke ser endringer.
FAST_DATO = datetime(2026, 11, 12, tzinfo=timezone.utc)

MARG = 20
TIDSKOLONNE_MM = 32
SIDEKOLONNE_MM = 55
KOLONNEAVSTAND_MM = 10
DATOLINJE = re.compile(r"^(\S.*?)\s{2,}(\S.*)$")


def er_overskrift(linje: str) -> bool:
    return linje.isupper() and not linje.startswith(" ")


def kulepunkt(tekst: str) -> str:
    return "• " + tekst[2:] if tekst.startswith("- ") else tekst


def skriv_linjer(pdf: FPDF, linjer: list[str], tidskolonne: float) -> None:
    """Skriver linjene mellom venstre og høyre marg slik de er satt nå."""
    bredde = pdf.epw
    for linje in linjer:
        pdf.set_font("DejaVu", "", 10)
        if not linje.strip():
            pdf.ln(2)
        elif er_overskrift(linje):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(text=linje.strip(), new_x="LMARGIN", new_y="NEXT")
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.l_margin + bredde, y)
            pdf.ln(1.5)
        elif linje.startswith(" "):
            pdf.set_x(pdf.l_margin + tidskolonne)
            pdf.multi_cell(bredde - tidskolonne, 5, kulepunkt(linje.strip()),
                           align="L", new_x="LMARGIN", new_y="NEXT")
        elif tidskolonne and (treff := DATOLINJE.match(linje)):
            tid, tekst = treff.groups()
            pdf.cell(tidskolonne, 5, tid)
            pdf.set_font("DejaVu", "B", 10)
            pdf.multi_cell(bredde - tidskolonne, 5, tekst,
                           align="L", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.multi_cell(bredde, 5, kulepunkt(linje.strip()),
                           align="L", new_x="LMARGIN", new_y="NEXT")


def lag_pdf(kilde: Path, ut: Path) -> None:
    linjer = kilde.read_text(encoding="utf-8").splitlines()
    navn, tittel, kontakt, *resten = linjer

    pdf = FPDF(format="A4")
    pdf.set_creation_date(FAST_DATO)
    pdf.set_title(f"CV – {navn}")
    pdf.set_margins(MARG, MARG, MARG)
    pdf.set_auto_page_break(True, margin=MARG)
    pdf.add_font("DejaVu", "", FONTER / "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", FONTER / "DejaVuSans-Bold.ttf")
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 20)
    pdf.cell(text=navn, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(text=tittel, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.cell(text=kontakt, new_x="LMARGIN", new_y="NEXT")

    if "[VENSTRE]" not in resten:
        skriv_linjer(pdf, resten, TIDSKOLONNE_MM)
    else:
        start = resten.index("[VENSTRE]")
        skille = resten.index("[HØYRE]")
        venstre = resten[start + 1:skille]
        hoyre = resten[skille + 1:]
        topp = pdf.get_y() + 2

        # Grå bakgrunn bak sidekolonnen, slik mange CV-maler har.
        pdf.set_fill_color(238, 238, 238)
        pdf.rect(MARG - 4, topp, SIDEKOLONNE_MM + 8, pdf.h - MARG - topp, style="F")

        hoyre_x = MARG + SIDEKOLONNE_MM + KOLONNEAVSTAND_MM
        pdf.set_left_margin(MARG)
        pdf.set_right_margin(pdf.w - hoyre_x + KOLONNEAVSTAND_MM)
        pdf.set_xy(MARG, topp)
        skriv_linjer(pdf, venstre, 0)

        pdf.set_left_margin(hoyre_x)
        pdf.set_right_margin(MARG)
        pdf.set_xy(hoyre_x, topp)
        skriv_linjer(pdf, hoyre, 28)

    pdf.output(ut)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Bruk: python testdata/lag_cv_pdf.py <par>, f.eks. A")
    mappe = EKSEMPLER / sys.argv[1].upper()
    kilde = mappe / "cv_kilde.txt"
    if not kilde.exists():
        sys.exit(f"Fant ikke {kilde}")
    ut = mappe / "cv.pdf"
    lag_pdf(kilde, ut)
    print(f"Laget {ut.relative_to(APP_DIR)}")


if __name__ == "__main__":
    main()
