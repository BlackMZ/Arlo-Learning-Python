# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Pete Yan <pete.yan@aliyun.com>
# Date  : 2021/9/8
#
# 请修改PamConnector.verify_login
# 完成设备校验代码
import base64
import getopt
import hashlib
import json
import sys
import time
import traceback

import muggle_ocr
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class PamConnector:
    def __init__(self, args):
        self.args = args
        self.user = None
        self.pwd = None
        self.type = None
        self.location = None
        self.remote = None
        self.driver = None

    def verify_login(self):
        """
        校验登录
        :rtype: 登录结果字符串
        """
        try:
            self.driver.get(self.location)
            time.sleep(3)
            self.driver.find_element_by_id("username").send_keys(self.user)
            time.sleep(1)
            self.driver.find_element_by_id("password").send_keys(self.pwd)
            time.sleep(1)
            self.driver.find_element_by_id("login").click()
            time.sleep(3)
            result = self.driver.find_element_by_id("tool").is_enabled()
            if result:
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
            self.driver = webdriver.Chrome('D:\Python\Python39\chromedriver', options=options)
            self.driver.maximize_window()
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
            sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
            img_text = sdk.predict(image_bytes=base64.b64decode(base64img))
        return img_text

    def action(self):
        if len(self.args) > 0:
            try:
                argv = self.args[1:]
                opts, args = getopt.getopt(argv, "u:p:t:l:s:")
                for opt, arg in opts:
                    if opt in ['-u']:
                        self.user = arg
                    elif opt in ['-p']:
                        self.pwd = arg
                    elif opt in ['-t']:
                        self.type = arg
                    elif opt in ['-l']:
                        self.location = arg
                    elif opt in ['-s']:
                        self.remote = arg

                self.get_driver()
                self.verify_login()
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
