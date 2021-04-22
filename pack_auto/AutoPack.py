#!/usr/bin/python
# -*- coding: UTF-8- -*-

import os
import GitManager
import re
import json
import os.path as path
import time
import shutil
import requests

HTTP_ROOT_PATH = '/Library/WebServer/Documents/'

HTTP_REMOTE_URL = 'http://192.168.2.54/'

TILE_PROJECT_ROOT_PATH = '/Users/talefun/Documents/TileProject'
TILE_PROJECT_NAME = 'TileMatchFun'
# TILE_WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=22e68ae6-9e35-4464-83f6-faee481e2e27" #张齐项目测试群007
TILE_WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a7074ccb-fb2f-45c9-9f23-d67fc0200fdc" #弹球tile自动打包通知群
# TILE_WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2b6597b9-3351-443e-ac94-06922240357f" #tile马龙群008
TILE_XXTEA_KEY = "f1fe6599-0918-48"
TILE_ANDROID_PACKAGE_NAME = "com.tile.match.master.puzzle"

BF_PROJECT_ROOT_PATH = '/Users/talefun/Documents/BvBClient3/BvBClient3'
BF_PROJECT_NAME = 'BreakerFun'
BF_WECHAR_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a7074ccb-fb2f-45c9-9f23-d67fc0200fdc' #弹球tile自动打包通知群
# BF_WECHAR_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2b6597b9-3351-443e-ac94-06922240357f" #tile马龙群008

BF_ANDROID_XXTEA_KEY = '5e768ec6-e117-4b'
BF_IOS_XXTEA_KEY = '5e768ec6-e117-4b'

BF_ANDROID_PACKAGE_NAME = 'com.bricksbreaker.balls.crusher.bricks'
BF_IOS_PACKAGE_NAME = 'com.bricksbreaker.balls.crusher.bricks'
BF_IOS_TARGET_NAME = 'Breaker Fun'
BF_IOS_WORKSPACE_NAME = 'BreakerFun'

GAME_INIT_PATH = '/assets/scripts/core/GameInit.ts'

COCOS_CREATOR_PATH = '/Applications/CocosCreator/Creator/{0}/CocosCreator.app/Contents/MacOS/CocosCreator'


