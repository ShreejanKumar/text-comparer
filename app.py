import streamlit as st
from difflib import ndiff
from html import escape
from PyPDF2 import PdfReader

def highlight_differences(text1, text2):
    """
    Compares two texts word by word and highlights differences.
    Returns the highlighted HTML for display.
    """
    diff = ndiff(text1.split(), text2.split())
    highlighted = []
    
    for word in diff:
        if word.startswith("- "):  # Word is only in the first text
            highlighted.append(f'<span style="background-color: #ffcccc;">{escape(word[2:])}</span>')
        elif word.startswith("+ "):  # Word is only in the second text
            highlighted.append(f'<span style="background-color: #ccffcc;">{escape(word[2:])}</span>')
        else:  # Word is in both texts
            highlighted.append(escape(word[2:]))
    
    return " ".join(highlighted)

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    """
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def main():
    st.title("Text Comparison Tool")
    st.write("Compare the content of a provided text with either a second text or a PDF.")

    # Text input areas
    text1 = st.text_area("Enter or paste Text 1:", height=200)
    uploaded_pdf = st.file_uploader("Upload a PDF file for Text 2:", type=["pdf"])
    text2_input = st.text_area("Alternatively, enter or paste Text 2:", height=200)

    # Determine the source of the second text
    text2 = ""
    if uploaded_pdf is not None:
        text2 = extract_text_from_pdf(uploaded_pdf)
        st.info("Text extracted from uploaded PDF.")
    elif text2_input.strip():
        text2 = text2_input.strip()
    
    if st.button("Compare Texts"):
        if not text1.strip():
            st.warning("Please enter text in the first text box.")
        elif not text2:
            st.warning("Please provide text for the second input, either by uploading a PDF or entering text.")
        else:
            # Highlight differences
            st.write("### Comparison Result:")
            highlighted_text = highlight_differences(text1, text2)
            st.markdown(f"<div style='font-family: monospace;'>{highlighted_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
