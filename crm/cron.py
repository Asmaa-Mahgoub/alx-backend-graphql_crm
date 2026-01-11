# crm/cron.py

from datetime import datetime
from django.conf import settings
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import traceback

def log_crm_heartbeat():
    """
    Cron job that runs every 5 minutes to log a heartbeat message confirming
    CRM application health. Optionally queries GraphQL 'hello' field.
    Logs are appended to /tmp/crm_heartbeat_log.txt
    """
    current_time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    message = f"{current_time} CRM is alive"

    # Append heartbeat to log file
    try:
        with open(log_file_path, "a") as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Failed to write heartbeat log: {e}")

    # GraphQL check using gql
    try:
        graphql_url = getattr(settings, "GRAPHQL_URL", "http://localhost:8000/graphql/")
        transport = RequestsHTTPTransport(url=graphql_url, use_json=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
            query {
                hello
            }
        """)
        result = client.execute(query)

        with open(log_file_path, "a") as f:
            if "hello" in result:
                f.write(f"{current_time} GraphQL endpoint responsive: {result['hello']}\n")
            else:
                f.write(f"{current_time} GraphQL returned unexpected data: {result}\n")

    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{current_time} GraphQL check failed: {str(e)}\n")
            f.write(f"{traceback.format_exc()}\n")

    return "Heartbeat logged successfully"


def update_low_stock():
    """
    Cron job that runs every 12 hours to update low-stock products via
    GraphQL mutation `updateLowStockProducts`.
    Logs updates to /tmp/low_stock_updates_log.txt
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = "/tmp/low_stock_updates_log.txt"

    try:
        graphql_url = getattr(settings, "GRAPHQL_URL", "http://localhost:8000/graphql/")
        transport = RequestsHTTPTransport(url=graphql_url, use_json=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    success
                    updatedProducts {
                        id
                        name
                        stock
                    }
                }
            }
        """)

        result = client.execute(mutation)

        # Log result
        with open(log_file_path, "a") as f:
            if "updateLowStockProducts" in result:
                data = result["updateLowStockProducts"]
                success = data.get("success", False)
                f.write(f"{current_time} - Success: {success}\n")
                updated = data.get("updatedProducts", [])
                for product in updated:
                    f.write(f"    Product ID: {product['id']}, Name: {product['name']}, Stock: {product['stock']}\n")
            else:
                f.write(f"{current_time} - Unexpected mutation result: {result}\n")

    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{current_time} - Mutation failed: {str(e)}\n")
            f.write(f"{traceback.format_exc()}\n")

    return "Low stock update completed"


# Optional: helpers to test cron functions locally
def test_heartbeat():
    print("Testing CRM heartbeat...")
    result = log_crm_heartbeat()
    print(result)
    print("Check log file: /tmp/crm_heartbeat_log.txt")
    return result

def test_low_stock():
    print("Testing Low Stock Update...")
    result = update_low_stock()
    print(result)
    print("Check log file: /tmp/low_stock_updates_log.txt")
    return result

