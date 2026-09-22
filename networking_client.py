"""Command-line TCP client for the Samoa Transit networking module."""

import json
import socket

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096


# Opens a TCP connection to the server and returns the socket object.
def connect_to_server():
    """Connect to the local Samoa Transit server."""
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, PORT))
    return connection


# Sends a JSON request followed by a newline, which marks the end of the message.
def send_request(connection, request):
    """Send one request to the server and return its decoded JSON response."""
    message = json.dumps(request) + "\n"
    connection.sendall(message.encode("utf-8"))

    response_data = b""

    while b"\n" not in response_data:
        chunk = connection.recv(BUFFER_SIZE)

        if not chunk:
            raise ConnectionError("The server closed the connection.")

        response_data += chunk

    response_line = response_data.split(b"\n", 1)[0]
    return json.loads(response_line.decode("utf-8"))


# Prints every route returned by the LIST_ROUTES server request.
def display_routes(response):
    """Display all routes returned from the server."""
    print("\n--- Available Bus Routes ---")

    if not response.get("success"):
        print(response.get("error", "Unknown server error."))
        return

    for index, route in enumerate(response.get("routes", []), start=1):
        print(f"{index}. {route}")


# Sends a village or destination to the server and displays matching routes.
def search_destination(connection):
    """Ask the server to search route stops for a destination."""
    search_text = input("\nEnter a village or destination: ").strip()

    request = {
        "type": "SEARCH",
        "query": search_text,
    }

    response = send_request(connection, request)

    if not response.get("success"):
        print(response.get("error", "Unknown server error."))
        return

    matches = response.get("matches", [])

    if not matches:
        print(f"No sample routes currently include '{search_text}'.")
        return

    print(f"\nRoutes that include '{search_text}':")

    for match in matches:
        print(f"- {match['summary']}")
        print(f"  Matching stops: {', '.join(match['matching_stops'])}")


# Asks the server for the stops belonging to a selected route.
def view_route_stops(connection):
    """Request and display the stops for one route."""
    route_number_text = input("\nEnter route number: ").strip()

    request = {
        "type": "STOPS",
        "route_number": route_number_text,
    }

    response = send_request(connection, request)

    if not response.get("success"):
        print(response.get("error", "Unknown server error."))
        return

    print(f"\n--- Stops for {response['route_name']} ---")
    print(
        f"{response['origin']} to {response['destination']} "
        f"| About {response['estimated_minutes']} minutes"
    )

    for index, stop in enumerate(response["stops"], start=1):
        print(f"{index}. {stop}")


# Displays the client menu before each request.
def display_menu():
    """Display the available client options."""
    print("\n=== Samoa Transit Network Client ===")
    print("1. View all bus routes")
    print("2. Search for a village or destination")
    print("3. View stops on a route")
    print("4. Exit")
    return input("Choose an option: ").strip()


# Runs the client menu and sends requests to the server until the user exits.
def start_client():
    """Start the Samoa Transit networking client."""
    print("Connecting to Samoa Transit server...")

    try:
        with connect_to_server() as connection:
            print("Connected successfully.")

            running = True

            while running:
                choice = display_menu()

                if choice == "1":
                    response = send_request(
                        connection,
                        {"type": "LIST_ROUTES"},
                    )
                    display_routes(response)

                elif choice == "2":
                    search_destination(connection)

                elif choice == "3":
                    view_route_stops(connection)

                elif choice == "4":
                    print("Fa'afetai for using Samoa Transit Network!")
                    running = False

                else:
                    print("Invalid option. Please choose 1, 2, 3, or 4.")

    except ConnectionRefusedError:
        print(
            "Could not connect to the server. "
            "Make sure networking_server.py is running first."
        )
    except (ConnectionError, json.JSONDecodeError) as error:
        print(f"Network error: {error}")


if __name__ == "__main__":
    start_client()