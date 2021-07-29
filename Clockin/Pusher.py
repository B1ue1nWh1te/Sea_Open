import requests
import time
import json
import sys

# 初始化
try:
    with open("Setting.json", "r") as f:
        Setting = json.load(f)

    # 企业微信Key
    CorpID = Setting["EnterpriseWechat"]["CorpID"]
    CorpSecret = Setting["EnterpriseWechat"]["CorpSecret"]
    AgentID = Setting["EnterpriseWechat"]["AgentID"]
    Manager = Setting["EnterpriseWechat"]["ManagerID"]

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[推送初始化异常]异常信息为:{}".format(ExceptionInformation)
    print(Text)


# 推送至企业微信
def PushToEnterpriseWechat(Message="", Type="text", Receiver="all", **kwargs):
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
                Articles.append({"title": kwargs.get("Title", "未定义标题"), "description": kwargs.get("Description", "未定义描述"), "url": kwargs.get(
                    "URL", "https://www.seaeye.cn/404.html"), "picurl": kwargs.get("ImageUrl", "https://www.seaeye.cn/img/404.jpg")})
            Data = {
                "touser": ToUser,
                "msgtype": "news",
                "agentid": AgentID,
                "news": {"articles": Articles}
            }
        Data = json.dumps(Data)  # 将json转换为str
        PostResponse = requests.post(PushUrl, Data)
        if (PostResponse.status_code == 200):
            print("[推送成功]")
            Status = "推送成功"
            return Status
        else:
            print("[推送失败]PostResponse状态码为:{}".format(PostResponse.status_code))
            Status = "推送失败"
            return Status
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[推送异常]异常信息为:{}".format(ExceptionInformation)
        print(Text)
        Status = "推送异常"
        return Status


if __name__ == "__main__":
    try:
        Type = input("输入消息类型:")
        if Type == "text":
            Message = input("输入指令:")
            Message, Receiver, Title = Message.split()
            flag = input("是否确定发送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat(Message, Type, Receiver, Title=Title)
            else:
                print("取消发送")
        elif Type == "image_text":
            Message = input("输入指令:")
            Receiver, Articles = Message.split()
            Articles = eval(Articles)
            flag = input("是否确定发送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat("", Type, Receiver, Articles=Articles)
            else:
                print("取消发送")
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[运行异常]异常信息为:{}".format(ExceptionInformation)
        print(Text)
