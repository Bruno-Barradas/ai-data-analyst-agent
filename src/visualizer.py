import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('dark_background')
COLORS = ['#00e5ff', '#7c3aed', '#10b981', '#f59e0b', '#ef4444', '#3b82f6']

def generate_all(df: pd.DataFrame, output_dir: str = 'visuals') -> list:
    """Gera todos os gráficos e salva em output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()

    # 1. Distribuição das colunas numéricas
    if numeric:
        fig, axes = plt.subplots(1, min(3, len(numeric)),
                                  figsize=(14, 4), facecolor='#0a0a0f')
        for i, col in enumerate(numeric[:3]):
            ax = axes[i] if len(numeric) > 1 else axes
            ax.hist(df[col].dropna(), bins=40, color=COLORS[i], alpha=0.85, edgecolor='none')
            ax.set_title(col, color='white', fontsize=11, pad=10)
            ax.set_facecolor('#12121a')
            ax.tick_params(colors='#64748b')
        fig.suptitle('Distributions', color='white', fontsize=13, y=1.02)
        plt.tight_layout()
        path = f'{output_dir}/01_distributions.png'
        plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0a0a0f')
        plt.close()
        saved.append(path)

    # 2. Correlação heatmap
    if len(numeric) >= 2:
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0a0a0f')
        corr = df[numeric].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='plasma',
                    ax=ax, linewidths=0.5, linecolor='#1a1a26',
                    cbar_kws={'shrink': 0.8})
        ax.set_facecolor('#12121a')
        ax.set_title('Correlation Matrix', color='white', pad=14)
        plt.tight_layout()
        path = f'{output_dir}/02_correlation_matrix.png'
        plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0a0a0f')
        plt.close()
        saved.append(path)

    # 3. Top categorias
    if cat_cols:
        col = cat_cols[0]
        top = df[col].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a0f')
        bars = ax.barh(top.index[::-1], top.values[::-1], color=COLORS[:len(top)], alpha=0.9)
        ax.set_facecolor('#12121a')
        ax.set_title(f'Top {col}', color='white', pad=14)
        ax.tick_params(colors='#94a3b8')
        ax.spines['bottom'].set_color('#2a2a40')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#2a2a40')
        plt.tight_layout()
        path = f'{output_dir}/03_top_categories.png'
        plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0a0a0f')
        plt.close()
        saved.append(path)

    # 4. Série temporal
    if date_cols and numeric:
        date_col = date_cols[0]
        num_col = numeric[0]
        df_temp = df.copy()
        df_temp['_period'] = df_temp[date_col].dt.to_period('M')
        monthly = df_temp.groupby('_period')[num_col].sum()
        fig, ax = plt.subplots(figsize=(12, 5), facecolor='#0a0a0f')
        ax.plot(range(len(monthly)), monthly.values, color=COLORS[0],
                linewidth=2.5, marker='o', markersize=4)
        ax.fill_between(range(len(monthly)), monthly.values,
                        alpha=0.15, color=COLORS[0])
        ax.set_facecolor('#12121a')
        ax.set_title(f'{num_col} Over Time (Monthly)', color='white', pad=14)
        ax.tick_params(colors='#94a3b8')
        for spine in ax.spines.values():
            spine.set_color('#2a2a40')
        plt.tight_layout()
        path = f'{output_dir}/04_time_series.png'
        plt.savefig(path, dpi=120, bbox_inches='tight', facecolor='#0a0a0f')
        plt.close()
        saved.append(path)

    print(f"  📊 {len(saved)} gráficos salvos em /{output_dir}/")
    return saved