from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from django.conf import settings


class HealthCheckMiddleware(MiddlewareMixin):
    """ Middleware to handle Health check requests (from EC2, for example), without validating
    ALLOWED_HOST and other authorisation middleware.
    """
    def process_request(self, request):
        if request.META['PATH_INFO'] == settings.HEALTH_CHECK_PATH_INFO:
            return HttpResponse(settings.HEALTH_CHECK_HEALTHY_RESPONSE)
