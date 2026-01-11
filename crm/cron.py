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
    # Get current timestamp
    current_time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    message = f"{current_time} CRM is alive"

    # Append heartbeat to log file
    try:
        with open(log_file_path, "a") as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Failed to write heartbeat log: {e}")

    # -----------------------------
    # GraphQL check using gql
    # -----------------------------
    try:
        graphql_url = getattr(settings, "GRAPHQL_URL", "http://localhost:8000/graphql/")
        transport = RequestsHTTPTransport(url=graphql_url, use_json=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # GraphQL query
        query = gql("""
            query {
                hello
            }
        """)

        result = client.execute(query)

        # Append GraphQL response to log
        with open(log_file_path, "a") as f:
            if "hello" in result:
                f.write(f"{current_time} GraphQL endpoint responsive: {result['hello']}\n")
            else:
                f.write(f"{current_time} GraphQL returned unexpected data: {result}\n")

    except Exception as e:
        # Log GraphQL errors
        with open(log_file_path, "a") as f:
            f.write(f"{current_time} GraphQL check failed: {str(e)}\n")
            f.write(f"{traceback.format_exc()}\n")

    return "Heartbeat logged successfully"


# Optional: helper to test heartbeat locally
def test_heartbeat():
    """Run this in Django shell to test the cron function"""
    print("Testing CRM heartbeat...")
    result = log_crm_heartbeat()
    print(result)
    print("Check log file: /tmp/crm_heartbeat_log.txt")
    return result
