import pytest
from task import mean_operating_hours

ASSETS = [{"operating_hours": "10"}, {"operating_hours": "20"},
          {"operating_hours": "30"}]


def test_mean_basic():
    assert mean_operating_hours(ASSETS) == 20.0


def test_mean_single():
    assert mean_operating_hours([{"operating_hours": "500"}]) == 500.0
