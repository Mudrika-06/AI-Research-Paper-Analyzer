from io import BytesIO
from docx import Document


def export_docx(title, content):

    document = Document()

    document.add_heading(
        title,
        level=0
    )

    for line in content.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line.startswith("# "):

            document.add_heading(
                line[2:],
                level=1
            )

        elif line.startswith("## "):

            document.add_heading(
                line[3:],
                level=2
            )

        elif line.startswith("- "):

            document.add_paragraph(
                line[2:],
                style="List Bullet"
            )

        else:

            document.add_paragraph(line)

    output = BytesIO()

    document.save(output)

    return output.getvalue()
