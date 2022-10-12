from rest_framework.permissions import AllowAny
from .models import Client, Room, Reserved, Jwt
from . import errors
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serialazers as s
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import ObjectDoesNotExist


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = s.RoomSerializer


class ReservedList(generics.ListAPIView):
    serializer_class = s.ReservedSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            if request.client is not None:
                login = data["login"]
                self.queryset = Client.objects.get(login=login).reserved_set.all()
                return self.list(request, *args, **kwargs)
            else:
                return errors.handler400()
        except KeyError:
            return errors.handler400()


class ReservedCancel(generics.DestroyAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            if request.client is not None:
                try:
                    self.queryset = Reserved.objects.get(
                        room_id=Room.objects.get(name=data["room_name"]).room_id,
                        start_date=data["start_date"],
                        end_date=data["end_date"],
                    )
                    self.queryset.delete()
                    return Response({"code": 200, "message": "Success"})
                except ObjectDoesNotExist:
                    return errors.handler404()
        except KeyError:
            return errors.handler400()


class RoomFilter(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = s.RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["cost", "seating_capacity"]


class FreeRoomList(generics.ListAPIView):
    serializer_class = s.RoomSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            start_date = data["start_date"]
            end_date = data["end_date"]

            reserved = Reserved.objects.filter(start_date__gte=start_date) & Reserved.objects.filter(
                end_date__lte=end_date
            )

            excluded_id = []
            for res in reserved:
                excluded_id.append(res.room_id.room_id)

            self.queryset = Room.objects.exclude(room_id__in=excluded_id)

            return self.list(request, *args, **kwargs)
        except KeyError:
            return errors.handler400()


class RegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = s.RegisterSerializer

    def perform_create(self, serializer):
        return serializer.save(client=self.request.client)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        token = Jwt.objects.filter(client_id=instance)
        instance_serializer = s.JwtSerializer(token[0])
        return Response(instance_serializer.data)


class CreateReservation(generics.CreateAPIView):
    queryset = Reserved.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = s.ReservedSerializer

    def create(self, request, *args, **kwargs):

        client_id = Client.objects.get(login=request.data["login"]).client_id
        room_id = Room.objects.get(name=request.data["room_name"]).room_id

        reserved = Reserved.objects.filter(start_date__gte=request.data["start_date"]) & Reserved.objects.filter(
            end_date__lte=request.data["end_date"]
        )

        excluded_id = [res.room_id.room_id for res in reserved]

        if room_id not in excluded_id:
            serializer = self.get_serializer(
                data={
                    "client_id": client_id,
                    "room_id": room_id,
                    "start_date": request.data["start_date"],
                    "end_date": request.data["end_date"],
                }
            )

            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)

            return JsonResponse({"code": 200, "message": "Room reserved successfully"}, status=200)

        else:
            return JsonResponse({"code": 400, "message": "Room has been reserved. Choice another one"}, status=400)


class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        login = data["login"]
        password = data["password"]

        client = [client for client in Client.objects.filter(login=login) & Client.objects.filter(password=password)]

        if len(client) == 0:
            return errors.handler404()

        client = client[0]

        jwt_token = Jwt.objects.filter(client_id=client)

        if len(jwt_token) == 0:
            return errors.handler400()

        return JsonResponse({"Authorization": str(jwt_token[0])}, status=200)
