import streamlit as st
from difflib import ndiff
from html import escape

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

def main():
    st.title("Text Comparison Tool")
    st.write("Upload or enter two texts to compare their content and highlight differences.")

    # Text input areas
    text1 = st.text_area("Enter or paste Text 1:", height=200)
    text2 = st.text_area("Enter or paste Text 2:", height=200)

    if st.button("Compare Texts"):
        if not text1.strip() or not text2.strip():
            st.warning("Please enter text in both fields to compare.")
        else:
            # Highlight differences
            st.write("### Comparison Result:")
            highlighted_text = highlight_differences(text1, text2)
            st.markdown(f"<div style='font-family: monospace;'>{highlighted_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
