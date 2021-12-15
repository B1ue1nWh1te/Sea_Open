from io import BytesIO
import requests
import time
import cv2
import sys
import re

Information = "[安全微课自动刷课脚本]已启动\n使用前请确保你之前已经进入过安全微课且完成了初始化的考试\n"

# 构造请求头
Headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

# 获取时间戳


def GetTimeStamp():
    return round(time.time())

# 登录


def Login():
    # 获取时间戳
    TimeStamp = GetTimeStamp()

    print("正在获取登录二维码")

    # 访问登录二维码接口
    LoginBarCodeApi = f"https://weiban.mycourse.cn/pharos/login/genBarCodeImageAndCacheUuid.do?timestamp={TimeStamp}"
    data = requests.get(LoginBarCodeApi, headers=Headers).json()["data"]

    # 暂存二维码相关数据
    BarCodePayload = {"barCodeCacheUserId": data["barCodeCacheUserId"]}
    BarCodeImageUrl = data["imagePath"]

    # 获取二维码图片
    BarCodeImage = cv2.VideoCapture(BarCodeImageUrl).read()[1]

    print("使用微信扫码授权登录后关闭二维码窗口")

    # 展示二维码
    cv2.imshow("Scan", BarCodeImage)
    cv2.waitKey(0)

    # 刷新时间戳
    TimeStamp = GetTimeStamp()

    # 扫码验证
    BarCodeCheckApi = f"https://weiban.mycourse.cn/pharos/login/barCodeWebAutoLogin.do?timestamp={TimeStamp}"
    data = requests.post(BarCodeCheckApi, headers=Headers, data=BarCodePayload).json()

    if(data["code"] != '0'):
        print("登录失败 请检查扫码情况")
    else:
        # 读取用户token
        data = data["data"]
        tenantCode = data["tenantCode"]
        token = data["token"]
        userId = data["userId"]
        userProjectId = data["normalUserProjectId"]

        # 刷新时间戳
        TimeStamp = GetTimeStamp()

        # 获取个人信息接口
        GetInformationApi = f"https://weiban.mycourse.cn/pharos/my/getInfo.do?timestamp={TimeStamp}"
        Payload = {
            'userId': userId,
            'tenantCode': tenantCode,
            'token': token
        }
        data = requests.post(GetInformationApi, headers=Headers, data=Payload).json()["data"]

        # 读取用户姓名学号
        Name = data["realName"]
        Number = data["studentNumber"]

        print("[{} {}]登录成功 开始自动刷课\n".format(Name, Number))
        Study(tenantCode, token, userId, userProjectId)

# 刷课主函数


def Study(tenantCode, token, userId, userProjectId):
    try:
        CourseType = {'3': "必修课程", '1': "匹配课程", '2': "自选课程"}
        for chooseType in CourseType:
            print("当前处理[{}]".format(CourseType[chooseType]))
            # 限制自选课的刷课数量
            if(chooseType == "2"):
                n = 10
            else:
                n = 300

            Name1 = CourseType[chooseType]
            Payload1 = {
                'userProjectId': userProjectId,
                'chooseType': chooseType,
                'userId': userId,
                'tenantCode': tenantCode,
                'token': token
            }

            # 刷新时间戳
            TimeStamp = GetTimeStamp()

            # 获取大类课程列表接口
            GetListApi = f"https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp={TimeStamp}"
            data1 = requests.post(GetListApi, headers=Headers, data=Payload1).json()["data"]

            for i in data1:
                if(int(i["finishedNum"]) < int(i["totalNum"])):
                    Name2 = i["categoryName"]
                    categoryCode = i["categoryCode"]
                    Payload2 = {
                        'userProjectId': userProjectId,
                        'chooseType': chooseType,
                        'categoryCode': categoryCode,
                        'name': '',
                        'userId': userId,
                        'tenantCode': tenantCode,
                        'token': token
                    }

                    # 刷新时间戳
                    TimeStamp = GetTimeStamp()

                    # 获取课程列表接口
                    GetItemApi = f"https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp={TimeStamp}"
                    data2 = requests.post(GetItemApi, headers=Headers, data=Payload2).json()["data"]

                    for j in data2:
                        # 刷课数量达标则退出
                        if(n == 0):
                            break
                        if(j["finished"] != 1):
                            Name3 = j["resourceName"]
                            resourceId = j["resourceId"]

                            # 刷新时间戳
                            TimeStamp = GetTimeStamp()

                            # 开始学习接口
                            StudyApi = f"https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={TimeStamp}"
                            StudyPayload = {
                                'courseId': resourceId,
                                'userProjectId': userProjectId,
                                'tenantCode': tenantCode,
                                'userId': userId,
                                'token': token
                            }
                            rs = requests.post(StudyApi, headers=Headers, data=StudyPayload)

                            # 新增了延迟10.1秒
                            time.sleep(10.1)

                            userCourseId = j.get("userCourseId", "")
                            # userCourseId为空时的处理
                            if(userCourseId == ""):
                                # 刷新时间戳
                                TimeStamp = GetTimeStamp()

                                # 获取课程链接接口
                                GetCourseUrlApi = f"https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp={TimeStamp}"
                                data3 = requests.post(GetCourseUrlApi, headers=Headers, data=StudyPayload).json().get("data", "")

                                # 仍无法获取userCourseId，跳过
                                if(data3 == ""):
                                    print(f"[{Name1}-{Name2}-{Name3}]无法获取userCourseId 已跳过")
                                    continue
                                userCourseId = re.findall('userCourseId\\u003d(.*?)\\u0026tenantCode', data3)[0]

                            # 完成学习接口
                            TimeStamp = int(round(time.time() * 1000))
                            FinishApi = f"https://weiban.mycourse.cn/pharos/usercourse/finish.do?userCourseId={userCourseId}&tenantCode={tenantCode}&_={TimeStamp}"
                            rf = requests.get(FinishApi, headers=Headers)
                            if(rs.status_code == 200 and rf.status_code == 200):
                                n -= 1
                                print(f"[{Name1}-{Name2}-{Name3}]已自动完成")
                            else:
                                print(f"[{Name1}-{Name2}-{Name3}]失败")
            print("[{}]已完成\n".format(CourseType[chooseType]))
        print("自动刷课完成")
    except requests.exceptions.ConnectionError:
        print("连接断开 即将重试")
        Study(tenantCode, token, userId, userProjectId)
    except Exception:
        ExceptionInformation = sys.exc_info()
        Time = time.strftime("%H:%M:%S")
        Text = "[{}][运行异常]异常信息为:{}\n即将重试".format(Time, ExceptionInformation)
        print(Text)
        Study(tenantCode, token, userId, userProjectId)


if __name__ == '__main__':
    print(Information)
    Login()
