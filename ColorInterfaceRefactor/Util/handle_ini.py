'''
 * @Descripttion : ini配置文件操作
 * @Author       : Tommy
 * @Date         : 2021-06-17 16:51:35
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-17 17:33:20
'''
import configparser


class HandleIni(object):
    def __init__(self, filename):
        self.filename = filename

    def load_ini(self):
        '''
         * @name: Tommy
         * @msg: 打开ini文件对象
         * @param {*}
         * @return {文件对象}
        '''
        ini_path = self.filename
        cf = configparser.ConfigParser()
        cf.read(ini_path, encoding='utf-8-sig')
        return cf

    def get_ini_value(self, key, section=None):
        '''
         * @name: Tommy
         * @msg: 获取ini文件值
         * @param {key:ini文件内key,section:默认server}
         * @return {返回对应key的value}
        '''
        if section is None:
            section = 'server'
        cf = self.load_ini()
        data = cf.get(section, key)
        return data


handle_ini = HandleIni(
    r"C:\Users\xt875\Documents\ToolSuit\ColorInterfaceRefactor\Config\config.ini"
)

if __name__ == "__main__":
    hi = HandleIni(
        r"C:\Users\xt875\Documents\ToolSuit\ColorInterfaceRefactor\Config\config.ini"
    )
    print(hi.get_ini_value("Result"))
