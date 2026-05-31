import os
import tempfile

import cairosvg
from pypdf import PdfWriter


def from_svg_to_pdf(
    list_svg_path: list,
    pdf_name: str,
    save_path: str
):
    os.makedirs(save_path, exist_ok=True)

    output_pdf = os.path.join(
        save_path,
        f"{pdf_name}.pdf"
    )

    writer = PdfWriter()
    temp_files = []

    try:
        for svg_path in list_svg_path:
            temp_pdf = tempfile.NamedTemporaryFile(
                suffix=".pdf",
                delete=False
            )
            temp_pdf.close()

            # covert one .svg to one .pdf
            cairosvg.svg2pdf(
                url=svg_path,
                write_to=temp_pdf.name
            )

            temp_files.append(temp_pdf.name)
            writer.append(temp_pdf.name)

        with open(output_pdf, "wb") as f:
            writer.write(f)

        return output_pdf

    finally:
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)