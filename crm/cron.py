import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    status = "CRM is alive"

    # Optional: ping GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"}
        )
        if response.ok:
            status += f" | GraphQL says: {response.json()['data']['hello']}"
        else:
            status += " | GraphQL ping failed"
    except Exception as e:
        status += f" | GraphQL error: {e}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - {status}\n")





def update_low_stock():
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

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = "/tmp/low_stock_updates_log.txt"

        if response.ok:
            data = response.json()["data"]["updateLowStockProducts"]
            with open(log_path, "a") as log_file:
                log_file.write(f"{timestamp} - {data['message']}\n")
                for product in data["updated"]:
                    log_file.write(f"{timestamp} - {product}\n")
        else:
            with open(log_path, "a") as log_file:
                log_file.write(f"{timestamp} - Mutation failed: {response.status_code}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - Error: {e}\n")