'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-09 16:12:49
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-12-07 18:54:34
'''
from flask import Flask
from flask import request
from flask import send_from_directory, send_file, render_template, jsonify
import json

app = Flask(__name__)


@app.route("/", methods=['POST'])
def login33():
    username = request.form.get("username")
    password = request.form.get("password")
    data = json.dumps(
        {
            "username": username,
            "password": password,
            "Msg": "叶辉给了HBB一坨翔吃吃"
        },
        ensure_ascii=False)
    return data


@app.route("/get", methods=['GET'])
def get_fun():
    data = json.dumps({
        "username": "了不起的QA",
        "password": "11111"
    },
        ensure_ascii=False)
    return data


@app.route("/getConfig", methods=['GET'])
def getConfig():
    username = request.args.get("username")
    data = json.dumps({"username": username}, ensure_ascii=False)
    return data


@app.route("/report", methods=['GET'])
def getReport():
    pass


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "了不起的QA" and password == 123456:
        return {"errorCode": 200, "errorMsg": "登录成功"}
    else:
        return {"errorCode": 301, "errorMsg": "用户名或密码错误"}


@app.route("/userinfo", methods=['GET'])
def userinfo():
    username = request.args.get("username")
    if username is not None:
        return {"errorCode": 200, "userinfo": {"username": username}}
    else:
        return {"errorCode": 301, "errorMsg": "用户名非法"}


if __name__ == "__main__":
    app.run()
