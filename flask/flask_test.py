'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-07-09 16:12:49
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-07-09 16:39:25
'''
from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route("/", methods=['POST'])
def login():
    username = request.form.get("username1")
    password = request.form.get("password1")
    data = json.dumps({
        "username": username,
        "password": password,
        "Msg":"叶辉给了HBB一坨翔吃吃"
    }, ensure_ascii=False)
    return data


if __name__ == "__main__":
    app.run()