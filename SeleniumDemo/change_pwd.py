# coding=UTF-8
import sys
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def change_pwd(url, username, old_password, new_password):
    print(url)
    print(username)
    print(old_password)
    print(new_password)
    # driver = webdriver.remote('http://81.68.68.227:4444/wd/hub')
    options = Options()
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get(url)

    # elem = driver.find_element_by_xpath("//div[2]/div[1]/div/div[1]/ul/li[2]")
    # elem.click()
    account = driver.find_element_by_id("username")
    account.send_keys(username)
    time.sleep(3)
    passw = driver.find_element_by_id("password")
    passw.send_keys(old_password)
    time.sleep(3)
    driver.find_element_by_id("loginbtn").click()
    time.sleep(1)
    driver.quit()
    print("result=" + "true")
    return "success"


if __name__ == '__main__':
    change_pwd("https://47.101.139.48", "test", "pass", "12345")
# change_pwd(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
