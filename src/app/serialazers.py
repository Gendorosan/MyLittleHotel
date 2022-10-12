from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from .models import Room, Reserved, Client, Jwt
from rest_framework import serializers
import jwt
from rest_framework.response import Response

JWT_SECRET = "TOP SECRET"


class RoomSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    seating_capacity = serializers.IntegerField()


class ReservedSerializer(serializers.Serializer):
    room_id = serializers.CharField()
    client_id = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = Reserved
        fields = "__all__"

    def create(self, validated_data):
        reservation = Reserved.objects.create(
            room_id_id=validated_data["room_id"],
            client_id_id=validated_data["client_id"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
        )

        reservation.save()

        return reservation


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Client.objects.all())])
    login = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Client.objects.all())])

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Client
        fields = ("login", "password", "email", "name", "phone_number")

    def create(self, validated_data):
        client = Client.objects.create(
            login=validated_data["login"],
            email=validated_data["email"],
            name=validated_data["name"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )

        client.save()
        auth_token = jwt.encode({"login": validated_data["login"]}, JWT_SECRET, algorithm="HS256")

        jwt_token = Jwt.objects.create(
            token=auth_token, client_id=[client for client in Client.objects.filter(login=validated_data["login"])][0]
        )

        return client


class JwtSerializer(serializers.Serializer):
    token = serializers.CharField()


def get_all_rooms(rooms):
    return {
        "rooms": [
            {"name": room.name, "price": float(room.cost), "seating_capacity": room.seating_capacity} for room in rooms
        ]
    }
