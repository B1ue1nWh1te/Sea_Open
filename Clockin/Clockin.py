from PIL import Image
from io import BytesIO
import pytesseract
import requests
import json
import time
import sys
import os


# 日志
def Log(Text):
    try:
        Time = time.strftime("%H:%M:%S")
        Text = "{}  {}".format(Time, Text)
        print(Text)
        LogFile.write(Text + "\n")

    except Exception:
        ExceptionInformation = sys.exc_info()
        Time = time.strftime("%H:%M:%S")
        Text = "{}  [写入日志异常]异常信息为:{}".format(Time, ExceptionInformation)
        print(Text)


# 推送至企业微信
def PushToEnterpriseWechat(Message="", Title="自动打卡"):
    try:
        Log(Message)
        global CorpID, CorpSecret, AgentID, Manager
        Key = {"corpid": CorpID, "corpsecret": CorpSecret}
        AccessToken = {"access_token": requests.get(TokenApi, params=Key, timeout=3).json()['access_token']}
        Time = time.strftime("%m{}%d{} %H:%M:%S").format('月', '日')
        Message = "[{}]{}\n{}".format(Title, Time, Message)
        Data = {
            "touser": Manager,
            "msgtype": "text",
            "agentid": AgentID,
            "text": {
                "content": Message
            }
        }
        Data = json.dumps(Data)  # 将json转换为str
        PostResponse = requests.post(PushApi, params=AccessToken, data=Data, timeout=3)

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[推送异常]异常信息为:{}".format(ExceptionInformation)
        Log(Text)


# 解验证码
def Devercode():
    try:
        GetVercodeUrl = "https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode"
        VercodeToken = requests.get(GetVercodeUrl, headers=Headers).json()["data"]["Token"]
        VercodeUrl = "https://fangkong.hnu.edu.cn/imagevcode?token=" + VercodeToken
        VercodeResponse = requests.get(VercodeUrl, headers=Headers)
        VercodeImage = Image.open(BytesIO(VercodeResponse.content))
        Vercode = pytesseract.image_to_string(VercodeImage, config="--psm 7 vercode")  # 命令解释：指定页面分段模式 将图片视作单行文本
        if Vercode != "":
            Vercode = Vercode.replace("\n", "")
            Vercode = Vercode.replace(" ", "")
            Vercode = Vercode[:-1]
            if len(Vercode) == 4:
                return [Vercode, VercodeToken]
            else:
                return Devercode()
        else:
            return Devercode()

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[解码异常]异常信息为:{}".format(ExceptionInformation)
        Log(Text)
        return ["解码异常"]


# 登录
def Login(Username, Password):
    try:
        Log("[{}]正在尝试登录".format(Username))
        LoginUrl = "https://fangkong.hnu.edu.cn/api/v1/account/login"
        VercodeList = Devercode()
        if VercodeList[0] == "解码异常":
            Log("[登录失败]解码异常")
            return ["解码异常"]
        Vercode = VercodeList[0]
        Token = VercodeList[1]
        message = {
            'Code': Username,
            'Password': Password,
            'Token': Token,
            'Vercode': Vercode,
            'WechatUserinfoCode': ''
        }
        Data = json.dumps(message)
        LoginResponse = requests.post(LoginUrl, headers=Headers, data=Data)
        Content = LoginResponse.json()
        if Content["msg"] == "验证码错误":
            Log("[登录失败][验证码错误]程序识别出的验证码不正确,即将重试")
            return Login(Username, Password)
        elif Content["msg"] == "账号或密码错误":
            return ["账号或密码错误"]
        elif Content["msg"] == "成功":
            CookiesDict = requests.utils.dict_from_cookiejar(LoginResponse.cookies)
            Time = str(int(time.time()))
            LoginedHeaders = {
                'Host': 'fangkong.hnu.edu.cn',
                'Content-Type': 'application/json',  # 重要
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Origin': 'https://fangkong.hnu.edu.cn',
                'Referer': 'https://fangkong.hnu.edu.cn/app/',
                'Cookie': f"Hm_lvt_d7e34467518a35dd690511f2596a570e={Time};TOKEN={CookiesDict['TOKEN']};.ASPXAUTH={CookiesDict['.ASPXAUTH']}"
            }
            return LoginedHeaders
        else:
            return ["其他异常", Content["msg"]]

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[登录异常]异常信息为:{}".format(ExceptionInformation)
        Log(Text)
        return ["登录异常"]


