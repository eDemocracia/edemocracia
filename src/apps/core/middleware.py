
class CookieHandler:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.delete_cookies = []
        response = self.get_response(request)

        [
            response.set_cookie(x, request.COOKIES[x])
            for x in request.COOKIES.keys()
            if x not in response.cookies.keys()
        ]

        [response.delete_cookie(x) for x in request.delete_cookies]

        return response
