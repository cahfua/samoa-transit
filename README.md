
# Samoa Transit

## Overview

Samoa Transit is a transportation software prototype that provides sample bus route information for locations in Samoa. The program allows users to view bus routes, search for villages or destinations, and view stops along selected routes.

I created this software because transportation information in Samoa can be difficult to find in one place. My long-term goal is to eventually create a Samoa transit application that could help local passengers and visitors better understand routes, stops, and travel information.

The project has been developed through three programming modules:

- Module 1: Kotlin console application.
- Module 2: Python networking using TCP client/server communication.
- Module 3: SQL relational database using Python and SQLite.

For Module 3, I expanded Samoa Transit by creating a relational database to store and manage bus routes and stops. Users can add, view, search, update, and delete information through a console menu.

The village names are real locations in Samoa. However, the routes, stops, and estimated travel times are sample data created for this prototype and are not official bus schedules.

## Software Demo Videos

Module 2 - Networking:

[Watch Module 2 Demonstration](https://www.youtube.com/watch?v=lHVscLjTroQ)

Module 3 - SQL Relational Databases:

[Watch Module 3 Demonstration](https://youtu.be/9yh8OpbxHuI?si=cC8UY1BD9zRfDVel)

## Development Environment

I developed this software using IntelliJ IDEA, Python 3, SQLite, and Kotlin.

For Module 3, I used Python's built-in sqlite3 library to create and manage a relational database.

The Python program builds and executes SQL commands, retrieves results from the database, and displays the information through a console menu.

The project demonstrates SQL, relational databases, primary keys, foreign keys, functions, loops, conditional statements, user input, and data management.

## Module 3 - SQL Relational Databases

### Purpose

The purpose of this module is to learn how to create and use a relational database with Python.

In my previous modules, the bus route information was stored directly in the program. For this module, I wanted to create a database that could store the information separately and allow users to make changes.

Using a relational database makes it easier to organize routes and stops and manage their relationships.

### Database Structure

The program creates a SQLite database named `samoa_transit.db`.

The database contains two related tables.

#### Routes Table

- route_id: Primary key used to identify each route.
- route_name: Name of the bus route.
- origin: Starting village.
- destination: Destination village.
- estimated_minutes: Estimated travel time in minutes.

#### Stops Table

- stop_id: Primary key used to identify each stop.
- route_id: Foreign key connecting each stop to a route.
- stop_name: Name of the village or bus stop.
- stop_order: Position of the stop along the route.

The relationship between these tables allows one route to contain multiple stops.

The database uses foreign keys and ON DELETE CASCADE so that deleting a route also removes its associated stops.

### SQL Operations

The program demonstrates the following SQL commands:

1. CREATE TABLE - Creates the routes and stops tables.
2. INSERT - Adds new bus routes and stops.
3. SELECT - Retrieves routes and searches for information.
4. UPDATE - Changes the estimated travel time of a route.
5. DELETE - Removes a route and its associated stops.
6. INNER JOIN - Combines route and stop information from two related tables.
7. LEFT JOIN - Displays routes with their associated stops.
8. COUNT - Counts the total number of routes and stops.
9. AVG - Calculates the average estimated travel time.

All SQL commands are executed through the Python program using the sqlite3 library.

### Features

The Module 3 application allows users to:

1. View all available bus routes.
2. Search for routes by name or village.
3. View the stops for a selected route.
4. Add a new bus route.
5. Update a route's estimated travel time.
6. Delete an existing route.
7. Add an intermediate stop to a route.
8. View all routes and stops using a SQL JOIN.
9. Display database statistics.

### How to Run Module 3

1. Install Python 3 if it is not already installed.
2. Open the SamoaTransit project in IntelliJ IDEA.
3. Open the terminal in the main project folder.
4. Run the following command:

```bash
python database_main.py
```

The program automatically creates the SQLite database and tables if they do not already exist.

When the routes table is empty, the program adds six sample Samoa Transit routes and their stops.

The main menu allows users to select the different database operations.

No additional Python packages are required.

### Main Menu

```text
===== SAMOA TRANSIT DATABASE =====

1. View all routes (SELECT)
2. Search routes (SELECT)
3. View route stops (JOIN)
4. Add a new route (INSERT)
5. Update route travel time (UPDATE)
6. Delete a route (DELETE)
7. Add a stop to a route (INSERT)
8. View all routes and stops (JOIN)
9. Database statistics (COUNT / AVG)
0. Exit
```

### Example Usage

A user can select option 1 to view the six sample routes.

Option 2 allows the user to search for a village such as Faleolo.

Option 4 allows the user to add a new bus route. The program saves the information in the SQLite database.

Option 5 allows the user to update the estimated travel time.

Option 6 allows the user to delete a route.

Option 8 demonstrates a SQL JOIN by displaying routes together with their associated stops.

### Module 3 Source Files

- `database_main.py` - Contains the main menu, user input, and functions that interact with the database.
- `transit_database.py` - Contains the database connection, table creation, sample data, and SQL operations.
- `samoa_transit.db` - SQLite database generated automatically when the program runs.

## Module 2 - Networking

### Overview

Module 2 uses a Python client/server application to demonstrate TCP socket communication.

The client sends requests to the server, the server processes the requests, and the server returns the requested information.

The networking application uses sample data stored in `transit_data.py` and operates separately from the Module 3 database application.

### Development Environment

The networking application was developed using IntelliJ IDEA and Python.

The program uses Python socket programming to demonstrate TCP client/server communication.

The server listens for incoming client connections on `127.0.0.1` using port `5000`.

The client connects to the server and sends requests based on the user's menu selection.

### How to Run Module 2

The program requires two terminals running in the project folder.

#### Start the Server

Open the first terminal and run:

```bash
python networking_server.py
```

The server should display:

```text
SAMOA TRANSIT NETWORK SERVER
Listening on 127.0.0.1:5000
Waiting for clients...
```

Leave the server running.

#### Start the Client

Open a second terminal in the same project folder and run:

```bash
python networking_client.py
```

The client displays the following menu:

```text
=== Samoa Transit Network Client ===

1. View all bus routes
2. Search for a village or destination
3. View stops on a route
4. Exit
```

### Networking Features

The client can:

1. View all available bus routes.
2. Search for a village or destination.
3. View stops for a selected bus route.

The client sends requests to the server using TCP sockets.

The server processes the requests and sends the appropriate information back to the client.

This module demonstrates client/server communication, JSON messages, socket programming, sending and receiving data, and processing user requests.

## Module 1 - Kotlin

The original Samoa Transit application was developed using Kotlin.

The application provides a console menu that allows users to:

1. View available bus routes.
2. Search for destinations.
3. View stops along a selected route.
4. Estimate travel times.
5. Add stops to existing routes.

The Kotlin source files are located in the `src` folder.

## Project Files

```text
SamoaTransit/
|
|-- src/
|   |-- BusRoute
|   |-- Main.kt
|   |-- TransitData.kt
|
|-- database_main.py
|-- transit_database.py
|-- networking_client.py
|-- networking_server.py
|-- transit_data.py
|-- README.md
|-- .gitignore
```

The SQLite database file `samoa_transit.db` is generated automatically when the database program runs.

## Future Improvements

Future improvements could include:

- Connecting the networking client/server to the SQLite database.
- Adding more bus routes and stops throughout Samoa.
- Including real-time bus information.
- Creating a graphical or web-based user interface.
- Developing a mobile application.
- Adding official transportation information if it becomes available.

## Useful Websites

- [Python Documentation](https://docs.python.org/3/)
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite Foreign Keys](https://www.sqlite.org/foreignkeys.html)
- [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
- [IntelliJ IDEA Documentation](https://www.jetbrains.com/help/idea/)
- [GitHub](https://github.com/)
- [Samoa Transit GitHub Repository](https://github.com/cahfua/samoa-transit)

## Author

Celestine Ahfua

CSE 310 - Applied Programming

BYU-Pathway Worldwide