import requests
import settings

settings.init()

def weatherNow():
    appId = settings.WEATHER_TOKEN
    res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': 'Mogilev,BY', 'type': 'like', 'units': 'metric', 'APPID': appId})
    data = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
        for d in data['list']]
    city_id = data['list'][0]['id']

    res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appId})
    data = res.json()
    tempNowInt = round((data['main']['temp_min'] + data['main']['temp_max']) /2 )
    if tempNowInt > 0:
        tempNowStr = '+' + str(tempNowInt)
    else:
        tempNowStr = str(tempNowInt)
    weather = 'Погода в *Могилеве* сейчас: \n ' + tempNowStr + '℃\n' + str(data['weather'][0]['description']) + getEmoji(str(data['weather'][0]['description']))
    return weather

def weatherFiveDays():
    appId = settings.WEATHER_TOKEN
    res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': 'Mogilev,BY', 'type': 'like', 'units': 'metric', 'APPID': appId})
    data = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
        for d in data['list']]
    city_id = data['list'][0]['id']
    textMassage = ''
    res1 = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appId})
    data = res1.json()
    weather = 'Погода в Могилеве \n'
    dayBefore = ''
    for i in data['list']:
        dayNow = str(i['dt_txt'])[0:10]
        weatherDescription = i['weather'][0]['description']
        if dayNow != dayBefore:
            weather = weather + '         📅*' + dayNow + '*📅' + '\n'
        tempNowInt = round((i['main']['temp_min'] + i['main']['temp_max']) /2 )
        if tempNowInt > 0:
            tempNowStr = '+' + str(tempNowInt)
        else:
            tempNowStr = str(tempNowInt)
        weather = weather + '⌚' + str(i['dt_txt'])[11:20]+ ' *' + tempNowStr + '* ℃ ' + weatherDescription + str(getEmoji(weatherDescription)) + '\n'
        dayBefore = dayNow
    return weather

def getEmoji(weather):
    if weather == 'пасмурно':
        return "☁"
    elif weather == 'переменная облачность':
        return "☁☀☁"
    elif weather == 'облачно с прояснениями':
        return "⛅"
    elif weather == 'небольшая облачность':
        return "☀☁"
    elif weather == 'дождь':
        return "🌧"
    elif weather == 'небольшой дождь':
        return "🌦"
    elif weather == 'ясно':
        return "🌞"
    else:
        return " "