from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="tech_challenge_optimizer")
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return location.latitude, location.longitude, location.address
        return None, None, None
    except GeocoderTimedOut:
        return None, None, None
