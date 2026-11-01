import streamlit as st
import pandas as pd
from modules.text_preprocessor import setup_nltk

setup_nltk()

from modules.pdf_processor import (
    extract_pdf_pages,
    get_document_statistics
)

from modules.summarizer import summarize_text

from modules.keyword_extractor import extract_keywords

from modules.question_answering import answer_question

from modules.quiz_generator import generate_quiz

from modules.notes_generator import generate_notes

from modules.paper_comparator import compare_papers

from utils.export_utils import export_docx


st.set_page_config(
    page_title="ResearchLens AI",
    page_icon="📚",
    layout="wide"
)


# SESSION STATE

if "documents" not in st.session_state:
    st.session_state.documents = {}

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "notes" not in st.session_state:
    st.session_state.notes = ""


# SIDEBAR

with st.sidebar:

    st.title("📚 ResearchLens AI")

    st.caption(
        "AI-Powered Research Paper Analyzer"
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Upload Documents",
            "Smart Summarizer",
            "Chat with PDF",
            "NLP Analysis",
            "Quiz Generator",
            "Study Notes",
            "Compare Papers"
        ]
    )

    st.divider()

    st.success("100% API-Free NLP Application")

    st.caption(
        "Local processing • No paid AI API"
    )


st.title("ResearchLens AI")

st.caption(
    "Analyze research papers, extract knowledge "
    "and generate academic study material."
)


# HELPER FUNCTIONS

def get_active_document():

    name = st.session_state.get(
        "active_document"
    )

    return st.session_state.documents.get(
        name
    )


# DASHBOARD

if page == "Dashboard":

    documents = st.session_state.documents

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Documents",
        len(documents)
    )

    col2.metric(
        "Total Pages",
        sum(
            d["stats"]["pages"]
            for d in documents.values()
        )
    )

    col3.metric(
        "Total Words",
        sum(
            d["stats"]["words"]
            for d in documents.values()
        )
    )

    st.subheader("Welcome to ResearchLens AI")

    st.write(
        """
        Your intelligent research workspace.

        Upload research papers and use NLP techniques
        to summarize, analyze, compare and understand
        academic documents.
        """
    )

    st.info(
        "Start by uploading a research paper from "
        "the Upload Documents section."
    )


# UPLOAD DOCUMENTS

