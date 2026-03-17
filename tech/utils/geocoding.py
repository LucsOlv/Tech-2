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

def get_address(lat, lon):
    """
    Retorna o endereço formatado a partir da latitude e longitude
    usando geocodificação reversa.
    """
    try:
        geolocator = Nominatim(user_agent="tech_challenge_optimizer")
        location = geolocator.reverse((lat, lon), timeout=10)
        if location and location.address:
            # Pega parte mais significativa do endereço para não ficar muito longo
            address_parts = location.address.split(",")
            if len(address_parts) >= 2:
                return f"{address_parts[0].strip()}, {address_parts[1].strip()}"
            return location.address
        return "Endereço Desconhecido"
    except Exception:
        return "Endereço Desconhecido"
