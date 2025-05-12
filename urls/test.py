from fastapi import APIRouter

from apis.test import handle_on_issue, handle_on_issue_status
from schemas.onissueschema import OnIssueResponse

router = APIRouter()

router.post("/onissue", response_model=OnIssueResponse)(handle_on_issue)
router.post("/onissuestatus", response_model=OnIssueResponse)(handle_on_issue_status)