import pandas as pd

def cast_columns(df, column_types):
    for col, dtype in column_types.items():
        if col in df.columns:
            if dtype == 'datetime64[ns]':
                df[col] = pd.to_datetime(df[col])
            else:
                df[col] = df[col].astype(dtype)
    return df