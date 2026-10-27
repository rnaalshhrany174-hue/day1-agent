"""Task 5 — criticality summary for the morning report."""


def summarize_by_criticality(assets):
    """Return a dict {criticality: count}, e.g. {"High": 2, "Low": 1}."""
    summary = {}
    for a in assets:
        level = a.get("Criticality")
        summary[level] = summary.get(level, 0) + 1
