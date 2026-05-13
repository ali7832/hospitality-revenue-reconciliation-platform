from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class BookingRecord(BaseModel):
    booking_id: str
    ota: str
    guest_name: str
    room_revenue: float = Field(ge=0)
    expected_commission: float = Field(ge=0)
    actual_commission: float = Field(ge=0)
    expected_payout: float = Field(ge=0)
    actual_payout: float = Field(ge=0)


class ReconciliationRequest(BaseModel):
    tenant_id: str
    period: str
    bookings: list[BookingRecord]


class ExceptionItem(BaseModel):
    booking_id: str
    ota: str
    category: str
    severity: Severity
    variance_amount: float
    summary: str
    recommended_action: str


class ReconciliationSummary(BaseModel):
    tenant_id: str
    period: str
    total_bookings: int
    total_revenue: float
    expected_payout: float
    actual_payout: float
    payout_variance: float
    exception_count: int
    leakage_risk: float


class ReconciliationResult(BaseModel):
    summary: ReconciliationSummary
    exceptions: list[ExceptionItem]
    executive_brief: str


class DashboardMetric(BaseModel):
    label: str
    value: str
    delta: str
    tone: str
