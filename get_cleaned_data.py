import pandas as pd

def get_cleaned_data(
    filepath, 
    date_cols=None, 
    outlier_callback=None,
    outlier_cols=None,
    dropna_subset=None,
    remove_duplicates=True
):  
    df = pd.read_csv(filepath)
    
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
    
    if remove_duplicates:
        df = df.drop_duplicates()

    df = df.dropna(subset=dropna_subset)
    
    if outlier_callback:
        df = outlier_callback(df, outlier_cols)
        
    return df