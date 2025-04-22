from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 400:
        response.data = {
            "error": {
                "code": "400 Bad Request",
                "message": response.data
            }
        }
    return response