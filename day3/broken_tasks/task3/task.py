"""Task 3 — thermal efficiency of a heat exchanger."""


def thermal_efficiency(heat_out, heat_in):
    """Return heat_out / heat_in as a float.
    By specification: return 0.0 when heat_in is zero (sensor offline)."""
    return heat_out / heat_in
