# !/usr/bin/python3
# Author : Zhoujing
# Email : 854021135@qq.com

import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

EXECUTOR_PATH = r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe'


def _save_pic():
    counter = 1

    def _save():
        nonlocal counter
        base_dir = 'd:/seleniumtest/'
        filename = '{}{:%Y%m%d%H%M%S}{:03}.png'.format(base_dir, datetime.datetime.now(), counter)
        counter += 1
        driver.save_screenshot(filename)

    return _save


save_pic = _save_pic()

driver = webdriver.PhantomJS(EXECUTOR_PATH)
driver.set_window_size(1920, 2400)
url = 'https://movie.douban.com/'

driver.get(url)
try:
    ele = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, 'inp-query')))
    ele.send_keys('朝花夕誓')
    ele.send_keys(Keys.ENTER)
    save_pic()
finally:
    driver.close()


# username = driver.find_element_by_id('userMail')
# username.send_keys('wei.xu@magedu.com')
# pwd = driver.find_element_by_id('userPassword')
# pwd.send_keys('magedu.com18')
#
# save_pic()
# # driver.find_element_by_css_selector('button.btn.btn-green.block.btn-login').click()
# pwd.send_keys(Keys.ENTER)
# time.sleep(2)
# print(driver.current_url)
# print(driver.get_cookies())
# save_pic()
# driver.close()




