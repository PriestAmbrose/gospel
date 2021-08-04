import collections
import datetime
import read_hip
import spec_days

def peri_sort(key):
    gospels={"матfе'а":0,"ма'рка":200,"луки`":400,"i=wа'нна":600}
    slav_numbers={"р":100,"i":10,"к":20,"л":30,"м":40,"н":50,"о":70,"п":80,"с":40,"ч":90,
    "а":1,"в":2,"г":3,"д":4,"е":5,"s":6,"з":7,"и":8,"f":9}
    result=gospels[key.split()[0]]
    for letter in key.split()[1]:
        result+=slav_numbers.get(letter,0)
    return result


#article_dict,year_dict=read_hip.add_daily_readings(year=2020)
article_dict1,year_dict1=read_hip.add_month_services(year=2020)#should be 99 articles
#FIXME that algorithm doesn't take into account 
#readings change for Exaltation of the Cross and Epiphany
#also it have problems for Carnival readings

#article_dict2=read_hip.add_general_services() #used to give 62 articles
#TODO the resultive year does not include special days from previous and next year
#this return tuple of article, year dictionary 
#for today year

spec_days.correct_specday_dates(article_dict1, year_dict1,year=2021)
#datetime.datetime.today().year)

'''for key in article_dict1:
    print(key,peri_sort(key))'''

'''d=collections.OrderedDict(sorted(
    read_hip.add_general_services(
        article_dict
        ).items(),key=lambda x:len(x[1])
    ))'''
    

d=collections.OrderedDict(sorted(article_dict1.items(),
    key=lambda x:datetime.date(*map(int,x[1][0][:11].split()))
    #key=lambda x:len(x[1])
    #key=lambda x:x[1][0]
    #key=lambda x:peri_sort(x[0])
    ))

f=open("3.hip","w", encoding="utf8")
for k,v in d.items():
    if len(v)==1:
        print(k,len(v),v,"\n\n",file=f)
f.close()
print(d)

'''unique_articles={k:v for k,v in d.items() if len(v)==1}
for key in unique_articles:
    day=datetime.date(*map(int,unique_articles[key][0][:10].split()))\
    +datetime.timedelta(read_hip.NEW_OLD_DIFF)
    print(key, day, year_dict.get(day,[]))'''

'''f=open("3.hip","w")
i=1
for key in article_dict2:
    if key not in article_dict1:
        print(i,key,len(article_dict2[key]), *article_dict2[key],sep="\n",file=f,end="\n\n")
        i+=1
f.close()  #there are altogether 62 articles 31 common with the monthly services,
#31 are unique, including 4 unique general services: to prophets, women martyrs, priest martyrs,
#apostles/unmercinaries'''
    
'''f=open("2.hip","w")
print(*[x for x in d.items() if len(x[1])==1],sep="\n\n",file=f)
'''

'''hard code section
мы сохраняем уникальность чтений из месяцеслова, то есть не трогаем те чтения,
которые встречаются только один раз
те, которые встречают много раз - мы оставляем уникальные назначение конкретному святому,
предпочтение отдавая тому, что указано в самом Евангелии
а назначения общие мы убираем, с целью как можно более тематического покрытия дней '''
# При заглядывании в Евангелие выяснилось, что МФ. 39 - это суббота 7 либо перед Воздвижением
    # выбираем, значит, перед воздвижением
    # Мф. 8 - это неделя по просвещении
