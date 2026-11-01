import random

from modules.text_preprocessor import get_sentences


def generate_quiz(pages, count=5):

    all_sentences = []

    for page in pages:

        all_sentences.extend(
            get_sentences(page["text"])
        )

    candidates = [
        s for s in all_sentences
        if 8 <= len(s.split()) <= 30
    ]

    random.shuffle(candidates)

    questions = []

    for sentence in candidates:

        words = sentence.split()

        if len(words) < 8:
            continue

        target = max(
            range(len(words)),
            key=lambda i: len(words[i])
        )

        answer = words[target].strip(
            ".,!?;:"
        )

        if len(answer) < 5:
            continue

        words[target] = "________"

        question = " ".join(words)

        questions.append({
            "question": question,
            "answer": answer
        })

        if len(questions) >= count:
            break

    return questions
