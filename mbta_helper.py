import os
import json
import urllib.request
import urllib.parse

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Helpful error messages if keys are missing
if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN is not set. Check your .env file.")
if MBTA_API_KEY is None:
    raise RuntimeError("MBTA_API_KEY is not set. Check your .env file.")

# Base URLs
MAPBOX_BASE_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_BASE_URL = "https://api-v3.mbta.com/"


def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request,
    return a Python dict containing the JSON response.
    """
    with urllib.request.urlopen(url) as resp:
        text = resp.read().decode("utf-8")
        data = json.loads(text)
    return data


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place (as strings).
    """
    # URL-encode the place name
    encoded_query = urllib.parse.quote(place_name)

    # Mapbox Searchbox API: ?q=...&access_token=...
    # limit=1: only need the first result
    url = (
        f"{MAPBOX_BASE_URL}"
        f"?q={encoded_query}"
        f"&access_token={MAPBOX_TOKEN}"
        f"&limit=1"
    )

    data = get_json(url)

    features = data.get("features", [])
    if not features:
        raise RuntimeError(f"No location found for '{place_name}'")

    # geometry.coordinates = [lon, lat]
    coords = features[0]["geometry"]["coordinates"]
    lon, lat = coords[0], coords[1]

    return str(lat), str(lon)


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.

    wheelchair_accessible is True if wheelchair_boarding == 1, False otherwise.
    """
    params = {
        "api_key": MBTA_API_KEY,
        "sort": "distance",
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "filter[location_type]": "1",
        "page[limit]": "1",  # only want the closest stop
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{MBTA_BASE_URL}stops?{query_string}"

    data = get_json(url)
    stops = data.get("data", [])

    if not stops:
        raise RuntimeError(
            f"No MBTA stops found near lat={latitude}, lon={longitude}"
        )
    stop = stops[0]
    stop_id = stop["id"]
    print("debug print stop_id:", stop_id)
    
    attributes = stop.get("attributes", {})

    station_name = attributes.get("name", "Unknown stop")
    wheelchair_code = attributes.get("wheelchair_boarding", 0)
    # 0 = unknown, 1 = accessible, 2 = not accessible
    wheelchair_accessible = wheelchair_code == 1
    return station_name, wheelchair_accessible, stop_id

# def get_next_scheduled_train(stop_id: str) -> dict | None:
#     """
#     Gets the departure time of the first scheduled train. Can be subbed 
#     instead of using MBTA's own internal WebAPI
#     """
#     params = {
#         "api_key": MBTA_API_KEY,
#         "filter[stop]": stop_id,
#         "sort": "departure_time",
#         "page[limit]": "1",
#     }

#     url = f"{MBTA_BASE_URL}schedules?{urllib.parse.urlencode(params)}"
#     data = get_json(url)

#     schedules = data.get("data", [])
#     if not schedules:
#         return None
#     return schedules[0]["attributes"]["departure_time"]

def find_stop_near(place_name: str) -> tuple[str, bool, dict | None]:
    """
    Given a place name or address, return the nearest MBTA stop and whether
    it is wheelchair accessible.
    """
    lat, lng = get_lat_lng(place_name)
    station_name, accessible, stop_id = get_nearest_station(lat, lng)
    next_train = get_next_train_webapi(stop_id)
    next_train = next_train['arrival_time']
    return station_name, accessible, next_train

def get_next_train_webapi(stop_id: str) -> dict | None:
    """
    Uses the MBTA's public WebAPI from their website to retrieve
    the next train at the given stop_id. Has better accuracy than V3-MBTA
    schedules end point
    """
    url = f"https://www.mbta.com/api/stops/{stop_id}/schedules?future_departures=true&last_stop_departures=false"
    data = get_json(url)

    if not data:
        return None

    next_trip = data[0]  # the first item is the next departure

    return {
        "arrival_time": next_trip.get("arrival_time")
    }

def main():
    """
    Simple manual tests.
    Run: python mbta_helper.py
    """
    test_place = "Brookline High School"
    print("Testing get_lat_lng:")
    print(test_place, "->", get_lat_lng(test_place))

    print("\nTesting find_stop_near:")
    print(test_place, "->", find_stop_near(test_place))

    print("\nTesting get_next_scheduled_train:")
    station, wheelchair_or_not, schedule = find_stop_near(test_place)
    print("Next train:", schedule)


if __name__ == "__main__":
    main()
