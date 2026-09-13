// Represents one bus route in the Samoa Transit prototype.
// The route name, origin, and destination do not change, while the estimated
// travel time and stop list can be updated while the program is running.
class BusRoute(
    val routeName: String,
    val origin: String,
    val destination: String,
    val stops: MutableList<String>,
    var estimatedMinutes: Int
) {
    // Returns a short description of the route for menus and search results.
    fun summary(): String {
        return "$routeName | $origin to $destination | About $estimatedMinutes minutes"
    }

    // Adds a stop before the final destination if the stop is not already listed.
    fun addStopBeforeDestination(stopName: String): Boolean {
        val alreadyExists = stops.any { it.equals(stopName, ignoreCase = true) }

        if (alreadyExists) {
            return false
        }

        val insertPosition = if (stops.isEmpty()) 0 else stops.lastIndex
        stops.add(insertPosition, stopName)

        estimatedMinutes += 5
        return true
    }

    // Finds a stop by name without requiring matching capitalization.
    fun findStopIndex(stopName: String): Int {
        return stops.indexOfFirst {
            it.equals(stopName.trim(), ignoreCase = true)
        }
    }
}