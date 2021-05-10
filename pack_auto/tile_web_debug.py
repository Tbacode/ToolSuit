'''
 * @Descripttion : tile打包web版
 * @Author       : Tommy
 * @Date         : 2021-04-25 17:20:07
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-04-25 17:33:39
'''
from AutoPack import AutoPack

project = "TileMatchFun"
platform = "web"
debug = "true"
version = None
unmerge = None
assignBranch = None
message = "build complete, from QA AutoPack"
engine = "2.3.4"
compress = None

if __name__ == "__main__":
    m_autopack = AutoPack(project, platform, debug, version, unmerge,
                          assignBranch, message, engine, compress)
    m_autopack.package()
