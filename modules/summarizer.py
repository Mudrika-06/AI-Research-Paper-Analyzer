
from modules.text_preprocessor import setup_nltk

setup_nltk()

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.utils import get_stop_words


def summarize_text(text, sentence_count=5):
    """Generate an extractive summary from document text."""

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
        return f"Summary generation failed: {error}"


# Backward-compatible function name
def generate_summary(text, sentence_count=5):
    return summarize_text(text, sentence_count)
