# process_sales_data.py
import pandas as pd
import os

# -----------------------------
# Read the generated CSV
# -----------------------------
df = pd.read_csv('sales_data.csv')
df['date'] = pd.to_datetime(df['date'])

# -----------------------------
# Exercise 1: Basic Stats
# -----------------------------
print("\n=== Exercise 1: Basic Statistics ===")
print("\nFirst 5 rows:")
print(df.head())

total_quantity = df['quantity'].sum()
print(f"\nTotal quantity sold: {total_quantity}")

avg_price = df['unit_price'].mean()
print(f"Average unit price: ${avg_price:.2f}")

min_age = df['customer_age'].min()
max_age = df['customer_age'].max()
print(f"Customer age range: {min_age} to {max_age}")

store_counts = df['store_id'].value_counts()
print("\nSales by store:")
print(store_counts)

# -----------------------------
# Exercise 2: Filtering & Grouping
# -----------------------------
print("\n=== Exercise 2: Filtering & Grouping ===")
df['revenue'] = df['quantity'] * df['unit_price']

filtered = df[(df['quantity'] > 5) & (df['unit_price'] < 50)]
filtered.to_csv('filtered_sales.csv', index=False)
print(f"Filtered {len(filtered)} records saved to filtered_sales.csv")

store_revenue = df.groupby('store_id')['revenue'].sum().reset_index()
print("\nTotal revenue by store:")
print(store_revenue)

product_avg_quantity = df.groupby('product_id')['quantity'].mean().reset_index()
print("\nAverage quantity per product (first 5):")
print(product_avg_quantity.head())

df['day_of_week'] = df['date'].dt.day_name()
day_counts = df['day_of_week'].value_counts()
print("\nSales by day of week:")
print(day_counts)

# -----------------------------
# Exercise 3: Transformations & Summaries
# -----------------------------
print("\n=== Exercise 3: Transformations & Summaries ===")
df['month'] = df['date'].dt.month_name()

def categorize_age(age):
    if age < 30:
        return 'Young'
    elif age <= 50:
        return 'Adult'
    else:
        return 'Senior'

df['age_category'] = df['customer_age'].apply(categorize_age)

monthly_sales = df.groupby('month')['revenue'].sum().reset_index()
print("\nMonthly sales totals:")
print(monthly_sales)

top_products = df.groupby('product_id')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(3)
print("\nTop 3 products by revenue:")
print(top_products)

os.makedirs('store_reports', exist_ok=True)
for store_id in df['store_id'].unique():
    store_data = df[df['store_id'] == store_id]
    total_revenue = store_data['revenue'].sum()
    avg_order_value = store_data['revenue'].mean()
    transaction_count = len(store_data)
    most_popular = store_data['product_id'].value_counts().idxmax()

    summary = pd.DataFrame({
        'Metric': ['Total Revenue', 'Average Order Value', 'Transaction Count', 'Most Popular Product'],
        'Value': [f"${total_revenue:.2f}", f"${avg_order_value:.2f}", transaction_count, most_popular]
    })

    summary_file = f'store_reports/{store_id}_summary.csv'
    summary.to_csv(summary_file, index=False)
    print(f"Created summary for {store_id}")

print("\nPipeline complete! All CSVs generated. (Bar chart skipped)")