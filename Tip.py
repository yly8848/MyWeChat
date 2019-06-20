import requests


# 每日播报


def get_ciba():
    '''获取每日一句'''
    reqs = requests.get('http://open.iciba.com/dsapi')
    json = reqs.json()
    content = json['content']
    note = json['note']
    return f"{content}\n{note}"


def get_weather(city_code):
    '''天气情况'''

    weather_url = f'http://t.weather.itboy.net/api/weather/city/{city_code}'
    reqs = requests.get(weather_url)
    json = reqs.json()

    status = json['status']
    if status is 200:
        city = json['cityInfo']['city']

        # 时间
        ymd = json['data']['forecast'][0]['ymd']
        week = json['data']['forecast'][0]['week']

        # 温度
        wendu = json['data']['wendu'] + '℃'
        high = json['data']['forecast'][0]['high']
        low = json['data']['forecast'][0]['low']

        # 风向风力
        fx = json['data']['forecast'][0]['fx']
        fl = json['data']['forecast'][0]['fl']

        # 天气描述
        types = json['data']['forecast'][0]['type']
        notice = json['data']['forecast'][0]['notice']

        return f"{ymd} {week}\n{city}\n{fx} {fl}\n温度: {wendu} {types}\n{high} {low}\n{notice}"

    else:
        return ""
