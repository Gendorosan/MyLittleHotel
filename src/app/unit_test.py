import json
import urllib.error
import urllib.parse
import urllib.request
import requests

API_BASEURL = "http://127.0.0.1:8000/"
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6InF3ZXJ0eSJ9.Xvdu_WJtN7McLcwL0LkdQKQM1PWwUhEfQJPC5w-UgrM"
login = "qwerty"
password = "qwerty"


def request(path, method="POST", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


def test_free_rooms():
    print(
        requests.post(
            API_BASEURL + "api/get_free_rooms", data=json.dumps({"start_date": "2022-10-5", "end_date": "2022-10-7"})
        ).text
    )


def test_registration():
    data = {"login": login, "password": password, "name": "Ivan", "phone_number": "0000", "email": "email@mail.ru"}

    print(requests.post(API_BASEURL + "api/registration", data=json.dumps(data)).text)


def test_authentication():
    data = {
        "login": login,
        "password": password,
    }
    headers = {
        "xsrfCookieName": "csrftoken",
        "xsrfHeaderName": "X-CSRFTOKEN",
    }
    print(requests.post(API_BASEURL + "api/authentication", data=json.dumps(data), headers=headers).text)


def test_reserved_rooms():
    data = {"login": login}
    headers = {"xsrfCookieName": "csrftoken", "xsrfHeaderName": "X-CSRFTOKEN", "Authorization": jwt_token}
    print(requests.post(API_BASEURL + "api/get_reserved_rooms", data=json.dumps(data), headers=headers).text)


def test_cancel_reservation():
    data = {"login": login, "room_name": "Люкс №2", "start_date": "2022-10-5", "end_date": "2022-10-7"}
    headers = {"xsrfCookieName": "csrftoken", "xsrfHeaderName": "X-CSRFTOKEN", "Authorization": jwt_token}
    print(requests.post(API_BASEURL + "api/cancel_reservation", data=json.dumps(data), headers=headers).text)


def test_create_reservation():
    data = {"login": login, "room_name": "Люкс №2", "start_date": "2022-10-5", "end_date": "2022-10-7"}
    headers = {"xsrfCookieName": "csrftoken", "xsrfHeaderName": "X-CSRFTOKEN", "Authorization": jwt_token}
    print(requests.post(API_BASEURL + "api/create_reservation", data=json.dumps(data), headers=headers).text)


def test_minimum_price():
    print(request("api/minimum_price", method="GET")[1])


def test_maximum_price():
    print(request("api/maximum_price", method="GET")[1])


def test_maximum_seating_capacity():
    print(request("api/maximum_seating_capacity", method="GET")[1])


def test_minimum_seating_capacity():
    print(request("api/minimum_seating_capacity", method="GET")[1])


def test_all_rooms():
    print(request("api/all_rooms", method="GET")[1])


print("registration test")
test_registration()
print("\nauthentication test")
test_authentication()
print("\nall rooms test")
test_all_rooms()
print("\norder by minimum price test")
test_minimum_price()
print("\norder by maximum price test")
test_maximum_price()
print("\norder by maximum seating capacity test")
test_maximum_seating_capacity()
print("\norder by minimum seating capacity test")
test_minimum_seating_capacity()
print("\nfree room between '2022-10-5' and '2022-10-7'")
test_free_rooms()
print("\nreserved rooms test")
test_reserved_rooms()
print("\ncreate reservation test on dates '2022-10-5' and '2022-10-7' Room -> 'Люкс №2'")
test_create_reservation()
print("\nreserved rooms test")
test_reserved_rooms()
print("\nfree room between '2022-10-5' and '2022-10-7'")
test_free_rooms()
print("\ncancel reservation test on dates '2022-10-5' and '2022-10-7' Room -> 'Люкс №2'")
test_cancel_reservation()
print("\nreserved rooms test")
test_reserved_rooms()
print("\nfree room between '2022-10-5' and '2022-10-7'")
test_free_rooms()
