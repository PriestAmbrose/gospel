import pytest
import spec_days
import read_hip

def test_get_delta():
    assert spec_days.get_delta(1,-7)==-1
    assert spec_days.get_delta(2,6)==4
    assert spec_days.get_delta(7,7)==7
    assert spec_days.get_delta(2,-6)==-3


def test_correct_specday_dates():
    with pytest.raises(SystemExit,match="function correcting special days cannot see it"):
        spec_days.correct_specday_dates()
    
    article_dict1,year_dict1=read_hip.add_month_services(year=2021)
    spec_days.correct_specday_dates(article_dict1, year_dict1, year=2021)
    assert article_dict1["матfе'а д~"][0][:10] == "2021 12 27"

    article_dict1,year_dict1=read_hip.add_month_services(year=2019)
    spec_days.correct_specday_dates(article_dict1, year_dict1, year=2019)
    assert article_dict1["матfе'а _е~"][0][:10] == "2018 12 30" 

    #test year_dict1


