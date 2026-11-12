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
- En innrykket linje fortsetter i tekstkolonnen. Starter den med «- »,
  blir den et kulepunkt.
- En tom linje gir litt luft.
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

TIDSKOLONNE_MM = 32
DATOLINJE = re.compile(r"^(\S.*?)\s{2,}(\S.*)$")


def er_overskrift(linje: str) -> bool:
    return linje.isupper() and not linje.startswith(" ")


def lag_pdf(kilde: Path, ut: Path) -> None:
    linjer = kilde.read_text(encoding="utf-8").splitlines()
    navn, tittel, kontakt, *resten = linjer

    pdf = FPDF(format="A4")
    pdf.set_creation_date(FAST_DATO)
    pdf.set_title(f"CV – {navn}")
    pdf.set_margins(20, 20, 20)
    pdf.add_font("DejaVu", "", FONTER / "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", FONTER / "DejaVuSans-Bold.ttf")
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 20)
    pdf.cell(text=navn, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(text=tittel, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.cell(text=kontakt, align="L", new_x="LMARGIN", new_y="NEXT")

    bredde = pdf.epw
    tekstbredde = bredde - TIDSKOLONNE_MM

    for linje in resten:
        if not linje.strip():
            pdf.ln(2)
        elif er_overskrift(linje):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(text=linje.strip(), align="L", new_x="LMARGIN", new_y="NEXT")
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.l_margin + bredde, y)
            pdf.ln(1.5)
        elif linje.startswith(" "):
            tekst = linje.strip()
            if tekst.startswith("- "):
                tekst = "• " + tekst[2:]
            pdf.set_font("DejaVu", "", 10)
            pdf.set_x(pdf.l_margin + TIDSKOLONNE_MM)
            pdf.multi_cell(tekstbredde, 5, tekst, align="L", new_x="LMARGIN", new_y="NEXT")
        elif treff := DATOLINJE.match(linje):
            tid, tekst = treff.groups()
            pdf.set_font("DejaVu", "", 10)
            pdf.cell(TIDSKOLONNE_MM, 5, tid)
            pdf.set_font("DejaVu", "B", 10)
            pdf.multi_cell(tekstbredde, 5, tekst, align="L", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("DejaVu", "", 10)
            pdf.multi_cell(bredde, 5, linje.strip(), align="L", new_x="LMARGIN", new_y="NEXT")

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
