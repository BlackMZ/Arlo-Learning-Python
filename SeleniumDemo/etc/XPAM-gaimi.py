# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Pete Yan <pete.yan@aliyun.com>
# Date  : 2021/9/8
#
# 请修改PamConnector.verify_modify_pwd
# 完成变更设备登录密码代码
import base64
import getopt
import hashlib
import json
import sys
import time
import traceback

#import muggle_ocr
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
        self.via_user = None
        self.via_pwd = None
        self.location = None
        self.remote = None
        self.driver = None

    def verify_modify_pwd(self):
        """
        修改设备登录密码
        :rtype: 密码修改结果
        """
        try:
            print(self.via_pwd)
            print(self.via_user)
            print(self.pwd)
            self.driver.get(self.location)
            VerificationCode=self.driver.find_element(By.XPATH,"//*[@id='validImg']")
            if  VerificationCode:
                self.driver.get(self.location)
                self.driver.find_element(By.ID, "username").send_keys(self.user)
                time.sleep(1)
                self.driver.find_element(By.ID, "password").send_keys(self.pwd)
                time.sleep(1)
            else:
                self.driver.find_element(By.ID, "username").send_keys(self.user)
                time.sleep(1)
                self.driver.find_element(By.ID, "password").send_keys(self.pwd)
                time.sleep(1)
                img_element = self.driver.find_element(By.ID, "validImg")
                if img_element is not None:
                    img_txt = self.get_img_txt(img_element.screenshot_as_base64)
                    # 填充验证码输入框
                    self.driver.find_element(By.ID, "validate").send_keys(img_txt)
                    time.sleep(1)

            self.driver.find_element(By.ID, "submit").click()
            time.sleep(1)
            result = self.driver.find_element(By.XPATH,"//div[@class='agent-info pointer']").is_enabled()
            time.sleep(3)
            if result:
                time.sleep(1)
                self.driver.find_element(By.XPATH,"//div[@class='agent-info pointer']").click()
                time.sleep(1)
                self.driver.find_element(By.ID,"btnChangePwd").click()
                time.sleep(1)
                self.driver.switch_to.frame(36)
                time.sleep(1)
                cur_pwd = self.driver.find_element(By.NAME, "password").send_keys(self.pwd)
                time.sleep(1)
                new_pwd1 = self.driver.find_element(By.NAME, "newPassword").send_keys(self.new_pwd)
                time.sleep(1)
                new_pwd2 = self.driver.find_element(By.NAME, "reNewPassword").send_keys(self.new_pwd)
                time.sleep(1)
                self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
                time.sleep(1)
                print("result=" + "true")
            else:
                print("result=" + "false")
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
        elif self.type == 'remote':
            options = Options()
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
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
                    elif opt in ['-v']:
                        self.via_user = arg
                    elif opt in ['-i']:
                        self.via_pwd = arg
                self.get_driver()
                self.verify_modify_pwd()
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
