from django.urls import path, re_path
from .. import handlers


urlpatterns = [
    path('all_rooms', handlers.all_rooms, name='all_rooms'),
    path('minimum_price', handlers.minimum_price, name='minimum_price'),
    path('maximum_price', handlers.maximum_price, name='maximum_price'),
    path('minimum_seating_capacity', handlers.minimum_seating_capacity, name='minimum_seating_capacity'),
    path('maximum_seating_capacity', handlers.maximum_seating_capacity, name='minimum_seating_capacity'),
    path('get_free_rooms', handlers.get_free_rooms, name='get_free_rooms'),
    path('registration', handlers.registration, name='registration'),
    path('authentication', handlers.authentication, name='authentication'),
    path('get_reserved_rooms', handlers.get_reserved_rooms, name='get_reserved_rooms'),
    path('cancel_reservation', handlers.cancel_reservation, name='cancel_reservation'),
    path('create_reservation', handlers.create_reservation, name='create_reservation')
    # path('<int:room_id>', handlers.details, name='details'),
    # path('api/', include('app.internal.urls')),
]
