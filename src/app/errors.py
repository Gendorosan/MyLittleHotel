from django.http import JsonResponse


def handler404():
    return JsonResponse({"errors": [{"code": 404, "message": "Not found."}]}, status=404)


def handler400():
    return JsonResponse({"code": 400, "message": "Validation Failed"}, status=400)


def handler409():
    return JsonResponse({"errors": [{"code": 409, "message": "This object already in the database"}]}, status=409)
