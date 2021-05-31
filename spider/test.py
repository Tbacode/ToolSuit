'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2021-05-31 18:06:53
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-05-31 18:32:58
'''
from Util.handle_spider import HandleSpider

m_handleSpider = HandleSpider()
m_handleSpider.get_element_by_bs4_cssselector("https://www.baidu.com",
                                              '#s-top-left > a:nth-child(1)')