elif page == "Upload Documents":

    st.subheader("Upload Research Papers")

    uploaded_files = st.file_uploader(
        "Select PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for uploaded_file in uploaded_files:

            if uploaded_file.name in st.session_state.documents:
                continue

            if uploaded_file.size > 15 * 1024 * 1024:

                st.error(
                    f"{uploaded_file.name} exceeds 15 MB."
                )

                continue

            try:

                with st.spinner(
                    f"Processing {uploaded_file.name}..."
                ):

                    pages = extract_pdf_pages(
                        uploaded_file.getvalue()
                    )

                    full_text = "\n".join(
                        p["text"] for p in pages
                    )

                    if len(full_text.split()) > 150000:

                        st.warning(
                            "Document exceeds the recommended "
                            "word limit."
                        )

                        continue

                    stats = get_document_statistics(
                        pages
                    )

                    st.session_state.documents[
                        uploaded_file.name
                    ] = {
                        "pages": pages,
                        "text": full_text,
                        "stats": stats
                    }

                    st.session_state.active_document = (
                        uploaded_file.name
                    )

                st.success(
                    f"{uploaded_file.name} processed successfully."
                )

            except Exception as error:

                st.error(str(error))


    if st.session_state.documents:

        st.subheader("Your Document Library")

        selected = st.selectbox(
            "Select active document",
            list(st.session_state.documents.keys())
        )

        st.session_state.active_document = selected

        doc = st.session_state.documents[selected]

        a, b, c = st.columns(3)

        a.metric(
            "Pages",
            doc["stats"]["pages"]
        )

        b.metric(
            "Words",
            doc["stats"]["words"]
        )

        c.metric(
            "Characters",
            doc["stats"]["characters"]
        )

        with st.expander("Preview document text"):

            st.write(
                doc["text"][:5000]
            )


# SMART SUMMARIZER

elif page == "Smart Summarizer":

    doc = get_active_document()

    if doc is None:

        st.warning(
            "Please upload a PDF first."
        )

    else:

        st.subheader("Research Paper Summarizer")

        depth = st.selectbox(
            "Summary depth",
            [
                "Short",
                "Medium",
                "Detailed"
            ]
        )

        sentence_count = {
            "Short": 5,
            "Medium": 10,
            "Detailed": 20
        }[depth]

        if st.button(
            "Generate Summary",
            type="primary"
        ):

            with st.spinner(
                "Analyzing research paper..."
            ):

                st.session_state.summary = (
                    summarize_text(
                        doc["text"],
                        sentence_count
                    )
                )

        if st.session_state.summary:

            st.markdown(
                st.session_state.summary
            )

            st.download_button(
                "Download Summary",
                st.session_state.summary,
                file_name="research_summary.txt"
            )

            st.download_button(
                "Download Word Document",
                export_docx(
                    "Research Paper Summary",
                    st.session_state.summary
                ),
                file_name="research_summary.docx"
            )


# CHAT WITH PDF

elif page == "Chat with PDF":

    doc = get_active_document()

    if doc is None:

        st.warning(
            "Upload a PDF first."
        )

    else:

        st.subheader("Ask Questions About Your Paper")

        question = st.text_input(
            "Enter your question"
        )

        if st.button("Find Answer"):

            if question.strip():

                with st.spinner(
                    "Searching document..."
                ):

                    answers = answer_question(
                        question,
                        doc["pages"]
                    )

                if answers:

                    st.success(
                        "Relevant information found."
                    )

                    for index, result in enumerate(
                        answers,
                        start=1
                    ):

                        with st.container(
                            border=True
                        ):

                            st.write(
                                f"**Result {index}**"
                            )

                            st.write(
                                result["answer"]
                            )

                            st.caption(
                                f"Page {result['page']} "
                                f"| Relevance: {result['score']}"
                            )

                else:

                    st.warning(
                        "No relevant information found."
                    )


# NLP ANALYSIS

elif page == "NLP Analysis":

    doc = get_active_document()

    if doc is None:

        st.warning(
            "Upload a PDF first."
        )

    else:

        st.subheader(
            "Natural Language Processing Analysis"
        )

        keywords = extract_keywords(
            doc["text"],
            top_n=20
        )

        st.markdown(
            "### Important Keywords"
        )

        if keywords:

            df = pd.DataFrame(
                keywords,
                columns=[
                    "Keyword",
                    "TF-IDF Score"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.bar_chart(
                df.set_index("Keyword")
            )

        else:

            st.info(
                "Not enough text for keyword extraction."
            )

        st.markdown(
            "### Document Statistics"
        )

        st.json(
            doc["stats"]
        )


# QUIZ GENERATOR

elif page == "Quiz Generator":

    doc = get_active_document()

    if doc is None:

        st.warning(
            "Upload a PDF first."
        )

    else:

        st.subheader(
            "Research Paper Quiz Generator"
        )

        count = st.slider(
            "Number of questions",
            3,
            15,
            5
        )

        if st.button(
            "Generate Quiz",
            type="primary"
        ):

            st.session_state.quiz = (
                generate_quiz(
                    doc["pages"],
                    count
                )
            )

        if st.session_state.get("quiz"):

            st.markdown(
                "### Test Your Knowledge"
            )

            for index, question in enumerate(
                st.session_state.quiz,
                start=1
            ):

                st.write(
                    f"**Q{index}.** "
                    f"{question['question']}"
                )

                with st.expander(
                    "Reveal Answer"
                ):

                    st.success(
                        question["answer"]
                    )


# STUDY NOTES

elif page == "Study Notes":

    doc = get_active_document()

    if doc is None:

        st.warning(
            "Upload a PDF first."
        )

    else:

        st.subheader(
            "Automatic Study Notes"
        )

        if st.button(
            "Generate Notes",
            type="primary"
        ):

            with st.spinner(
                "Preparing notes..."
            ):

                st.session_state.notes = (
                    generate_notes(
                        doc["text"]
                    )
                )

        if st.session_state.notes:

            st.markdown(
                st.session_state.notes
            )

            st.download_button(
                "Download Notes",
                st.session_state.notes,
                file_name="study_notes.txt"
            )

            st.download_button(
                "Download Word Notes",
                export_docx(
                    "Research Study Notes",
                    st.session_state.notes
                ),
                file_name="study_notes.docx"
            )


# COMPARE PAPERS

elif page == "Compare Papers":

    documents = st.session_state.documents

    if len(documents) < 2:

        st.info(
            "Upload at least two research papers."
        )

    else:

        st.subheader(
            "Research Paper Comparison"
        )

        names = list(documents.keys())

        paper1 = st.selectbox(
            "First paper",
            names,
            index=0
        )

        paper2 = st.selectbox(
            "Second paper",
            names,
            index=1
        )

        if paper1 != paper2:

            if st.button(
                "Compare Research Papers",
                type="primary"
            ):

                result = compare_papers(
                    documents[paper1]["text"],
                    documents[paper2]["text"]
                )

                st.markdown(
                    "### Common Keywords"
                )

                st.write(
                    result["common"]
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        "### Unique to Paper 1"
                    )

                    st.write(
                        result["paper1_unique"]
                    )

                with col2:

                    st.markdown(
                        "### Unique to Paper 2"
                    )

                    st.write(
                        result["paper2_unique"]
                    )

        else:

            st.warning(
                "Select two different documents."
            )


st.divider()

st.caption(
    "ResearchLens AI | Local NLP Processing | "
    "No External AI API Required"
)
