import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

N = 50000

# Datas com sazonalidade (picos em Novembro/Dezembro)
start_date = datetime(2023, 1, 1)
dates = []
for _ in range(N):
    day_offset = np.random.exponential(180)
    d = start_date + timedelta(days=int(day_offset % 365))
    # Black Friday boost
    if d.month == 11 and d.day >= 24:
        if random.random() < 0.4:
            d = d.replace(month=11, day=random.randint(24, 30))
    dates.append(d)

products = {
    'Electronics': (450, 200),
    'Clothing': (85, 40),
    'Home & Garden': (120, 60),
    'Sports': (95, 50),
    'Books': (25, 15),
    'Beauty': (55, 30),
    'Toys': (45, 25),
    'Food': (35, 20),
}

categories = list(products.keys())
weights = [0.25, 0.20, 0.15, 0.12, 0.08, 0.08, 0.07, 0.05]

regions = ['Southeast', 'South', 'Northeast', 'Midwest', 'North']
region_weights = [0.42, 0.15, 0.18, 0.14, 0.11]

cat_list = random.choices(categories, weights=weights, k=N)
prices, quantities, revenues = [], [], []

for cat in cat_list:
    mean_p, std_p = products[cat]
    price = max(5, np.random.normal(mean_p, std_p))
    qty = max(1, int(np.random.exponential(2)))
    prices.append(round(price, 2))
    quantities.append(qty)
    revenues.append(round(price * qty, 2))

df = pd.DataFrame({
    'order_id': [f'ORD-{i:06d}' for i in range(1, N+1)],
    'date': dates,
    'customer_id': [f'CUST-{random.randint(1000, 15000):05d}' for _ in range(N)],
    'product_category': cat_list,
    'product_name': [f'{cat} Item {random.randint(1,50)}' for cat in cat_list],
    'quantity': quantities,
    'unit_price': prices,
    'revenue': revenues,
    'region': random.choices(regions, weights=region_weights, k=N),
    'payment_method': random.choices(
        ['Credit Card', 'Debit Card', 'Pix', 'Boleto'],
        weights=[0.45, 0.25, 0.20, 0.10], k=N
    ),
    'is_returned': np.random.choice([0, 1], p=[0.92, 0.08], size=N),
    'customer_rating': np.random.choice([1,2,3,4,5], p=[0.05,0.08,0.15,0.35,0.37], size=N),
})

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)
df.to_csv('data/sample_dataset.csv', index=False)
print(f"✅ Dataset gerado: {len(df)} linhas × {len(df.columns)} colunas")
print(df.head(3))