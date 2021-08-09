'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-09 16:12:49
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-08-04 00:37:31
'''
from flask import Flask
from flask import request
from flask import send_from_directory, send_file, render_template, jsonify
import json

app = Flask(__name__)


@app.route("/", methods=['POST'])
def login():
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
        "username": "叶辉",
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


if __name__ == "__main__":
    app.run()
