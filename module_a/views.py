from django.http import JsonResponse


def handler404(*args, **kwargs):
    return JsonResponse({'status': 'not-found', 'message': 'Not found'}, status=404)
