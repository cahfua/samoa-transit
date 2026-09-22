"""TCP server for the Samoa Transit networking module."""

import json
import socket
import threading

from transit_data import SAMPLE_ROUTES, route_summary

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096


# Sends one JSON response followed by a newline so the client knows the message is complete.
def send_json(connection, data):
    """Serialize a response as JSON and send it through the TCP connection."""
    message = json.dumps(data) + "\n"
    connection.sendall(message.encode("utf-8"))


# Handles the LIST_ROUTES request by returning all available route summaries.
def handle_list_routes():
    """Return the available Samoa Transit routes."""
    return {
        "success": True,
        "type": "route_list",
        "routes": [route_summary(route) for route in SAMPLE_ROUTES],
    }


# Handles a destination search by checking every stop on every sample route.
def handle_search(query):
    """Search route stops for a village or destination name."""
    search_text = str(query).strip()

    if not search_text:
        return {
            "success": False,
            "error": "Please provide a village or destination to search for.",
        }

    matches = []

    for route in SAMPLE_ROUTES:
        matching_stops = [
            stop
            for stop in route["stops"]
            if search_text.lower() in stop.lower()
        ]

        if matching_stops:
            matches.append(
                {
                    "route_name": route["route_name"],
                    "matching_stops": matching_stops,
                    "summary": route_summary(route),
                }
            )

    return {
        "success": True,
        "type": "search_results",
        "query": search_text,
        "matches": matches,
    }


# Handles a stop request by returning the ordered stops for a selected route.
def handle_stops(route_number):
    """Return the stops for the requested route number."""
    try:
        number = int(route_number)
    except (TypeError, ValueError):
        return {
            "success": False,
            "error": "Route number must be a number.",
        }

    if number < 1 or number > len(SAMPLE_ROUTES):
        return {
            "success": False,
            "error": "That route number does not exist.",
        }

    route = SAMPLE_ROUTES[number - 1]

    return {
        "success": True,
        "type": "route_stops",
        "route_name": route["route_name"],
        "origin": route["origin"],
        "destination": route["destination"],
        "estimated_minutes": route["estimated_minutes"],
        "stops": route["stops"],
    }


# Chooses which server function should process a client's request.
def process_request(request):
    """Process a JSON request and return a JSON-ready response dictionary."""
    if not isinstance(request, dict):
        return {"success": False, "error": "Request must be a JSON object."}

    request_type = str(request.get("type", "")).upper()

    if request_type == "LIST_ROUTES":
        return handle_list_routes()

    if request_type == "SEARCH":
        return handle_search(request.get("query", ""))

    if request_type == "STOPS":
        return handle_stops(request.get("route_number"))

    return {
        "success": False,
        "error": "Unknown request type. Use LIST_ROUTES, SEARCH, or STOPS.",
    }


# Handles one connected client and allows several requests before the client disconnects.
def handle_client(connection, address):
    """Receive and respond to newline-delimited JSON requests from one client."""
    print(f"Client connected: {address}")

    try:
        buffer = ""

        while True:
            chunk = connection.recv(BUFFER_SIZE)

            if not chunk:
                break

            buffer += chunk.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                if not line.strip():
                    continue

                try:
                    request = json.loads(line)
                    response = process_request(request)
                except json.JSONDecodeError:
                    response = {
                        "success": False,
                        "error": "The server received invalid JSON.",
                    }

                send_json(connection, response)

    except ConnectionResetError:
        print(f"Client disconnected unexpectedly: {address}")
    finally:
        connection.close()
        print(f"Client disconnected: {address}")


# Creates the TCP server, waits for client connections, and starts a thread for each client.
def start_server():
    """Start the Samoa Transit TCP server on the local computer."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("========================================")
        print("       SAMOA TRANSIT NETWORK SERVER")
        print("========================================")
        print(f"Listening on {HOST}:{PORT}")
        print("Waiting for clients...\n")

        while True:
            connection, address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, address),
                daemon=True,
            )
            client_thread.start()


if __name__ == "__main__":
    start_server()