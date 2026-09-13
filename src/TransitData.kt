// Creates the sample Upolu routes used by the Samoa Transit prototype.
// Village names are real Samoa place names, but the routes and travel times
// are demonstration data only and are not official bus schedules.
fun createSampleRoutes(): MutableList<BusRoute> {
    return mutableListOf(
        BusRoute(
            routeName = "Apia to Faleolo",
            origin = "Apia",
            destination = "Faleolo",
            stops = mutableListOf(
                "Apia",
                "Vailoa",
                "Vaitele",
                "Faleula",
                "Leauvaa",
                "Malie",
                "Nofoalii",
                "Faleolo"
            ),
            estimatedMinutes = 45
        ),

        BusRoute(
            routeName = "Apia to Mulifanua",
            origin = "Apia",
            destination = "Mulifanua",
            stops = mutableListOf(
                "Apia",
                "Vailoa",
                "Vaitele",
                "Faleula",
                "Leauvaa",
                "Malie",
                "Nofoalii",
                "Faleolo",
                "Mulifanua"
            ),
            estimatedMinutes = 55
        ),

        BusRoute(
            routeName = "Apia to Falefa",
            origin = "Apia",
            destination = "Falefa",
            stops = mutableListOf(
                "Apia",
                "Matautu",
                "Laulii",
                "Luatuanuu",
                "Solosolo",
                "Saoluafata",
                "Falefa"
            ),
            estimatedMinutes = 50
        ),

        BusRoute(
            routeName = "Apia to Lalomanu",
            origin = "Apia",
            destination = "Lalomanu",
            stops = mutableListOf(
                "Apia",
                "Vailima",
                "Tiavi",
                "Lotofaga",
                "Saleapaga",
                "Lalomanu"
            ),
            estimatedMinutes = 75
        ),

        BusRoute(
            routeName = "Apia to Siumu",
            origin = "Apia",
            destination = "Siumu",
            stops = mutableListOf(
                "Apia",
                "Vailima",
                "Tiavi",
                "Siumu"
            ),
            estimatedMinutes = 45
        ),

        BusRoute(
            routeName = "Apia to Lefaga",
            origin = "Apia",
            destination = "Lefaga",
            stops = mutableListOf(
                "Apia",
                "Vailoa",
                "Vaitele",
                "Tafaigata",
                "Safaatoa",
                "Lefaga"
            ),
            estimatedMinutes = 60
        )
    )
}