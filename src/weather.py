"""Shared weather helper. Not a lesson concept — just the bit 04 and 07 both need.

Open-Meteo (https://open-meteo.com) is a free weather API. No account, no key,
no card. That is why we can use it live in a classroom.

Two endpoints are involved:

    geocoding-api.open-meteo.com/v1/search   a place name  -> a latitude/longitude
    api.open-meteo.com/v1/forecast           a lat/lon     -> the weather

The weather calls themselves live inside the tools in 04 and 07, so you can see
what a tool actually does. Only the name-to-coordinates step is shared, because
both of them need it and it is the boring half.
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEZONE = "Asia/Colombo"


def geocode(place: str) -> tuple[float, float, str]:
    """Turn a place name into (latitude, longitude, the name the API matched).

    Returning the matched name matters: ask for "Polonnaruwa" and you get
    Polonnaruwa, but ask for something ambiguous and you want to know what it
    decided you meant.
    """
    results = requests.get(
        GEOCODE_URL,
        params={"name": place, "count": 1, "language": "en", "format": "json"},
        timeout=20,
    ).json().get("results")

    if not results:
        raise LookupError(f"Open-Meteo has no place called {place!r}")

    hit = results[0]
    return hit["latitude"], hit["longitude"], hit["name"]
