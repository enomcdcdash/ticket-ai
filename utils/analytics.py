import pandas as pd

# =========================================
# BASIC KPI SUMMARY
# =========================================
def get_basic_kpi(df):

    summary = {}

    summary["total_rows"] = len(df)

    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) > 0:
        summary["total_numeric"] = df[numeric_cols[0]].sum()
    else:
        summary["total_numeric"] = 0

    summary["columns"] = list(df.columns)

    return summary


# =========================================
# TOP CATEGORY ANALYSIS
# =========================================
def get_top_category(df):

    object_cols = df.select_dtypes(include='object').columns
    numeric_cols = df.select_dtypes(include='number').columns

    if len(object_cols) == 0 or len(numeric_cols) == 0:
        return None

    group_col = object_cols[0]
    value_col = numeric_cols[0]

    result = (
        df.groupby(group_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return result


# =========================================
# GENERATE DATA SUMMARY
# =========================================
def generate_data_summary(df):

    summary = []

    summary.append(f"Dataset contains {len(df)} rows.")

    summary.append(f"Columns: {list(df.columns)}")

    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:

        summary.append(
            f"Column {col} total = {df[col].sum()}"
        )

    return "\n".join(summary)