from app.models import ExceptionItem, ReconciliationRequest, ReconciliationResult, ReconciliationSummary, Severity


def classify_severity(amount: float) -> Severity:
    absolute = abs(amount)
    if absolute >= 500:
        return Severity.critical
    if absolute >= 200:
        return Severity.high
    if absolute >= 75:
        return Severity.medium
    return Severity.low


def run_reconciliation(payload: ReconciliationRequest) -> ReconciliationResult:
    total_revenue = sum(item.room_revenue for item in payload.bookings)
    expected_payout = sum(item.expected_payout for item in payload.bookings)
    actual_payout = sum(item.actual_payout for item in payload.bookings)
    exceptions: list[ExceptionItem] = []

    for booking in payload.bookings:
        commission_variance = booking.actual_commission - booking.expected_commission
        payout_variance = booking.actual_payout - booking.expected_payout

        if abs(commission_variance) >= 25:
            exceptions.append(
                ExceptionItem(
                    booking_id=booking.booking_id,
                    ota=booking.ota,
                    category="commission_variance",
                    severity=classify_severity(commission_variance),
                    variance_amount=round(commission_variance, 2),
                    summary=f"Commission variance detected for {booking.booking_id} on {booking.ota}.",
                    recommended_action="Open OTA dispute package and validate contract commission tier.",
                )
            )

        if abs(payout_variance) >= 25:
            exceptions.append(
                ExceptionItem(
                    booking_id=booking.booking_id,
                    ota=booking.ota,
                    category="payout_variance",
                    severity=classify_severity(payout_variance),
                    variance_amount=round(payout_variance, 2),
                    summary=f"Payout variance detected for {booking.booking_id} on {booking.ota}.",
                    recommended_action="Route to finance operations queue and request settlement evidence.",
                )
            )

    payout_variance = actual_payout - expected_payout
    leakage_risk = sum(abs(item.variance_amount) for item in exceptions if item.variance_amount < 0)
    summary = ReconciliationSummary(
        tenant_id=payload.tenant_id,
        period=payload.period,
        total_bookings=len(payload.bookings),
        total_revenue=round(total_revenue, 2),
        expected_payout=round(expected_payout, 2),
        actual_payout=round(actual_payout, 2),
        payout_variance=round(payout_variance, 2),
        exception_count=len(exceptions),
        leakage_risk=round(leakage_risk, 2),
    )

    brief = (
        f"RevenueOps reconciled {summary.total_bookings} bookings for {payload.period}. "
        f"Detected {summary.exception_count} exceptions with estimated leakage risk of ${summary.leakage_risk}."
    )
    return ReconciliationResult(summary=summary, exceptions=exceptions, executive_brief=brief)


def demo_dashboard_metrics() -> list[dict[str, str]]:
    return [
        {"label": "Reconciled Revenue", "value": "$4.82M", "delta": "+12.4% MoM", "tone": "positive"},
        {"label": "Leakage Prevented", "value": "$318K", "delta": "+8.1%", "tone": "positive"},
        {"label": "Open Exceptions", "value": "47", "delta": "-18 today", "tone": "warning"},
        {"label": "SLA Compliance", "value": "98.7%", "delta": "+2.2%", "tone": "positive"},
    ]


def demo_disputes() -> list[dict[str, str]]:
    return [
        {"id": "DSP-9182", "ota": "Expedia", "amount": "$95", "status": "Evidence requested", "owner": "Finance Ops"},
        {"id": "DSP-9183", "ota": "Agoda", "amount": "$72.50", "status": "Contract review", "owner": "Revenue Analyst"},
        {"id": "DSP-9184", "ota": "Airbnb", "amount": "$525", "status": "Escalated", "owner": "Director Finance"},
    ]


def demo_audit_events() -> list[dict[str, str]]:
    return [
        {"time": "09:15", "actor": "RevenueOps AI", "event": "Ingested OTA settlement batch for May 2026"},
        {"time": "09:17", "actor": "Sarah Coleman", "event": "Approved Expedia dispute package DSP-9182"},
        {"time": "09:22", "actor": "RevenueOps AI", "event": "Flagged Airbnb payout variance as critical"},
        {"time": "09:31", "actor": "Auditor Console", "event": "Exported reconciliation evidence bundle"},
    ]
