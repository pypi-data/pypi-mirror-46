from django.conf import settings
from django.http import HttpResponse

try:
	API_ENDPOINTS = settings.API_ENDPOINTS
except AttributeError:
	API_ENDPOINTS = [
		('admin/', False),
		('', True),
	]

apibrowser = """<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>APIBrowser</title><link href=https://apibrowser.storage.googleapis.com/static/css/app.568f5941d42567ef2a65c5cdb7b32463.css rel=stylesheet integrity="sha256-wu9idIWIq6GpemTy2UjJyALKwWzhx3asHU+SG2udyEE=" crossorigin=anonymous></head><body><div id=app></div><script type=text/javascript src=https://apibrowser.storage.googleapis.com/static/js/app.9f8edfd9b0e1afb81473.js integrity="sha256-Sdgc+hP8zDdwQwDYypvPePGGs3m7Auqw9Qs9uxOwCoQ=" crossorigin=anonymous></script></body></html>"""


def is_api_endpoint(path):
	for prefix, result in API_ENDPOINTS:
		if path.startswith(prefix):
			return result

	return False


class APIBrowserServerMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request, *args, **kwargs):
		if is_api_endpoint(request.path):
			if request.method == 'GET' and 'text/html' in request.META['HTTP_ACCEPT']:
				return HttpResponse(apibrowser)

		return self.get_response(request, *args, **kwargs)
