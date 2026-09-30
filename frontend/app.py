import os
import sys
import streamlit as st
import requests

# Ensure ai_core can be imported from frontend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ai_core.generator import sanitize_text, format_html_preview, format_docx, format_pdf

# Page Configuration & Layout
st.set_page_config(page_title="LegalEase", layout="centered")

# Company Logo
WEB_LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "Image", "Logo.png")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(WEB_LOGO_PATH):
        st.image(WEB_LOGO_PATH, use_container_width=True)

# Title
st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)
st.markdown("---")

# Input Form
st.subheader("Document Specifications")
document_type = st.text_input("Document Type", placeholder="e.g., Non-Disclosure Agreement")
parties = st.text_area("Parties Involved", placeholder="e.g., Party A (Disclosing) and Party B (Receiving)")
terms = st.text_area("Terms and Conditions", placeholder="e.g., 2-year duration; confidential source code; California governing law")
dates = st.text_input("Effective Date", placeholder="e.g., October 1, 2026")

# Session state initialization
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False

# Step 1: Generate Document with Backend AI
if st.button("Generate Document", type="primary"):
    if not (document_type and parties and terms and dates):
        st.error("Please fill in all the input fields before generating.")
    else:
        with st.spinner("Drafting formal legal document with AI..."):
            try:
                response = requests.post(
                    "http://localhost:8000/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates
                    },
                    timeout=120
                )
                if response.status_code == 200:
                    raw_text = response.json().get("document", "")
                    st.session_state.generated_text = sanitize_text(raw_text)
                    st.success("Document successfully drafted!")
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend server: {str(e)}")

# If document has been generated, show Preview, Edit, and Export options
if st.session_state.generated_text:
    st.markdown("### Document Preview")

    # Step 2: HTML Preview Rendering (Dark-themed scrollable card)
    styled_html = format_html_preview(st.session_state.generated_text)
    st.markdown(f"<div style='margin-bottom: 20px;'>{styled_html}</div>", unsafe_allow_html=True)

    # Step 3: Editable Document Preview Toggle
    toggle_label = "Hide Editor" if st.session_state.show_edit else "Edit Document"
    if st.button(toggle_label):
        st.session_state.show_edit = not st.session_state.show_edit
        st.rerun()

    if st.session_state.show_edit:
        edited_text = st.text_area(
            "Edit Document Below:",
            st.session_state.generated_text,
            height=300
        )
        st.session_state.generated_text = edited_text

    st.markdown("### Export Options")
    # Clean filename base
    clean_filename = f"{document_type.replace(' ', '_').lower()}_document"

    btn_col1, btn_col2, btn_col3 = st.columns(3)

    # Step 4: Multi-Format Download Options
    with btn_col1:
        st.download_button(
            label="📄 Download as .TXT",
            data=st.session_state.generated_text,
            file_name=f"{clean_filename}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with btn_col2:
        docx_file = format_docx(st.session_state.generated_text, document_type, terms)
        st.download_button(
            label="📝 Download as .DOCX",
            data=docx_file.getvalue(),
            file_name=f"{clean_filename}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with btn_col3:
        pdf_file = format_pdf(st.session_state.generated_text, document_type)
        st.download_button(
            label="📕 Download as .PDF",
            data=pdf_file.getvalue(),
            file_name=f"{clean_filename}.pdf",
            mime="application/pdf",
            use_container_width=True
        )