# 获取信息
def GetInformation(LoginedHeaders):
    try:
        PersonalInfomationUrl = "https://fangkong.hnu.edu.cn/api/v1/clockinlog/isclockinloginfo"
        PersonalDict = requests.get(PersonalInfomationUrl, headers=LoginedHeaders).json()
        Name = PersonalDict["data"]["Name"]
        ClassName = PersonalDict["data"]["ClassName"]
        Status = PersonalDict["msg"]
        Information = {
            "姓名": Name,
            "班级": ClassName,
            "打卡状态": Status
        }
        return Information

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[获取信息异常]异常信息为:{}".format(ExceptionInformation)
        Log(Text)
        return ["获取信息异常"]


# 打卡
def ClockIn(LoginedHeaders, ClockinInformation):
    try:
        Province = ClockinInformation[0]
        City = ClockinInformation[1]
        Country = ClockinInformation[2]
        Address = ClockinInformation[3]
        Longitude = ClockinInformation[4]
        Latitude = ClockinInformation[5]
        Temperature = ClockinInformation[6]
        ClockInUrl = "https://fangkong.hnu.edu.cn/api/v1/clockinlog/add"
        '''message = {
            "Longitude": Longitude,
            "Latitude": Latitude,
            "RealProvince": Province,
            "RealCity": City,
            "RealCounty": Country,
            "RealAddress": Address,
            "BackState": 1,
            "MorningTemp": Temperature,
            "NightTemp": Temperature,
            "tripinfolist": []
        }'''
        message = {
            "Temperature": Temperature,
            "RealProvince": Province,
            "RealCity": City,
            "RealCounty": Country,
            "RealAddress": Address,
            "MorningTemp": Temperature,
            "NightTemp": Temperature,
            "IsUnusual": "0",
            "UnusualInfo": "",
            "IsTouch": "0",
            "IsInsulated": "0",
            "IsSuspected": "0",
            "IsDiagnosis": "0",
            "tripinfolist": [{
                "aTripDate": "",
                "FromAdr": "",
                "ToAdr": "",
                "Number": "",
                "trippersoninfolist": []
            }],
            "toucherinfolist": [],
            "dailyinfo": {
                "IsVia": "0",
                "DateTrip": ""
            },
            "IsInCampus": "0",
            "IsViaHuBei": "0",
            "IsViaWuHan": "0",
            "InsulatedAddress": "",
            "TouchInfo": "",
            "IsNormalTemperature": "1",
            "Longitude": Longitude,
            "Latitude": Latitude
        }
        Data = json.dumps(message)
        ClockInDict = requests.post(ClockInUrl, headers=LoginedHeaders, data=Data).json()
        if ClockInDict["msg"] == "成功":
            return ["成功"]
        else:
            return ["其他异常", ClockInDict["msg"]]

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[打卡异常]异常信息为:{}".format(ExceptionInformation)
        Log(Text)
        return ["打卡异常"]


# 打卡流水线
def ClockLine(Account):
    global RetryAccount
    Username = Account[0]
    Password = Account[1]
    ClockinInformation = Account[2].split("-")
    LoginedHeaders = Login(Username, Password)
    Status = list(LoginedHeaders)[0]
    if (Status == "账号或密码错误"):
        Message = "[登录失败] [{}]\n账号与密码不匹配\n警告:请手动打卡!".format(Username)
        PushToEnterpriseWechat(Message)
    elif (Status == "登录异常"):
        Message = "[登录失败] [{}]在登录时出现程序异常".format(Username)
        RetryAccount.append(Account)
        PushToEnterpriseWechat(Message)
    elif (Status == "其他异常"):
        Message = "[登录失败] [{}]\n在登录时出现其他问题\n提示为:{}".format(Username, list(LoginedHeaders)[1])
        RetryAccount.append(Account)
        PushToEnterpriseWechat(Message)
    elif (Status == "解码异常"):
        Message = "[登录失败] [{}]在登录时解码异常"
        RetryAccount.append(Account)
        PushToEnterpriseWechat(Message)
    else:
        Information = GetInformation(LoginedHeaders)
        if (list(Information)[0] == "获取信息异常"):
            Message = "[获取信息异常] [{}]\n在获取信息时出现程序异常".format(Username)
            RetryAccount.append(Account)
            PushToEnterpriseWechat(Message)
            return 1
        District = ClockinInformation[0] + ClockinInformation[1] + ClockinInformation[2]
        if (Information["打卡状态"] == "今日已打卡"):
            Message = "[今日已打] [{}]\n[姓名]{} [班级]{}\n[地区]{}".format(Username, Information["姓名"], Information["班级"], District)
            PushToEnterpriseWechat(Message)
            return 1
        Log("[{}]正在尝试打卡".format(Username))
        Status = ClockIn(LoginedHeaders, ClockinInformation)
        if (Status[0] == "成功"):
            CInformation = "[打卡信息]\n地区:{}\n早晚体温:{}℃".format(District, ClockinInformation[6])
            Message = "[打卡成功] [{}]\n[姓名]{} [班级]{}\n{}".format(Username, Information["姓名"], Information["班级"], CInformation)
            PushToEnterpriseWechat(Message)
        elif (Status[0] == "打卡异常"):
            Message = "[打卡失败] [{}]在打卡时出现程序异常".format(Username)
            RetryAccount.append(Account)
            PushToEnterpriseWechat(Message)
        elif (Status[0] == "其他异常"):
            Message = "[打卡失败] [{}]在打卡时出现其他问题\n提示为:{}".format(Username, Status[1])
            RetryAccount.append(Account)
            PushToEnterpriseWechat(Message)


