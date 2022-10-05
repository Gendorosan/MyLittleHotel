from django.http import JsonResponse


def handler404():
    return JsonResponse(
        {
            'errors': [
                {
                    'code': 'notfound',
                    'message': 'Not found.'
                }
            ]
        }, status=404
    )
