# coding=UTF-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from selenium import webdriver
import sys

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


def get_driver():
    options = Options()
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Remote(command_executor='http://81.68.68.227:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME, options=options)
    driver.maximize_window()
    return driver


def verify_pwd(url, username, password):
    print("the script is executing.....")

    try:
        driver = get_driver()
        driver.get(url)
        driver.find_element_by_id("username").send_keys(username)
        time.sleep(1)
        driver.find_element_by_id("password").send_keys(password)
        time.sleep(1)
        driver.find_element_by_id("loginbtn").click()
        time.sleep(1)
        driver.switch_to.frame("topframe")
        result = driver.find_element_by_id("loginuser").is_enabled()
        if result:
            print("result=" + "true")
        else:
            print("result=" + "false")
    except Exception as e:
        print(e.__class__)
        print("result=" + "false")
    finally:
        driver.quit()
    # return "success"

    print("the script has finished executing.....")

# def change_pwd(url, username, old_password, new_password):
#     print(url)
#     print(username)
#     print(old_password)
#     print(new_password)
#     return True


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
    # if_test(True)
    # variate()
    # operator()
    # str = get_random_set(6)
    # print(str)
    # verify_pwd("https://47.101.139.48", "admin", "En&4sODTkuCh")

# verify_pwd(sys.argv[1], sys.argv[2], sys.argv[3])
