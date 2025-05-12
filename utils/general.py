from datetime import datetime

from bson import ObjectId
from fastapi.responses import JSONResponse

from common.constants import FAILURE, SUCCESS

def serialize_document(doc):

    if isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    
    if isinstance(doc, dict):
        new_doc = {}
        for key, value in doc.items():
            new_doc[key] = serialize_document(value)
        return new_doc

    if isinstance(doc, ObjectId):
        return str(doc)

    if isinstance(doc, datetime):
        return doc.isoformat()

    return doc

def failed_response_handler(status_code: int, detail: str):
    return JSONResponse(
        status_code = status_code,
        content = {
            "status": FAILURE,
            "message": detail,
            "data": None,
            "error": {"detail": detail},
            "meta_data": {}
        }
    )

def success_response_handler(status_code: int, detail: str, data: dict = {}):
    return JSONResponse(
        status_code = status_code,
        content = {
            "status": SUCCESS,
            "message": detail,
            "data": data,
            "error": {},
            "meta_data": {}
        }
    )