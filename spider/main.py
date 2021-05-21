'''
 * @Descripttion : 爬虫主逻辑
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:16:44
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-05-21 16:39:06
'''
# from Util.handle_excel import HandleExcel
from Util.handle_spider import HandleSpider


def url_in_list(url, handleobj, xpath, hrefxpath):
    '''
     * @name: Tommy
     * @msg: 根据xpath获取页面内所有子链接，返回一个链接list
     * @param {url:页面地址;handleobj:handleSpider实例化对象;xpath:目标元素xpath;hrefxpath:链接xpath}
     * @return {url子链接集合}
    '''
    html = handleobj.get_html(url)
    html_list = handleobj.get_elements_by_xpath(html, xpath)
    list_return = []
    for index, item in enumerate(html_list):
        href = handleobj.get_element_value_by_xpath(item, hrefxpath.format(index + 1))
        list_return.append(href[0])
    return list_return


def url_combination(homeUrl, linkUrl_list):
    '''
     * @name: Tommy
     * @msg: 组装主页面链接和子链接形成完整的链接集合返回
     * @param {homeUrl:主页链接; linkUrl_list:子链接集合}
     * @return {url链接集合}
    '''
    url_list_return = []
    for link_item in linkUrl_list:
        url_list_return.append(homeUrl + link_item)
    return url_list_return


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