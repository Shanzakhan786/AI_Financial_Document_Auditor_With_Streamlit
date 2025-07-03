import numpy as np
import pandas as pd
from app.utils.benford import benford_analysis

def analyze_financials(df):
    results = {"errors": [], "ratios": {}, "benford": {}, "fraud_risks": []}

    # Convert all possible numeric columns except 'Label'
    df_numeric = df.copy()
    for col in df.columns:
        if col != "Label":
            df_numeric[col] = pd.to_numeric(df[col], errors='coerce')

    # Dynamically find a 'Total' column if it exists
    total_col = None
    for col in df_numeric.columns:
        if col.lower() == 'total':
            total_col = col
            break

    # Check for total mismatches if a total column exists
    if total_col:
        # Sum all numeric columns except 'Label' and 'Total' for ComputedTotal
        sum_cols = [col for col in df_numeric.columns if col not in ['Label', total_col]]
        if sum_cols:
            df_numeric['ComputedTotal'] = df_numeric[sum_cols].sum(axis=1)
            errors = df_numeric[df_numeric['ComputedTotal'] != df_numeric[total_col]]
            if not errors.empty:
                results["errors"] = errors.to_dict()
        else:
            results["errors"] = []
    else:
        results["errors"] = []

    # 2. Financial ratios
    try:
        if 'Label' in df_numeric.columns and 'Amount' in df_numeric.columns:
            current_assets = df_numeric.loc[df_numeric['Label'] == 'Current Assets', 'Amount'].values[0]
            current_liabilities = df_numeric.loc[df_numeric['Label'] == 'Current Liabilities', 'Amount'].values[0]
            current_ratio = round(current_assets / current_liabilities, 2)
            results["ratios"]["Current Ratio"] = current_ratio
    except Exception:
        pass
    try:
        total_debt = float(df.loc[df['Label'].str.lower() == 'total debt']['Amount'].values[0])
        total_equity = float(df.loc[df['Label'].str.lower() == 'total equity']['Amount'].values[0])
        debt_equity = round(total_debt / total_equity, 2)
        results["ratios"]["Debt-Equity Ratio"] = debt_equity
    except Exception:
        pass

    # 3. Benford's Law analysis (on Amount column)
    try:
        if 'Amount' in df.columns:
            benford_result = benford_analysis(df['Amount'])
            results["benford"] = benford_result
            if benford_result.get('suspicious', False):
                results["fraud_risks"].append("Benford's Law anomaly detected in Amount column.")
    except Exception:
        pass

    # 4. Fraud risk indicators
    # Round-number bias
    if 'Amount' in df.columns:
        round_numbers = df['Amount'].apply(lambda x: float(x) % 100 == 0 if pd.notnull(x) else False)
        if round_numbers.sum() / len(df) > 0.3:
            results["fraud_risks"].append("High proportion of round numbers in Amount column.")
    # Duplicate entries
    if df.duplicated().sum() > 0:
        results["fraud_risks"].append("Duplicate rows detected in data.")

    # If nothing found, add a message
    if not results["errors"] and not results["ratios"]:
        results["message"] = "No errors or ratios detected. Please check your data structure."

    return results