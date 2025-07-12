import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Set up GraphQL transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range for pending orders
today = datetime.date.today()
last_week = today - datetime.timedelta(days=7)

query = gql("""
query {
  pendingOrders(startDate: "%s", endDate: "%s") {
    id
    customerEmail
  }
}
""" % (last_week.isoformat(), today.isoformat()))

try:
    result = client.execute(query)
    orders = result.get("pendingOrders", [])

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            log_file.write(f"{timestamp} - Order ID: {order['id']}, Email: {order['customerEmail']}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Reminder job failed: {e}")