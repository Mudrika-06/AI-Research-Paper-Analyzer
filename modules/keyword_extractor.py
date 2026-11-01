
from sklearn.feature_extraction.text import TfidfVectorizer
from modules.text_preprocessor import clean_text


def extract_keywords(text, top_n=15):

    text = clean_text(text)

    if not text.strip():
        return []

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=3000
        )

        matrix = vectorizer.fit_transform([text])

        scores = matrix.toarray()[0]
        terms = vectorizer.get_feature_names_out()

        ranked = sorted(
            zip(terms, scores),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            {
                "keyword": term,
                "score": round(float(score), 4)
            }
            for term, score in ranked[:top_n]
        ]

    except ValueError:
        return []
