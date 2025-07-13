#!/bin/bash

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
OUTPUT=$(python3 manage.py shell << END
from crm.models import Customer
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=365)
inactive = Customer.objects.exclude(order__order_date__gte=cutoff)
deleted = inactive.count()
inactive.delete()
print(f"{deleted} customers deleted.")
END
)

echo "$TIMESTAMP - $OUTPUT" >> /tmp/customercleanuplog.txt