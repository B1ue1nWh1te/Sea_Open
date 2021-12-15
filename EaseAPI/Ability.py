import requests
import time
import json
import sys
import re
import Logger


# 初始化
try:
    Logger.Log("[使能初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # 使能配置
    Headers = Setting["Ability"]["Headers"]
    EaseApi = Setting["Ability"]["EaseApi"]

    Logger.Log("[使能初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[使能初始化异常]异常信息为:{}".format(ExceptionInformation)
    Logger.Log(Text)
    sys.exit(0)


# 搜索网易云音乐
def GetSongs(Name=""):
    try:
        if Name == "":
            Logger.Log(f"[搜索接口]未输入歌曲名称")
            return {"code": -1, "data": ""}
        Logger.Log(f"[搜索接口]正在搜索[{Name}]")
        EaseDict = requests.get(EaseApi, params={"keywords": Name}, headers=Headers, timeout=3).json()
        if EaseDict["code"] == 200:
            musicurl = []
            musicname = []
            singer = []
            imageurl = []
            for i in range(5):
                musicurl.append(f"http://music.163.com/song/media/outer/url?id={EaseDict['result']['songs'][i]['id']}.mp3")
                musicname.append(EaseDict["result"]["songs"][i]["name"])
                singer.append(EaseDict["result"]["songs"][i]["artists"][0]["name"])
                imageurl.append(EaseDict["result"]["songs"][i]["artists"][0]["img1v1Url"])
            Data = []
            for i in range(5):
                Data.append({"name": musicname[i], "artist": singer[i], "cover": imageurl[i], "source": musicurl[i], "url": "", "favorited": "true"})
            Logger.Log(f"[搜索接口]获取[{Name}]歌曲信息成功")
            return {"code": 200, "data": Data}
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[搜索接口]获取歌曲信息异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return {"code": -1, "data": []}
