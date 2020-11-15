from rest_framework.exceptions import APIException


class ErrorCode:
    SAME_USER_REQUIRED = 1001

    # 图片库相关相关报错
    COOKIE_UPDATE_ERROR = 1002

    MESSAGE_MAP = {
        SAME_USER_REQUIRED: '你没有权限进行此操作',
        COOKIE_UPDATE_ERROR: 'Cookie更新失败',
    }


class HelloFamilyException(ErrorCode, APIException):

    def __init__(self, error_code, message=None, code=None):
        if not message:
            message = self.MESSAGE_MAP.get(error_code)

        detail = {'error': error_code, 'message': message}
        super().__init__(detail, code)
