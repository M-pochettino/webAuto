import time
import allure
from faker import Faker
from selenium.webdriver.common.by import By

from util_tools.basePage import BasePage


class UserAddPage(BasePage):  # 定义一个名为UserAddPage的类，继承自BasePage，表示新增用户页面的操作类
    url = '#/admin/system/user/index'  # 定义用户管理页面的URL，作为类的属性

    # 定义新增用户按钮的定位器，通过XPATH定位元素
    settle_button = (By.XPATH, "//button[@aria-disabled='false' and contains(@class, 'el-button--primary') and span[text()='新 增']]")
    # 定义用户名输入框的定位器
    username_input = (By.XPATH, '//form[@class="el-form el-form--default el-form--label-right"]//label[text()="用户名"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定义密码输入框的定位器
    password_input = (By.XPATH, '//label[text()="密码"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定义姓名输入框的定位器
    name_input = (By.XPATH, '//label[text()="姓名"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定义手机号输入框的定位器
    phone_input = (By.XPATH, '//form[@class="el-form el-form--default el-form--label-right"]//label[text()="手机号"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定义角色选择框的定位器
    role_select = (By.XPATH, '//label[text()="角色"]/following-sibling::div//div[@class="el-select__suffix"]/i[@class="el-icon el-select__caret el-select__icon"]')
    # 定义岗位选择框的定位器
    post_select = (By.XPATH, '//label[text()="岗位"]/following-sibling::div//div[@class="el-select__suffix"]/i[@class="el-icon el-select__caret el-select__icon"]')
    # 定义部门选择框的定位器
    dept_select = (By.XPATH, '//label[text()="部门"]/following-sibling::div//div[@class="el-select__suffix"]/i[@class="el-icon el-select__caret el-select__icon"]')
    # 定义邮箱输入框的定位器
    email_input = (By.XPATH, '//label[text()="邮箱"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定义昵称输入框的定位器
    nickname_input = (By.XPATH, '//label[text()="昵称"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定义禁用标志单选按钮的定位器
    lockFlag_radio = (By.XPATH, "//label[contains(@class, 'el-radio') and contains(span[@class='el-radio__label'], '禁用')]/span[@class='el-radio__input']/input[@type='radio']")
    # 定义确认按钮的定位器
    submit_user = (By.XPATH, "//button[contains(@class, 'el-button') and contains(., '确认')]")

    def user_add(self):  # 定义新增用户的方法
        # 打开用户管理页面
        self.open_url(self.url)
        # 将页面URL附加到Allure报告中，用于记录
        allure.attach(self.url, '打开测试页面', attachment_type=allure.attachment_type.TEXT)
        # 暂停1秒，等待页面加载完成
        time.sleep(1)
        # 点击新增用户按钮，打开新增用户表单
        self.click(self.settle_button)
        # 暂停1秒，等待新增用户表单加载完成
        time.sleep(1)

        # 实例化Faker对象，用于生成随机测试数据，使用简体中文环境
        fake = Faker("zh_CN")
        # 在用户名输入框中输入随机生成的用户名，后缀加上"harry"
        self.send_keys(self.username_input, fake.user_name() + "harry")
        # 在密码输入框中输入固定密码"123456"
        self.send_keys(self.password_input, "123456")
        # 在姓名输入框中输入随机生成的姓名
        self.send_keys(self.name_input, fake.name())
        # 在手机号输入框中输入随机生成的手机号
        self.send_keys(self.phone_input, fake.phone_number())
        # 选择角色，选择项为"产品经理"
        self.selects_by_single_level(self.role_select, "产品经理")
        # 选择岗位，选择项为"总监"
        self.selects_by_single_level(self.post_select, "总监")
        # 选择部门，选择项为"总裁办 -> 技术部 -> 产品部"
        self.selects_by_multi_level(self.dept_select, ["总裁办", "技术部", "产品部"])
        # 暂停1秒，等待下拉菜单的加载完成
        time.sleep(1)
        # 在邮箱输入框中输入随机生成的邮箱地址
        self.send_keys(self.email_input, fake.email())
        # 在昵称输入框中输入固定昵称"nick"
        self.send_keys(self.nickname_input, "nick")
        # 选择禁用单选按钮
        self.click(self.lockFlag_radio)
        # 点击确认按钮，提交新增用户表单
        self.click(self.submit_user)
        # 暂停1秒，等待提交操作完成
        time.sleep(1)

        # 截取当前页面的屏幕截图并附加到Allure报告中，用于记录提交后的页面状态
        allure.attach(self.screenshots_png(), '提交用户添加页面截屏', attachment_type=allure.attachment_type.PNG)
