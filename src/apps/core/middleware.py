
class CookieHandler:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        extra_cookies = [
            x
            for x in request.COOKIES.keys()
            if x not in response.cookies.keys()
        ]

        for cookie in extra_cookies:
            response.set_cookie(cookie, request.COOKIES[cookie])
        return response
