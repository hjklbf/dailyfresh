from django.http import HttpRequest,HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
class url():
    def process_response(self, request, response):
        url_list=[
            '/user/register/',
            '/user/register_handle/',
            '/user/register_exist/',
            '/user/login/',
            '/user/login_handle/',
            '/user/logout/'
        ]
        if not request.is_ajax() and request.path not in url_list:
            response.set_cookie('red_url',request.get_full_path())
        return response

