
import sqlite3
from pathlib import Path

# Store the database in the same folder as this Python file.
DATABASE_PATH = Path(__file__).resolve().parent / "samoa_transit.db"

SAMPLE_ROUTES = [
    ("Apia - Faleolo", "Apia", "Faleolo", 45,
     ["Apia", "Vailoa", "Vaitele", "Faleula", "Leauvaa",
      "Malie", "Nofoalii", "Faleolo"]),
    ("Apia - Mulifanua", "Apia", "Mulifanua", 55,
     ["Apia", "Vailoa", "Vaitele", "Faleula", "Leauvaa",
      "Malie", "Nofoalii", "Faleolo", "Mulifanua"]),
    ("Apia - Falefa", "Apia", "Falefa", 50,
     ["Apia", "Matautu", "Laulii", "Luatuanuu",
      "Solosolo", "Saoluafata", "Falefa"]),
    ("Apia - Lalomanu", "Apia", "Lalomanu", 75,
     ["Apia", "Vailima", "Tiavi", "Lotofaga",
      "Saleapaga", "Lalomanu"]),
    ("Apia - Siumu", "Apia", "Siumu", 45,
     ["Apia", "Vailima", "Tiavi", "Siumu"]),
    ("Apia - Lefaga", "Apia", "Lefaga", 60,
     ["Apia", "Vailoa", "Vaitele", "Tafaigata",
      "Safaatoa", "Lefaga"]),
]


def connect_database():
    """Open the SQLite database and enable foreign key relationships."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create the routes and stops tables if they do not exist."""
    with connect_database() as connection:
        connection.execute("""
                           CREATE TABLE IF NOT EXISTS routes (
                                                                 route_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                 route_name TEXT NOT NULL UNIQUE,
                                                                 origin TEXT NOT NULL,
                                                                 destination TEXT NOT NULL,
                                                                 estimated_minutes INTEGER NOT NULL
                                                                 CHECK (estimated_minutes > 0)
                               )
                           """)

        connection.execute("""
                           CREATE TABLE IF NOT EXISTS stops (
                                                                stop_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                route_id INTEGER NOT NULL,
                                                                stop_name TEXT NOT NULL,
                                                                stop_order INTEGER NOT NULL,
                                                                FOREIGN KEY (route_id)
                               REFERENCES routes(route_id)
                               ON DELETE CASCADE,
                               UNIQUE (route_id, stop_order)
                               )
                           """)


def seed_database():
    """Add sample routes and stops only when the database is empty."""
    with connect_database() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM routes"
        ).fetchone()[0]

        if count > 0:
            return

        for name, origin, destination, minutes, stops in SAMPLE_ROUTES:
            cursor = connection.execute("""
                                        INSERT INTO routes
                                            (route_name, origin, destination, estimated_minutes)
                                        VALUES (?, ?, ?, ?)
                                        """, (name, origin, destination, minutes))

            route_id = cursor.lastrowid

            for position, stop_name in enumerate(stops, start=1):
                connection.execute("""
                                   INSERT INTO stops
                                       (route_id, stop_name, stop_order)
                                   VALUES (?, ?, ?)
                                   """, (route_id, stop_name, position))


def get_all_routes():
    """Retrieve all routes ordered by their database ID."""
    with connect_database() as connection:
        rows = connection.execute("""
                                  SELECT route_id, route_name, origin,
                                         destination, estimated_minutes
                                  FROM routes
                                  ORDER BY route_id
                                  """).fetchall()
        return [dict(row) for row in rows]


def search_routes(search_term):
    """Find routes matching a name, origin, or destination."""
    pattern = f"%{search_term}%"

    with connect_database() as connection:
        rows = connection.execute("""
                                  SELECT route_id, route_name, origin,
                                         destination, estimated_minutes
                                  FROM routes
                                  WHERE route_name LIKE ?
                                     OR origin LIKE ?
                                     OR destination LIKE ?
                                  ORDER BY route_id
                                  """, (pattern, pattern, pattern)).fetchall()

        return [dict(row) for row in rows]


