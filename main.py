# main.py

import streamlit as st
from pdf_parser import extract_full_text_only
from pdf_labeler import label_pdf_content_markdown
from user_query import init_retrieval, answer_query_with_rag

# Session state setup
if "markdown_output" not in st.session_state:
    st.session_state.markdown_output = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="📄 RAG PDF Assistant", layout="wide")
st.title("📄 PDF Content Labeling + RAG Query Assistant")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Extracting content..."):
        full_text = extract_full_text_only("temp.pdf")

    st.subheader("📖 Extracted Text Preview")
    st.text_area("Raw Text", full_text[:3000] + "...", height=300)

    if st.button("🔍 Label Content with AI"):
        with st.spinner("Labeling using LLM..."):
            markdown_output = label_pdf_content_markdown(full_text)
            st.session_state.markdown_output = markdown_output
            init_retrieval(markdown_output)

        if "error" in markdown_output.lower():
            st.error("LLM labeling may have failed.")
            st.text_area("⚠️ Raw Output", markdown_output, height=300)
        else:
            st.subheader("✅ Labeled Markdown Output")
            st.markdown(markdown_output)

    st.markdown("---")
    st.subheader("💬 Ask a Question About the PDF")

user_question = st.text_input("Type your question here:")

if st.button("🎯 Get Answer"):
    if not st.session_state.markdown_output:
        st.warning("Please label the PDF first.")
    elif user_question.lower() in st.session_state.markdown_output.lower():
        st.info("⚡ Exact match found in document. Running RAG for more details.")
        with st.spinner("Thinking..."):
            answer, updated_history = answer_query_with_rag(
                user_question, st.session_state.chat_history
            )
            st.session_state.chat_history = updated_history
            st.success("✅ Answer")
            st.write(answer)
    else:
        with st.spinner("Thinking..."):
            answer, updated_history = answer_query_with_rag(
                user_question, st.session_state.chat_history
            )
            st.session_state.chat_history = updated_history
            if answer.startswith("❌"):
                st.error(answer)
            else:
                st.success("✅ Answer")
                st.write(answer)


    if st.button("🔄 Reset Chat"):
        st.session_state.chat_history = []
        st.success("🔁 Chat history cleared.")
