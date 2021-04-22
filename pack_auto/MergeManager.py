from subprocess import check_output
import fileinput
import os
#专门用来解决合并冲突的类

BOTH_ADDED = "both added:"
BOTH_MODIFIED_CN = "双方修改："
BOTH_MODIFIED = "both modified:"
ADDED_BY_US = "added by us:"
ADDED_BY_THEM = "added by them:"
DELETED_BY_US = "deleted by us:"
DELETED_BY_THEM = "deleted by them:"

class MergeManager:
    def __init__(self, gitPath):
        self.m_gitPath = gitPath
        
    def match_str_head(self, s, template):
        s = s.strip()
        return True if s.find(template) == 0 else False

    def extract_path(self, s, template):
        s = s.strip()
        assert self.match_str_head(s, template)
        s = s[len(template):]  # remove prefix
        return s.strip()

    def read_stat(self):
        check_output("git status > _tmp.txt", shell=True)
        stat = {"both-added": [],
                "both-modified": [],
                "added-by-us": [],
                "added-by-them": [],
                "deleted-by-us": [],
                "deleted-by-them": []}
        print("==== git status ====")
        for line in fileinput.input("_tmp.txt"):
            print(line, end="")
            if self.match_str_head(line, BOTH_ADDED):
                stat["both-added"].append(
                    self.extract_path(line, BOTH_ADDED))
            elif self.match_str_head(line, BOTH_MODIFIED):
                stat["both-modified"].append(
                    self.extract_path(line, BOTH_MODIFIED))
            elif self.match_str_head(line, BOTH_MODIFIED_CN):
                stat["both-modified"].append(
                    self.extract_path(line, BOTH_MODIFIED_CN))
            elif self.match_str_head(line, ADDED_BY_US):
                stat["added-by-us"].append(
                    self.extract_path(line, ADDED_BY_US))
            elif self.match_str_head(line, ADDED_BY_THEM):
                stat["added-by-them"].append(
                    self.extract_path(line, ADDED_BY_THEM))
            elif self.match_str_head(line, DELETED_BY_US):
                stat["deleted-by-us"].append(
                    self.extract_path(line, DELETED_BY_US))
            elif self.match_str_head(line, DELETED_BY_THEM):
                stat["deleted-by-them"].append(
                    self.extract_path(line, DELETED_BY_THEM))
        print("==== end of git status ====\n")
        os.remove("_tmp.txt")
        return stat
    
    def addMaohao(slef, f):
        return "\"" + f + "\""

    def merge(self, branchName):
        os.chdir(self.m_gitPath)
        ret = os.system('git merge ' + branchName + ' -m "merge complete"')
        print(ret)
        stat = self.read_stat()
        for f in stat["both-added"]:
            check_output("git add " + self.addMaohao(f), shell=True)
        for f in stat["both-modified"]:
            check_output("git checkout --theirs " + self.addMaohao(f), shell=True)
            check_output("git add " + self.addMaohao(f), shell=True)
        for f in stat["added-by-us"]:
            check_output("git add " + self.addMaohao(f), shell=True)
        for f in stat["added-by-them"]:
            check_output("git rm " + self.addMaohao(f), shell=True)
        for f in stat["deleted-by-us"]:
            check_output("git rm " + self.addMaohao(f), shell=True)
        for f in stat["deleted-by-them"]:
            check_output("git add " + self.addMaohao(f), shell=True)
        
        ret = os.system('git commit -m "merge complete"')
        print(ret)