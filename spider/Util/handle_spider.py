'''
 * @Descripttion : 封装对于爬虫行为的操作
 * @Author       : Tommy
 * @Date         : 2021-05-12 17:17:39
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-08 09:13:46
'''
from fake_useragent import UserAgent
# from threading import Thread, Lock
# from queue import Queue
from lxml import etree
import requests
from bs4 import BeautifulSoup
import time
import random
from loguru import logger


class HandleSpider(object):
    def __init__(self):
        '''
         * @name: Tommy
         * @msg: HandleExcel 初始化
         * @param {初始化url,headers}
         * @return {*}
        '''
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41'
        }
        self.cookies = {
            'Cookie':
            '_ga=GA1.2.1743206621.1622956802; _pbjs_userid_consent_data=3524755945110770; _pubcid=e3c90a11-78ae-411d-a40a-a60644c921ce; __gads=ID=d4e65c5a0dffd87a-2225cf8c3cc900be:T=1622956803:S=ALNI_MaezBM-UjHzsK8HUOykXsNCkXncEQ; _gid=GA1.2.763363196.1623076186; _lr_env_src_ats=false; pbjs-unifiedid={"TDID":"9b65f6c2-6de8-47e7-a2d6-b33de1cf8796","TDID_LOOKUP":"FALSE","TDID_CREATED_AT":"2021-06-07T14:29:52"}; pbjs-id5id={"created_at":"2021-06-07T14:28:26.346618Z","id5_consent":true,"original_uid":"ID5-ZHMOqCbhpVrXg6xwXpNWIU2fmBQOMp-e8LZtPb6rkw!ID5*Gmj--OgGUhIa9zAbMH4g4WFtLC9ULoEo3tAF2n2eGCQAAKAk--rpIx1Vf1ml2orC","universal_uid":"ID5-ZHMOm-URN5ws-6NwVlrGtMXd4nU31bbqX2_wfQltiw!ID5*nIXoOV0otEFa4V7Vtpv_sHIIeJSz-nDALJLKhrvEyP0AAC0mZ-N6LN2muoKMbCq9","signature":"ID5_AZuhGWtemEksvOinvxyZ4pIw6iLB3knHUTMupRx5Y_gaafQgNFsPc2kfvH2mixI1bmXoCQJI8PMNNmcYZ4cPZLA","link_type":1,"cascade_needed":true,"privacy":{"jurisdiction":"other","id5_consent":true}}; pbjs-id5id_last=Mon, 07 Jun 2021 14:29:53 GMT; _gat=1; cto_bidid=Z17-al9ZQWM0a3duSk5temlYR016V2QwUVZXTHZlaERvWmdtZnlDV1pSaDlxYmtxZ1BOemolMkZuZ1NSYTk5ZFlKTEUxekMzUWNORXBlQTRMcnpacnFVQ05zYWVnJTNEJTNE; cto_bundle=R7DZHl9MZyUyRjRiJTJGU3FhZ3JWeDVIN0tQUyUyQiUyRnFNMW55ejFtVFNGRGFoZ29GODhVMk5zN3dHOWZ4MEZZVjVPUzVmOFNvY2g2UnN3ejhKcWdUS2x1Z3hPMlZ1TjByOFUzJTJGeXR4TVdtSGIyWUNsaXRFZG5kTTVuT09zOU0yM3duNHJqaFRpRDQ; _lr_retry_request=true'
        }
        logger.debug("User-Agent：" + str(self.headers))
        # 创建url队列、线程锁
        # self.url_queue = Queue()
        # self.lock = Lock()

    def get_html(self, url):
        '''
         * @name: Tommy
         * @msg: 获取html页面内容
         * @param {*}
         * @return {*}
        '''
        i = 0
        logger.debug("get_html请求开始:" + url)
        time.sleep(random.randint(1, 10))
        logger.debug("延迟请求结束")
        while i < 3:
            try:
                html = requests.get(url=url,
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    timeout=20).text
            except Exception:
                logger.error("重试--超时链接：" + url)
                i += 1
                html = None
            else:
                break
        return html

    def get_elements_by_xpath(self, html, xpath):
        '''
         * @name: Tommy
         * @msg: 通过xpath获取元素对象集合
         * @param {html文本对象，xpath变量}
         * @return {element集合}
        '''
        tree = etree.HTML(html)
        element_list = tree.xpath(xpath)
        return element_list

    def get_element_value_by_xpath(self, element, xpath):
        '''
         * @name: Tommy
         * @msg: 通过xpath获取元素对象的属性值
         * @param {元素item，xpath变量}
         * @return {返回xpath固定值}
        '''
        element_value = element.xpath(xpath)
        return element_value

    def get_element_by_bs4_cssselector(self, url, css_selector):
        # 设置请求间隔
        logger.debug("get_element_by_bs4_cssselector请求开始")
        time.sleep(random.randint(1, 10) * 2)
        logger.debug("延迟请求结束")
        html = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html, "lxml")
        txt = soup.prettify()
        print(type(txt))
        with open("html.txt", 'w', encoding='utf-8') as f:
            f.write(txt)
        # info = soup.select(css_selector)
        # print(info)