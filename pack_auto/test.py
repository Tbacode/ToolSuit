'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-04-22 10:44:57
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-05-06 10:28:11
'''
from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/')
def Home():
    data = json.dumps({"username": "Tommy", "password": "1123444"})
    return data


@app.route('/login', methods=['GET'])
def Login():
    username = request.args.get("username")
    password = request.args.get("password")
    data = json.dumps({"username": username, "password": password})
    return data


@app.route('/getGalleyList', methods=['GET'])
def get_GalleyList():
    '''
    getGalleyList 路由
    '''
    data = json.dumps({
        "data": {
            "errorcode": 100,
            "picList": [{
                "picName": "111111"
            }, {
                "picName": "222222"
            }]
        }
    })
    return data


if __name__ == "__main__":
    app.run()