from sklearn.feature_extraction.text import TfidfVectorizer

from modules.text_preprocessor import clean_text


def extract_keywords(text, top_n=20):

    text = clean_text(text)

    if len(text.split()) < 5:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=3000
    )

    try:

        matrix = vectorizer.fit_transform(
            [text]
        )

        scores = matrix.toarray()[0]

        features = vectorizer.get_feature_names_out()

        results = sorted(
            zip(features, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return results[:top_n]

    except ValueError:

        return []
