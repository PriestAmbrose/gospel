import re
import datetime
import dateutil.easter

import read_hip

def test_is_pericope():
    '''
    Definition of what is read_hip.is_pericope as a regular expression
    '''
    #is_pericope doesn't work with raw data
    assert not re.search(read_hip.is_pericope, "матfе'а, зача'ло _о~")

    #it works with formats gospelName pericopeNumber:
    assert re.search(read_hip.is_pericope, "матfе'а _о~")
    assert re.search(read_hip.is_pericope, "матfе'а _о~")
    assert re.search(read_hip.is_pericope, "i=wа'нна _кс~_е")
    assert re.search(read_hip.is_pericope, "луки` р~и w\т полу`")

    #it should be able to process strange pericope formats
    assert re.search(read_hip.is_pericope, "луки` ми` w\т полу`")
    assert re.search(read_hip.is_pericope, "ма'рка _е=")

def test_add_month_services():
    article_dict, year_dict = read_hip.add_month_services(year=2022)

    assert len(article_dict)==99


def test_iterate_year():
    year = 2021
    
    easter = dateutil.easter.easter(year, dateutil.easter.EASTER_ORTHODOX)

    get_date=read_hip.iterate_year(year)
    current_date=next(get_date)
    assert current_date == easter
    for i in range (1):
        current_date=next(get_date)
    

