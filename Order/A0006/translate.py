import requests
import random
from hashlib import md5

# API KEY
appid = '输入你的APPID'
appkey = '输入你的APPKEY'

api = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}


# 生成MD5签名
def makeMD5(s, encoding='utf-8'):
    temp = s.encode(encoding)
    result = md5(temp).hexdigest()
    return result


# 输入英文字符串，执行翻译
def translate(query):
    try:
        salt = random.randint(32768, 65536)
        string = appid + query + str(salt) + appkey
        sign = makeMD5(string)
        payload = {'appid': appid, 'q': query, 'from': 'en', 'to': 'zh', 'salt': salt, 'sign': sign}
        r = requests.post(api, params=payload, headers=headers)
        result = r.json()
        result = result["trans_result"][0]["dst"]
        return result
    except:
        print("[翻译出错]请检查文本、网络、API账户、访问频率等是否正常")
        return None


if __name__ == "__main__":
    q = input("请输入要翻译的英文：")
    while q != "":
        print(f'翻译结果：{translate(q)}')
        q = input("请输入要翻译的英文：")
