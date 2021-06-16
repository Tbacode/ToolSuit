'''
 * @Description  : 
 * @Autor        : Tommy
 * @Date         : 2021-06-14 18:03:05
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-06-16 11:47:54
'''
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('http://www.baidu.com')
driver.find_element_by_id('kw')