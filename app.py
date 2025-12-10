import streamlit as st
from pdf_qa import build_index_from_pdf, answer_question

st.set_page_config(page_title="Chat with PDF", page_icon="📄", layout="centered")
st.title("📄 Chat with a PDF")
st.write("Upload a PDF, then ask questions and get answers based only on the PDF.")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if "index" not in st.session_state:
    st.session_state.index = None
if "chunks" not in st.session_state:
    st.session_state.chunks = None

if uploaded is not None and st.session_state.index is None:
    with st.spinner("Reading PDF and building search index..."):
        idx, chunks = build_index_from_pdf(uploaded)
        st.session_state.index = idx
        st.session_state.chunks = chunks
    st.success("PDF loaded! Ask your question below.")

question = st.text_input("Your question", placeholder="e.g., What is the main conclusion?")

if st.button("Ask", type="primary"):
    if st.session_state.index is None:
        st.error("Upload a PDF first.")
    elif not question.strip():
        st.error("Type a question.")
    else:
        with st.spinner("Searching and generating answer..."):
            answer, sources = answer_question(
                question,
                st.session_state.index,
                st.session_state.chunks
            )

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources (from PDF)")
        for i, s in enumerate(sources, 1):
            st.markdown(f"**Source {i}:** {s[:600]}{'...' if len(s) > 600 else ''}")
