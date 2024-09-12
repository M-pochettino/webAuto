from selenium.webdriver.common.by import By
import allure
from util_tools.basePage import BasePage
from urllib.parse import urlparse, parse_qs
from time import sleep
from util_tools.connectRedis import ConnectRedis


class LoginPage(BasePage):
    # 定义登录页面的URL路径
    url = ''

    # 定义页面中用户名输入框的定位器，使用CSS选择器定位
    username_input = (By.CSS_SELECTOR, '.el-form-item__content .el-input__inner[type="text"]')
    # 定义页面中密码输入框的定位器，使用CSS选择器定位
    password_input = (By.CSS_SELECTOR, '.el-form-item__content .el-input__inner[type="password"]')
    # 定义验证码输入框的定位器，使用CSS选择器定位
    captcha_input = (By.CSS_SELECTOR, '.el-input__inner[placeholder="请输入验证码"]')
    # 定义验证码图片的定位器，使用CSS选择器定位
    captcha_image_locator = (By.CSS_SELECTOR, '.el-col.el-col-8 img')
    # 定义登录按钮的定位器，使用CSS选择器定位
    submit_button = (By.CSS_SELECTOR, '.el-button.login-content-submit')
    # 定义登录结果的断言定位器，使用XPath定位
    assert_result = (By.XPATH, '//*[@id="ECS_MEMBERZONE"]/font/font')

    def __init__(self, driver):
        # 调用父类BasePage的初始化方法
        super().__init__(driver)
        # 将driver实例保存到实例变量中
        self.driver = driver

    # 定义一个通用的查找元素的方法，使用传入的定位器类型和定位器查找元素
    def find_element(self, by, locator):
        return self.driver.find_element(by, locator)

    # 定义一个获取元素属性值的方法，传入元素和属性名称，返回属性值
    def get_attribute(self, element, attribute):
        return element.get_attribute(attribute)

    # 定义登录操作方法，接收用户名和密码作为参数
    def login(self, user_name, pass_word):
        # 打开指定的登录页面URL
        self.open_url(self.url)

        # 使用allure记录一个步骤，附加URL并说明打开登录测试页面
        allure.attach(self.url, '打开登录测试页面', attachment_type=allure.attachment_type.TEXT)
        # 输入用户名到用户名输入框
        self.send_keys(self.username_input, user_name)
        # 输入密码到密码输入框
        self.send_keys(self.password_input, pass_word)
        # 等待1秒钟，通常用于确保页面加载完毕或验证码生成完毕
        sleep(1)
        # 查找验证码图片元素
        captcha_img = self.find_element(*self.captcha_image_locator)
        # 获取验证码图片的src属性（图片的URL）
        src = self.get_attribute(captcha_img, 'src')
        # 解析验证码图片URL，以提取其中的查询参数
        parsed_url = urlparse(src)
        # 获取URL中的查询参数，返回一个字典形式的结果
        query_params = parse_qs(parsed_url.query)
        # 从查询参数中提取randomStr的值，这个值可能用于生成验证码
        random_str_value = query_params.get('randomStr', [None])[0]
        # 拼接Redis中存储验证码的键名
        key = f'DEFAULT_CODE_KEY:{random_str_value}'
        # 创建一个Redis连接实例
        conn = ConnectRedis()
        # 从Redis缓存中获取验证码的实际值
        value = conn.get(key)
        # 关闭Redis连接
        conn.close()
        # 将获取到的验证码值输入到验证码输入框中
        self.send_keys(self.captcha_input, value)
        # 点击登录按钮，提交登录表单
        self.click(self.submit_button)

        # 使用allure记录一个步骤，附加当前输入内容的截图
        allure.attach(self.screenshots_png(), f'{user_name}:输入内容截屏', attachment_type=allure.attachment_type.PNG)
