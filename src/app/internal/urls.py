from django.urls import path
from .. import handlers

urlpatterns = [
    path('all_rooms', handlers.all_rooms, name='all_rooms'),
    path('minimum_price', handlers.minimum_price, name='minimum_price'),
    path('maximum_price', handlers.maximum_price, name='maximum_price'),
    path('minimum_seating_capacity', handlers.minimum_seating_capacity, name='minimum_seating_capacity'),
    path('maximum_seating_capacity', handlers.maximum_seating_capacity, name='minimum_seating_capacity'),
    # path('<int:room_id>', handlers.details, name='details'),
    # path('api/', include('app.internal.urls')),
]
