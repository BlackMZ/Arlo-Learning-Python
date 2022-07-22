=====================================================================
===========================web类资产对接说明===========================
=====================================================================
web类资产对接是指通过python脚本方式来实现资产账号的登录、改密、发现等功能。
只要是b/s架构的资产，比如网络设备、安全设备、应用系统，都可以通过此方式来快速对接。

===========================准备工作===================================
1.熟悉python语言
2.熟悉selenium/xpath等知识
	https://www.selenium.dev/zh-cn/documentation/webdriver/
	https://blog.csdn.net/weixin_36279318/article/details/79475388
	https://www.runoob.com/xpath/xpath-tutorial.html
3.搭建python开发环境（包括安装selenium库，muggle_ocr库）
4.下载Chrome浏览器
5.下载WebDriver（下载Chrome版本对应的）
	https://chromedriver.storage.googleapis.com/index.html

===========================脚本开发===================================
注意：
修改此行代码中webdriver路径为自己电脑上的路径
self.driver = webdriver.Chrome('/Users/daniel/Downloads/chromedriver', options=options)

验证码识别：
## 修改验证码xpath
#img_element = self.driver.find_element_by_class_name("getCaptcha")
#if img_element is not None:
	#img_txt = self.get_img_txt(img_element.screenshot_as_base64)
	## 填充验证码输入框
	#self.driver.find_element_by_xpath("//input[@placeholder='请输入验证码']").send_keys(img_txt)
	#time.sleep(1)

===========================本地调试说明================================
调用说明：
python xxx.py 参数列表


参数说明：
-t local表示本地调试模式，remote表示远程调用模式
-s 远程WebDriver地址，适用于remote模式
-l URL
-u 账号
-p 密码
-n 新密码
-v 经由哪个账号改密，适用于当前账号不能改密的情况
-i 经由哪个密码改密，适用于当前账号不能改密的情况

客服系统
账号：5145  密码：Hlt123456   
https://portal-ynt.hltgz.com/#/agentlogin

调用示例：
登录：
（无验证码）
python XPAM-dengluyanzheng.py -t local -l https://portal-ynt.hltgz.com/#/agentlogin -u 5145 -p "Hlt123456"
（有验证码）
python educity_demo_verify.py -t local -l https://www.educity.cn/login.html -u 16657112952 -p '123Qwe!@#'

改密：
python XPAM-gaimi.py -t local -l https://portal-ynt.hltgz.com/#/agentlogin -u 5145 -p "Hlt123456" -n "Hlt1234567"

发现：
python XPAM-faxianzhanghu.py -t local -l https://portal-ynt.hltgz.com/#/agentlogin -u 5145 -p "Hlt123456"
