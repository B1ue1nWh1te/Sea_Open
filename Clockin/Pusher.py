import requests
import time
import json
import sys

# 初始化
try:
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # 企业微信Key
    CorpID = Setting["EnterpriseWechat"]["CorpID"]
    CorpSecret = Setting["EnterpriseWechat"]["CorpSecret"]
    AgentID = Setting["EnterpriseWechat"]["AgentID"]
    Manager = Setting["EnterpriseWechat"]["ManagerID"]

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[推送初始化异常]异常信息为:{}".format(ExceptionInformation)


# 推送至企业微信
def PushToEnterpriseWechat(Type="text", Receiver="all", Message="", **kwargs):
    try:
        global CorpID, CorpSecret, AgentID, Manager
        Key = {"corpid": CorpID, "corpsecret": CorpSecret}
        ResponseDict = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken", params=Key).json()
        PushUrl = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ResponseDict['access_token']}"

        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = Manager
        else:
            ToUser = "|".join(Receiver)

        if Type == "text":
            Time = time.strftime("%m{}%d{} %H:%M:%S").format('月', '日')
            Message = "[{}]{}\n{}".format(
                kwargs.get("Title", "未定义标题"), Time, Message)
            Data = {
                "touser": ToUser,
                "msgtype": "text",
                "agentid": AgentID,
                "text": {
                    "content": Message
                }
            }
        elif Type == "image_text":
            Articles = kwargs.get("Articles", [])

            if len(Articles) == 0:
                Text = "[推送失败]内容为空"
                return 0

            Data = {
                "touser": ToUser,
                "msgtype": "news",
                "agentid": AgentID,
                "news": {"articles": Articles}
            }

        Data = json.dumps(Data)  # 将json转换为str
        PostResponse = requests.post(PushUrl, Data)

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[推送异常]异常信息为:{}".format(ExceptionInformation)
