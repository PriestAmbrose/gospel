import re
import datetime
from threading import currentThread
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
    easter = datetime.date(2021,5,2)

    get_date=read_hip.iterate_year(year)
    current_date=next(get_date)
    assert current_date == easter #make sure that it starts from Easter
    
    current_date=next(get_date)
    assert current_date == easter #make sure about Easter evening

    for i in range(48+6): #going to the Saturday before Pentecost plus Sundays have two readings
        current_date=next(get_date)
    assert current_date == datetime.date(2021,6,19)

    current_date = next(get_date)
    assert current_date == datetime.date(2021,6,19) #this day should have two readings



    


    

