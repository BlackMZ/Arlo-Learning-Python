# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Pete Yan <pete.yan@aliyun.com>
# Date  : 2021/9/8
#
# 请修改PamConnector.discover_account
# 完成发现账号的代码
import base64
import getopt
import hashlib
import json
import sys
import time
import traceback

# import muggle_ocr
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class PamConnector:
    def __init__(self, args):
        self.args = args
        self.user = None
        self.pwd = None
        self.type = None
        self.new_pwd = None
        self.location = None
        self.remote = None
        self.driver = None

    def discover_account(self):
        """
        账号发现
        :return:
        """
        try:
            self.driver.get(self.location)
            if self.driver.find_element_by_id("validcode").is_displayed():
                verificationCode = self.driver.find_element(By.XPATH, "//*[@id='validImg']")
                self.driver.find_element(By.LINK_TEXT, "管理控制台").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "txtUsername").send_keys(self.user)
                time.sleep(1)
                self.driver.find_element(By.ID, "txtPassword").send_keys(self.pwd)
                time.sleep(1)
                img_txt = self.get_img_txt(verificationCode.screenshot_as_base64)
                # 填充验证码输入框
                self.driver.find_element(By.ID, "validate").send_keys(img_txt)
                time.sleep(1)
            else:
                self.driver.find_element(By.LINK_TEXT, "管理控制台").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "txtUsername").send_keys(self.user)
                time.sleep(1)
                self.driver.find_element(By.ID, "txtPassword").send_keys(self.pwd)
                time.sleep(1)
            self.driver.find_element(By.ID, "devLogin").click()
            time.sleep(2)
            if self.driver.find_element(By.CSS_SELECTOR, ".nav-user-photo").is_enabled():
                self.driver.find_element(By.LINK_TEXT, "坐席管理").click()
                time.sleep(1)
                self.driver.find_element(By.LINK_TEXT, "客服列表").click()
                time.sleep(1)
                self.driver.switch_to.frame('iframePage')
                time.sleep(1)
                total_pages = self.driver.find_element(By.XPATH, "//*[@id='data']/div[3]/div/div[1]/div/span[2]")
                #页面计数就像上面账户计数一样
                total_user = 0
                for i in range(int(total_pages.text)):
                    discover_username_elements = self.driver.find_elements(By.XPATH, "//*[@id='table']/tbody/tr/td[2]")
                    for i in range(0, len(discover_username_elements)):
                        print("username=" + discover_username_elements[i].text)
                        total_user += 1
                    self.driver.find_element(By.XPATH, "//*[@id='data']/div[3]/div/div[2]/div[4]").click()
                print(total_user)

        except Exception:
            print(traceback.print_exc())
            print("result=" + "false")
        finally:
            if self.driver is not None:
                self.driver.quit()

    def get_driver(self):
        if self.type == 'local':
            options = Options()
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\96.0.4664.45\chromedriver.exe',
                                           options=options)
            self.driver.maximize_window()
        elif self.type == 'remote':
            options = Options()
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            driver = webdriver.Remote(command_executor=self.remote,
                                      desired_capabilities=DesiredCapabilities.CHROME, options=options)
            driver.maximize_window()
            self.driver = driver

    def get_img_txt(self, base64img):
        img_text = ''
        status = requests.get(url='https://pam-openapi.secmind.cn/api/net/status')
        if json.loads(status.text).get('success') is True:
            sign_plain = "WwanDdou" + "" + base64img + "" + "vgdffs"
            hl = hashlib.md5()
            hl.update(sign_plain.encode(encoding='utf-8'))
            sign_cipher = hl.hexdigest()
            params = {
                'sign': sign_cipher,
                'typeId': '',
                'image': base64img,
                'assetType': ''
            }
            resp = requests.post(json=params, url='https://pam-openapi.secmind.cn/api/captcha/identity')
            resp_data = json.loads(resp.text)
            if resp_data.get('success') is True:
                img_text = resp_data.get('code')
        else:
            img_text = ''
        return img_text

    def action(self):
        if len(self.args) > 0:
            try:
                argv = self.args[1:]
                opts, args = getopt.getopt(argv, "u:p:t:n:l:s:v:i:")
                for opt, arg in opts:
                    if opt in ['-u']:
                        self.user = arg
                    elif opt in ['-p']:
                        self.pwd = arg
                    elif opt in ['-t']:
                        self.type = arg
                    elif opt in ['-n']:
                        self.new_pwd = arg
                    elif opt in ['-l']:
                        self.location = arg
                    elif opt in ['-s']:
                        self.remote = arg
                self.get_driver()
                self.discover_account()
            except Exception as e:
                print(traceback.print_exc())


def main():
    if len(sys.argv) < 2:
        print('Abort: Please input command arguments!')
        exit(0)
    connector = PamConnector(sys.argv)
    connector.action()


def quit_main(signum, frame):
    print('Quit successful by user action.')
    sys.exit()


if __name__ == '__main__':
    print('-= WELCOME TO SECMIND-PAM =-')
    try:
        main()
    except Exception:
        print(traceback.print_exc())
