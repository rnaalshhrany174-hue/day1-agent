"""Task 4 — inspection scheduling."""
from datetime import datetime


def is_overdue(last_inspection, today, max_days=180):
    """True when the asset's last inspection is MORE than max_days
    before today. Dates are 'YYYY-MM-DD' strings."""
    last = datetime.strptime(last_inspection, "%Y-%m-%d")
    now = datetime.strptime(today, "%Y-%m-%d")
    return (now - last).days < max_days
