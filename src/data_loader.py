import pandas as pd
import numpy as np

def load_and_clean(filepath: str) -> pd.DataFrame:
    """Carrega CSV e aplica limpeza básica."""
    df = pd.read_csv(filepath)

    # Detecta e converte colunas de data
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass

    # Remove duplicatas e linhas totalmente vazias
    df = df.drop_duplicates()
    df = df.dropna(how='all')

    return df

def get_summary(df: pd.DataFrame) -> dict:
    """Retorna resumo estruturado do dataset."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()

    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    return {
        'shape': df.shape,
        'numeric_cols': numeric_cols,
        'categorical_cols': cat_cols,
        'date_cols': date_cols,
        'missing_values': missing[missing > 0].to_dict(),
        'missing_pct': missing_pct[missing_pct > 0].to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict(),
    }