from task import summarize_by_criticality

ASSETS = [{"criticality": "High"}, {"criticality": "High"},
          {"criticality": "Low"}]


def test_counts():
    assert summarize_by_criticality(ASSETS) == {"High": 2, "Low": 1}


def test_empty():
    assert summarize_by_criticality([]) == {}
