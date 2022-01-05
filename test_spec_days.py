import pytest
import spec_days

def test_get_delta():
    assert spec_days.get_delta(1,-7)==-1
    assert spec_days.get_delta(2,6)==4
    assert spec_days.get_delta(7,7)==7
    assert spec_days.get_delta(2,-6)==-3


def test_correct_specday_dates():
    with pytest.raises(SystemExit,match="function correcting special days cannot see it"):
        spec_days.correct_specday_dates()