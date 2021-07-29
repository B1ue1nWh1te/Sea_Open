import requests
import sys

# 获取天气
def GetWeather(WeatherCity):
    try:
        Url = "http://wthrcdn.etouch.cn/weather_mini?city=" + WeatherCity
        WeatherDict = requests.get(Url).json()
        WeatherDetail = "[天气信息]{}\n今日天气:{} {}/{}\n明日天气:{} {}/{}\n温馨提示:{}".format(WeatherCity, WeatherDict["data"]["forecast"][0]["type"], WeatherDict["data"]["forecast"][0]["high"].replace("高温 ", ""), WeatherDict["data"]["forecast"][0]["low"].replace(
            "低温 ", ""), WeatherDict["data"]["forecast"][1]["type"], WeatherDict["data"]["forecast"][1]["high"].replace("高温 ", ""), WeatherDict["data"]["forecast"][1]["low"].replace("低温 ", ""),  WeatherDict["data"]["ganmao"])
        return WeatherDetail
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[获取天气异常]异常信息为:{}".format(ExceptionInformation)
        Status = "获取天气异常"
        return Status
