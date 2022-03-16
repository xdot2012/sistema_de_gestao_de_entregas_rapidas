from networkx import DiGraph
from vrpy import VehicleRoutingProblem
import certifi
import ssl
import requests
import folium
import polyline

import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import io
from PIL import Image

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


def save_png(img_data):
    img = Image.open(io.BytesIO(img_data))
    img.save('image.png')


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


def get_map(route):
    m = folium.Map(location=[(route['start_point'][0] + route['end_point'][0]) / 2,
                             (route['start_point'][1] + route['end_point'][1]) / 2],
                   zoom_start=13)

    folium.PolyLine(
        route['route'],
        weight=8,
        color='blue',
        opacity=0.6
    ).add_to(m)

    folium.Marker(
        location=route['start_point'],
        icon=folium.Icon(icon='play', color='green')
    ).add_to(m)

    folium.Marker(
        location=route['end_point'],
        icon=folium.Icon(icon='stop', color='red')
    ).add_to(m)

    return m

if __name__ == '__main__':
    # Montar Grafo e Resolução de problemas de roteamento
    G = DiGraph()
    G.add_edge("Source", 1, cost=1)
    G.add_edge("Source", 2, cost=2)
    G.add_edge(1, "Sink", cost=0)
    G.add_edge(2, "Sink", cost=2)
    G.add_edge(1, 2, cost=1)
    G.add_edge(2, 1, cost=1)
    G.nodes[1]["demand"] = 5
    G.nodes[2]["demand"] = 4

    prob = VehicleRoutingProblem(G, load_capacity=10)
    prob.solve()

    # Adquirir Coordenadas
    firstLocation = get_location("Maria de Freitas, Sete Lagoas, Minas Gerais")
    lastLocation = get_location("Avelino Macedo, Sete Lagoas, Minas Gerais")

    # Adquirir Melhor Rota
    if firstLocation and lastLocation:
        route = get_route(firstLocation.longitude, firstLocation.latitude, lastLocation.longitude, lastLocation.latitude)

        # (Temporário) Salvar Mapa
        m = get_map(route)
        save_png(m._to_png(5))
    else:
        print("ERRO!!! LOCAL NÃO ENCONTRADO!!!")

