
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from modules.text_preprocessor import get_sentences


def summarize_text(text, sentence_count=5):
    """Generate an extractive summary using TF-IDF sentence scoring."""

    if not text or not text.strip():
        return "No readable text found in the research paper."

    sentences = get_sentences(text)

    if not sentences:
        return text[:1500]

    if len(sentences) <= sentence_count:
        return " ".join(sentences)

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        matrix = vectorizer.fit_transform(sentences)

        # Score each sentence by its average TF-IDF weight.
        scores = matrix.sum(axis=1).A1

        # Give a small preference to sentences with useful length.
        adjusted_scores = []

        for sentence, score in zip(sentences, scores):
            word_count = len(sentence.split())

            if word_count < 5:
                score *= 0.5
            elif word_count > 60:
                score *= 0.85

            adjusted_scores.append(score)

        ranked_indices = sorted(
            range(len(sentences)),
            key=lambda index: adjusted_scores[index],
            reverse=True
        )

        selected_indices = sorted(
            ranked_indices[:max(1, sentence_count)]
        )

        summary = " ".join(
            sentences[index] for index in selected_indices
        )

        return summary if summary.strip() else "Unable to generate summary."

    except ValueError:
        # Fallback for text that cannot be vectorized.
        return " ".join(sentences[:sentence_count])

    except Exception as error:
        return f"Summary generation failed: {error}"


# Support both names used by earlier versions of the app.
def generate_summary(text, sentence_count=5):
    return summarize_text(text, sentence_count)
