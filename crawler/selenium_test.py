from selenium import webdriver
import datetime
import random
import time


EXECUTOR_PATH = r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe'
MAXRETRIES = 5

driver = webdriver.PhantomJS(EXECUTOR_PATH)
driver.set_window_size(1280, 2400)
url = 'https://www.oschina.net/search?scope=project&q=python'
driver.get(url)


def save_pic():
    base_dir = 'd:/seleniumtest/'
    filename = '{}{:%Y%m%d%H%M%S}{:03}.png'.format(base_dir, datetime.datetime.now(), random.randint(1,100))
    driver.save_screenshot(filename)


save_pic()

for i in range(5):
    time.sleep(1)
    try:

        # ActionChains(driver).click(ele1).perform()
        time.sleep(0.2)
        ele = driver.find_element_by_css_selector('div.ui.search.selection.dropdown.small.project-catalog')
        ele1 = ele.find_element_by_css_selector('i.dropdown.icon').click()
        target = ele.find_element_by_xpath("//a[text()='Web应用开发']")
        target.click()
        print('ok')
        save_pic()
        break
    except Exception as e:
        print(e)

driver.close()














