from rest_framework.test import APITestCase, RequestsClient
from ..models import Room, Reserved, Client, Jwt
from ..serialazers import RoomSerializer
from rest_framework import status
import json
import jwt

JWT_SECRET = "TOP SECRET"
jwt_token = jwt.encode({"login": "gendorosan"}, JWT_SECRET, algorithm="HS256")


class RoomTestCate(APITestCase):
    def setUp(self):
        Room.objects.create(room_id=1, name="luxe", cost=10000, seating_capacity=1)
        Room.objects.create(room_id=2, name="luxe2", cost=10500, seating_capacity=1)
        Client.objects.create(
            client_id=1,
            login="gendorosan",
            password="123wqdwfq",
            name="Gena",
            phone_number="+7800553535",
            email="sobaka@babaka.com",
        )
        Jwt.objects.create(token=jwt_token, client_id_id=1)
        Reserved.objects.create(start_date="2022-10-05", end_date="2022-10-07", client_id_id=1, room_id_id=1)

    def test_get_all_room(self):
        room_1 = Room.objects.get(room_id=1)
        room_2 = Room.objects.get(room_id=2)
        url = "http://127.0.0.1:8000/api/all_rooms"
        response = self.client.get(url)
        serializer_data = RoomSerializer([room_1, room_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_room_filter(self):
        room_1 = Room.objects.get(room_id=1)
        room_2 = Room.objects.get(room_id=2)
        url = "http://127.0.0.1:8000/api/room_filter?seating_capacity=1"
        response = self.client.get(url)
        serializer_data = RoomSerializer([room_1, room_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_free_room(self):
        room_2 = Room.objects.get(room_id=2)
        url = "http://127.0.0.1:8000/api/get_free_rooms"
        client = RequestsClient()
        client.headers.update(
            {
                "authorization": jwt_token,
                "content-type": "application/json",
                "xsrfCookieName": "csrftoken",
                "xsrfHeaderName": "X-CSRFTOKEN",
            }
        )
        response = client.post(
            url, data=json.dumps({"login": "gendorosan", "start_date": "2022-10-5", "end_date": "2022-10-7"})
        )
        serializer_data = RoomSerializer(room_2).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json()[0], dict(serializer_data))
