import json
from datetime import datetime

try:
    with open('envs/dev/checkov-report.json') as f:
        report = json.load(f)
    passed = report.get('summary', {}).get('passed', 0)
    failed = report.get('summary', {}).get('failed', 0)
except Exception:
    passed, failed = 0, 0

html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Compliance Dashboard</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
    .pass {{ color: #16a34a; font-weight: bold; }}
    .fail {{ color: #dc2626; font-weight: bold; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; margin: 20px 0; }}
  </style>
</head>
<body>
  <h1>🛡️ Infrastructure Compliance Dashboard</h1>
  <div class="card">
    <h2>Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</h2>
    <p class="pass">✅ Passed Policies: {passed}</p>
    <p class="fail">❌ Failed Policies: {failed}</p>
  </div>
</body>
</html>
"""

with open('dashboard/index.html', 'w') as f:
    f.write(html)
print("Dashboard generated successfully at dashboard/index.html")
