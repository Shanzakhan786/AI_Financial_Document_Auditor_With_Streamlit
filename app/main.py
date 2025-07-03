from fastapi import FastAPI, UploadFile
from app.utils.file_parser import parse_document
from app.utils.analyzer import analyze_financials
from app.utils.report_generator import generate_pdf_report

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile):
    data = await parse_document(file)
    analysis = analyze_financials(data)
    report_path = generate_pdf_report(analysis)
    return {"message": "Audit complete", "report": report_path}