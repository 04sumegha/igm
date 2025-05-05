from bson import ObjectId
from fastapi import HTTPException, Request
import logging
import uuid
from datetime import datetime, timezone
from models.issue import Issue
from schemas.createissueschema import CreateIssueReq
from schemas.updateissueschema import UpdateIssueReq
from utils.pagination import pagination

async def create_issue(payload: CreateIssueReq, request: Request):
    try:
        db = request.app.mongodb
        issue_collection = db["Issue"]

        network_issue_id = uuid.uuid4()
        expected_resolution_time = "P1D"

        action = {
            "id": str(uuid.uuid4()),
            "descriptor": {
                "code": "OPEN",
                "short_desc": payload.description.short_desc,
                "name": payload.description.code,
                "images": payload.description.images
            },
            "updated_at": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "action_by": payload.complainant_id,
            "actor_details": {"name": payload.actor_name},
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

        return {
            "message": "Issue created successfully",
            "network_issue_id": network_issue_id,
            "issue_id": str(result.inserted_id)
        }

    except Exception as e:
        logging.error(f"Error in creating issue: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
def serialize_issue(issue):
    issue["_id"] = str(issue["_id"])
    return issue
    
async def get_all_issues(userId: str, request: Request, offset: int = 1, limit: int = 10):
    try:
        db = request.app.mongodb
        issue_collection = db["Issue"]

        cursor = issue_collection.find({"source_id": userId})
        all_issues = await cursor.to_list(length = None)
        paginated_issues = pagination(limit = limit, offset = offset, data = all_issues)
        paginated_issues_serial = [serialize_issue(issue) for issue in paginated_issues]

        return{
            "message": "Issues fetched successfully",
            "data": paginated_issues_serial
        }

    except Exception as e:
        logging.error(f"Error getting all the issues for a user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
async def get_issue(userId: str, issueId: str, request: Request):
    try:
        db = request.app.mongodb
        issue_collection = db["Issue"]

        issue = await issue_collection.find_one({
            "_id": ObjectId(issueId),
            "source_id": userId
        })

        if not issue:
            raise HTTPException(status_code = 404, detail = "Issue not found with this id")
        
        serialize_issue(issue)
        
        return{
            "message": "Issue fetched successfully",
            "data": issue
        }

    except Exception as e:
        logging.error(f"Error getting the issue: {e}")
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
async def update_issue(issueId: str, userId: str, payload: UpdateIssueReq, request: Request):
    try:
        db = request.app.mongodb
        issue_collection = db["Issue"]

        issue = await issue_collection.find_one({
            "_id": ObjectId(issueId),
            "source_id": userId
        })

        if not issue:
            raise HTTPException(status_code = 404, detail = "Issue not found with this id")

        update_fields = {}
        if payload.status:
            update_fields["status"] = payload.status
            update_fields["actual_resolution_time"] = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        
        if payload.level:
            level_order = {"ISSUE": 1, "GRIEVANCE": 2, "DISPUTE": 3}
            old_level = issue["level"]
            if level_order[payload.level] < level_order[old_level]:
                raise HTTPException(status_code=400, detail="Cannot downgrade the issue level")
            
            update_fields["level"] = payload.level
            
            if payload.level == "GRIEVANCE":
                update_fields["expected_resolution_time"] = "P7D"
            elif payload.level == "DISPUTE":
                update_fields["expected_resolution_time"] = "P28D"

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
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
            "actor_details": {"name": payload.actor_name},
            "ref_id": payload.ref_id,
            "ref_type": payload.ref_type
        }
        
        await issue_collection.update_one(
            {"_id": ObjectId(issueId)},
            {
                "$set": update_fields,
                "$push": {"actions": action}
            }
        )

        return {"message": "Issue updated successfully"}

    except Exception as e:
        logging.error(f"Error in updating issue: {e}")
        raise HTTPException(status_code = 500, detail = "Internal server error")