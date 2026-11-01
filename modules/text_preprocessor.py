import os
import nltk

# Store NLTK data in a writable directory
NLTK_DATA_DIR = "/tmp/nltk_data"

os.makedirs(NLTK_DATA_DIR, exist_ok=True)

if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)


def setup_nltk():
    """Download required NLTK resources if they are missing."""

    resources = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }

    for resource_path, package_name in resources.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            try:
                success = nltk.download(
                    package_name,
                    download_dir=NLTK_DATA_DIR,
                    quiet=True
                )

                if not success:
                    print(f"Could not download NLTK resource: {package_name}")

            except Exception as error:
                print(f"NLTK download error ({package_name}): {error}")

    return True
    
