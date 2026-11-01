from modules.summarizer import summarize_text
from modules.keyword_extractor import extract_keywords


def generate_notes(text):

    summary = summarize_text(
        text,
        sentence_count=12
    )

    keywords = extract_keywords(
        text,
        top_n=15
    )

    notes = f"""
# Research Paper Study Notes

## Overview

{summary}

## Important Keywords

"""

    for keyword, score in keywords:

        notes += (
            f"\n- {keyword.title()}"
        )

    notes += """

## Revision Tips

- Understand the research objective.
- Identify the methodology.
- Remember important findings.
- Review the limitations.
- Understand the conclusion.
"""

    return notes
