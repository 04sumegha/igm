from schemas.onissueschema import OnIssueReq, OnIssueResponse, MessageAck, Ack, ErrorRes

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