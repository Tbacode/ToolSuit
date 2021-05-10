import socket
import re
import AutoPack
import requests

HOST = ''
PORT = 9999
# 打包
PACKAGE_METHOD = '/package'
# 获取包对应的git hash
GET_HASH_BY_PACKAGE_METHOD = '/gethash'
# 项目KEY
PROJECT_KEY = 'project'
# 打包平台KEY
PLATFORM_KEY = 'platform'
# 是否显示debug按钮
DEBUG_KEY = 'debug'
# 版本key
VERSION_KEY = 'version'
# 是否需要合并develop分支
UN_MERGE_KEY = 'unmerge'
# 指定需要合并的打包分支
ASSIGN_BRANCH_KEY = 'assign_branch'
# 打包说明信息 由机器人转发给群里 必须选项
MESSAGE_CONTENT_KEY = 'message'
# 没有指定版本的时候 默认打包仓库
DEFAULT_BRANCH = 'default'
# 使用引擎版本 如果不指定 tile默认使用2.3.4 bf默认使用2.4.4
ENGINE_VERSION = 'engine'
# 压图 默认不传 就不压图 目前只有bf生效
COMPRESS_PICTURE = 'compress'


class HttpService:
    def __init__(self):
        self.m_serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                       1)
        self.m_ispacking = False

    def start(self):
        self.m_serverSocket.bind((HOST, PORT))
        self.m_serverSocket.listen(100)
        while True:
            clientSocket, clientAddr = self.m_serverSocket.accept()
            clientip = clientAddr[0]
            request = clientSocket.recv(1024).decode()
            content = self.parseRequest(request, clientip)
            self.sendResponse(content, clientSocket)

    def sendResponse(self, content, clientSocket):
        response_start_line = 'HTTP/1.1 200 OK\r\n'
        response_headers = 'Server: My server\r\n'
        response = response_start_line + response_headers + '\r\n' + content
        clientSocket.sendall(response.encode())
        clientSocket.close()

    def parseRequest(self, request, clientip):
        if request == '':
            return 'request is null'
        requestLine, body = request.split('\r\n', 1)
        headerList = requestLine.split(' ')
        method = headerList[0].upper()
        path = headerList[1]
        if method == 'GET':
            content = ''
            index = path.find('?')
            if index == -1:
                content = 'param incorrent. usage: http://192.168.2.54:9999/package?project=tile&platform=android&debug=true'
            else:
                path, queryString = path.split('?', 1)
                if path == PACKAGE_METHOD:
                    if self.m_ispacking:
                        content = 'someone is packing, please wait'
                    else:
                        self.m_ispacking = True
                        content = self.package(queryString, clientip)
                        self.m_ispacking = False
                elif path == GET_HASH_BY_PACKAGE_METHOD:
                    content = 'function develop ing..'
            return content
        elif method == 'POST':
            return 'not support POST'
        else:
            return 'not support method'

    def package(self, params, clientip):
        args = params.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        if PLATFORM_KEY in query.keys():
            message = None
            if MESSAGE_CONTENT_KEY in query.keys():
                message = query[MESSAGE_CONTENT_KEY]
            else:
                return 'incorrent param: must have message'
            project = query[PROJECT_KEY]
            if project == None:
                return 'incorrent param: must have project'
            platform = query[PLATFORM_KEY]
            version = DEFAULT_BRANCH
            if VERSION_KEY in query.keys():
                version = query[VERSION_KEY]
            if platform == 'android' or platform == 'ios' or platform == 'web':
                debug = None
                if DEBUG_KEY in query.keys():
                    debug = query[DEBUG_KEY]
                    if debug != 'true':
                        debug = None
                else:
                    debug = None
                unmerge = None
                if UN_MERGE_KEY in query.keys():
                    unmerge = query[UN_MERGE_KEY]

                assignBranch = None
                if ASSIGN_BRANCH_KEY in query.keys():
                    assignBranch = query[ASSIGN_BRANCH_KEY]
                engineVersion = '2.3.4'
                compress = None
                if project == 'bf':
                    engineVersion = '2.4.4'
                    if COMPRESS_PICTURE in query.keys():
                        compress = True
                elif project == 'tile':
                    engineVersion = '2.3.4'
                else:
                    print('not support platform ' + platform +
                          ' use default engine')
                if ENGINE_VERSION in query.keys():
                    engineVersion = query[ENGINE_VERSION]

                autopack = AutoPack.AutoPack(project, platform, debug, version,
                                             unmerge, assignBranch, message,
                                             engineVersion, compress)
                autopack.sendFixedMessageToWechat('有人在打包，打包命令来自：' + clientip)
                ret = autopack.package()
                if ret != 'OK':
                    autopack.sendFixedMessageToWechat(ret + ':' + clientip)
                return ret
            else:
                return 'incorrent param: platform only support [android,ios,web]'
        else:
            return 'incorrent param: must have platform'