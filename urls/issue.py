from fastapi import APIRouter
from apis.issue import create_issue, get_all_issues, get_issue, update_issue

router = APIRouter(prefix = "/issue")

router.post("/create")(create_issue)
router.get("/get-all-issues/{userId}")(get_all_issues)
router.get("/get-issue/{userId}/{issueId}")(get_issue)
router.put("/update/{userId}/{issueId}")(update_issue)