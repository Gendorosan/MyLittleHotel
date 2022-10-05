from django.urls import path
from .models import Client, Room, Reserved

from django.http import JsonResponse

from django.http import Http404, HttpResponseRedirect


def all_rooms(request):
    rooms = Room.objects.all()

    return JsonResponse(
        {
            'rooms': [
                {
                    'name': room.name,
                    'price': room.cost,
                    'seating_capacity': room.seating_capacity
                } for room in rooms
            ]
        }, status=200, json_dumps_params={'ensure_ascii': False}
    )


def minimum_price(request):
    rooms = Room.objects.order_by('cost')

    return JsonResponse(
        {
            'rooms': [
                {
                    'name': room.name,
                    'price': room.cost,
                    'seating_capacity': room.seating_capacity
                } for room in rooms
            ]
        }, status=200, json_dumps_params={'ensure_ascii': False}
    )


def maximum_price(request):
    rooms = Room.objects.order_by('-cost')

    return JsonResponse(
        {
            'rooms': [
                {
                    'name': room.name,
                    'price': room.cost,
                    'seating_capacity': room.seating_capacity
                } for room in rooms
            ]
        }, status=200, json_dumps_params={'ensure_ascii': False}
    )


def minimum_seating_capacity(request):
    rooms = Room.objects.order_by('-seating_capacity')

    return JsonResponse(
        {
            'rooms': [
                {
                    'name': room.name,
                    'price': room.cost,
                    'seating_capacity': room.seating_capacity
                } for room in rooms
            ]
        }, status=200, json_dumps_params={'ensure_ascii': False}
    )


def maximum_seating_capacity(request):
    rooms = Room.objects.order_by('-seating_capacity')

    return JsonResponse(
        {
            'rooms': [
                {
                    'name': room.name,
                    'price': room.cost,
                    'seating_capacity': room.seating_capacity
                } for room in rooms
            ]
        }, status=200, json_dumps_params={'ensure_ascii': False}
    )


"""
def details(request, room_id):
    try:
        a = Room.objects.get(id=room_id)
    except:
        raise Http404("Номер не найден!")
    return render(request, 'hotel/details.html', {'room', a})
"""
"""
rooms = Room.objects.all()
return render(request, 'hotel/rooms.html', {'rooms': rooms})
"""


def test1(request):
    if request.method == 'GET':
        return JsonResponse(
            {
                'GET': [
                    {
                        'code': 'GET',
                        'message': 'GET'
                    }
                ]
            }, status=200
        )
    if request.method == 'POST':
        return JsonResponse(
            {
                'POST': [
                    {
                        'code': 'POST',
                        'message': 'POST'
                    }
                ]
            }, status=200
        )
