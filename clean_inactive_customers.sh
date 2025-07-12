#!/bin/bash
# Delete inactive customers with no orders in the past year

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
OUTPUT=$(python3 manage.py shell << END
from crm.models import Customer, Order
from datetime import timedelta, datetime

cutoff_date = datetime.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(order__order_date__gte=cutoff_date)

count = inactive_customers.count()
inactive_customers.delete()

print(f"{count} customers deleted.")
END
)

echo "$TIMESTAMP - $OUTPUT" >> /tmp/customer_cleanup_log.txt