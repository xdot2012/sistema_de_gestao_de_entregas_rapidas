from networkx import DiGraph
from vrpy import VehicleRoutingProblem
import certifi
import ssl
import requests
import polyline

import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


def get_location(name):
    geolocator = Nominatim(user_agent="xdot2012@gmail.com")
    try:
        return geolocator.geocode(name, timeout=5)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s" % (e.msg))


def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc)
    if r.status_code != 200:
        return {}

    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']

    out = {'route': routes,
           'start_point': start_point,
           'end_point': end_point,
           'distance': distance
           }

    return out


def get_path(pickup_lon, pickup_lat, lon_lat_dict_array):
    loc = "{},{}".format(pickup_lon, pickup_lat)
    for item in lon_lat_dict_array:
        loc += ";{},{}".format(item['longitude'], item['latitude'])

    url = "http://router.project-osrm.org/trip/v1/driving/"
    url_options = "?roundtrip=true&source=first"
    r = requests.get(url + loc + url_options)
    if r.status_code != 200:
        return {}

    res = r.json()
    out = {
        'waypoints': res['waypoints'],
        'trips': res['trips']
    }
    return out


if __name__ == '__main__':
    # Adquirir Coordenadas
    from routing.models import Branch, ClientAddress
    from routing.router import get_path
    branch = Branch.objects.all().first()
    other_locations = ClientAddress.objects.all().values('longitude', 'latitude')[:5]
    get_path(branch.longitude, branch.latitude, other_locations)

