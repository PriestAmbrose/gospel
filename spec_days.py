import re
import datetime

import read_hip


def get_delta(feast,day):
    '''возвращает на сколько дней следует сдвинуть календарь, чтобы потом вернуть дату
    искомого дня после/до праздника
    feast_day - день недели в формате 1...7 (iso)
    day - искомый день до (отрицательное число) или после (положительное число) праздника
    например, если праздник - понедельник (feast_day=1), 
    и нужно найти первое воскресенье до праздника (day=-7) , то вернёт -1'''
    
    week = -7 if day<0 else 7
    if abs(day)==feast:
        return week
    elif abs(day)>7:
        return get_delta(feast, day-week)+week
    else:
        return (abs(day)-feast)%week
    
    
def correct_specday_dates(article_dict=None,year_dict=None,
                        file_name="special_days.hip", year=datetime.date.today().year):
    ''' This function corrects in the dictionary of articles dates for special 
    Saturdays and Sundays before and after feastday (there are 13 special days)
    which are taken from the file file_name, the dates are corrected according to new style,
    but added in article in old style for uniformity, they are also added to year_dict'''
    
    '''Корректирует даты всех 13 особых дней месяцеслова (суббота, воскресение
    до и после великих праздников) для года year в словаре статей article_dict.
    Внимание! Даты вычисляются для астрономического календаря, то есть,
    сначала для конца (сентябрь-декабрь), а затем для начала года (январь- август)
    Ключи (евангельские чтения) берутся из готового файла file_name
    Этот файл создан вручную для специальных дней с добавлением даты праздника по новому стилю
    и смещения, например, -6 - суббота перед праздником'''
    
    #Сейчас немного подкорректируем словарь, чтобы все специальные дни в списке
    # оказались на пером месте. При чтении в первую очередь статей месяцеслова 
    # это всегда оказывается так, кроме зачала Мф. 4, которое для Недели по Рождестве
    # оказывается на последнем месте
    #print(article_dict["матfе'а д~"])
    if article_dict is None:
        article_dict={}

    if year_dict is None:
        year_dict={}
        
    try:
        article_dict["матfе'а д~"].insert(0,article_dict["матfе'а д~"].pop())
    except:
        raise SystemExit("function correcting special days cannot see it")

    #print(article_dict["матfе'а д~"])
    with open(file_name, encoding="utf8") as f:
        for line in re.split('\n\n%<',f.read()):
            spec_day_info=line.split(" day ")
            feast=datetime.date(year, *map(int,spec_day_info[0].split())) #old calendar dates
            feast+=datetime.timedelta(read_hip.NEW_OLD_DIFF) #conversion to new calendar dates
            spec_date=feast+datetime.timedelta(get_delta(feast.isoweekday(),int(spec_day_info[1])))
            #conversion back to old calendar dates to save in dictionary articles
            corr_article=(spec_date-datetime.timedelta(read_hip.NEW_OLD_DIFF)).strftime("%Y %m %d")
            key=re.search(read_hip.is_pericope,line).group(0)
            # !!! Внимание. Все специальные дни в словаре должны теперь оказаться на первом месте в списке
            try:
                corr_article+=article_dict[key][0][10:] #10 characters take month-day pair 
            except:
                raise SystemExit("function correcting special days cannot see it")
            '''print(feast,feast.strftime("Feast(NC) %Y %m %d %A\n"))
            print(spec_date.strftime("SPEC DATE(OC) %Y %m %d\n\n"))'''
            
            article_dict[key][0]=corr_article
            year_dict[spec_date]=year_dict.get(spec_date,[])+[corr_article]
           
            '''print(len(article_dict[key]),key,
                *article_dict[key],sep="\n\n",
                end="***********\n\n")'''
                
    return article_dict, year_dict