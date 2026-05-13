from app.models import BookingRecord, ReconciliationRequest
from app.services import run_reconciliation


def test_reconciliation_detects_exceptions():
    payload = ReconciliationRequest(
        tenant_id="hotel-group-alpha",
        period="2026-05",
        bookings=[
            BookingRecord(
                booking_id="BK-1",
                ota="Expedia",
                guest_name="Demo Guest",
                room_revenue=1000,
                expected_commission=150,
                actual_commission=250,
                expected_payout=850,
                actual_payout=700,
            )
        ],
    )

    result = run_reconciliation(payload)

    assert result.summary.total_bookings == 1
    assert result.summary.exception_count == 2
    assert result.summary.leakage_risk == 150
    assert "RevenueOps reconciled" in result.executive_brief
