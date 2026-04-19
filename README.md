![Cover](visuals/cover.png)

# 🤖 AI Data Analyst Agent

> Automated data analysis pipeline powered by Claude AI.
> Run once, get full insights — EDA, statistics, visualizations, and AI-generated recommendations.

```bash
python ai_analyst.py your_dataset.csv
```

---

## 🎯 Business Problem

Data analysts spend 60–80% of their time on repetitive EDA tasks.
This agent automates the entire exploratory phase, delivering structured
insights and actionable recommendations in under 60 seconds.

## ⚡ What It Does Automatically

| Step | Output |
|------|--------|
| Data Loading | Detects types, cleans nulls, parses dates |
| Statistical EDA | Descriptive stats, skewness, kurtosis |
| Correlation Analysis | Top variable relationships |
| Outlier Detection | IQR-based anomaly flagging |
| Visualizations | 4 professional charts saved to /visuals |
| AI Insights | Claude API generates executive report |
| Report Export | Markdown report saved to /reports |

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/ai-data-analyst-agent
cd ai-data-analyst-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your Anthropic API key

# 4. Generate sample dataset
python data/generate_dataset.py

# 5. Run the agent
python ai_analyst.py data/sample_dataset.csv
```

## 📊 Sample Output

```
🤖 AI Data Analyst Agent
========================================
📂 Loading: data/sample_dataset.csv
   ✓ 50,000 rows × 12 columns
   ✓ Numeric: ['quantity', 'unit_price', 'revenue', ...]
   ✓ Categorical: ['product_category', 'region', ...]

📊 Statistical analysis...
   ✓ Full EDA complete

🎨 Generating visualizations...
   📊 4 charts saved in /visuals/

🧠 Querying Claude API for insights...
   ✓ AI insights generated

✅ Report saved: reports/analysis_report_20240315_143022.md
```

## 🛠️ Tech Stack

- **Python 3.10+** — core language
- **Pandas / NumPy** — data manipulation
- **Matplotlib / Seaborn** — visualizations
- **Anthropic Claude API** — AI-powered insights
- **python-dotenv** — environment management

## 📁 Project Structure

```
ai-data-analyst-agent/
├── ai_analyst.py       # Main CLI script
├── requirements.txt
├── .env.example
├── src/
│   ├── data_loader.py  # Load & clean
│   ├── analyzer.py     # Statistical analysis
│   └── visualizer.py   # Chart generation
├── data/
│   └── sample_dataset.csv
├── visuals/            # Generated charts
└── reports/            # Generated reports
```

## 📬 Contact

Bruno Barradas — [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)
