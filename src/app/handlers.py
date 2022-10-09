from .models import Client, Room, Reserved, Jwt
from . import errors
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import jwt
import json

JWT_SECRET = "TOP SECRET"


def create_client(login, password, name, phone_number, email):
    Client.objects.create(login=login, password=password, name=name, phone_number=phone_number, email=email)


def add_jwt(jwt_token, client_id):
    Jwt.objects.create(token=jwt_token, client_id=client_id)


def check_free_rooms(start_date, end_date):
    reserved = Reserved.objects.filter(start_date__gte=start_date) & Reserved.objects.filter(end_date__lte=end_date)
    free_rooms = []
    if len(reserved) != 0:
        excluded_id = []
        for res in reserved:
            excluded_id.append(res.room_id.room_id)
        for room in Room.objects.exclude(room_id__in=excluded_id):
            free_rooms.append({"name": str(room), "price": float(room.cost), "seating_capacity": room.seating_capacity})
    else:
        for room in Room.objects.all():
            free_rooms.append({"name": str(room), "price": float(room.cost), "seating_capacity": room.seating_capacity})
    return {"rooms": free_rooms}


def all_rooms(request):
    rooms = Room.objects.all()
    return JsonResponse(
        {
            "rooms": [
                {"name": room.name, "price": float(room.cost), "seating_capacity": room.seating_capacity}
                for room in rooms
            ]
        },
        status=200,
        json_dumps_params={"ensure_ascii": False},
    )


@csrf_exempt
def minimum_price(request):
    rooms = Room.objects.order_by("cost")
    return JsonResponse(
        {
            "rooms": [
                {"name": room.name, "price": float(room.cost), "seating_capacity": room.seating_capacity}
                for room in rooms
            ]
        },
        status=200,
        json_dumps_params={"ensure_ascii": False},
    )


def maximum_price(request):
    rooms = Room.objects.order_by("-cost")

    return JsonResponse(
        {
            "rooms": [
                {"name": room.name, "price": float(room.cost), "seating_capacity": room.seating_capacity}
                for room in rooms
            ]
        },
        status=200,
        json_dumps_params={"ensure_ascii": False},
    )


def minimum_seating_capacity(request):
    rooms = Room.objects.order_by("seating_capacity")

    return JsonResponse(
        {
            "rooms": [
                {"name": room.name, "price": float(room.cost), "seating_capacity": room.seating_capacity}
                for room in rooms
            ]
        },
        status=200,
        json_dumps_params={"ensure_ascii": False},
    )


def maximum_seating_capacity(request):
    rooms = Room.objects.order_by("-seating_capacity")

    return JsonResponse(
        {
            "rooms": [
                {"name": room.name, "price": float(room.cost), "seating_capacity": room.seating_capacity}
                for room in rooms
            ]
        },
        status=200,
        json_dumps_params={"ensure_ascii": False},
    )


# Комнаты, свободные в заданном интервале
@csrf_exempt
def get_free_rooms(request):
    data = json.loads(request.body.decode("utf-8"))
    start_date = data["start_date"]
    end_date = data["end_date"]
    if start_date > end_date:
        return errors.handler400()
    return JsonResponse(check_free_rooms(start_date, end_date), status=200, json_dumps_params={"ensure_ascii": False})


@csrf_exempt
def registration(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        login = data["login"]
        password = data["password"]
        name = data["name"]
        phone_number = data["phone_number"]
        email = data["email"]
        jwt_token = jwt.encode({"login": login}, JWT_SECRET, algorithm="HS256")

        # Если такой пользователь уже существует, вернем код 400
        if len([client for client in Client.objects.filter(login=login)]) > 0:
            return JsonResponse({"code": 400, "message": "Such login already exists"}, status=400)

        create_client(login, password, name, phone_number, email)
        add_jwt(jwt_token, [client for client in Client.objects.filter(login=login)][0])

        return JsonResponse({"Authorization": jwt_token}, status=200)
    except IntegrityError:
        errors.handler409()


@csrf_exempt
def authentication(request):
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


@csrf_exempt
def get_reserved_rooms(request):
    try:
        login_from_data = json.loads(request.body.decode("utf-8"))["login"]
        login_from_jwt = jwt.decode(request.headers["Authorization"], JWT_SECRET, algorithms=["HS256"])["login"]

        if login_from_data != login_from_jwt:
            return errors.handler400()

        reserved_rooms = []
        for res in Reserved.objects.filter(client_id=Client.objects.get(login=login_from_data)):
            reserved_rooms.append(
                {
                    "name": str(res.room_id),
                    "price": float(res.room_id.cost),
                    "seating_capacity": res.room_id.seating_capacity,
                    "start_date": res.start_date,
                    "end_date": res.end_date,
                }
            )

        return JsonResponse({"rooms": reserved_rooms}, status=200, json_dumps_params={"ensure_ascii": False})
    except KeyError:
        return errors.handler400()

@csrf_exempt
def cancel_reservation(request):
    data = json.loads(request.body.decode("utf-8"))
    login_from_data = data["login"]
    reservation = data["room_name"]
    start_date = data["start_date"]
    end_date = data["end_date"]

    if start_date > end_date:
        return errors.handler400()

    login_from_jwt = jwt.decode(request.headers["Authorization"], JWT_SECRET, algorithms=["HS256"])["login"]

    if login_from_data != login_from_jwt:
        return errors.handler400()

    room = Room.objects.get(name=reservation)
    reserved_room = Reserved.objects.get(room_id=room, start_date=start_date, end_date=end_date)
    reserved_room.delete()

    return JsonResponse({"code": 200, "message": "Success"}, status=200)


@csrf_exempt
def create_reservation(request):
    data = json.loads(request.body.decode("utf-8"))
    login_from_data = data["login"]
    reservation = data["room_name"]
    start_date = data["start_date"]
    end_date = data["end_date"]

    if start_date > end_date:
        return errors.handler400()

    login_from_jwt = jwt.decode(request.headers["Authorization"], JWT_SECRET, algorithms=["HS256"])["login"]

    if login_from_data != login_from_jwt:
        return errors.handler400()

    free_rooms = check_free_rooms(start_date, end_date)
    for room in free_rooms["rooms"]:
        if room["name"] == reservation:
            room = Room.objects.get(name=reservation)
            client = Client.objects.get(login=login_from_data)
            Reserved.objects.create(room_id=room, client_id=client, start_date=start_date, end_date=end_date)

            return JsonResponse({"code": 200, "message": "Room reserved successfully"}, status=200)
    return JsonResponse({"code": 400, "message": "Room has been reserved. Choice another one"}, status=400)
