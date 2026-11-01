from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

from modules.text_preprocessor import clean_text


def summarize_text(text, sentence_count=10):

    text = clean_text(text)

    if not text:
        return "No text available."

    try:

        parser = PlaintextParser.from_string(
            text,
            Tokenizer("english")
        )

        summarizer = TextRankSummarizer()

        summary = summarizer(
            parser.document,
            sentence_count
        )

        if not summary:
            return "Not enough text to summarize."

        return "\n\n".join(
            str(sentence) for sentence in summary
        )

    except Exception as error:

        return f"Summary generation failed: {error}"