class AutoPack:
    def __init__(self, project, platform, debug, version, unmerge, assignBranch, message, engine, compress):
        self.m_project = project
        self.m_platform = platform
        self.m_debug = debug
        self.m_version = version
        self.m_unmerge = unmerge
        self.m_assignBranch = assignBranch
        self.m_message = message
        self.m_engine = engine
        self.m_compress = compress
    
    def package(self):
        enginePath = COCOS_CREATOR_PATH.format(self.m_engine)
        if not os.path.exists(enginePath):
            return 'not support engine version ' + self.m_engine 
        projectName = ''
        projectPath = ''
        if self.m_project == 'tile':
            projectName = TILE_PROJECT_NAME
            projectPath = TILE_PROJECT_ROOT_PATH
        elif self.m_project == 'bf':
            projectName = BF_PROJECT_NAME
            projectPath = BF_PROJECT_ROOT_PATH
        else:
            return 'not support project ' + self.m_project
        gitManager = GitManager.GitManager(self.m_project, self.m_platform, self.m_version, self.m_unmerge, self.m_assignBranch)
        ret = gitManager.switchToAutoBranch()
        if ret != None:
            return ret
        #处理gameinit的debug值
        gameInitPath = projectPath + GAME_INIT_PATH
        self.modifyGameInitFile(gameInitPath)
        #gitlog

        localGitPath = gitManager.getLocalGitPath()
        if self.m_platform == 'android':
            self.packageAndroid(projectName, projectPath, localGitPath, enginePath)
        elif self.m_platform == 'ios':
            self.packageIOS(projectName, projectPath, localGitPath, enginePath)
        elif self.m_platform == 'web':
            self.packageWeb(projectName, projectPath, localGitPath, gitManager.getCurrentBranchName(), enginePath)
        else:
            return 'none platform ' + self.m_platform
        #删除gitlog文件
        os.system('rm -rf {0}/gitLog.gitlog'.format(localGitPath))
        self.sendFixedMessageToWechat('build complete, from client message:' + self.m_message)
        return 'OK'

    #构建
    def packageAndroid(self, projectName, projectPath, gitLocalPath, enginePath):
        print('android')
        #Construct
        xxteaKey = ''
        buildPackage = ''
        if self.m_project == 'tile':
            xxteaKey = TILE_XXTEA_KEY
            buildPackage = TILE_ANDROID_PACKAGE_NAME
        elif self.m_project == 'bf':
            xxteaKey = BF_ANDROID_XXTEA_KEY
            buildPackage = BF_ANDROID_PACKAGE_NAME
        encryptJs = 'false'
        if self.m_debug == None:
            isDebug = 'true'
        
        #临时处理一下bf压图问题 打包机默认不压图 不然打包会等很久
        if self.m_compress == None and self.m_project == 'bf':
            toolsRoot = path.realpath("{0}/tools".format(projectPath))
            os.chdir(toolsRoot)
            os.system('node setETC.js ../assets/textures 0')
            os.system('node setETC.js ../assets/resources/textures 0')
            os.system('node setETC.js ../assets/resources/spines/game 0')
            os.system('node setETC.js ../assets/resources/spines/game/rescue/texture/ 0')
        
        buildParam = ' --build "platform=android;appABIs=[\'armeabi-v7a\',\'arm64-v8a\'];zipCompressJs=false;md5Cache=false;encryptJs=' + encryptJs + ';xxteaKey=' + xxteaKey + ';apiLevel=android-30;template=link;package=' + buildPackage + '"'
        print('===================cocos creator build start====================')
        ret = os.system(enginePath + ' --path ' + projectPath + buildParam)
        print(ret)
        print('===================cocos creator build complete====================')
        # Android工程所在目录
        androidRootPath = path.realpath("{0}/build/jsb-link/frameworks/runtime-src/proj.android-studio/".format(projectPath))
        print('===================adb build start====================')
        print("{0}".format(androidRootPath))
        os.chdir(androidRootPath)
        ret = os.system("./gradlew assembleRelease")
        print(ret)
        print('===================adb build complete====================')
        outputFile1 = androidRootPath + "/app/build/outputs/apk/release/output.json"
        outputFile2 = androidRootPath + "/app/release/output.json"
        outputFile = ''
        if not os.path.exists(outputFile1):
            outputFile = outputFile2
        elif not os.path.exists(outputFile2):
            outputFile = outputFile1
        else:
            mtime1 = os.stat(outputFile1).st_mtime
            mtime2 = os.stat(outputFile2).st_mtime
            if mtime1 > mtime2:
                outputFile = outputFile1
            else:
                outputFile = outputFile2

        if not os.path.exists(outputFile):
            self.sendFixedMessageToWechat('android build fail')
            return
        jsonFile = open(outputFile, 'r', encoding='utf-8')
        outputJson = json.load(jsonFile)
        versionName = outputJson[0]["apkData"]["versionName"]
        strTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        isDebug = 'debug'
        if self.m_debug == None:
            isDebug = 'release'
        apkName = projectName + "-v{0}-{1}-{2}.apk".format(versionName, isDebug, strTime)
        httpRootPath = HTTP_ROOT_PATH + self.m_project + '/' + self.m_platform
        oriPath = androidRootPath + "/app/build/outputs/apk/release/"
        if not os.path.exists(oriPath):
            oriPath = androidRootPath + "/app/release/"
        self.copyFile(oriPath, 'apk', httpRootPath, apkName)
        self.sendMessageToWechat(apkName)
        gitLogTxtName = projectName + "-v{0}-{1}-{2}.txt".format(versionName, isDebug, strTime)
        self.copyFile(gitLocalPath, 'gitlog', httpRootPath, gitLogTxtName)
        self.sendMessageToWechat(gitLogTxtName)

    def packageIOS(self, projectName, projectPath, gitLocalPath, enginePath):
        print('ios')
        buildPackage = ''
        xxteaKey = ''
        targetName = ''
        workspaceName = ''
        if self.m_project == 'tile':
            xxteaKey = TILE_XXTEA_KEY
            buildPackage = ''
            print('===================tile has no ios project====================')
            return
        elif self.m_project == 'bf':
            xxteaKey = BF_IOS_XXTEA_KEY
            buildPackage = BF_IOS_PACKAGE_NAME
            targetName = BF_IOS_TARGET_NAME
            workspaceName = '{0}.xcodeproj'.format(BF_IOS_WORKSPACE_NAME)
            
        buildParam = ' --build "platform=ios;zipCompressJs=false;md5Cache=false;encryptJs=true;xxteaKey=' + xxteaKey + ';template=link;package=' + buildPackage + '"'
        print('===================cocos creator build start====================')
        ret = os.system(enginePath + ' --path ' + projectPath + buildParam)
        print(ret)
        print('===================cocos creator build complete====================')
        iosRootPath = path.realpath("{0}/build/jsb-link/frameworks/runtime-src/proj.ios_mac/".format(projectPath))
        os.chdir(iosRootPath)
        print('===================clean product====================')
        ret = os.system('xcodebuild clean -configuration release -alltargets')
        print('===================clean product complete====================')
        print('===================start archive====================')
        tempIOSPath = path.realpath("{0}/build/jsb-link/frameworks/runtime-src/proj.ios_mac/temp-ios".format(projectPath))
        os.system('rm -rf {0}'.format(tempIOSPath))
        os.system('mkdir {0}'.format(tempIOSPath))
        strTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        isDebug = 'debug'
        if self.m_debug == None:
            isDebug = 'release'
        archivePath = "{0}/{1}-{2}-{3}.xcarchive".format(tempIOSPath, BF_IOS_WORKSPACE_NAME, strTime, isDebug)
        ret = os.system('xcodebuild archive -project {0} -scheme "{1}" -configuration release -archivePath {2}'.format(workspaceName, targetName, archivePath))
        print('===================archive complete====================')
        os.system('cp ios/Info.plist temp-ios/')
        exportPath = '/Library/WebServer/Documents/bf/ios/' + strTime
        os.system('mkdir {0}'.format(exportPath))
        exportPlistPath = '{0}/Info.plist'.format(tempIOSPath)
        os.system('xcodebuild -exportArchive -archivePath {0} -exportOptionsPlist {1} -exportPath "{2}"'.format(archivePath, exportPlistPath, exportPath))
        print('===================exportArchive complete====================')
        ipaName = strTime + '/' + BF_IOS_TARGET_NAME + '.ipa'
        self.sendMessageToWechat(ipaName)
        httpRootPath = HTTP_ROOT_PATH + self.m_project + '/' + self.m_platform
        gitLogTxtName = projectName + "-v{0}-{1}-{2}.txt".format(self.m_version, isDebug, strTime)
        self.copyFile(gitLocalPath, 'gitlog', httpRootPath, gitLogTxtName)
        self.sendMessageToWechat(gitLogTxtName)
        #打包完成过后删除临时文件夹
        os.system('rm -rf {0}'.format(tempIOSPath))

    def packageWeb(self, projectName, projectPath, gitLocalPath, branchName, enginePath):
        print('web')
        buildParam = ' --build "platform=web-desktop;previewWidth=416;previewHeight=750' + '"'
        ret = os.system(enginePath + ' --path ' + projectPath + buildParam)
        print(ret)
        print('===================cocos creator build complete====================')
        httpRootPath = HTTP_ROOT_PATH + self.m_project + '/' + self.m_platform
        strTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        webName = projectName + "-{0}-{1}".format(branchName, strTime)
        oriPath = path.realpath("{0}/build/web-desktop".format(projectPath))
        self.copyFolder(oriPath, httpRootPath + '/' + webName)
        self.sendMessageToWechat(webName)
        gitLogTxtName =  webName + '.txt'
        self.copyFile(gitLocalPath, 'gitlog', httpRootPath, gitLogTxtName)
        self.sendMessageToWechat(gitLogTxtName)

    def modifyGameInitFile(self, gameInitPath):
        temp = gameInitPath + '.temp'
        #源代码
        oriCode = ''
        #目标代码
        tarCode = ''
        if self.m_debug == None:
            oriCode = 'talefun.DEBUG = true;'
            tarCode = 'talefun.DEBUG = false;'
        else:
            oriCode = 'talefun.DEBUG = false;'
            tarCode = 'talefun.DEBUG = true;'
        with open(gameInitPath, mode='r') as fr, open(temp, mode='w') as fw:
            for line in fr:
                re_sub_list = re.sub(oriCode, tarCode, line) # 这里用re.sub进行替换后放入 re_sub_list中
                fw.writelines(re_sub_list)
            os.remove(gameInitPath)
            os.rename(temp, gameInitPath)

    def copyFile(self, copyDir, claasma, dstDir, fileName):
        allList = os.listdir(copyDir)
        for i in allList:
            if '.' in i and claasma in i:
                _, bb = i.split('.')
                if claasma in bb:
                    shutil.copyfile(copyDir + "/" + i, dstDir + "/" + fileName)
                    break

    def copyFolder(self, oriPath, tarPath):
        shutil.copytree(oriPath, tarPath)

    def sendMessageToWechat(self, name):
        remoteUrl = HTTP_REMOTE_URL + self.m_project + '/' + self.m_platform + '/' + name
        url = ''
        if self.m_project == 'tile':
            url = TILE_WECHAT_URL
        elif self.m_project == 'bf':
            url = BF_WECHAR_URL
        headers = {"Content-Type": "text/plain"}
        data = {
            "msgtype": "text",
            "text": {
                "content": remoteUrl
            }
        }
        res = requests.post(url, json=data, headers=headers)
        print(res.text)

    def sendFixedMessageToWechat(self, message):
        url = ''
        if self.m_project == 'tile':
            url = TILE_WECHAT_URL
        elif self.m_project == 'bf':
            url = BF_WECHAR_URL

        headers = {"Content-Type": "text/plain"}
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        res = requests.post(url, json=data, headers=headers)
        print(res.text)