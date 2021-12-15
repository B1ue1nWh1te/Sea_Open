from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import sys

from Ability import *
import Logger


# 初始化
try:
    Logger.Log("[API服务初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # API服务配置
    Host = Setting["Api"]["Host"]
    Port = Setting["Api"]["Port"]
    app = Flask(__name__)
    CORS(app)
    Logger.Log("[API服务初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[API服务初始化异常]异常信息为:{}".format(ExceptionInformation)
    Logger.Log(Text)
    sys.exit(0)


# 网易云搜索接口
@app.route('/search/', methods=['GET'])
def Search():
    Name = request.args.get("name")
    result = GetSongs(Name)
    return jsonify(result)


if __name__ == "__main__":
    #app.run(host=Host, port=Port, use_reloader=True, debug=True)
    WSGIServer((Host, Port), app).serve_forever()
