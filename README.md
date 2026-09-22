# Samoa Transit

## Overview

Samoa Transit is a Python client/server transportation prototype that provides sample bus route information for locations in Samoa. The program allows users to view bus routes, search for a village or destination, and view the stops on a selected route.

The client communicates with the server using TCP sockets. The client sends requests to the server, the server processes those requests, and the server sends the requested information back to the client.

I created this software because transportation information in Samoa can be difficult to find in one place. My long-term goal is to eventually create a Samoa transit application that could help local passengers and visitors better understand routes, stops, and travel information.

The village names used in this project are real Samoa locations. The bus routes, stops, and travel-time estimates are sample data created for this prototype and are not official bus schedules.

[Software Demo Video](https://www.youtube.com/watch?v=lHVscLjTroQ)

## Development Environment

I developed this software using IntelliJ IDEA and Python.

The program uses Python socket programming to demonstrate TCP client/server communication. The server listens for incoming client connections on `127.0.0.1` using port `5000`. The client connects to the server and sends requests based on the user's menu selection.

The project demonstrates socket programming, client/server communication, sending and receiving data, functions, conditional statements, loops, lists, dictionaries, and string processing.

## How to Run

The program requires two terminals running in the project folder.

### Start the Server

Open the first terminal and run:

    python networking_server.py

The server should display:

    SAMOA TRANSIT NETWORK SERVER
    Listening on 127.0.0.1:5000
    Waiting for clients...

Leave the server running.

### Start the Client

Open a second terminal in the same project folder and run:

    python networking_client.py

The client will display the following menu:

    === Samoa Transit Network Client ===
    1. View all bus routes
    2. Search for a village or destination
    3. View stops on a route
    4. Exit

### Available Features

1. View all bus routes
2. Search for a village or destination
3. View stops on a route

The client sends requests to the server, and the server returns the appropriate information.

## Networking

This project uses TCP socket communication between a client and server.

The server listens for connections on `127.0.0.1:5000`. The client connects to the server and sends requests based on the user's selected menu option.

The server processes three main types of requests:

- View all available bus routes.
- Search for a village or destination.
- View stops for a selected bus route.

The server sends the results back to the client, which displays the information to the user.

This demonstrates how a client and server communicate by connecting, sending requests, processing information, and returning responses.

## Future Improvements

Future versions of Samoa Transit could include:

- More complete bus routes and stops throughout Samoa.
- Real-time bus information.
- A database for storing routes and stops.
- A graphical or web-based user interface.
- Mobile application support.
- Official transportation data if it becomes available.

## Useful Websites

* [Python Documentation](https://docs.python.org/3/)
* [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
* [IntelliJ IDEA Documentation](https://www.jetbrains.com/help/idea/)
* [GitHub](https://github.com/)
* [Samoa Transit GitHub Repository](https://github.com/cahfua/samoa-transit)