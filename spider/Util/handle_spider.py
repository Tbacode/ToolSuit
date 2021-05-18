'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:17:39
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-05-18 11:27:32
'''


class HandleSpider(object):
    def __init__(self, url):
        '''
         * @name: Tommy
         * @msg: HandleExcel 初始化
         * @param {初始化url,headers}
         * @return {*}
        '''
        self.url = url
        self.headers = {
            'User-Agent':
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }

    def get_html_by_bs4(self):
        '''
         * @name: Tommy
         * @msg: 获取html的bs4对象
         * @param {*}
         * @return {*}
        '''
        # TODO：获取html对象
        pass

    def get_element_by_find(self):
        '''
         * @name: Tommy
         * @msg: 通过find方法查找dom对象
         * @param {*}
         * @return {*}
        '''
        pass

    def get_elements_by_findall(self):
        '''
         * @name: Tommy
         * @msg: 通过findall方法查找多个dom对象
         * @param {*}
         * @return {*}
        '''
        pass

    def get_element_value(self):
        '''
         * @name: Tommy
         * @msg: 返回单一dom对象文本内容
         * @param {*}
         * @return {*}
        '''
        pass

    def get_element_attr_value(self):
        '''
         * @name: Tommy
         * @msg: 返回dom对象属性值
         * @param {*}
         * @return {*}
        '''
        pass
