from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.text_preprocessor import get_sentences


def answer_question(
    question,
    pages,
    top_k=5
):

    sentences = []

    for page in pages:

        for sentence in get_sentences(
            page["text"]
        ):

            sentences.append({
                "text": sentence,
                "page": page["page"]
            })

    if not sentences:
        return []

    corpus = [
        question
    ] + [
        item["text"] for item in sentences
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:

        matrix = vectorizer.fit_transform(
            corpus
        )

        scores = cosine_similarity(
            matrix[0:1],
            matrix[1:]
        )[0]

        ranked = sorted(
            zip(scores, sentences),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, item in ranked[:top_k]:

            if score > 0:

                results.append({
                    "answer": item["text"],
                    "page": item["page"],
                    "score": round(
                        float(score), 3
                    )
                })

        return results

    except ValueError:

        return []
