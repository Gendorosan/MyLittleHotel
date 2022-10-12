from django.urls import path
from .. import views

urlpatterns = [
    path("all_rooms", views.RoomList.as_view()),
    path("room_filter", views.RoomFilter.as_view()),
    path("get_reserved_rooms", views.ReservedList.as_view()),
    path("cancel_reservation", views.ReservedCancel.as_view()),
    path("get_free_rooms", views.FreeRoomList.as_view()),
    path("registration", views.RegisterView.as_view()),
    path("authentication", views.LoginView.as_view()),
    path("create_reservation", views.CreateReservation.as_view()),
]
