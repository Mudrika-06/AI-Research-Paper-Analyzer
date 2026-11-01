
import re


def clean_text(text):
    """Clean extracted text while preserving useful punctuation."""

    if not text:
        return ""

    text = str(text)
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_sentences(text):
    """Split text into sentences without requiring NLTK."""

    text = clean_text(text)

    if not text:
        return []

    # Split at sentence-ending punctuation followed by whitespace.
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 15
    ]


def tokenize_words(text):
    """Extract words from text."""

    if not text:
        return []

    return re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", text.lower())


def preprocess_text(text):
    """Basic text preprocessing for NLP analysis."""

    words = tokenize_words(clean_text(text))

    return " ".join(words)
