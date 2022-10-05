from django.urls import path
from .models import Client, Room, Reserved

from django.http import JsonResponse

from django.http import Http404, HttpResponseRedirect

JsonResponse.charset = 'utf-8'

def test(request):
    rooms = Room.objects.all()

    print({'rooms': [room.name for room in rooms]})
    for room in rooms:
        print(room)

    return JsonResponse(
        {
            'rooms': [room.name for room in rooms]
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
