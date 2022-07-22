# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Pete Yan <pete.yan@aliyun.com>
# Date  : 2021/9/8
#
# 请修改PamConnector.verify_modify_pwd
# 完成变更设备登录密码代码
import getopt
import signal
import hashlib
import sys
import json
import time
import traceback
import requests

from secmind.rpa import webdriver, Options
from secmind.rpa import DesiredCapabilities


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
            self.driver.get(self.location)
            self.driver.find_element_by_name("username").send_keys(self.user)
            time.sleep(1)
            self.driver.find_element_by_name("pwd").send_keys(self.pwd)
            time.sleep(1)
            self.driver.find_element_by_xpath("//button[contains(.,'登录')]").click()
            time.sleep(4)
            if self.driver.find_element_by_id("guide-header-personal-centre").is_enabled():
                self.driver.find_element_by_xpath("//*[@id='guideOverlap']/div/div/div[1]/div[1]").click()
                time.sleep(1)
                self.driver.find_element_by_class_name("main-verical-center").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//body/div[2]/div/div/div[1]/div").click()
                time.sleep(5)
                self.driver.find_element_by_xpath("//span[contains(.,'修改密码')]").click()
                time.sleep(1)
                cur_pwd = self.driver.find_element_by_xpath("//div[2]/div/input")
                cur_pwd.clear()
                cur_pwd.send_keys(self.pwd)
                time.sleep(1)
                new_pwd1 = self.driver.find_element_by_xpath("//div[2]/div/div[2]/div/input")
                new_pwd1.clear()
                new_pwd1.send_keys(self.new_pwd)
                time.sleep(1)
                new_pwd2 = self.driver.find_element_by_xpath("//div[3]/div/div[2]/div/input")
                new_pwd2.clear()
                new_pwd2.send_keys(self.new_pwd)
                time.sleep(1)
                self.driver.find_element_by_xpath("//div[4]/div[2]/button").click()
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
            # self.driver = webdriver.Chrome('./chromedriver', options=options)
            self.driver = webdriver.Chrome('D:\Python\Python39\chromedriver', options=options)
            self.driver.maximize_window()
        elif self.type == 'remote':
            options = Options()
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            # driver = webdriver.Chrome(options=options)
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
            # sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
            # img_text = sdk.predict(image_bytes=base64.b64decode(base64img))
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
