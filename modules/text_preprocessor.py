import re
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def setup_nltk():

    resources = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4"
    }

    for path, package in resources.items():

        try:
            nltk.data.find(path)

        except LookupError:

            try:
                nltk.download(
                    package,
                    quiet=True
                )
            except Exception:
                pass


def clean_text(text):

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    text = re.sub(
        r'[^\w\s.,!?;:()-]',
        ' ',
        text
    )

    return text.strip()


def get_sentences(text):

    setup_nltk()

    text = clean_text(text)

    try:

        return [
            s.strip()
            for s in sent_tokenize(text)
            if len(s.split()) > 3
        ]

    except LookupError:

        return [
            s.strip()
            for s in re.split(r'(?<=[.!?])\s+', text)
            if len(s.split()) > 3
        ]


def preprocess_text(text):

    setup_nltk()

    try:

        stop_words = set(
            stopwords.words("english")
        )

    except LookupError:

        stop_words = set()

    lemmatizer = WordNetLemmatizer()

    words = word_tokenize(
        clean_text(text).lower()
    )

    processed = []

    for word in words:

        if word.isalpha() and word not in stop_words:

            try:
                processed.append(
                    lemmatizer.lemmatize(word)
                )
            except LookupError:
                processed.append(word)

    return processed
