import getopt
import sys
import time
import traceback

from secmind.rpa import webdriver, Options
from secmind.rpa import DesiredCapabilities


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
            self.driver.find_element_by_id("locale").click()
            time.sleep(1)
            self.driver.find_element_by_xpath("//*[@id='locale']/option[1]").click()
            time.sleep(1)
            self.driver.find_element_by_id("username").send_keys(self.user)
            time.sleep(1)
            self.driver.find_element_by_id("password").send_keys(self.pwd)
            time.sleep(1)
            self.driver.find_element_by_id("login-submit").click()
            time.sleep(3)
            if self.driver.find_element_by_id("top-user").is_enabled():
                self.driver.find_element_by_link_text("配置").click()
                time.sleep(3)
                # self.driver.find_element_by_link_text("用户管理").click()
                time.sleep(3)
                table = self.driver.find_element_by_xpath("//*[@id='tabContent']/iframe")
                self.driver.switch_to_frame(table)
                total = self.driver.find_element_by_xpath("//*[@id='paging']/div[4]/span[3]").text
                num = total.replace(" ", "")
                total_num = int(num[1:(len(num) - 1)])
                total_page = int((total_num / 30)) + 1
                for i in range(0, int(total_page)):
                    discover_username_elements = self.driver.find_elements_by_xpath(
                        "//*[@id='resultTable']/tbody/tr/td[2]")
                    for i in range(1, len(discover_username_elements)):
                        print("username=" + discover_username_elements[i].text)
                    self.driver.find_element_by_xpath("//*[@id='paging']/div[3]/a").click()
                    time.sleep(2)
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
            # driver = webdriver.Chrome(options=options)
            driver = webdriver.Remote(command_executor=self.remote,
                                      desired_capabilities=DesiredCapabilities.CHROME, options=options)
            driver.maximize_window()
            self.driver = driver

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
