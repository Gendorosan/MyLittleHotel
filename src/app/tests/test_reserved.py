from rest_framework.test import APITestCase
from ..models import Room, Reserved, Client, Jwt
from rest_framework import status
import json
import jwt
from rest_framework.test import RequestsClient
from ..serialazers import ReservedSerializer

JWT_SECRET = "TOP SECRET"
jwt_token = jwt.encode({"login": "gendorosan"}, JWT_SECRET, algorithm="HS256")


class ReservedTestCate(APITestCase):
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

    def test_get_reserved_room(self):
        url = "http://127.0.0.1:8000/api/get_reserved_rooms"
        client = RequestsClient()
        client.headers.update(
            {
                "authorization": jwt_token,
                "content-type": "application/json",
                "xsrfCookieName": "csrftoken",
                "xsrfHeaderName": "X-CSRFTOKEN",
            }
        )
        response = client.post(url, data=json.dumps({"login": "gendorosan"}))

        serializer_data = ReservedSerializer(Reserved.objects.get(reserved_id=1)).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json()[0], dict(serializer_data))

    def test_success_cancel_reservation(self):
        url = "http://127.0.0.1:8000/api/cancel_reservation"
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
            url,
            data=json.dumps(
                {"login": "gendorosan", "room_name": "luxe", "start_date": "2022-10-5", "end_date": "2022-10-7"}
            ),
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_fail_cancel_reservation(self):
        url = "http://127.0.0.1:8000/api/cancel_reservation"
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
            url,
            data=json.dumps(
                {"login": "gendorosan", "room_name": "luxe2", "start_date": "2022-10-5", "end_date": "2022-10-7"}
            ),
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_reservation(self):
        url = "http://127.0.0.1:8000/api/create_reservation"
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
            url,
            data=json.dumps(
                {"login": "gendorosan", "room_name": "luxe2", "start_date": "2022-10-5", "end_date": "2022-10-7"}
            ),
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
