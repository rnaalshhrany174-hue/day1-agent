from task import thermal_efficiency


def test_normal_ratio():
    assert thermal_efficiency(75, 100) == 0.75


def test_zero_input_means_sensor_offline():
    assert thermal_efficiency(50, 0) == 0.0


def test_zero_output():
    assert thermal_efficiency(0, 100) == 0.0
