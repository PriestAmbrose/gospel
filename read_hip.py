'''This module reads from .hip file of monthly articles on saints (unchangeable feasts).
it has two main functions:
add_month_services to add to dictionary of pericope articles services to saints of uncheangeable year
add_general_services to add to dictionary of articles pericopes that are read for general services
Perhaps it should be better called read_unch '''


import re
import calendar
import datetime
import dateutil.easter

NEW_OLD_DIFF=13 #the difference between old and new calendar

is_pericope=r"(матfе'а|ма'рка|луки`|i=wа'нна)( [рiклмнопсч_авгдеsзиf]{,3})[~=`]"\
r"([_авгдеsзиfi]{,2}( w\\т полу`)?)"


def iterate_year(year=datetime.date.today().year):
    '''This function shoud give the correct date while walking through the calendar 
    of changeable daily readings in the Gospel for particular year. The construction of this function
    is strongly dependent on the structure of the document where the calendar is'''
    current_date=dateutil.easter.easter(year, dateutil.easter.EASTER_ORTHODOX)
    day_after_Easter=0
    yield current_date #for Easter itself
    yield current_date #for Easter evening
    while True:
        day_after_Easter+=1
        current_date+=datetime.timedelta(1)
        if day_after_Easter//7==6 and day_after_Easter%7==6:
            #the Saturday after Pentecost has extra reading
            yield current_date
        yield current_date
#FIXME that algorithm doesn't take into account 
#readings change for Exaltation of the Cross and Epiphany
#also it have problems for Meatfare readings

def add_daily_readings(article_dict=None,year_dict=None,
                        file_name="5skazan.hip",
                        year=datetime.date.today().year):
    '''This function readings changeable daily readings from the file file_name
    into the dicitonary of articles article_dict (where key=pericope, value =article) 
    and year_dict (where key= date, value = article) and returns resulting dictionaries
    article_dict and year_dict'''
    

    if article_dict is None:
        article_dict={}

    if year_dict is None:
        year_dict={}

    with open(file_name, encoding="utf8") as file:
        list_of_weeks=re.split('\n\n%<',file.read())
        get_date=iterate_year(year)
        current_date=next(get_date)
    for week_readings in list_of_weeks:
        daily_readings=week_readings.split('\n\n')
        header=daily_readings[0]
        #print(header)
        for article in daily_readings:
            corr_article=header+article.replace("\n","").replace(",","").replace(" зача'ло","")  
            #for unification because in some articles commas and word "зачало" are missing 
            #and \n is inside important sequences (keys)
            if re.search(is_pericope,corr_article):
                corr_article=re.sub(is_pericope,r"\1\2~\3",corr_article) #remove `= and leave only ~
                year_dict[current_date]=year_dict.get(current_date,[])+[corr_article]
                if not re.search("На о_у='трени", corr_article):
                    current_date=next(get_date) #we change the date only if it is next day
                    #but morning readings are the same day, so we don't change the date
                for pericope in re.finditer(is_pericope,corr_article):
                    article_dict[pericope.group(0)]=article_dict.get(pericope.group(0),[])+[corr_article]
                    
    return article_dict,year_dict                    
                        

def print_date(year=datetime.date.today().year):
    ''' Возвращает в виде строки пару "месяц число" для статей месяцеслова, чтобы вписывать их 
    в соответствующую строку в начале. '''
    
    yield 1,30 # пропускаем начальные строки, туда дату ставим любую
    for month in [9,10,11,12,1,2,3,4,5,6,7,8]:
        for day in range(1,calendar.monthrange(year,month)[1]+1):# так как месяцеслов високосный, 
        #то и год year должен быть любой високосный
            yield month,day                        
                        
