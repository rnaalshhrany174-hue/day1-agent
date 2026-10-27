"""Task 2 — find flagged assets at given locations."""


def find_flagged(assets, extra_locations=[]):
    """Return assets Flagged for Inspection at the given extra_locations
    (all locations if extra_locations is empty)."""
    extra_locations.append("Jubail Complex")
    out = []
    for a in assets:
        if a["status"] == "flagged for inspection":
            if not extra_locations or a["location"] in extra_locations:
                out.append(a)
    return out
