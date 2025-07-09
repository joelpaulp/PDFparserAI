import streamlit as st
from pdf_parser import extract_full_text_only
from pdf_labeler import label_pdf_content_markdown
from user_query import init_retrieval, answer_query_with_rag
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate API Key
if not os.getenv("OPENROUTER_API_KEY"):
    st.error("❌ API key not found. Please set OPENROUTER_API_KEY in a .env file.")
    st.stop()

# Session state
if "markdown_output" not in st.session_state:
    st.session_state.markdown_output = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_ready" not in st.session_state:
    st.session_state.chat_ready = False

st.set_page_config(page_title="📄 PDF Chat Assistant", layout="wide")
st.title("📄 PDF Chat Assistant (RAG + LLM)")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("🚀 Start Chat"):
        with st.spinner("Processing PDF..."):
            full_text = extract_full_text_only("temp.pdf")
            markdown_output = label_pdf_content_markdown(full_text)
            st.session_state.markdown_output = markdown_output
            init_retrieval(markdown_output)
            st.session_state.chat_ready = True

if st.session_state.chat_ready:
    st.success("✅ PDF processed. You can now chat with it below!")

    st.markdown("---")
    st.subheader("💬 Ask a Question")

    user_question = st.text_input("Type your question here:")

    def enhance_prompt(user_input):
        return f"""You are an AI assistant helping a user understand a complex, labeled document.

            Please provide a precise, helpful answer to the following query, using only relevant content from the document:

            Question: {user_input.strip()}
            """


    if st.button("🎯 Get Answer"):
        if not st.session_state.markdown_output:
            st.warning("Please upload and process a PDF first.")
        elif not user_question.strip():
            st.warning("Please enter a question.")
        else:
            enhanced_input = enhance_prompt(user_question)
            with st.spinner("Thinking..."):
                answer, updated_history = answer_query_with_rag(
                    enhanced_input, st.session_state.chat_history
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
