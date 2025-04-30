from fastapi import FastAPI
from schemas.onissueschema import Ack, ErrorRes, MessageAck, OnIssueResponse, OnIssueReq

app = FastAPI()

@app.post("/onissue", response_model=OnIssueResponse)
def handle_on_issue(payload: OnIssueReq, ack: bool = True):
    if ack:
        return OnIssueResponse(
            message=MessageAck(
                ack=Ack(status="ACK")
            )
        )
    else:
        return OnIssueResponse(
            message=MessageAck(
                ack=Ack(status="NACK")
            ),
            error=ErrorRes(
                code="40000",
                message="Some error occurred during processing."
            )
        )
    
@app.post("/onissuestatus", response_model=OnIssueResponse)
def handle_on_issue_status(payload: OnIssueReq, ack: bool = True):
    if ack:
        return OnIssueResponse(
            message=MessageAck(
                ack=Ack(status="ACK")
            )
        )
    else:
        return OnIssueResponse(
            message=MessageAck(
                ack=Ack(status="NACK")
            ),
            error=ErrorRes(
                code="40000",
                message="Some error occurred during processing."
            )
        )