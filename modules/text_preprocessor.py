
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# NLTK resource directory
NLTK_DATA_DIR = "/tmp/nltk_data"

if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)


def setup_nltk():
    """Download required NLTK resources when missing."""

    import os
    os.makedirs(NLTK_DATA_DIR, exist_ok=True)

    resources = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }

    for resource_path, package in resources.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            try:
                nltk.download(
                    package,
                    download_dir=NLTK_DATA_DIR,
                    quiet=True
                )
            except Exception as error:
                print(f"NLTK download failed for {package}: {error}")


def clean_text(text):
    """Clean extracted PDF text."""

    if not text:
        return ""

    text = str(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'()\-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize_sentences(text):
    """Split text into sentences, with a regex fallback."""

    if not text:
        return []

    try:
        return nltk.sent_tokenize(text)
    except LookupError:
        return [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text)
            if sentence.strip()
        ]


def tokenize_words(text):
    """Split text into words."""

    if not text:
        return []

    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def preprocess_text(text, remove_stopwords=True, lemmatize=True):
    """Preprocess text for NLP analysis."""

    text = clean_text(text)
    words = tokenize_words(text)

    if remove_stopwords:
        try:
            stop_words = set(stopwords.words("english"))
            words = [word for word in words if word not in stop_words]
        except LookupError:
            pass

    if lemmatize:
        try:
            lemmatizer = WordNetLemmatizer()
            words = [lemmatizer.lemmatize(word) for word in words]
        except LookupError:
            pass

    return " ".join(words)
