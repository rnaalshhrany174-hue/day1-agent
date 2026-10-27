from task import is_overdue


def test_overdue():
    assert is_overdue("2025-01-01", "2026-01-01") is True


def test_recent_not_overdue():
    assert is_overdue("2025-12-01", "2026-01-01") is False


def test_boundary_exactly_max_days():
    # exactly 180 days is NOT overdue ("more than")
    assert is_overdue("2025-07-05", "2026-01-01") is False
