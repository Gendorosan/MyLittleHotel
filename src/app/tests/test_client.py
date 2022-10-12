from django.test import TestCase
from rest_framework.test import APITestCase
import json
from django.urls import reverse
from rest_framework.test import APITestCase, RequestsClient
import json
from rest_framework import status
from ..models import Client, Jwt
import jwt

JWT_SECRET = "TOP SECRET"
jwt_token = jwt.encode({"login": "gendorosan"}, JWT_SECRET, algorithm="HS256")
jwt_token2 = jwt.encode({"login": "gendorosan2"}, JWT_SECRET, algorithm="HS256")


class ClientTestCate(APITestCase):
    def setUp(self):
        Client.objects.create(
            client_id=1,
            login="gendorosan2",
            password="123wqdwfq",
            name="Gena",
            phone_number="+7800553535",
            email="sobaka@babaka.com",
        )
        Jwt.objects.create(token=jwt_token2, client_id_id=1)

    def test_registration(self):
        url = "http://127.0.0.1:8000/api/registration"
        client = RequestsClient()
        client.headers.update(
            {"content-type": "application/json", "xsrfCookieName": "csrftoken", "xsrfHeaderName": "X-CSRFTOKEN"}
        )
        response = client.post(
            url,
            data=json.dumps(
                {
                    "login": "gendorosan",
                    "password": "1d32gdfsge",
                    "name": "Gena",
                    "phone_number": "+7800553535",
                    "email": "sobaka@nebabaka.com",
                }
            ),
        )
        return_data = {"token": jwt_token}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), return_data)

    def test_authentication(self):
        url = "http://127.0.0.1:8000/api/authentication"
        client = RequestsClient()
        client.headers.update(
            {"content-type": "application/json", "xsrfCookieName": "csrftoken", "xsrfHeaderName": "X-CSRFTOKEN"}
        )
        response = client.post(
            url,
            data=json.dumps(
                {
                    "login": "gendorosan2",
                    "password": "123wqdwfq",
                }
            ),
        )

        return_data = {"Authorization": jwt_token2}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), return_data)