def add_month_services(article_dict=None,year_dict=None,
                        file_name="6sobornik.hip",
                        year=datetime.date.today().year):
    
    ''' The function opens a hip file
    
    file_name - name of a .hip file
    
    article_dict - dictionary of articles where to add articles from file,
    it is a collection of key:value
    where key - is pericope and value is a list of articles from the file where 
    that pericope occures with appended at the beginning month and day.
    
    year_dict - is a dictionary of the same articles but wit key - datetime of year "year"
    
    The articles in the file  are themselves separated in 
    the file with \n\n and a Church-slavonic number" '''
    
    if article_dict is None:
        article_dict={}

    if year_dict is None:
        year_dict={}

    with open(file_name, encoding="utf8") as file:
        list_of_articles=re.split('\n\n..?~.?.? ',file.read()) #splitting into articles
        #which start with \n\n and a Church-slavonic number making a simple list of them
    #print(list_of_articles) 
    #f=open("log","w+") #DEBUG
    new_date=print_date() # print_date()- iterator that generates date to store in an article
    for article in list_of_articles: #creating dictionary for each gospel reading
        try:
            date_key=datetime.date(year,*next(new_date))
        except:
            continue #the articles include saint John Cassian for leap year, so we skip ortherwise 
        if date_key==datetime.date(year,1,5):
            continue  #5 января под Богоявление не положено никакой памяти дату не проставляем
        corr_article=article.replace("\n","").replace(",","").replace(" зача'ло","") 
        #for unification we eliminate commas as well
        #because in some articles commas are missing and \n is inside important sequences (keys)
        if re.search(is_pericope,corr_article):
            corr_article=re.sub(is_pericope,r"\1\2~\3",corr_article) #remove `= and leave only ~
            corr_article=date_key.strftime("%Y %m %d ")+corr_article 
            #in the article table we keep it in old style
            date_key+=datetime.timedelta(NEW_OLD_DIFF) #in the year table we keep it in new style
            year_dict[date_key]=year_dict.get(date_key,[])+[corr_article]
            #each gospel reading contains list of saints(articles about each saint)
            for pericope in re.finditer(is_pericope,corr_article):
                article_dict[pericope.group(0)]=article_dict.get(pericope.group(0),[])+[corr_article]
            
            '''if (pericope.group(0)=="луки`, зача'ло н~а"): # DEBUG
            print(month_day+article, end="\n**********\n",file=f)'''
    #f.close()
    return article_dict, year_dict
    
    
    
def add_general_services(article_dict=None, file_name="7obtreb.hip"):
    ''' добавляет к словарю статей из месяцеслова article_dict также статьи
    из раздела общей службы святым из файла filename'''
    
    if article_dict is None:
        article_dict={}

    with open(file_name, encoding="utf8") as file:
        list_of_articles=re.split('\n\n%<',file.read())
    for article in list_of_articles:
        corr_article=article.replace("\n","").replace(",","").replace(" зача'ло","")
        #sometimes there is no commas, that is why we have to replace twice for unification (eliminate ,)
        corr_article=re.sub(is_pericope,r"\1\2~\3",corr_article) #remove `= and leave only ~
        for pericope in re.finditer(is_pericope,corr_article):
            #if not article_dict.get(pericope.group(0)): #добавляем общее святым только если нет других
            #this comment depends on the algorithmic decision
                article_dict[pericope.group(0)]=article_dict.get(pericope.group(0),[])+[corr_article]
        
    #добавить в словарь зачала, указанные с помощью "или" в файле общих служб святым #FIXME hardcode
    #print(len(article_dict["луки` н~а"])) #DEBUG
    key="луки` н~а"
    article_dict[key]=article_dict.get(key,[])+[
"Слу'жба ст~ы'хъ а=п\\слwвъ _о='бща.%> _Е=v\\глiе а=п\\сла" 
"_е=ди'нагw, матfе'а, зача'ло л~д. А=п\\слwмъ _о='бще," 
"_е=v\\глiе луки`, зача'ло н~ и=ли` н~а."]
    key="луки` н~в"
    article_dict[key]=article_dict.get(key,[])+[
"Слу'жба сщ~енному'ченикwвъ _о='бща.%> _Е=v\\глiе луки`," 
"зача'ло к~д, и=ли` н~в, и=ли` _о~з."]
    key="луки` _о~з"
    article_dict[key]=article_dict.get(key,[])+[
"Слу'жба сщ~енному'ченикwвъ _о='бща.%> _Е=v\\глiе луки`," 
"зача'ло к~д, и=ли` н~в, и=ли` _о~з."]
    key="матfе'а _о~в"
    article_dict[key]=article_dict.get(key,[])+[
"Над\\ъ и=му'щимъ ду'хъ неду'га:%> _Е=v\глiе матfе'а," 
"зача'ло к~и, и=ли` _о~в. И=ли` ма'рка, зача'ло f~_i, и=ли`" 
"м~. И=ли` луки`, м~s. (л. с_е~_i w=б.)"]
    key="ма'рка м~"
    article_dict[key]=article_dict.get(key,[])+[
"Над\\ъ и=му'щимъ ду'хъ неду'га:%> _Е=v\\глiе матfе'а," 
"зача'ло к~и, и=ли` _о~в. И=ли` ма'рка, зача'ло f~_i, и=ли`" 
"м~. И=ли` луки`, м~s. (л. с_е~_i w=б.)"]

# we another service with a misprint in pericope (= instead of ~)
    key="матfе'а и~ w\т полу`"
    article_dict[key]=article_dict.get(key,[])+[
"Во о_у=мире'нiи и= соедине'нiи правосла'вныя вjь'ры:%>" 
"_Е=v\глiе матfе'а, зача'ло и= w\т полу`."]

    '''print(len(article_dict["луки`, зача'ло н~а"]))
    print(list(article_dict["луки`, зача'ло н~а"][0]),end='') #DEBUG
    print(list_of_articles[-1])
    for i in article_dict.values():
        print(len(i))
    print(len(article_dict))'''
    
    return article_dict
    
    
