# Import libraries
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Generate fake sales data
np.random.seed(42)
dates = [datetime(2023,1,1) + timedelta(days=x) for x in range(365)]
products = ['Laptop', 'Phone', 'Tablet', 'Monitor']

data = {
    'Order_Date': np.random.choice(dates, 1000),
    'Product': np.random.choice(products, 1000),
    'Sales_Amount': np.round(np.random.uniform(100, 2000, 1000), 2),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 1000)
}

df = pd.DataFrame(data)

# 2. Create SQL database and analyze
conn = sqlite3.connect(':memory:')
df.to_sql('sales', conn, index=False)

# Top-selling products query
query = """
SELECT 
    Product,
    COUNT(*) AS Transactions,
    ROUND(SUM(Sales_Amount), 2) AS Revenue
FROM sales
GROUP BY Product
ORDER BY Revenue DESC;
"""
top_products = pd.read_sql(query, conn)

# 3. Visualize
plt.figure(figsize=(10,5))
plt.bar(top_products['Product'], top_products['Revenue'])
plt.title('Revenue by Product (2023)')
plt.ylabel('Total Sales ($)')
plt.savefig('sales_by_product.png')
plt.show()

conn.close()