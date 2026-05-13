const metricsEl = document.querySelector('#metrics');
const exceptionsEl = document.querySelector('#exceptions');
const briefEl = document.querySelector('#brief');
const briefTitle = document.querySelector('#briefTitle');

async function loadDashboard(){
  const response = await fetch('/api/v1/dashboard');
  const data = await response.json();
  metricsEl.innerHTML = data.metrics.map(metric => `
    <div class="metric">
      <span>${metric.label}</span>
      <strong>${metric.value}</strong>
      <small>${metric.delta}</small>
    </div>
  `).join('');
}

async function runDemo(){
  const payload = {
    tenant_id: 'hotel-group-alpha',
    period: '2026-05',
    bookings: [
      {booking_id:'BK-1001', ota:'Booking.com', guest_name:'Ayesha Khan', room_revenue:1250, expected_commission:187.5, actual_commission:187.5, expected_payout:1062.5, actual_payout:1062.5},
      {booking_id:'BK-1002', ota:'Expedia', guest_name:'Omar Malik', room_revenue:2100, expected_commission:315, actual_commission:410, expected_payout:1785, actual_payout:1690},
      {booking_id:'BK-1003', ota:'Agoda', guest_name:'Mina Shah', room_revenue:850, expected_commission:127.5, actual_commission:188, expected_payout:722.5, actual_payout:650},
      {booking_id:'BK-1004', ota:'Airbnb', guest_name:'Daniel Ross', room_revenue:3200, expected_commission:480, actual_commission:480, expected_payout:2720, actual_payout:2195}
    ]
  };
  const response = await fetch('/api/v1/reconciliation/run', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  briefTitle.textContent = `$${data.summary.leakage_risk} leakage risk detected`;
  briefEl.textContent = data.executive_brief;
  exceptionsEl.innerHTML = data.exceptions.map(item => `
    <div class="exception">
      <span class="badge">${item.severity.toUpperCase()} - ${item.category}</span>
      <strong>${item.booking_id} · ${item.ota}</strong>
      <p>${item.summary}</p>
      <p><b>Variance:</b> $${item.variance_amount}</p>
      <p><b>Action:</b> ${item.recommended_action}</p>
    </div>
  `).join('');
}

document.querySelector('#runDemo').addEventListener('click', runDemo);
loadDashboard();
