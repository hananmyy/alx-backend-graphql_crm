import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    status = "CRM is alive"

    # GraphQL endpoint setup
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Ping the hello field
    try:
        query = gql("{ hello }")
        response = client.execute(query)
        status += f" | GraphQL says: {response.get('hello', 'No response')}"
    except Exception as e:
        status += f" | GraphQL error: {e}"

    # Log result
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - {status}\n")





def update_low_stock():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mutation = """
    mutation {
      updateLowStockProducts {
        updated
        message
      }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation}
        )
        log_path = "/tmp/lowstockupdates_log.txt"

        if response.ok:
            data = response.json()["data"]["updateLowStockProducts"]
            with open(log_path, "a") as log:
                log.write(f"{timestamp} - {data['message']}\n")
                for name in data["updated"]:
                    log.write(f"{timestamp} - Restocked: {name}\n")
        else:
            with open(log_path, "a") as log:
                log.write(f"{timestamp} - Mutation failed: {response.status_code}\n")

    except Exception as e:
        with open("/tmp/lowstockupdates_log.txt", "a") as log:
            log.write(f"{timestamp} - Exception: {e}\n")