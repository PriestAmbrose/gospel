import re
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








