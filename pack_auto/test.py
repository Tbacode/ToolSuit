from git import Repo
import fileinput
import os
from subprocess import check_output
import re
import os.path as path

BF_PROJECT_ROOT_PATH = '/Users/talefun/Documents/BvBClient3/BvBClient3'
androidRootPath = path.realpath("{0}/build/jsb-link/frameworks/runtime-src/proj.android-studio/".format(BF_PROJECT_ROOT_PATH))
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
print('===================adb build start====================')
print("{0}".format(outputFile))
