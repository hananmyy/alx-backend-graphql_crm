import datetime
import requests
from celery import shared_task

@shared_task
def generate_crm_report():
    query = """
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query}
        )
        if response.ok:
            data = response.json()["data"]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log = f"{timestamp} - Report: {data['totalCustomers']} customers, {data['totalOrders']} orders, {data['totalRevenue']} revenue\n"
            with open("/tmp/crm_report_log.txt", "a") as f:
                f.write(log)
    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{timestamp} - Error: {e}\n")