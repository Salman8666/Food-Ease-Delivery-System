import csv
from io import StringIO

def generate_sales_csv(orders_data):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Order ID', 'Total Amount', 'Status', 'Date'])
    for order in orders_data:
        writer.writerow([order.id, order.total_amount, order.status, order.created_at])
    return output.getvalue()