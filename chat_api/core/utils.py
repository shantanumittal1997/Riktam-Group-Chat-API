from rest_framework.response import Response

def create_response(message: str, status:int, data: dict = dict()):

    response = {
        "msg": message,
        "status": status
    }

    if data and isinstance(data, dict):
        response.update(data)

    return Response(response, status=status)