def success_response(data=None, message="Success"):
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message="Something went wrong", status="error"):
    return {
        "success": False,
        "status": status,
        "message": message,
    }