def get_route(route_id):
    """Retrieve one route using its ID."""
    with connect_database() as connection:
        row = connection.execute("""
                                 SELECT route_id, route_name, origin,
                                        destination, estimated_minutes
                                 FROM routes
                                 WHERE route_id = ?
                                 """, (route_id,)).fetchone()

        return dict(row) if row else None


def get_route_stops(route_id):
    """Use a SQL JOIN to retrieve stops with their route information."""
    with connect_database() as connection:
        rows = connection.execute("""
                                  SELECT r.route_id, r.route_name,
                                         r.estimated_minutes,
                                         s.stop_id, s.stop_name, s.stop_order
                                  FROM routes AS r
                                           INNER JOIN stops AS s
                                                      ON r.route_id = s.route_id
                                  WHERE r.route_id = ?
                                  ORDER BY s.stop_order
                                  """, (route_id,)).fetchall()

        return [dict(row) for row in rows]


def get_all_routes_with_stops():
    """Use a LEFT JOIN to show routes and their ordered stops."""
    with connect_database() as connection:
        rows = connection.execute("""
                                  SELECT r.route_id, r.route_name,
                                         r.origin, r.destination,
                                         r.estimated_minutes,
                                         s.stop_name, s.stop_order
                                  FROM routes AS r
                                           LEFT JOIN stops AS s
                                                     ON r.route_id = s.route_id
                                  ORDER BY r.route_id, s.stop_order
                                  """).fetchall()

        return [dict(row) for row in rows]


def add_route(name, origin, destination, minutes):
    """Insert a new bus route and its starting and ending stops."""
    with connect_database() as connection:
        cursor = connection.execute("""
                                    INSERT INTO routes
                                        (route_name, origin, destination, estimated_minutes)
                                    VALUES (?, ?, ?, ?)
                                    """, (name, origin, destination, minutes))

        route_id = cursor.lastrowid

        connection.executemany("""
                               INSERT INTO stops (route_id, stop_name, stop_order)
                               VALUES (?, ?, ?)
                               """, [
                                   (route_id, origin, 1),
                                   (route_id, destination, 2)
                               ])

        return route_id


def update_route_time(route_id, new_minutes):
    """Update the estimated travel time for an existing route."""
    with connect_database() as connection:
        cursor = connection.execute("""
                                    UPDATE routes
                                    SET estimated_minutes = ?
                                    WHERE route_id = ?
                                    """, (new_minutes, route_id))

        return cursor.rowcount > 0


def delete_route(route_id):
    """Delete a route and automatically delete its related stops."""
    with connect_database() as connection:
        cursor = connection.execute("""
                                    DELETE FROM routes
                                    WHERE route_id = ?
                                    """, (route_id,))

        return cursor.rowcount > 0


def add_stop(route_id, stop_name):
    """Insert a stop before the destination and reorder the final stop."""
    with connect_database() as connection:
        rows = connection.execute("""
                                  SELECT stop_id, stop_order
                                  FROM stops
                                  WHERE route_id = ?
                                  ORDER BY stop_order
                                  """, (route_id,)).fetchall()

        if not rows:
            return False

        destination_stop = rows[-1]
        destination_order = destination_stop["stop_order"]

        # Move the destination to a later position before inserting.
        connection.execute("""
                           UPDATE stops
                           SET stop_order = ?
                           WHERE stop_id = ?
                           """, (destination_order + 1, destination_stop["stop_id"]))

        connection.execute("""
                           INSERT INTO stops (route_id, stop_name, stop_order)
                           VALUES (?, ?, ?)
                           """, (route_id, stop_name, destination_order))

        return True


def get_statistics():
    """Use aggregate SQL functions to count routes and stops."""
    with connect_database() as connection:
        route_count = connection.execute(
            "SELECT COUNT(*) FROM routes"
        ).fetchone()[0]

        stop_count = connection.execute(
            "SELECT COUNT(*) FROM stops"
        ).fetchone()[0]

        average_minutes = connection.execute(
            "SELECT AVG(estimated_minutes) FROM routes"
        ).fetchone()[0]

        return route_count, stop_count, average_minutes