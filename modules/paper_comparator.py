from modules.keyword_extractor import extract_keywords


def compare_papers(text1, text2):

    keywords1 = extract_keywords(
        text1,
        top_n=20
    )

    keywords2 = extract_keywords(
        text2,
        top_n=20
    )

    set1 = {
        word for word, score in keywords1
    }

    set2 = {
        word for word, score in keywords2
    }

    common = set1.intersection(set2)

    unique1 = set1.difference(set2)

    unique2 = set2.difference(set1)

    return {
        "common": sorted(common),
        "paper1_unique": sorted(unique1),
        "paper2_unique": sorted(unique2)
    }
