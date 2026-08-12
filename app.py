import os
import tempfile
import streamlit as st
from utils import detect_and_extract, summarize_extracted_text

# Configure page metadata and wide layout
st.set_page_config(
    page_title="Multi-Format AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, modern aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State variables
if "raw_text" not in st.session_state:
    st.session_state["raw_text"] = ""
if "summary" not in st.session_state:
    st.session_state["summary"] = ""
if "warning" not in st.session_state:
    st.session_state["warning"] = ""

def process_upload_and_extract(uploaded_file, text_input):
    """Saves uploaded buffer to temporary file, runs OCR/extraction, and returns text & warnings."""
    extracted_text = ""
    warning_msg = ""

    if uploaded_file is not None:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            extracted_text, warn = detect_and_extract(tmp_path)
            if warn:
                warning_msg = f"⚠️ {warn}"
        except Exception as e:
            return f"Error extracting from file: {str(e)}", f"⚠️ Extraction Failed: {str(e)}"
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    elif text_input and text_input.strip():
        extracted_text = text_input.strip()
    else:
        return "", "⚠️ No Input: Please upload a supported file (.txt, .docx, .pdf, .jpg, .png) or enter text."

    if not extracted_text or len(extracted_text.strip()) < 10:
        if not warning_msg:
            warning_msg = "⚠️ Quality Alert: Extracted text is too short or empty. Image quality may be low or file contains no readable text."

    return extracted_text, warning_msg

# Header Section
st.markdown('<div class="main-header">📝 Multi-Format AI Text Summarizer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Summarize content seamlessly from Plain Text (<code>.txt</code>), Word (<code>.docx</code>), PDFs (Vector & Scanned OCR), and Handwritten Notes (<code>.jpg</code>, <code>.jpeg</code>, <code>.png</code>).</div>',
    unsafe_allow_html=True
)

# Sidebar - Settings & Documentation
with st.sidebar:
    st.header("⚙️ Settings")
    max_len = st.slider("Max Summary Length", min_value=30, max_value=300, value=150, step=10, key="slider_max")
    min_len = st.slider("Min Summary Length", min_value=10, max_value=100, value=30, step=5, key="slider_min")

    st.markdown("---")
    st.header("ℹ️ Supported Formats")
    st.markdown("""
    - **Plain Text**: `.txt`
    - **Word Documents**: `.docx`
    - **Vector PDF**: `.pdf`
    - **Scanned PDF**: `.pdf` (Tesseract OCR)
    - **Handwritten Notes**: `.jpg`, `.jpeg`, `.png` (Neural TrOCR)
    """)

    st.markdown("---")
    if st.button("🧹 Clear All Output", use_container_width=True):
        st.session_state["raw_text"] = ""
        st.session_state["summary"] = ""
        st.session_state["warning"] = ""
        st.rerun()

# Main UI Layout - 2 Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Input Source")
    uploaded_file = st.file_uploader(
        "Upload Document or Image",
        type=["txt", "docx", "pdf", "jpg", "jpeg", "png"],
        help="Supports .txt, .docx, vector/scanned .pdf, and handwritten .jpg/.png images"
    )

    text_input = st.text_area(
        "Or Paste Text Directly",
        height=160,
        placeholder="Type or paste your text content here..."
    )

    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        extract_clicked = st.button("🔍 Extract Text Only", use_container_width=True)
    with btn_col2:
        summarize_clicked = st.button("⚡ Extract & Summarize", type="primary", use_container_width=True)

    # Action Handlers
    if extract_clicked:
        with st.spinner("Processing input and running OCR/text extraction..."):
            raw_txt, warn = process_upload_and_extract(uploaded_file, text_input)
            st.session_state["raw_text"] = raw_txt
            st.session_state["warning"] = warn
            st.session_state["summary"] = ""

    if summarize_clicked:
        with st.spinner("Extracting text and generating neural AI summary..."):
            raw_txt, warn = process_upload_and_extract(uploaded_file, text_input)
            st.session_state["raw_text"] = raw_txt
            st.session_state["warning"] = warn

            if raw_txt and len(raw_txt.strip()) >= 10:
                try:
                    summary_res = summarize_extracted_text(raw_txt, max_length=max_len, min_length=min_len)
                    st.session_state["summary"] = summary_res
                except Exception as e:
                    st.session_state["summary"] = f"Error during summarization: {str(e)}"
            else:
                st.session_state["summary"] = "Cannot generate summary: Text content insufficient."

with col2:
    st.subheader("📊 Processing & AI Results")

    # Display Warning Banner if active
    if st.session_state["warning"]:
        st.warning(st.session_state["warning"])

    # Raw Text Accordion / Display
    st.markdown("##### 👁️ Extracted Raw Text (Verification)")
    st.text_area(
        label="Raw Text Output",
        value=st.session_state["raw_text"],
        placeholder="Extracted text will appear here for verification...",
        height=200,
        disabled=False
    )

    # AI Summary Display
    st.markdown("##### 📌 AI Generated Summary")
    st.text_area(
        label="Summary Output",
        value=st.session_state["summary"],
        placeholder="Generated AI summary will appear here...",
        height=160,
        disabled=False
    )

    summary_res_val = st.session_state["summary"]
    if summary_res_val and not summary_res_val.startswith("Cannot generate") and not summary_res_val.startswith("Error"):
        st.download_button(
            label="💾 Download Summary (.txt)",
            data=summary_res_val,
            file_name="ai_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
