#!/bin/bash

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT" || exit 1

# Run Django shell command
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
OUTPUT=$(python3 manage.py shell << END
from crm.models import Customer, Order
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=365)
inactive = Customer.objects.exclude(order__order_date__gte=cutoff)
deleted = inactive.count()
inactive.delete()
print(f"{deleted} customers deleted.")
END
)

# Log result
if [ -n "$OUTPUT" ]; then
  echo "$TIMESTAMP - $OUTPUT" >> /tmp/customercleanuplog.txt
else
  echo "$TIMESTAMP - No output, possible error." >> /tmp/customercleanuplog.txt
fi