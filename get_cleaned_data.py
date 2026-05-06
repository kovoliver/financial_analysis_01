import pandas as pd

def get_cleaned_data(
    filepath, 
    date_cols=None, 
    outlier_callback=None,
    outlier_cols=None,
    dropna_subset=None,
    remove_duplicates=True
):
    """
    Univerzális adattisztító függvény.
    
    :param filepath: A CSV fájl elérési útja.
    :param date_cols: Lista az oszlopnevekről, amiket dátummá kell alakítani.
    :param outlier_callback: Egy függvény, ami megkapja a DF-et és visszadja a tisztítottat.
    :param dropna_subset: Oszlopok listája, ahol a hiányzó értékeket keresse. Ha None, mindenhol nézi.
    :param remove_duplicates: Alapértelmezetten True, eltávolítja az azonos sorokat.
    """
    
    # 1. Beolvasás
    df = pd.read_csv(filepath)
    
    # 2. Dátumok kezelése
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
    
    # 3. Duplikátumok eltávolítása (Alapértelmezett: True)
    if remove_duplicates:
        df = df.drop_duplicates()
    
    # 4. Hiányzó értékek kezelése (NaN/Null)
    # Ha a dropna_subset None, akkor az összes oszlopot nézi
    df = df.dropna(subset=dropna_subset)
    
    # 5. Outlierek tisztítása callback függvénnyel
    if outlier_callback:
        df = outlier_callback(df, outlier_cols)
        
    return df