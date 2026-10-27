from task import find_flagged

ASSETS = [
    {"asset_id": "PMP-1001", "status": "Flagged for Inspection",
     "location": "Yanbu Terminal"},
    {"asset_id": "CMP-1002", "status": "In Service",
     "location": "Yanbu Terminal"},
    {"asset_id": "TNK-1003", "status": "Flagged for Inspection",
     "location": "Riyadh Plant A"},
]


def test_finds_all_when_no_filter():
    assert {a["asset_id"] for a in find_flagged(ASSETS)} == \
        {"PMP-1001", "TNK-1003"}


def test_filter_by_location():
    got = find_flagged(ASSETS, ["Yanbu Terminal"])
    assert [a["asset_id"] for a in got] == ["PMP-1001"]


def test_no_state_leak_between_calls():
    find_flagged(ASSETS, ["Yanbu Terminal"])
    got = find_flagged(ASSETS)
    assert {a["asset_id"] for a in got} == {"PMP-1001", "TNK-1003"}
