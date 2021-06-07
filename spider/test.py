'''
 * @Descripttion : 爬虫主逻辑
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:16:44
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-07 17:06:45
'''
from Util.handle_excel import HandleExcel
from Util.handle_spider import HandleSpider
import operator
from functools import reduce
from loguru import logger


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
        href = handleobj.get_element_value_by_xpath(
            item, hrefxpath.format(index + 1))
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


def get_devices_info(html, handleobject, xpath):
    '''
     * @name: Tommy
     * @msg: 根据xpath获取设备详情信息返回str
     * @param {html:页面对象, handleobject:spider实例对象, xpath:xpath路径}
     * @return {*}
    '''
    info_elements = handleobject.get_elements_by_xpath(html, xpath)
    try:
        # logger.debug("info_elements:" + info_elements)
        info = handleobject.get_element_value_by_xpath(info_elements[0],
                                                       xpath + '/text()')
        info = info[0].strip()
    except IndexError:
        return None
    return info


def reduce_list(double_dimensional_url_list):
    '''
     * @name: Tommy
     * @msg: 将二维的urllist转化成一维
     * @param {linkUrl_list:二维链接集合}
     * @return {一维url集合}
    '''
    return reduce(operator.add, double_dimensional_url_list)


def main(url):
    m_handleSpider = HandleSpider()
    """
    遍历每一个品牌的完整链接
    进入品牌列表页面
    获取所有机型详情子url
    并组装成完整url集合
    """
    devices_url = url
    url = "https://www.gsmarena.com/"
    # 提前声明一个空的二维list存放每个分页的设备子链接
    double_dimensional_url_list = []
    # 获取当前品牌的所有分页链接
    devices_page_child_url_list = url_in_list(
        devices_url, m_handleSpider, '//*[@id="body"]/div/div[3]/div[1]/a',
        '//*[@id="body"]/div/div[3]/div[1]/a[{}]/@href')
    devices_page_full_url_list = url_combination(url,
                                                 devices_page_child_url_list)
    print(devices_page_full_url_list)
    # 获取第一分页页面所有设备链接
    devices_info_child_url_list = url_in_list(
        devices_url, m_handleSpider, '//*[@id="review-body"]/div[1]/ul/li',
        '//*[@id="review-body"]/div[1]/ul/li[{}]/a/@href')
    devices_info_full_url_list = url_combination(url,
                                                 devices_info_child_url_list)
    double_dimensional_url_list.append(devices_info_full_url_list)
    # 此时进入分页循环遍历
    for index, page_item_url in enumerate(devices_page_full_url_list):
        devices_info_child_url_list = url_in_list(
            page_item_url, m_handleSpider,
            '//*[@id="review-body"]/div[1]/ul/li',
            '//*[@id="review-body"]/div[1]/ul/li[{}]/a/@href')
        devices_info_full_url_list = url_combination(
            url, devices_info_child_url_list)
        double_dimensional_url_list.append(devices_info_full_url_list)
        print(double_dimensional_url_list[index + 1])
    # 最后将所有设备分页遍历后，获得的二维设备详情url转换为一维
    devices_detail_full_url_list = reduce_list(double_dimensional_url_list)
    print(devices_detail_full_url_list)
    m_handleExcel = HandleExcel(
        r"C:\Users\xt875\Documents\ToolSuit\spider\DevicesInfo.xlsx")
    # 此时正式进入信息爬取页面的循环遍历
    for detail_index, detail_item in enumerate(devices_detail_full_url_list):
        list_info = []
        logger.debug("detail_item:" + detail_item)
        html = m_handleSpider.get_html(detail_item)
        if html is None:
            logger.error("html is None")
            m_handleExcel.excel_celldata_add(detail_index + 1,
                                             1, 'realme',
                                             detail_item)
            continue
        devices_name = get_devices_info(
            html, m_handleSpider, '//*[@id="body"]/div/div[1]/div/div[1]/h1')
        resolution = get_devices_info(
            html, m_handleSpider, '//*[@id="specs-list"]/table[4]/tr[3]/td[2]')
        os = get_devices_info(html, m_handleSpider,
                              '//*[@id="specs-list"]/table[5]/tr[1]/td[2]')
        CPU = get_devices_info(html, m_handleSpider,
                               '//*[@id="specs-list"]/table[5]/tr[3]/td[2]')
        memory = get_devices_info(
            html, m_handleSpider, '//*[@id="specs-list"]/table[6]/tr[2]/td[2]')
        list_info.append(devices_name)
        list_info.append(resolution)
        list_info.append(os)
        list_info.append(CPU)
        list_info.append(memory)
        for index, item in enumerate(list_info):
            if item is not None:
                m_handleExcel.excel_celldata_add(detail_index + 1, index + 1,
                                                 'realme', item)
            else:
                logger.debug("存在为None选项")
                m_handleExcel.excel_celldata_add(detail_index + 1, index + 1,
                                                 'realme', detail_item)


if __name__ == "__main__":
    url = "https://www.gsmarena.com/realme-phones-118.php"
    main(url)
