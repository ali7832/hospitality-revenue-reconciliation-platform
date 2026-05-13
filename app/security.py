from enum import Enum
from pydantic import BaseModel


class Role(str, Enum):
    executive = "executive"
    finance_lead = "finance_lead"
    revenue_operator = "revenue_operator"
    auditor = "auditor"


class UserSession(BaseModel):
    user_id: str
    name: str
    email: str
    tenant_id: str
    role: Role
    permissions: list[str]


def demo_login() -> UserSession:
    return UserSession(
        user_id="usr_finance_001",
        name="Sarah Coleman",
        email="finance.lead@hotelgroup.ai",
        tenant_id="hotel-group-alpha",
        role=Role.finance_lead,
        permissions=[
            "dashboard:read",
            "reconciliation:run",
            "exceptions:manage",
            "disputes:create",
            "audit:read",
        ],
    )
