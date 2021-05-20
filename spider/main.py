'''
 * @Descripttion : 爬虫主逻辑
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:16:44
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-05-20 15:49:57
'''
# from Util.handle_excel import HandleExcel
from Util.handle_spider import HandleSpider


def main(url):
    devices_url_list = []
    m_handleSpider = HandleSpider()
    home_html = m_handleSpider.get_html(url)
    ul_list = m_handleSpider.get_elements_by_xpath(
        home_html, '//*[@id="body"]/aside/div[1]/ul/li')
    for index, item in enumerate(ul_list):
        href = m_handleSpider.get_element_value_by_xpath(
            item,
            '//*[@id="body"]/aside/div[1]/ul/li[{}]/a/@href'.format(index + 1))
        devices_url_list.append(url + href[0])
    print(devices_url_list)

    # 循环每个设备的索引界面
    for devices_url in devices_url_list:

        devices_html = m_handleSpider.get_html(devices_url)
        # 获取当前页面所有设备链接
        devices_li = m_handleSpider.get_elements_by_xpath(
            devices_html, '//*[@id="review-body"]/div[1]/ul/li')
        devices_info_url_list = []
        for index, devices_url_item in enumerate(devices_li):
            devices_a_href = m_handleSpider.get_element_value_by_xpath(
                devices_url_item,
                '//*[@id="review-body"]/div[1]/ul/li[{}]/a/@href'.format(
                    index + 1))
            devices_info_url_list.append(url + devices_a_href[0])
        print(devices_info_url_list)


if __name__ == "__main__":
    url = "https://www.gsmarena.com/"
    main(url)