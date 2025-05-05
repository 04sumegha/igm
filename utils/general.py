from fastapi.responses import JSONResponse

def failed_response_handler(status_code: int, detail: str):
    return JSONResponse(
        status_code = status_code,
        content = {
            "status": "Failure",
            "message": detail,
            "data": None,
            "error": {"detail": detail},
            "meta_data": {}
        }
    )

def success_response_handler(status_code: int, detail: str, data: dict):
    return JSONResponse(
        status_code = status_code,
        content = {
            "status": "Success",
            "message": detail,
            "data": data,
            "error": {},
            "meta_data": {}
        }
    )