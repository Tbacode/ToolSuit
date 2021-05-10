from git import Repo
import os
import re
import MergeManager

#tile仓库本地地址
TILE_GIT_PATH = '/Users/talefun/Documents/TileProject'
#breaker fun仓库本地地址
BF_GIT_PATH = '/Users/talefun/Documents/BvBClient3'

#自动打包仓库头
AUTO_PACKAGE_BRANCH_HEAD = 'auto/'
#没有指定版本的时候 默认打包仓库
DEFAULT_BRANCH = 'default' 
#开发分支名称
DEVELOP_BRANCH = 'develop'

class GitManager:
    def __init__(self, project, platform, version, unmerge, assignBranch):
        self.m_project = project
        self.m_platform = platform
        self.m_version = version
        self.m_unmerge = unmerge
        self.m_assignBranch = assignBranch
        self.m_gitLocalPath = ''
    
    #切换到打包分支
    def switchToAutoBranch(self):
        self.m_gitLocalPath = ''
        if self.m_project == 'tile':
            self.m_gitLocalPath = TILE_GIT_PATH
        elif self.m_project == 'bf':
            self.m_gitLocalPath = BF_GIT_PATH
        repo = Repo(self.m_gitLocalPath)
        brachPath = AUTO_PACKAGE_BRANCH_HEAD
        if self.m_platform == 'android':
            brachPath = brachPath + 'android/'
        elif self.m_platform == 'ios':
            brachPath = brachPath + 'ios/'
        elif self.m_platform == 'web':
            brachPath = brachPath + 'web/'
        else:
            return 'error platform'
        
        os.chdir(self.m_gitLocalPath)
        os.system('git fetch')

        #如果有指定分支 就先切到指定分支拉取最新到代码，准备合并到新的打包分支
        if self.m_assignBranch != None:
            if repo.active_branch.name != self.m_assignBranch:
                try:
                    repo.head.reset(index=True, working_tree=True)
                    repo.git.checkout(self.m_assignBranch)
                except:
                    return 'assgin branch ' + self.m_assignBranch + ' not exist'
            repo.git.checkout('.')
            repo.git.pull()
        else:
            #切到dev拉取最新的代码
            print(repo.active_branch.name)
            #拉取develop分支上最新的代码
            if repo.active_branch.name != DEVELOP_BRANCH:
                repo.head.reset(index=True, working_tree=True)
                repo.git.checkout(DEVELOP_BRANCH)
            # 拉取最新代码
            repo.git.checkout('.')
            repo.git.pull()
        
        #如果是web平台 直接打包
        if self.m_platform == 'web':
            return None
        maxVersionBranch = ''
        if self.m_version != DEFAULT_BRANCH:
            brachPath = brachPath + self.m_platform + '_v' + self.m_version
        else:
            #如果没有选择版本 就用当前最大的打包版本号
            branches = repo.refs
            branchHead = ''
            if self.m_project == 'tile':
                branchHead = 'release/' + self.m_platform + '/' + self.m_platform
            elif self.m_project == 'bf':
                branchHead = self.m_platform + '/' + self.m_platform
            maxVersion = 100
            for b in branches:
                if 'refs/tags' in b.path or 'refs/heads' in b.path or 'refs/stash' in b.path:
                    continue
                if branchHead in b.remote_head and 'auto' not in b.remote_head:
                    version = int(re.sub("\D", "", b.remote_head))
                    if maxVersion < version:
                        maxVersion = version
                        maxVersionBranch = b.remote_head
                    else:
                        pass
                else:
                    pass
            if maxVersionBranch.find('release') != -1:
                brachPath = maxVersionBranch.replace('release', 'auto')
            else:
                brachPath = 'auto/' + maxVersionBranch
            
        #删除已经存在的本地打包分支 切最新的分支打包 防止各种代码合并冲突
        self.deleteBranchIfExist(repo, brachPath, self.m_gitLocalPath)

        #如果不是默认版本
        if self.m_version != DEFAULT_BRANCH:
            try:
                #如果指定了版本 比如是Android 1.0.0版本，就从release/android/android_v1.0.0切出 auto/android/android_v1.0.0分支
                oriBranch = ''
                if self.m_project == 'tile':
                    oriBranch = 'release/' + self.m_platform + '/' + self.m_platform + '_v' + self.m_version
                elif self.m_project == 'bf':
                    oriBranch = self.m_platform + '/' + self.m_platform + '_v' + self.m_version
                repo.git.checkout(oriBranch)
                tarBranch = 'auto/' + self.m_platform + '/' + self.m_platform + '_v' + self.m_version
                #新建分支 并且切到最新分支
                repo.create_head(tarBranch)
                repo.git.checkout(tarBranch)
            except:
                return 'The packaging branch where the specified version is located does not exist'
            
        else:
            #如果没有指定版本，就从当前最大的打包分支切出来打包
            oriBranch = maxVersionBranch
            tarBranch = brachPath
            print(tarBranch + ' branch not exist, will create immed from ' + oriBranch)
            try:
                repo.git.checkout(oriBranch)
                repo.create_head(tarBranch)
                repo.git.checkout(tarBranch)
            except:
                return 'there is no ' + oriBranch + ' exist can checkout'
        #打包日志
        os.chdir(self.m_gitLocalPath)

        #如果没有指定不合并 就合并develop的最新代码
        if self.m_unmerge == None:
            if self.m_assignBranch != None:
                mergeBranch = repo.branches[self.m_assignBranch]
            else:
                mergeBranch = repo.branches[DEVELOP_BRANCH]
            #合并代码
            try:
                # currentBranch = repo.branches[brachPath]
                # base = repo.merge_base(repo.active_branch, mergeBranch)
                # repo.index.merge_tree(mergeBranch, base=base)
                # repo.index.commit('[auto package tool] Merge dev into new_branch', parent_commits=(currentBranch.commit, mergeBranch.commit))
                # repo.head.reset(index=True, working_tree=True)
                # os.system('git merge {0} --commit -m \" Merge {1} into new_branch\"'.format(mergeBranch.name, mergeBranch.name))
                mergeManager = MergeManager.MergeManager(self.m_gitLocalPath)
                mergeManager.merge(mergeBranch.name)
                # os.system('git commit -m \"Merge dev into new_branch\"')
                # currentBranch = repo.branches[brachPath]
                # repo.index.commit('[auto package tool] Merge dev into new_branch', parent_commits=(currentBranch.commit, mergeBranch.commit))
                # repo.head.reset(index=True, working_tree=True)
            except:
                return 'can not merge develop code, please contact coder'

        os.system("git log '{0}' -50 --date=format:'%Y-%m-%d %H:%M:%S' --name-only --pretty=format:'[%cd](%an):%s'  > ./gitLog.gitlog".format(repo.active_branch.name))
        return None
        #分支操作完毕 开始打包

    def deleteBranchIfExist(self, repo, branchName, gitLocalPath):
        for b in repo.branches:
            if branchName == b.name:
                os.chdir(gitLocalPath)
                os.system('git branch -D ' + branchName)
                return

    def getCurrentBranchName(self):
        repo = Repo(self.m_gitLocalPath)
        return repo.active_branch.name

    def getLocalGitPath(self):
        return self.m_gitLocalPath
