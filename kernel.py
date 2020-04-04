from aip import AipSpeech
import json
import urllib
import pygame
import time
import eyed3
import sys
import os
#sys.setdefaultencoding('utf-8')

baidu_APP_ID = '17299746'
baidu_API_KEY = 'lHUQUx9TD0IijABK2VpAQplh'
baidu_SECRET_KEY = '8NugvwVtvkcA7dxWAfNYXfa0D3LeAsa4'


def playmusic(music, times):
    music_file = eyed3.load(music)
    secs = int(music_file.info.time_secs)
    sample_freq = int(music_file.info.sample_freq)
    pygame.mixer.init(frequency=sample_freq)
    pygame.mixer.music.load(music)

    pygame.mixer.music.play()
    #os.system('mplayer %s' % music)
    if times == 'auto':
        time.sleep(secs)
    else:
        time.sleep(times)
    pygame.mixer.music.stop()
    #os.system('mplayer q')


def word2speech(str, type):
    client = AipSpeech(baidu_APP_ID, baidu_API_KEY, baidu_SECRET_KEY)
    result = client.synthesis(str, 'zh', 1, {
        'vol': 5,
    })
    soud_name = './data/'+type+'_auido.mp3'
    if not isinstance(result, dict):
        with open(soud_name, 'wb') as f:
            f.write(result)
        f.close()
        os.system('mplayer %s' % soud_name)



weather_app_key = '04ff5e899833087159256726d6c1e684'


def request_weather(city):
    url = "http://op.juhe.cn/onebox/weather/query"
    params = {
        "cityname": city,  # 要查询的城市，如：温州、上海、北京
        "key": weather_app_key,  # 应用APPKEY(应用详细页查询)
        "dtype": "",  # 返回数据的格式,xml或json，默认json

    }
    params = urllib.parse.urlencode(params).encode(encoding='UTF-8')
    f = urllib.request.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
            return res
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return 'NO DATA'
    else:
        print("request api error")
        return 'NO DATA'


news_app_key = '11c0c9885bc4c6433930a8aab25a0754'


def request_news(contant):
    url = "http://v.juhe.cn/toutiao/index"
    params = {
        # top(头条，默认),shehui(社会),guonei(国内),guoji(国际),yule(娱乐),tiyu(体育)junshi(军事),keji(科技),caijing(财经),shishang(时尚)
        "type": contant,
        "key": news_app_key,  # 应用APPKEY(应用详细页查询)
    }
    params = urllib.parse.urlencode(params).encode(encoding='UTF-8')
    f = urllib.request.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
            return res
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
            return 'NO DATA'
    else:
        print("request api error")
        return 'NO DATA'


def read_weather(cityname):
    weather_data = request_weather(cityname)
    if weather_data != 'NO DATA':
        read_weather_data = '早上好,今天'+cityname+'天气' + weather_data['result']['data']['realtime']['weather']['info'] + \
            ',实时气温' + \
            weather_data['result']['data']['realtime']['weather']['temperature'] + \
            '摄制度.空气湿度,百分之' + \
            weather_data['result']['data']['realtime']['weather']['humidity'] + \
            weather_data['result']['data']['realtime']['wind']['direct'] + \
            weather_data['result']['data']['realtime']['wind']['power'] + \
            ', 新的一天,要有个好心情哟'
        dt = list(time.localtime())
        result = str(dt[0])+str(dt[1])+str(dt[2])+str(dt[3])+str(dt[4])+'weather'
        word2speech(read_weather_data, result)


def read_news(contant, num):
    news_data = request_news(contant)
    read_data = ''
    if news_data != 'NO DATA':
        for num in range(num):
            read_data += '今日要闻, 第' + \
                str(num+1)+'条, ' + \
                    news_data["result"]['data'][num]['title']+'. '
        read_data += '今日要闻播报完毕, 记得吃早餐哟!'
        dt = list(time.localtime())
        result = str(dt[0])+str(dt[1])+str(dt[2])+str(dt[3])+str(dt[4])+'news'
        word2speech(read_data, result)

# while True:
#     data={}
#     with open("set.json",'r',encoding='utf-8') as json_file:
#         data=json.load(json_file)
#     json_file.close()
#     dt = list(time.localtime())  
#     hour = dt[3]  
#     minute = dt[4]  
#     print(hour)
#     print(minute)
#     if hour == data['hour'] and minute == data['minute'] :
#         playmusic('back.mp3',20)
#         read_weather(data['city'])
#         playmusic('back.mp3',5)
#         read_news(data['content'],5)
#     time.sleep(5)

# data={}
# with open("set.json",'r',encoding='utf-8') as json_file:
#     data=json.load(json_file)
# json_file.close()
# # playmusic('back.mp3',20)
# read_weather(data['city'])
# # playmusic('back.mp3',5)
# read_news(data['content'],5)
