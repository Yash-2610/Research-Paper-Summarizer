import streamlit as st
from pypdf import PdfReader
from evaluation import evaluate_response
from graph import graph
import time

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Research Paper Summarizer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Research Paper Summarizer")

st.markdown("""
### AI Research Paper Summarizer

This application can:

- ✅ Upload Research Papers
- ✅ Summarize Papers
- ✅ Answer Questions
- ✅ Extract Keywords
- ✅ Uses LangGraph
- ✅ Uses RAG
- ✅ Stores Conversation History
""")

# -------------------------------------------------
# Session Memory
# -------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------------------------
# Upload PDF
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.success("✅ PDF Uploaded Successfully")

    st.subheader("Extracted Text")

    st.text_area(
        "Paper Content",
        text,
        height=250
    )

    st.success("✅ Document Ready")

    st.divider()

    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    st.header("📑 Generate Summary")

    if st.button("Generate Summary"):

        state = {

            "text": text,

            "question": "",

            "summary": "",

            "answer": "",

            "keywords": "",

            "vector_store": None,

            "retrieved_chunks": [],

            "evaluation": "",

            "action": "summary"

        }

        with st.spinner("Generating Summary..."):
            start = time.time()

            try:
                result = graph.invoke(state)

                end = time.time()

                st.success("Summary Generated Successfully!")
                st.success(f"⏱ Execution Time: {end-start:.2f} seconds")

                st.write(result["summary"])

                evaluation = evaluate_response(result["summary"])

                st.subheader("📊 Response Evaluation")
                st.write(evaluation)

                st.session_state.history.append({
                    "Action": "Summary",
                    "Output": result["summary"]
                })

            except Exception as e:
                st.error(f"Error: {e}")

    st.divider()
    # -------------------------------------------------
    # QUESTION ANSWERING
    # -------------------------------------------------

    st.header("❓ Ask Questions")

    question = st.text_input(
        "Enter your question about the paper"
    )

    if st.button("Get Answer"):

        if question.strip() != "":

            state = {

                "text": text,

                "question": question,

                "summary": "",

                "answer": "",

                "keywords": "",

                "vector_store": None,

                "retrieved_chunks": [],

                "evaluation": "",

                "action": "qa"

            }

            with st.spinner("Searching..."):
                start = time.time()

                try:
                    result = graph.invoke(state)

                    end = time.time()

                    st.success("Answer Generated Successfully!")
                    st.success(f"⏱ Execution Time: {end-start:.2f} seconds")

                    st.write(result["answer"])
                    evaluation = evaluate_response(result["answer"])

                    st.subheader("📊 Response Evaluation")
                    st.write(evaluation)

                    st.subheader("📊 Response Evaluation")
                    st.write(result["evaluation"])

                    st.session_state.history.append({
                        "Question": question,
                        "Answer": result["answer"]
                    })

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")

    st.divider()

    # -------------------------------------------------
    # KEYWORD EXTRACTION
    # -------------------------------------------------

    st.header("🔑 Extract Keywords")

    if st.button("Extract Keywords"):

        state = {

            "text": text,

            "question": "",

            "summary": "",

            "answer": "",

            "keywords": "",

            "vector_store": None,

            "retrieved_chunks": [],

            "evaluation": "",

            "action": "keywords"

        }

        with st.spinner("Extracting Keywords..."):
            start = time.time()
            try:
                result = graph.invoke(state)
                end = time.time()

                st.success("Keywords Extracted Successfully!")
                st.success(f"⏱ Execution Time: {end-start:.2f} seconds")

                st.write(result["keywords"])
                evaluation = evaluate_response(result["keywords"])

                st.subheader("📊 Response Evaluation")
                st.write(evaluation)

                st.session_state.history.append({
                    "Action": "Keywords",
                    "Output": result["keywords"]
                })
            except Exception as e:
                st.error(f"Error: {e}")


    

    st.divider()

    # -------------------------------------------------
    # CONVERSATION HISTORY
    # -------------------------------------------------

    st.header("🧠 Conversation History")

    if st.button("Show Conversation History"):

        if len(st.session_state.history) == 0:

            st.info("No conversation history available.")

        else:

            for item in st.session_state.history:

                st.write(item)

                