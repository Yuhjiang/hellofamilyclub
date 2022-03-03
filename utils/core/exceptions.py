from rest_framework.exceptions import APIException


class WeiboFetchCookieError(Exception):
    """
    cookie失效
    """
    def __init__(self, detail):
        self.detail = detail


class HelloFamilyError(APIException):
    def __init__(self, error_code=500, msg=''):
        detail = {'error': error_code, 'errMsg': msg}
        super().__init__(detail=detail, code=error_code)
