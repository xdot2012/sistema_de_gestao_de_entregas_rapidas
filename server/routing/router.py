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


def get_trip_route_data(trips):
    legs_data = []
    trip = {
        'polyline': []
    }
    leg_count = 0
    for trip in trips:
        for leg in trip['legs']:
            leg_points = []
            steps = []
            for step in leg['steps']:
                step_points = []
                for location in polyline.decode(step['geometry']):
                    step_points.append([location[0], location[1]])
                    leg_points.append([location[0], location[1]])
                step_data = {
                    'points': step_points,
                    'name': step['name'],
                    'key': step['geometry'],
                    'duration': step['duration'],
                    'distance': step['distance'],
                    'type': None,
                }
                if 'maneuver' in step:
                    step_data['type'] = step['maneuver']['type']

                steps.append(step_data)
            legs_data.append({
                'steps': steps,
                'polyline': leg_points,
                'key': leg_count,
            })
            leg_count += 1

    data = {
        'full_path': polyline.decode(trip['geometry']),
        'legs': legs_data,
        'duration': trip['duration'],
        'distance': trip['distance'],
    }
    return data


def get_path(lon_lat_dict_array):
    loc = "{},{}".format(lon_lat_dict_array[0]['longitude'], lon_lat_dict_array[0]['latitude'])
    for item in lon_lat_dict_array[1:]:
        loc += ";{},{}".format(item['longitude'], item['latitude'])

    url = "http://router.project-osrm.org/trip/v1/driving/"
    url_options = "?roundtrip=true&source=first&steps=true"
    r = requests.get(url + loc + url_options)
    if r.status_code != 200:
        return {}

    res = r.json()
    out = {
        'waypoints': res['waypoints'],
        'trips': res['trips'],
        'route': get_trip_route_data(res['trips'])
    }
    return out


if __name__ == '__main__':
    # Adquirir Coordenadas
    from routing.models import Branch, ClientAddress
    from routing.router import get_path
    branch = Branch.objects.all().first()
    other_locations = ClientAddress.objects.all().values('longitude', 'latitude')[:5]
    get_path(branch.longitude, branch.latitude, other_locations)

