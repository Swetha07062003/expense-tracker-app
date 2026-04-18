import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('data/expenses.csv')

# Rename columns
df.columns = ['Date', 'Category', 'Amount', 'Payment', 'Notes']
df['Category'] = df['Category'].replace({
    'Medical': 'Health'
})

# Category-wise totals
category_total = df.groupby('Category')['Amount'].sum()
df['Date'] = pd.to_datetime(df['Date'])
print(category_total)

# Bar Chart
plt.figure(figsize=(8,5))
category_total.plot(kind='bar')
plt.title('Category-wise Spending')
plt.xlabel('Category')
plt.ylabel('Amount')
plt.tight_layout()
plt.savefig('outputs/charts/category_spending.png')
plt.show()

# Pie Chart
plt.figure(figsize=(7,7))
category_total.plot(
    kind='pie',
    autopct='%1.1f%%'
)

plt.title('Expense Distribution')
plt.ylabel('')
plt.savefig('outputs/charts/expense_distribution.png')
plt.show()
# Monthly spending trend
df['Month'] = df['Date'].dt.month_name()

df['Month_Number'] = df['Date'].dt.month

monthly_total = df.groupby(['Month_Number', 'Month'])['Amount'].sum().reset_index()
monthly_total = monthly_total.sort_values('Month_Number')

plt.figure(figsize=(8,5))
plt.plot(monthly_total['Month'], monthly_total['Amount'], marker='o')

plt.title('Monthly Expense Trend')
plt.xlabel('Month')
plt.ylabel('Amount')
plt.tight_layout()

plt.savefig('outputs/charts/monthly_trend.png')
plt.show()
# Overspending detection
threshold = df['Amount'].quantile(0.95)

high_expenses = df[df['Amount'] >= threshold]

print("\nOverspending Threshold:", threshold)
print("\nTop 5% Highest Expense Transactions:")
print(high_expenses[['Date', 'Category', 'Amount']])
high_expenses[['Date', 'Category', 'Amount']].to_csv(
    'outputs/high_expense_transactions.csv',
    index=False
)

print("\nHigh expense transactions saved successfully.")
# Payment method analysis
payment_totals = df.groupby('Payment')['Amount'].sum()

plt.figure(figsize=(6, 6))
payment_totals.plot(kind='pie', autopct='%1.1f%%')

plt.title('Spending by Payment Method')
plt.ylabel('')

plt.savefig('outputs/charts/payment_method_distribution.png')
plt.show()
# Generate summary report
highest_category = category_total.idxmax()
highest_amount = category_total.max()

summary = f"""
Expense Tracker Analysis Summary
--------------------------------
Highest Spending Category: {highest_category}
Amount Spent: {highest_amount}

Overspending Threshold: {threshold}

Total Transactions: {len(df)}

Most Expensive Transaction:
{high_expenses.iloc[0]['Date']} - {high_expenses.iloc[0]['Category']} - ₹{high_expenses.iloc[0]['Amount']}
"""
with open('outputs/summary_report.txt', 'w', encoding='utf-8') as file:
    file.write(summary)

print("\nSummary report saved to outputs/summary_report.txt")