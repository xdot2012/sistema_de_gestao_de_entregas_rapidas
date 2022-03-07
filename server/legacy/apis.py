import requests
import json
import ortools
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LocalSerializer, ClientSerializer, DeliveryManSerializer, OrderSerializer
from .models import Local, Client, DeliveryMan, Order, OrderProduct
from rest_framework.response import Response
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from django.db import transaction

api_key = '&key=AIzaSyD3iW-BDcjxvxPpQIr-YxZLu7TrcJ7I5hc'


class OrderApiView(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            order_obj = Order.objects.create(client_id=request.data['client'],
                                             created_by=request.user,
                                             delivery_type=request.data['delivery_type'])

            for item in request.data['products']:
                OrderProduct.objects.create(order_id=order_obj.pk, name=item['name'], quantity=item['quantity'])

        return Response(self.serializer_class(order_obj).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(finished_on=None)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def history(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryManViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMan.objects.all()
    serializer_class = DeliveryManSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @action(methods=['POST'], detail=False)
    def filter(self, request, *args, **kwargs):
        filters = request.data
        client_list = Client.objects.filter(**filters)
        serializer = self.get_serializer(client_list, many=True)
        return Response(serializer.data)


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = request.user
        except:
            return Response({'error': 'Usuário não existe'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if Local.objects.filter(user=user, name=serializer.validated_data['name']).exists():
            return Response({'error': 'Já existe um local com este nome!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Local.objects.create(
                name=serializer.validated_data['name'],
                latitude=serializer.validated_data['latitude'],
                longitude=serializer.validated_data['longitude'],
                user=user)
        except IntegrityError:
            return Response({'error': 'Local já existe'}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GenerateRouteAPI(APIView):
    def post(self, request):
        initial_point_pk = request.data['initial_point_pk']
        Initial_obj = []
        obj_list = []

        user_pk = request.user.pk
        local_list = Local.objects.filter(user=user_pk)
        local_url = ""
        distance_matrix = []

        for x in local_list:
            if x.pk == initial_point_pk:
                local_url = str(x.latitude) + ',' + str(x.longitude)

        if local_url == "":
            return Response(data="ponto inicial não cadastrado", status=status.HTTP_400_BAD_REQUEST)

        for x in local_list:
            if x.pk != initial_point_pk:
                local_url = local_url + "|" + str(x.latitude) + ',' + str(x.longitude)
                obj_list.append(x)
            else:
                Initial_obj.append(x)

        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        url = url + local_url + "&destinations=" + local_url + api_key

        payload = {}
        headers = {}

        api_response = requests.request("GET", url, headers=headers, data=payload)
        json.loads(api_response.text)

        local_len = len(local_list)

        for x in range(local_len):
            local_distance = []
            for y in range(local_len):
                local_distance.append(api_response.json()["rows"][x]["elements"][y]["distance"]["value"])
            distance_matrix.append(local_distance)

        def create_data_model():
            """Stores the data for the problem."""
            data = {}
            data['distance_matrix'] = distance_matrix  # yapf: disable
            data['num_vehicles'] = 1
            data['depot'] = 0
            return data

        def print_solution(manager, routing, solution):
            """Prints solution on console."""
            index = routing.Start(0)
            route_distance = 0
            plan_output = []
            plan_output.append([])
            while not routing.IsEnd(index):
                plan_output[0].extend(['{}'.format(manager.IndexToNode(index))])
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
            plan_output[0].extend(['{}'.format(manager.IndexToNode(index))])
            plan_output.append(['{}'.format(route_distance)])
            response = plan_output
            return (response)


        """Entry point of the program."""
        # Instantiate the data problem.
        data = create_data_model()

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            res = print_solution(manager, routing, solution)
            Initial_obj.extend(obj_list)
            route = []
            last = 0
            for x in res[0]:
                place = {
                    "name": Initial_obj[int(x)].name,
                    "pk": Initial_obj[int(x)].pk,
                    "distance": int(float(distance_matrix[int(last)][int(x)])/1000),
                }
                route.append(place)
                last = x

            if len(route) > 1:
                route = route[1:]
                
            response = {
                "initial_pont": {"name": Initial_obj[0].name,"pk": Initial_obj[0].pk},
                "route": route,
                "distance": int(float(res[1][0])/1000),
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(data="Resultado Não encontrado", status=status.HTTP_424_FAILED_DEPENDENCY)

