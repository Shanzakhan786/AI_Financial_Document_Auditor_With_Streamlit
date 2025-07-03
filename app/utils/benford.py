import numpy as np


def benford_analysis(data):
    # Remove NaN and non-numeric
    clean_data = [abs(float(x)) for x in data if str(x).replace(".", "", 1).isdigit()]
    leading_digits = [
        str(x)[0] for x in clean_data if str(x)[0].isdigit() and x != 0
    ]
    if not leading_digits:
        return {"observed": {}, "expected": {}, "suspicious": False}
    observed = {
        str(d): leading_digits.count(str(d)) / len(leading_digits)
        for d in range(1, 10)
    }
    expected = {str(d): np.log10(1 + 1 / int(d)) for d in range(1, 10)}
    # Chi-squared test
    chi2 = sum(
        (observed[str(d)] - expected[str(d)]) ** 2 / expected[str(d)] for d in range(1, 10)
    )
    suspicious = chi2 > 0.05 * 9  # Simple threshold, can be tuned
    return {
        "observed": observed,
        "expected": expected,
        "chi2": chi2,
        "suspicious": suspicious,
    }