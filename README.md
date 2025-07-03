# AI Financial Document Auditor

## Overview
This project is an AI-powered financial document auditor that helps automate the review of financial files (PDF, Excel, CSV) to detect inconsistencies, fraud risks, and provide financial insights. It uses machine learning, statistical analysis (including Benford's Law), and OCR for scanned documents.

## Features
- Upload and parse financial documents (PDF, Excel, CSV)
- Extract and display tabular data
- Automated detection of errors and inconsistencies
- Financial ratio analysis (e.g., Current Ratio)
- Benford's Law anomaly detection
- Fraud risk indicators (e.g., round-number bias, duplicate entries)
- Download audit results as JSON or CSV

## Requirements
- Python 3.8+
- All dependencies listed in `requirements.txt`
- For PDF/OCR support: Tesseract OCR and poppler (for pdf2image)
- For PDF report generation (optional): GTK 3 (WeasyPrint, currently disabled)

## Quick Start
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the Streamlit app:**
   ```sh
   streamlit run streamlit_app.py
   ```
3. **Upload a sample file:**
   Use `sample_financial_data.csv` or your own financial document.
4. **Download results:**
   Use the provided buttons to download audit results as JSON or CSV.

## Project Structure
```
├── streamlit_app.py           # Main Streamlit app
├── app/
│   ├── main.py                # FastAPI backend (optional)
│   ├── utils/
│   │   ├── file_parser.py     # File parsing logic
│   │   ├── analyzer.py        # Financial analysis logic
│   │   ├── benford.py         # Benford's Law analysis
│   │   └── report_generator.py# (PDF generation, currently disabled)
│   └── templates/
│       └── report.html        # (PDF report template, currently unused)
├── requirements.txt           # Python dependencies
├── sample_financial_data.csv  # Example dataset
```

## Notes
- PDF report generation is disabled by default due to system dependencies. Use the in-app download options for results.
- For PDF/OCR support, install Tesseract and Poppler, and ensure they are in your system PATH.
- For any issues, see the troubleshooting section in the WeasyPrint and Streamlit documentation.

## License
MIT License
