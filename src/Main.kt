// Samoa Transit
// A console-based prototype for exploring sample bus routes and stops in Upolu.

// Displays the program title and explains that the route information is sample data.
fun printBanner() {
    println("========================================")
    println("             SAMOA TRANSIT")
    println("========================================")
    println("Prototype route finder for Upolu, Samoa")
    println("Route times are sample estimates only.")
}

// Displays the main menu options available to the user.
fun displayMenu() {
    println()
    println("1. View all bus routes")
    println("2. Search for a village or destination")
    println("3. View stops on a route")
    println("4. Estimate travel time to a stop")
    println("5. Add a stop to a route")
    println("6. About this prototype")
    println("7. Exit")
    print("Choose an option: ")
}

// Displays every route currently stored in the route collection.
fun viewRoutes(routes: List<BusRoute>) {
    println("\n--- Available Bus Routes ---")

    for ((index, route) in routes.withIndex()) {
        println("${index + 1}. ${route.summary()}")
    }
}

// Searches all route stop lists for a village or destination entered by the user.
fun searchDestination(routes: List<BusRoute>) {
    print("\nEnter a village or destination: ")
    val searchText = readln().trim()

    if (searchText.isBlank()) {
        println("Please enter a village name.")
        return
    }

    val matchingRoutes = routes.filter { route ->
        route.stops.any { stop ->
            stop.contains(searchText, ignoreCase = true)
        }
    }

    if (matchingRoutes.isEmpty()) {
        println("No sample routes currently include '$searchText'.")
        println("Remember, this prototype does not contain every village in Samoa yet.")
    } else {
        println("\nRoutes that include '$searchText':")

        for (route in matchingRoutes) {
            println("- ${route.summary()}")
        }
    }
}

// Displays each stop on a route selected by the user.
fun viewRouteStops(routes: List<BusRoute>) {
    val route = selectRoute(routes) ?: return

    println("\n--- Stops for ${route.routeName} ---")

    for ((index, stop) in route.stops.withIndex()) {
        println("${index + 1}. $stop")
    }
}

// Estimates travel time from the route origin to a selected stop.
// The estimate divides the route's total time across the number of route segments.
fun estimateTravelTime(routes: List<BusRoute>) {
    val route = selectRoute(routes) ?: return

    println("\nStops on ${route.routeName}:")

    for (stop in route.stops) {
        println("- $stop")
    }

    print("Enter the stop you want to travel to: ")
    val stopName = readln().trim()

    val stopIndex = route.findStopIndex(stopName)

    if (stopIndex == -1) {
        println("'$stopName' is not listed on this sample route.")
        return
    }

    if (stopIndex == 0) {
        println("You are already at ${route.origin}.")
        return
    }

    val totalSegments = route.stops.size - 1

    val minutesPerSegment =
        route.estimatedMinutes.toDouble() / totalSegments

    val estimatedTime =
        (minutesPerSegment * stopIndex).toInt()

    println(
        "Estimated travel time from ${route.origin} " +
                "to ${route.stops[stopIndex]}: " +
                "about $estimatedTime minutes."
    )
}

// Adds a new stop to a selected route and updates the route's sample travel time.
// This function demonstrates modification of a Kotlin MutableList collection.
fun addStopToRoute(routes: MutableList<BusRoute>) {
    val route = selectRoute(routes) ?: return

    print("Enter the village/stop name to add: ")
    val newStop = readln().trim()

    if (newStop.isBlank()) {
        println("A stop name cannot be blank.")
        return
    }

    val wasAdded =
        route.addStopBeforeDestination(newStop)

    if (wasAdded) {
        println("$newStop was added to ${route.routeName}.")
        println(
            "The updated sample travel time is " +
                    "${route.estimatedMinutes} minutes."
        )
        println(
            "This change lasts only while the program is running."
        )
    } else {
        println("$newStop is already listed on this route.")
    }
}

// Lets the user choose a route by number and returns the selected BusRoute object.
// It returns null when the user's input is invalid.
fun selectRoute(routes: List<BusRoute>): BusRoute? {
    viewRoutes(routes)

    print("Select a route number: ")

    val selection =
        readln().toIntOrNull()

    if (
        selection == null ||
        selection !in 1..routes.size
    ) {
        println("Invalid route number.")
        return null
    }

    return routes[selection - 1]
}

// Displays the purpose and limitations of the current Samoa Transit prototype.
fun showAbout() {
    println("\n--- About Samoa Transit ---")

    println(
        "Samoa Transit is a learning prototype created in Kotlin."
    )

    println(
        "The long-term idea is to make public transportation " +
                "easier to understand"
    )

    println(
        "by showing routes, villages, stops, " +
                "and estimated travel times."
    )

    println()

    println(
        "This console version uses a small set of Upolu " +
                "locations so the core"
    )

    println(
        "programming ideas can be tested before building " +
                "a larger mobile version."
    )

    println(
        "The routes and times in this program are " +
                "demonstration data, not official schedules."
    )
}

// Starts the program, creates the sample route collection, and keeps the menu running
// until the user chooses the Exit option.
fun main() {
    val routes = createSampleRoutes()

    var running = true

    printBanner()

    while (running) {
        displayMenu()

        when (readln().trim()) {

            "1" -> {
                viewRoutes(routes)
            }

            "2" -> {
                searchDestination(routes)
            }

            "3" -> {
                viewRouteStops(routes)
            }

            "4" -> {
                estimateTravelTime(routes)
            }

            "5" -> {
                addStopToRoute(routes)
            }

            "6" -> {
                showAbout()
            }

            "7" -> {
                println()
                println("Fa'afetai for using Samoa Transit!")
                running = false
            }

            else -> {
                println(
                    "Invalid option. Please choose a number from 1 to 7."
                )
            }
        }
    }
}