# 运行开始
def Start():
    try:
        # 初始化
        global LogFile, AllAccount

        # 日志
        if not os.path.exists(os.getcwd() + "\\Log"):
            os.mkdir("Log")
        Course = f"{os.getcwd()}\\Log\\{time.strftime('%Y%m%d')}.txt"
        LogFile = open(Course, "a+", encoding="utf-8")

        # 加载数据数据
        with open("Data.txt", "r", encoding="utf-8") as DataBase:
            for line in DataBase:
                line = line.strip()
                List = line.split("---")
                AllAccount.append(List)

        ClockMain()

    except Exception:
        ExceptionInformation = sys.exc_info()
        Message = "[运行异常]警告：开始函数运行异常已退出。异常信息：{}".format(ExceptionInformation)
        PushToEnterpriseWechat(Message)
        sys.exit(1)


# 运行即将结束
def Finish():
    try:
        Message = "打卡已完成"
        PushToEnterpriseWechat(Message)
        Log("程序正常结束\n" + "-" * 50)
        LogFile.close()

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "程序未正常结束\n异常信息为:{}".format(ExceptionInformation)
        Log(Text)
        LogFile.close()
        sys.exit(1)


# 主函数
def ClockMain():
    try:
        global RetryAccount, AllAccount
        Url = "https://fangkong.hnu.edu.cn/app/"
        Try = requests.get(Url, headers=Headers, timeout=30)
        Code = Try.status_code
        if (Code != 200):
            Message = "[连接失败]将在3分钟后再次尝试连接"
            PushToEnterpriseWechat(Message)
            time.sleep(180)
            Try = requests.get(Url, headers=Headers, timeout=30)
            Code = Try.status_code
            if (Code == 200):
                Message = "[重连成功]"
                PushToEnterpriseWechat(Message)
            else:
                Message = "[连接失败]警告：主函数已退出。"
                PushToEnterpriseWechat(Message)
                sys.exit(1)

        for Account in AllAccount:
            ClockLine(Account)
        if (len(RetryAccount) != 0):
            Message = "即将对之前出现异常的账户进行重新尝试"
            PushToEnterpriseWechat(Message)
            for Account in RetryAccount:
                ClockLine(Account)
        Finish()

    except Exception:
        ExceptionInformation = sys.exc_info()
        Message = "[运行异常]警告:主函数运行异常 已退出\n异常信息:{}".format(ExceptionInformation)
        PushToEnterpriseWechat(Message)
        sys.exit(1)


if __name__ == '__main__':
    LogFile = ""  # 日志文件对象
    AllAccount = []  # 队列中所有账户的数据
    RetryAccount = []  # 队列中要重试的所有账户的数据
    Headers = {
        'Host': 'fangkong.hnu.edu.cn',  # 构造来源链接
        'Content-Type': 'application/json',  # 重要
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }

    # 企业微信Key
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)
    CorpID = Setting["EnterpriseWechat"]["CorpID"]
    CorpSecret = Setting["EnterpriseWechat"]["CorpSecret"]
    AgentID = Setting["EnterpriseWechat"]["AgentID"]
    Manager = Setting["EnterpriseWechat"]["ManagerID"]
    TokenApi = Setting["EnterpriseWechat"]["TokenApi"]
    PushApi = Setting["EnterpriseWechat"]["PushApi"]

    Start()
