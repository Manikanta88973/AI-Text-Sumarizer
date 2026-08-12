---
title: Multi Format AI Text Summarizer
emoji: 📝
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.30.0
app_file: app.py
pinned: false
---

# Multi-Format AI Text Summarizer

An extended AI-powered text summarizer application built with **Streamlit** that accepts text from multiple input formats: plain text (`.txt`), Word documents (`.docx`), vector PDFs (`.pdf`), scanned/image-based PDFs (`.pdf`), and images of handwritten notes (`.jpg`, `.jpeg`, `.png`).

---

## Features & Supported Formats

| Format | Extension | Extraction Method |
| :--- | :--- | :--- |
| **Plain Text** | `.txt` | Direct UTF-8 / latin-1 reader |
| **Word Documents** | `.docx` | `python-docx` paragraph parser |
| **Vector PDF** | `.pdf` | `pdfplumber` text extractor |
| **Scanned PDF** | `.pdf` | `pdf2image` conversion + `pytesseract` OCR |
| **Handwritten Images** | `.jpg`, `.jpeg`, `.png` | Hugging Face Neural `microsoft/trocr-base-handwritten` |

---

## Deployment Readiness for Streamlit Cloud & Hugging Face Spaces

This project is 100% prepared for deployment on **Streamlit Community Cloud** and **Hugging Face Spaces (Streamlit SDK)**:

- **System Binaries (`packages.txt`)**: Contains required Linux packages (`tesseract-ocr`, `tesseract-ocr-eng`, `poppler-utils`, `libgl1`, `libglib2.0-0`) automatically installed by Streamlit Cloud.
- **Python Packages (`requirements.txt`)**: Specifies `streamlit>=1.30.0` along with Hugging Face transformers, PyTorch, and document parsers.
- **Model Resource Caching (`utils.py`)**: Uses `@st.cache_resource` for lazy-loading neural models (`microsoft/trocr-base-handwritten` & `sshleifer/distilbart-cnn-12-6`) once into RAM/VRAM.

---

## System Dependencies (Local Setup)

In addition to Python packages, full OCR capabilities require external system binaries for Tesseract OCR and Poppler.

### 1. Tesseract OCR (Required for `pytesseract` OCR)

- **Windows**:
  - Download installer from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
  - Or install via Winget in PowerShell:
    ```powershell
    winget install --id UB-Mannheim.TesseractOCR
    ```
  - Standard installation directory (`C:\Program Files\Tesseract-OCR\tesseract.exe`) is automatically detected by `utils.py`.

- **Linux (Ubuntu / Debian / Streamlit Cloud)**:
  Automatically installed via `packages.txt` or manually:
  ```bash
  sudo apt-get update
  sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
  ```

- **macOS**:
  ```bash
  brew install tesseract
  ```

---

### 2. Poppler Utilities (Required for `pdf2image` Scanned PDF Conversion)

- **Windows**:
  - Download binary zip from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases/).
  - Extract and add `bin` directory to system `PATH`.

- **Linux (Ubuntu / Debian / Streamlit Cloud)**:
  Automatically installed via `packages.txt` or manually:
  ```bash
  sudo apt-get update
  sudo apt-get install -y poppler-utils
  ```

- **macOS**:
  ```bash
  brew install poppler
  ```

---

## Local Installation & Running with Streamlit

1. **Clone or Navigate to the Project Directory**:
   ```bash
   cd BlacksBucks
   ```

2. **Install Required Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the Web Interface**:
   Open your browser at `http://localhost:8501`.

---

## Verification & OCR Verification Workflow

1. **Upload File**: Select any supported file (`.txt`, `.docx`, `.pdf`, `.jpg`, `.jpeg`, `.png`) or enter text manually.
2. **Loading Indicator**: Watch the spinner while TrOCR neural model or PDF OCR runs.
3. **Verify Extracted Text**: Inspect the extracted content in the **Extracted Raw Text** box before summarizing.
4. **Graceful Quality Handling**: If an image or scanned document quality is low, a warning banner will notify you of low-confidence OCR results.
