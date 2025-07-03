import streamlit as st
import pandas as pd
import numpy as np
import json
from app.utils.file_parser import parse_document
from app.utils.analyzer import analyze_financials
# from app.utils.report_generator import generate_pdf_report  # PDF disabled
import traceback

st.set_page_config(page_title="AI Financial Document Auditor", layout="wide", page_icon="📊")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #f8fffe 0%, #e0f7fa 100%) !important;
    }
    .main {background-color: #ffffff;}
    .block-container {padding-top: 2rem;}
    .stButton>button {background-color: #4fc3f7; color: #003366; font-weight: bold; border-radius: 6px;}
    .stDownloadButton>button {background-color: #80cbc4; color: #003366; font-weight: bold; border-radius: 6px;}
    .stAlert {border-radius: 6px;}
    .stDataFrame {background-color: #fff; border-radius: 6px;}
    h1, h2, h3, h4 {color: #006064;}
    .sidebar .sidebar-content {background: linear-gradient(135deg, #b2ebf2 0%, #4fc3f7 100%); color: #003366;}
    .sidebar .sidebar-content img {margin-bottom: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(44,62,80,0.1);}
    .sidebar .sidebar-content h3, .sidebar .sidebar-content h4 {color: #006064;}
    .stDataFrame th {background-color: #b2ebf2; color: #003366;}
    .stDataFrame td {background-color: #f8fffe;}
    .stMarkdown small {color: #888;}
    </style>
""", unsafe_allow_html=True)

# Add a logo and sidebar for branding and navigation
with st.sidebar:
    st.image("https://scontent.flhe11-1.fna.fbcdn.net/v/t39.30808-6/438098864_122111971250300624_6356290812471494822_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeF7oJ175o_SQZnZEepmc2vyUHRb2CEm8ehQdFvYISbx6HNQyCP-YbbpixpFzx3z-uWZVORCIowzMPYvKYID5y4Z&_nc_ohc=cRdtvdFKjRYQ7kNvwEXl-fs&_nc_oc=Adl82C2xK_zYKJbetcgxuRTVL2w9mapXIa8Oh4E55N_UutseZGQtfwDFEvAI14h7f4s&_nc_zt=23&_nc_ht=scontent.flhe11-1.fna&_nc_gid=K-mb-A4BdWyDPyE_eJDu6g&oh=00_AfMijl7yOmzW76PnITtjWig36fs7y3WaIV-Fz98HGx10Jg&oe=686CA895", width=180)
    st.markdown("""
    ### Welcome!
    This tool helps you audit financial documents with AI.
    - Upload your file
    - Review results
    - Download reports
    """)
    st.markdown("---")
    st.markdown("**Contact:** www.itsolera.com")

st.title("📊 AI Financial Document Auditor")
st.markdown("""
#### Powered by Machine Learning, Benford's Law, and Automated Fraud Detection
Upload your financial files (PDF, Excel, CSV) to get instant audit insights, error checks, and fraud risk analysis. Download your results for compliance and reporting.
""")

uploaded_file = st.file_uploader(
    "**Upload Financial File** (PDF, Excel, CSV)",
    type=["pdf", "xlsx", "csv"],
    help="Supported formats: PDF, Excel (.xlsx), CSV"
)

if uploaded_file:
    st.success("File uploaded successfully ✅")
    try:
        data = parse_document(uploaded_file)
        if data is None or data.empty:
            st.error("Parsed data is empty. Please check your file format.")
        else:
            st.subheader("📄 Extracted Data Preview:")
            st.dataframe(data.head(20), use_container_width=True)

            analysis = analyze_financials(data)
            if not analysis or not isinstance(analysis, dict):
                st.error("Analysis failed or returned invalid result.")
            else:
                st.markdown("---")
                st.subheader("❗ Detected Issues & Errors:")
                if analysis.get("errors"):
                    st.warning("Some inconsistencies or errors were found in your data.")
                    st.json(analysis.get("errors", {}))
                else:
                    st.success("No major errors detected in your data.")

                st.subheader("📈 Financial Ratios:")
                if analysis.get("ratios"):
                    st.table(pd.DataFrame(list(analysis["ratios"].items()), columns=["Ratio", "Value"]))
                else:
                    st.info("No financial ratios could be calculated from your data.")

                # Download analysis as JSON
                def convert_np(obj):
                    if isinstance(obj, dict):
                        return {k: convert_np(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_np(i) for i in obj]
                    elif isinstance(obj, (np.generic, np.bool_)):
                        return obj.item()
                    else:
                        return obj
                analysis_clean = convert_np(analysis)
                analysis_json = json.dumps(analysis_clean, indent=2)
                st.download_button(
                    label="⬇️ Download Audit Analysis (JSON)",
                    data=analysis_json,
                    file_name="audit_analysis.json",
                    mime="application/json"
                )

                # Download errors as CSV if available
                if analysis.get("errors"):
                    errors_df = pd.DataFrame(analysis["errors"])
                    csv = errors_df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download Errors (CSV)",
                        data=csv,
                        file_name="audit_errors.csv",
                        mime="text/csv"
                    )
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.text(traceback.format_exc())

st.markdown("---")
st.markdown("""
<small>Developed by ITSOLERA PVT LTD | For support, contact your ML Team</small>
""", unsafe_allow_html=True)