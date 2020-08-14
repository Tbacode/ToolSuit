# -*- coding: utf-8 -*-
# @Author: Tommy
# @Date:   2019-05-13 17:22:14
# @Last Modified by:   Tommy
# @Last Modified time: 2019-05-15 10:45:08
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')

# driver.find_element_by_id('kw').send_keys('selenium2')
# driver.find_element_by_id('su').click()

driver = webdriver.Chrome()
driver.get('http://www.baidu.com')

# driver.find_element_by_id('idInput').clear()
# driver.find_element_by_id('idInput').send_keys('username')
# driver.find_element_by_id('pwdInput').clear()
# driver.find_element_by_id('pwdInput').send_keys('password')
# driver.find_element_by_id('loginBtn').click()

# element = WebDriverWait(driver, 5, 0.5).until(
#     EC.presence_of_element_located((By.ID, 'kw')))
# element.send_keys('selenium')
# cookie = driver.get_cookies()
# print(cookie)

driver.set_window_size(600, 600)
driver.find_element_by_id('kw').send_keys('selenium')
# driver.find_element_by_id('su').click()
sleep(2)

js = 'window.scrollTo(100, 450);'
driver.execute_script(js)
sleep(3)
