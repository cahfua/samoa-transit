"""Sample route data for the Samoa Transit networking module."""


SAMPLE_ROUTES = [
    {
        "route_name": "Apia to Faleolo",
        "origin": "Apia",
        "destination": "Faleolo",
        "estimated_minutes": 45,
        "stops": [
            "Apia",
            "Vailoa",
            "Vaitele",
            "Faleula",
            "Leauvaa",
            "Malie",
            "Nofoalii",
            "Faleolo",
        ],
    },
    {
        "route_name": "Apia to Mulifanua",
        "origin": "Apia",
        "destination": "Mulifanua",
        "estimated_minutes": 55,
        "stops": [
            "Apia",
            "Vailoa",
            "Vaitele",
            "Faleula",
            "Leauvaa",
            "Malie",
            "Nofoalii",
            "Faleolo",
            "Mulifanua",
        ],
    },
    {
        "route_name": "Apia to Falefa",
        "origin": "Apia",
        "destination": "Falefa",
        "estimated_minutes": 50,
        "stops": [
            "Apia",
            "Matautu",
            "Laulii",
            "Luatuanuu",
            "Solosolo",
            "Saoluafata",
            "Falefa",
        ],
    },
    {
        "route_name": "Apia to Lalomanu",
        "origin": "Apia",
        "destination": "Lalomanu",
        "estimated_minutes": 75,
        "stops": [
            "Apia",
            "Vailima",
            "Tiavi",
            "Lotofaga",
            "Saleapaga",
            "Lalomanu",
        ],
    },
    {
        "route_name": "Apia to Siumu",
        "origin": "Apia",
        "destination": "Siumu",
        "estimated_minutes": 45,
        "stops": [
            "Apia",
            "Vailima",
            "Tiavi",
            "Siumu",
        ],
    },
    {
        "route_name": "Apia to Lefaga",
        "origin": "Apia",
        "destination": "Lefaga",
        "estimated_minutes": 60,
        "stops": [
            "Apia",
            "Vailoa",
            "Vaitele",
            "Tafaigata",
            "Safaatoa",
            "Lefaga",
        ],
    },
]


def route_summary(route):
    """Create the short route description shown to the client."""
    return (
        f"{route['route_name']} | {route['origin']} to "
        f"{route['destination']} | About {route['estimated_minutes']} minutes"
    )