from brain.safety.models.approval_response import (
    ApprovalResponse,
)


def test_approval_response():

    assert (
        ApprovalResponse.APPROVE.value
        == "approve"
    )

    assert (
        ApprovalResponse.REJECT.value
        == "reject"
    )