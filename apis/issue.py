import json
import logging
import uuid
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import Request

from common.constants import (INTERNAL_SERVER_ERROR, ISSUE_NOT_FOUND, ONE_DAY, ONE_MONTH, ONE_WEEK, OPEN)
from models.issue import Issue
from schemas.createissueschema import CreateIssueReq
from schemas.updateissueschema import LevelEnum, UpdateIssueReq
from utils.cache import cache_manager
from utils.general import (failed_response_handler, serialize_document, success_response_handler)
from utils.pagination import pagination

async def create_issue(payload: CreateIssueReq, request: Request):

    """
    Use this API to create an issue
    """

    try:
        db = request.app.mongodb
        issue_collection = db["Issue"]

        network_issue_id = uuid.uuid4()
        expected_resolution_time = ONE_DAY

        action = {
            "id": str(uuid.uuid4()),
            "descriptor": {
                "code": OPEN,
                "short_desc": payload.description.short_desc,
                "name": payload.description.code,
                "images": payload.description.images
            },
            "updated_at": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "action_by": payload.complainant_id,
            "actor_details": {
                "userId": payload.source_id,
                "name": payload.actor_name
            },
            "ref_id": payload.ref_id,
            "ref_type": payload.ref_type
        }

        issue_model = Issue(
            network_issue_id=str(uuid.uuid4()),
            transaction_id=payload.transaction_id,
            status=payload.status,
            level=payload.level,
            expected_resolution_time={"duration": expected_resolution_time},
            complainant_id=payload.complainant_id,
            source_id=payload.source_id,
            order_id=payload.order_id,
            item_id=payload.item_id,
            description=payload.description.model_dump(),
            actions=[action]
        )

        result = await issue_collection.insert_one(issue_model.model_dump())

        issue_dict = issue_model.model_dump(exclude_unset = False)
        issue_serialized = serialize_document(issue_dict)
        json_data = json.dumps(issue_serialized)

        await cache_manager.set(str(result.inserted_id), json_data)

        return success_response_handler(status_code = 201, detail = "Issue created successfully", data = {
            "network_issue_id": str(network_issue_id),
            "issue_id": str(result.inserted_id)
        })

    except Exception as e:
        logging.error(f"Error in creating issue: {e}")
        return failed_response_handler(status_code = 500, detail = INTERNAL_SERVER_ERROR)
    
    
async def get_all_issues(userId: str, request: Request, offset: int = 1, limit: int = 10):

    """
    Use this API to get all issues for a particular user
    """

    try:
        db = request.app.mongodb
        issue_collection = db["Issue"]

        cursor = issue_collection.find({"source_id": userId})
        all_issues = await cursor.to_list(length = None)
        paginated_issues = pagination(limit = limit, offset = offset, data = all_issues)
        paginated_issues_serial = serialize_document(paginated_issues)

        return success_response_handler(status_code = 200, detail = "Issues fetched successfully", data = paginated_issues_serial)

    except Exception as e:
        logging.error(f"Error getting all the issues for a user: {e}")
        return failed_response_handler(status_code = 500, detail = INTERNAL_SERVER_ERROR)
    
async def get_issue(userId: str, issueId: str, request: Request):

    """
    Use this API to get a specific issue of a user
    """

    try:

        issue = await cache_manager.get(issueId)
        if issue is not None:
            return success_response_handler(status_code = 200, detail = "Issue fetched successfully", data = issue)

        db = request.app.mongodb
        issue_collection = db["Issue"]

        issue = await issue_collection.find_one({
            "_id": ObjectId(issueId),
            "source_id": userId
        })

        if not issue:
            return failed_response_handler(status_code = 404, detail = ISSUE_NOT_FOUND)
        
        issue = serialize_document(issue)

        return success_response_handler(status_code = 200, detail = "Issue fetched successfully", data = issue)

    except Exception as e:
        logging.error(f"Error getting the issue: {e}")
        return failed_response_handler(status_code = 500, detail = INTERNAL_SERVER_ERROR)
    
async def update_issue(issueId: str, userId: str, payload: UpdateIssueReq, request: Request):

    """
    Use this API to update an issue
    """

    try:

        db = request.app.mongodb
        issue_collection = db["Issue"]
        issue = await cache_manager.get(issueId)
        
        if issue is not None and issue["source_id"] != userId:
            return failed_response_handler(status_code = 403, detail = "Unauthorized")

        if issue is None:
            issue = await issue_collection.find_one({
                "_id": ObjectId(issueId),
                "source_id": userId
            })

        if not issue:
            return failed_response_handler(status_code = 404, detail = ISSUE_NOT_FOUND)

        update_fields = {}
        if payload.status:
            update_fields["status"] = payload.status
            update_fields["actual_resolution_time"] = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        
        if payload.level:
            level_order = {LevelEnum.Issue: 1, LevelEnum.Grievance: 2, LevelEnum.Dispute: 3}
            old_level = issue["level"]
            if level_order[payload.level] < level_order[old_level]:
                return failed_response_handler(status_code = 400, detail = "Cannot downgrade the issue level")
            
            update_fields["level"] = payload.level
            
            if payload.level == LevelEnum.Grievance:
                update_fields["expected_resolution_time"] = ONE_WEEK
            elif payload.level == LevelEnum.Dispute:
                update_fields["expected_resolution_time"] = ONE_MONTH
        
        descriptor = {
            "code": payload.action_type,
            "short_desc": payload.short_desc,
            "name": payload.action_type,
            "images": payload.actor_images
        }

        action = {
            "id": str(uuid.uuid4()),
            "descriptor": descriptor,
            "updated_at": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "action_by": payload.complainant_id,
            "actor_details": {
                "userId": userId,
                "name": payload.actor_name
            },
            "ref_id": payload.ref_id,
            "ref_type": payload.ref_type
        }
        
        updated_issue = await issue_collection.update_one(
            {"_id": ObjectId(issueId)},
            {
                "$set": update_fields,
                "$push": {"actions": action}
            }
        )

        updated_issue_db = await issue_collection.find_one({
            "_id": ObjectId(issueId)
        })
        serialized_data = serialize_document(updated_issue_db)
        json_data = json.dumps(serialized_data)
        await cache_manager.set(issueId, json_data)

        return success_response_handler(status_code = 200, detail = "Issue updated successfully")

    except Exception as e:
        logging.error(f"Error in updating issue: {e}")
        return failed_response_handler(status_code = 500, detail = INTERNAL_SERVER_ERROR)