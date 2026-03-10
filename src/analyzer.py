import pandas as pd
import numpy as np

def descriptive_stats(df: pd.DataFrame) -> dict:
    """Estatísticas descritivas das colunas numéricas."""
    numeric = df.select_dtypes(include=[np.number])
    stats = numeric.describe().round(2).to_dict()
    stats['skewness'] = numeric.skew().round(3).to_dict()
    stats['kurtosis'] = numeric.kurtosis().round(3).to_dict()
    return stats

def correlation_analysis(df: pd.DataFrame) -> dict:
    """Top correlações entre variáveis numéricas."""
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return {}
    corr = numeric.corr()
    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            pairs.append({
                'var1': cols[i],
                'var2': cols[j],
                'correlation': round(corr.iloc[i, j], 3)
            })
    pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
    return {'top_correlations': pairs[:5]}

def outlier_detection(df: pd.DataFrame) -> dict:
    """Detecta outliers via IQR em colunas numéricas."""
    result = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        if len(outliers) > 0:
            result[col] = {
                'count': len(outliers),
                'pct': round(len(outliers)/len(df)*100, 2)
            }
    return result

def top_categories(df: pd.DataFrame, n: int = 5) -> dict:
    """Top valores de cada coluna categórica."""
    result = {}
    for col in df.select_dtypes(include=['object']).columns:
        result[col] = df[col].value_counts().head(n).to_dict()
    return result

def time_series_insights(df: pd.DataFrame) -> dict:
    """Agrega receita/valores por período se houver coluna de data."""
    result = {}
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not date_cols or not num_cols:
        return result
    date_col = date_cols[0]
    num_col = num_cols[0]
    df_temp = df.copy()
    df_temp['_month'] = df_temp[date_col].dt.to_period('M')
    monthly = df_temp.groupby('_month')[num_col].sum().tail(12)
    result['monthly_trend'] = {str(k): round(v, 2) for k, v in monthly.items()}
    return result