import os
import gradio as gr
from utils import detect_and_extract, summarize_extracted_text

def process_file_or_text(file_obj, raw_text_input, max_len, min_len, progress=gr.Progress()):
    """Processes uploaded file or direct text input, returning raw text, warning, and summary."""
    extracted_text = ""
    warning_message = ""

    if file_obj is not None:
        file_path = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
        ext = os.path.splitext(file_path)[1].lower()

        # Update progress with specific loading indicator step
        if ext in [".jpg", ".jpeg", ".png"]:
            progress(0.2, desc="Running TrOCR Handwritten Neural Model...")
        elif ext == ".pdf":
            progress(0.2, desc="Extracting text / Running Scanned PDF OCR...")
        else:
            progress(0.2, desc="Reading file contents...")

        try:
            extracted_text, warn = detect_and_extract(file_path)
            if warn:
                warning_message = f"⚠️ **Quality Warning**: {warn}"
        except Exception as e:
            return (
                f"Error processing file: {str(e)}",
                f"⚠️ **Extraction Failed**: {str(e)}",
                "Summarization aborted due to extraction error."
            )

    elif raw_text_input and raw_text_input.strip():
        progress(0.3, desc="Processing direct text input...")
        extracted_text = raw_text_input.strip()
    else:
        return (
            "",
            "⚠️ **No Input**: Please upload a supported file (.txt, .docx, .pdf, .jpg, .png) or paste text.",
            ""
        )

    # Validate extracted text before summarizing
    if not extracted_text or len(extracted_text.strip()) < 10:
        return (
            extracted_text,
            "⚠️ **Quality Alert**: Extracted text is too short or empty. Image quality may be too low or file contains no readable text.",
            "Cannot generate summary: Text content insufficient."
        )

    progress(0.6, desc="Generating summary with AI model...")
    try:
        summary = summarize_extracted_text(extracted_text, max_length=max_len, min_length=min_len)
    except Exception as e:
        summary = f"Error during summarization: {str(e)}"

    progress(1.0, desc="Complete!")
    return extracted_text, warning_message, summary

def extract_only(file_obj, raw_text_input, progress=gr.Progress()):
    """Extracts raw text only without running full summarization."""
    if file_obj is not None:
        file_path = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
        ext = os.path.splitext(file_path)[1].lower()

        if ext in [".jpg", ".jpeg", ".png"]:
            progress(0.3, desc="Running TrOCR Handwritten OCR model...")
        elif ext == ".pdf":
            progress(0.3, desc="Extracting text / Running Scanned PDF OCR...")
        else:
            progress(0.3, desc="Extracting text...")

        try:
            extracted_text, warn = detect_and_extract(file_path)
            warning_msg = f"⚠️ **Quality Warning**: {warn}" if warn else ""
            return extracted_text, warning_msg
        except Exception as e:
            return f"Error: {str(e)}", f"⚠️ **Extraction Failed**: {str(e)}"

    elif raw_text_input and raw_text_input.strip():
        return raw_text_input.strip(), ""
    else:
        return "", "⚠️ **No Input**: Please upload a file or enter text."

# Build Gradio UI
with gr.Blocks(title="Multi-Format AI Text Summarizer") as app:
    gr.Markdown(
        """
        # 📝 Multi-Format AI Text Summarizer
        Summarize content from **Plain Text (`.txt`)**, **Word Documents (`.docx`)**, **PDFs (Vector & Scanned OCR)**, and **Handwritten Notes (`.jpg`, `.jpeg`, `.png` via TrOCR)**.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            file_upload = gr.File(
                label="📁 Upload Document or Image",
                file_types=[".txt", ".docx", ".pdf", ".jpg", ".jpeg", ".png"],
                type="filepath"
            )
            text_input = gr.Textbox(
                label="✏️ Or Paste Text Directly",
                lines=5,
                placeholder="Type or paste your text here..."
            )

            with gr.Accordion("⚙️ Summarization Parameters", open=False):
                max_length_slider = gr.Slider(
                    minimum=30, maximum=300, value=150, step=10, label="Max Summary Length"
                )
                min_length_slider = gr.Slider(
                    minimum=10, maximum=100, value=30, step=5, label="Min Summary Length"
                )

            with gr.Row():
                btn_extract = gr.Button("🔍 Extract Text Only", variant="secondary")
                btn_summarize = gr.Button("⚡ Extract & Summarize", variant="primary")

        with gr.Column(scale=1):
            warning_box = gr.Markdown(visible=True)

            with gr.Accordion("👁️ Extracted Raw Text (Verify OCR Accuracy)", open=True):
                raw_text_output = gr.Textbox(
                    label="Raw Text",
                    lines=8,
                    interactive=True,
                    placeholder="Extracted raw text will appear here for verification..."
                )

            summary_output = gr.Textbox(
                label="📌 AI Generated Summary",
                lines=6,
                interactive=False,
                placeholder="Generated summary will appear here..."
            )

    # Event handlers
    btn_extract.click(
        fn=extract_only,
        inputs=[file_upload, text_input],
        outputs=[raw_text_output, warning_box]
    )

    btn_summarize.click(
        fn=process_file_or_text,
        inputs=[file_upload, text_input, max_length_slider, min_length_slider],
        outputs=[raw_text_output, warning_box, summary_output]
    )

if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, share=False, theme=gr.themes.Soft())
