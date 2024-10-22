
from django.http import JsonResponse
from ..models import APIKey  # Import your APIKey model

class APIKeyAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get("X-API-KEY")

        if api_key:
            try:
                key = APIKey.objects.get(key=api_key, is_active=True)
                request.user = key.user
            except APIKey.DoesNotExist:
                return JsonResponse({"error": "Invalid API Key"}, status=403)
        else:
            return JsonResponse({"error": "API Key missing"}, status=403)

        return self.get_response(request)
