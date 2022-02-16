'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-01-26 18:17:10
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-01-27 14:01:01
'''
from Util.handle_excel import HandleExcel
from Util.handle_spider import HandleSpider


if __name__ == "__main__":
    excel = HandleExcel(
        r"C:\Users\talefun\Documents\ToolSuit\xiaohongshu\xiaohongshu.xlsx")
    spider = HandleSpider()
    rows = excel.get_rows()
    for i in range(rows):
        url = excel.get_cell_value(i + 1, 1)
        html_text = spider.get_html(url)
        # title = spider.get_elements_by_xpath(
        #     html_text, '//*[@id="app"]/div/div[2]/div[1]/div[2]/h1')
        # print("*" * 10)
        # print(title[0].text.strip())
        # print("#" * 10)
        # home = spider.get_elements_by_xpath(html_text, '/html/head/meta[24]/@content[0]')
        # print(home)
        dict_info = spider.get_elements_by_xpath(html_text, '/html/head/script[9]/text()')
        print(dict_info)
