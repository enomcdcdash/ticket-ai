import pandas as pd
import os

DB_PATH = "saved_dataset.pkl"

# =========================================
# SAVE DATAFRAME
# =========================================
def save_dataframe(df):

    df.to_pickle(DB_PATH)

# =========================================
# LOAD DATAFRAME
# =========================================
def load_dataframe():

    if os.path.exists(DB_PATH):

        return pd.read_pickle(DB_PATH)

    raise FileNotFoundError(
        "No dataset found"
    )