
import sqlite3

from transit_database import (
    initialize_database,
    seed_database,
    get_all_routes,
    search_routes,
    get_route,
    get_route_stops,
    get_all_routes_with_stops,
    add_route,
    update_route_time,
    delete_route,
    add_stop,
    get_statistics
)


def print_header():
    """Display the program title and purpose."""
    print("\n" + "=" * 45)
    print("       SAMOA TRANSIT DATABASE")
    print("=" * 45)
    print("Bus route and stop management using SQLite")


def display_menu():
    """Show all available database operations."""
    print("\nMAIN MENU")
    print("1. View all routes (SELECT)")
    print("2. Search routes (SELECT)")
    print("3. View route stops (JOIN)")
    print("4. Add a new route (INSERT)")
    print("5. Update route travel time (UPDATE)")
    print("6. Delete a route (DELETE)")
    print("7. Add a stop to a route (INSERT)")
    print("8. View all routes and stops (JOIN)")
    print("9. Database statistics (COUNT / AVG)")
    print("0. Exit")


def get_positive_number(prompt):
    """Ask for a positive whole number and validate the input."""
    while True:
        try:
            number = int(input(prompt))

            if number > 0:
                return number

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_required_text(prompt):
    """Read text and reject empty input."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def print_routes(routes):
    """Display a list of routes in a readable format."""
    if not routes:
        print("\nNo routes found.")
        return

    print("\nAVAILABLE BUS ROUTES")
    print("-" * 55)

    for route in routes:
        print(f"ID: {route['route_id']}")
        print(f"Route: {route['route_name']}")
        print(f"From: {route['origin']}")
        print(f"To: {route['destination']}")
        print(f"Estimated time: {route['estimated_minutes']} minutes")
        print("-" * 55)


def view_all_routes():
    """Retrieve and display every route from the database."""
    routes = get_all_routes()
    print_routes(routes)


def search_for_route():
    """Search for a bus route by village or route name."""
    keyword = get_required_text("\nEnter a village or route name: ")
    routes = search_routes(keyword)
    print_routes(routes)


def view_stops():
    """Display the ordered stops of a selected route using a JOIN."""
    view_all_routes()
    route_id = get_positive_number("\nEnter route ID: ")

    route = get_route(route_id)

    if route is None:
        print("Route not found.")
        return

    stops = get_route_stops(route_id)

    print(f"\nSTOPS FOR {route['route_name']}")
    print(f"Estimated travel time: {route['estimated_minutes']} minutes")

    if not stops:
        print("No stops have been recorded.")
        return

    for stop in stops:
        print(f"{stop['stop_order']}. {stop['stop_name']}")


def create_route():
    """Collect route details and insert a new route into SQLite."""
    print("\nADD NEW ROUTE")

    name = get_required_text("Route name: ")
    origin = get_required_text("Starting village: ")
    destination = get_required_text("Destination village: ")
    minutes = get_positive_number("Estimated travel time (minutes): ")

    try:
        route_id = add_route(name, origin, destination, minutes)
        print(f"\nRoute added successfully with ID {route_id}.")
        print("Starting and destination stops were also added.")

    except sqlite3.IntegrityError:
        print("Could not add route. The route name may already exist.")


def change_route_time():
    """Change the estimated travel time of an existing route."""
    view_all_routes()
    route_id = get_positive_number("\nEnter route ID to update: ")

    route = get_route(route_id)

    if route is None:
        print("Route not found.")
        return

    print(f"Current travel time: {route['estimated_minutes']} minutes")
    new_minutes = get_positive_number("New travel time (minutes): ")

    if update_route_time(route_id, new_minutes):
        print("Route travel time updated successfully.")
    else:
        print("No route was updated.")


def remove_route():
    """Confirm and delete a route and its related stops."""
    view_all_routes()
    route_id = get_positive_number("\nEnter route ID to delete: ")

    route = get_route(route_id)

    if route is None:
        print("Route not found.")
        return

    print(f"You selected: {route['route_name']}")
    confirm = input("Type YES to permanently delete this route: ").strip()

    if confirm == "YES":
        if delete_route(route_id):
            print("Route and related stops deleted successfully.")
        else:
            print("No route was deleted.")
    else:
        print("Deletion cancelled.")


def insert_stop():
    """Add an intermediate village before the route's destination."""
    view_all_routes()
    route_id = get_positive_number("\nEnter route ID: ")

    route = get_route(route_id)

    if route is None:
        print("Route not found.")
        return

    stop_name = get_required_text("New intermediate stop: ")

    if add_stop(route_id, stop_name):
        print(f"{stop_name} was added to {route['route_name']}.")
    else:
        print("Could not add the stop.")


def view_join_results():
    """Show routes and their stops using a LEFT JOIN query."""
    records = get_all_routes_with_stops()

    if not records:
        print("\nThe database contains no routes.")
        return

    current_route_id = None

    for record in records:
        if record["route_id"] != current_route_id:
            current_route_id = record["route_id"]

            print("\n" + "-" * 50)
            print(f"Route: {record['route_name']}")
            print(f"From: {record['origin']}")
            print(f"To: {record['destination']}")
            print(f"Time: {record['estimated_minutes']} minutes")
            print("Stops:")

        if record["stop_name"] is not None:
            print(f"  {record['stop_order']}. {record['stop_name']}")
        else:
            print("  No stops recorded.")


def show_statistics():
    """Display SQL aggregate results for the transit database."""
    route_count, stop_count, average = get_statistics()

    print("\nDATABASE STATISTICS")
    print(f"Total routes: {route_count}")
    print(f"Total stops: {stop_count}")

    if average is not None:
        print(f"Average route time: {average:.1f} minutes")
    else:
        print("Average route time: Not available")


def main():
    """Initialize the database and run the interactive program."""
    initialize_database()
    seed_database()

    print_header()

    while True:
        display_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_all_routes()
        elif choice == "2":
            search_for_route()
        elif choice == "3":
            view_stops()
        elif choice == "4":
            create_route()
        elif choice == "5":
            change_route_time()
        elif choice == "6":
            remove_route()
        elif choice == "7":
            insert_stop()
        elif choice == "8":
            view_join_results()
        elif choice == "9":
            show_statistics()
        elif choice == "0":
            print("\nThank you for using Samoa Transit!")
            break
        else:
            print("Invalid option. Please choose from the menu.")


if __name__ == "__main__":
    main()