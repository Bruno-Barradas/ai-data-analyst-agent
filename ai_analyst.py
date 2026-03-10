#!/usr/bin/env python3
"""
AI Data Analyst Agent
Uso: python ai_analyst.py 
"""

import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# Carrega variáveis de ambiente (.env)
load_dotenv()

# Adiciona src/ ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from data_loader import load_and_clean, get_summary
from analyzer import (descriptive_stats, correlation_analysis,
                      outlier_detection, top_categories, time_series_insights)
from visualizer import generate_all


def get_ai_insights(analysis_data: dict, client: anthropic.Anthropic) -> str:
    """Chama a Claude API para gerar insights em linguagem natural."""

    prompt = f"""Você é um Data Analyst sênior. Analise os dados abaixo e gere um relatório executivo.

DADOS DA ANÁLISE:
{json.dumps(analysis_data, indent=2, ensure_ascii=False, default=str)}

Gere um relatório com EXATAMENTE este formato em Markdown:

## 📊 Resumo Executivo
[2-3 frases sobre o dataset]

## 🔍 Principais Insights
1. [insight com número concreto]
2. [insight com número concreto]
3. [insight com número concreto]
4. [insight com número concreto]
5. [insight com número concreto]

## ⚠️ Pontos de Atenção
- [risco ou anomalia encontrada]
- [outlier ou padrão incomum]

## ✅ Recomendações de Negócio
1. [ação concreta baseada nos dados]
2. [ação concreta baseada nos dados]
3. [ação concreta baseada nos dados]

## 📈 Próximos Passos Analíticos
- [análise adicional recomendada]
- [modelo ou técnica sugerida]

Seja direto, use números reais dos dados, escreva em português."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def save_report(insights: str, summary: dict, filepath: str, output_dir: str = 'reports') -> str:
    """Salva o relatório completo em Markdown."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{output_dir}/analysis_report_{timestamp}.md"

    header = f"""# AI Data Analyst Report
**Arquivo:** {filepath}
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Dataset:** {summary['shape'][0]:,} linhas × {summary['shape'][1]} colunas

---

"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header + insights)

    return filename


def main():
    # Verifica argumentos
    if len(sys.argv) < 2:
        print("Uso: python ai_analyst.py ")
        print("Exemplo: python ai_analyst.py data/sample_dataset.csv")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"❌ Arquivo não encontrado: {filepath}")
        sys.exit(1)

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY não encontrada no .env")
        sys.exit(1)

    print("\n🤖 AI Data Analyst Agent")
    print("=" * 40)

    # 1. Carrega e limpa dados
    print(f"\n📂 Carregando: {filepath}")
    df = load_and_clean(filepath)
    summary = get_summary(df)
    print(f"   ✓ {summary['shape'][0]:,} linhas × {summary['shape'][1]} colunas")
    print(f"   ✓ Numéricas: {summary['numeric_cols']}")
    print(f"   ✓ Categóricas: {summary['categorical_cols']}")

    # 2. Análise estatística
    print("\n📊 Análise estatística...")
    stats = descriptive_stats(df)
    correlations = correlation_analysis(df)
    outliers = outlier_detection(df)
    categories = top_categories(df)
    time_insights = time_series_insights(df)
    print("   ✓ EDA completo")

    # 3. Gráficos
    print("\n🎨 Gerando visualizações...")
    charts = generate_all(df)

    # 4. IA Insights
    print("\n🧠 Consultando Claude API para insights...")
    client = anthropic.Anthropic(api_key=api_key)

    analysis_data = {
        'dataset_info': summary,
        'statistics': {k: v for k, v in stats.items() if k in ['mean', 'std', 'min', 'max', '50%']},
        'top_correlations': correlations.get('top_correlations', [])[:3],
        'outliers': outliers,
        'top_categories': {k: list(v.items())[:3] for k, v in categories.items()},
        'time_trends': time_insights,
    }

    insights = get_ai_insights(analysis_data, client)
    print("   ✓ Insights gerados pela IA")

    # 5. Salva relatório
    report_path = save_report(insights, summary, filepath)
    print(f"\n✅ Relatório salvo: {report_path}")
    print(f"📊 Gráficos em: visuals/")
    print("\n" + "=" * 40)
    print(insights)


if __name__ == '__main__':
    main()