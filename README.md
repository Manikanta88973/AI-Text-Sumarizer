# Multi-Format AI Text Summarizer

An extended AI-powered text summarizer application that accepts text from multiple input formats: plain text (`.txt`), Word documents (`.docx`), vector PDFs (`.pdf`), scanned/image-based PDFs (`.pdf`), and images of handwritten notes (`.jpg`, `.jpeg`, `.png`).

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

## System Dependencies (Required for OCR & Scanned PDFs)

In addition to Python packages, full OCR capabilities require external system binaries for Tesseract OCR and Poppler.

### 1. Tesseract OCR (Required for `pytesseract` OCR)

- **Windows**:
  - Download the official setup installer from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
  - Or install via Winget in PowerShell:
    ```powershell
    winget install --id UB-Mannheim.TesseractOCR
    ```
  - Standard installation directory (`C:\Program Files\Tesseract-OCR\tesseract.exe`) is automatically detected by `utils.py`.

- **Linux (Ubuntu / Debian)**:
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
  - Download the latest binary release zip from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases/).
  - Extract the zip file (e.g., to `C:\Program Files\poppler`) and add the `bin` directory to your system Environment `PATH`.

- **Linux (Ubuntu / Debian)**:
  ```bash
  sudo apt-get update
  sudo apt-get install -y poppler-utils
  ```

- **macOS**:
  ```bash
  brew install poppler
  ```

---

## Python Installation & Setup

1. **Clone or Navigate to the Project Directory**:
   ```bash
   cd BlacksBucks
   ```

2. **Install Required Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application**:
   ```bash
   python app.py
   ```

4. **Access the Web Interface**:
   Open your browser and navigate to `http://127.0.0.1:7860`.

---

## Verification & OCR Verification Workflow

1. **Upload File**: Select any supported file (`.txt`, `.docx`, `.pdf`, `.jpg`, `.jpeg`, `.png`) or enter text manually.
2. **Loading Indicator**: Watch the status indicator while TrOCR neural model or PDF OCR runs.
3. **Verify Extracted Text**: Expand the collapsible **Extracted Raw Text** accordion to inspect the extracted content before summarizing.
4. **Graceful Quality Handling**: If an image or scanned document quality is low, a warning banner will notify you of low-confidence OCR results.
