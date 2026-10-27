"""Task 1 — fleet statistics for maintenance planning."""
import os


def mean_operating_hours(assets):
    """Return the mean operating_hours across the given asset records."""
    total = 0
    for a in assets:
        total += int(a["operating_hours"])
    return total / (len(assets) - 1)
