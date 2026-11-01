from modules.text_preprocessor import setup_nltk

# Download tokenizer resources before importing/using Sumy
setup_nltk()

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.utils import get_stop_words


def generate_summary(text, sentence_count=5):

    if not text or not text.strip():
        return "No readable text found in the document."

    try:
        parser = PlaintextParser.from_string(
            text,
            Tokenizer("english")
        )

        summarizer = TextRankSummarizer()
        summarizer.stop_words = get_stop_words("english")

        summary_sentences = summarizer(
            parser.document,
            sentence_count
        )

        if not summary_sentences:
            return "Not enough text to generate a summary."

        return " ".join(str(sentence) for sentence in summary_sentences)

    except Exception as error:
        return f"Summary generation failed: {str(error)}"
