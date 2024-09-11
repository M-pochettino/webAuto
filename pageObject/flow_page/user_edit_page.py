import time
import allure
from faker import Faker
from selenium.webdriver.common.by import By

from util_tools.basePage import BasePage


class UserEditPage(BasePage):
    # 页面URL地址
    url = '#/admin/system/user/index'

    # 定位开关元素的定位器
    switch_locator = (By.XPATH, '//div[@class="el-switch el-switch--default is-checked"]')
    # 定位编辑按钮的定位器，使用Xpath定位第一个'修 改'按钮
    edit_button = (By.XPATH, "//button[normalize-space(span)='修 改'][1]")
    # 定位密码输入框的定位器
    password_input = (By.XPATH, '//label[text()="密码"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定位姓名输入框的定位器
    name_input = (By.XPATH, '//label[text()="姓名"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定位手机号输入框的定位器
    phone_input = (By.XPATH, '//form[@class="el-form el-form--default el-form--label-right"]//label[text()="手机号"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定位角色下拉框的定位器
    role_select = (By.XPATH, '//label[text()="角色"]/following-sibling::div//div[@class="el-select__suffix"]/i[@class="el-icon el-select__caret el-select__icon"]')
    # 定位岗位下拉框的定位器
    post_select = (By.XPATH, '//label[text()="岗位"]/following-sibling::div//div[@class="el-select__suffix"]/i[@class="el-icon el-select__caret el-select__icon"]')
    # 定位部门下拉框的定位器
    dept_select = (By.XPATH, '//label[text()="部门"]/following-sibling::div//div[@class="el-select__suffix"]/i[@class="el-icon el-select__caret el-select__icon"]')
    # 定位邮箱输入框的定位器
    email_input = (By.XPATH, '//label[text()="邮箱"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定位昵称输入框的定位器
    nickname_input = (By.XPATH, '//label[text()="昵称"]/following-sibling::div//input[@class="el-input__inner"]')
    # 定位确认提交按钮的定位器
    submit_user = (By.XPATH, "//button[contains(@class, 'el-button') and contains(., '确认')]")

    # 用户编辑操作方法
    def user_edit(self):
        fake = Faker("zh_CN")  # 使用Faker库生成随机中文数据
        self.open_url(self.url)  # 打开用户编辑页面
        allure.attach(self.url, '打开测试页面', attachment_type=allure.attachment_type.TEXT)  # 记录操作日志
        time.sleep(1)  # 等待页面加载
        self.click(self.edit_button)  # 点击编辑按钮
        self.send_keys(self.password_input, "123456", is_clear=True)  # 清空并输入新密码
        self.send_keys(self.name_input, fake.name(), is_clear=True)  # 清空并输入随机生成的姓名
        self.send_keys(self.phone_input, fake.phone_number(), is_clear=True)  # 清空并输入随机生成的手机号
        self.selects_by_single_level(self.role_select, "产品经理")  # 选择角色为“产品经理”
        self.selects_by_single_level(self.post_select, "总监")  # 选择岗位为“总监”
        self.selects_by_multi_level(self.dept_select, ["总裁办", "技术部", "研发部", "UI设计部"])  # 选择多个部门
        time.sleep(1)  # 等待页面响应
        self.send_keys(self.email_input, fake.email(), is_clear=True)  # 清空并输入随机生成的邮箱
        self.send_keys(self.nickname_input, "nic", is_clear=True)  # 清空并输入昵称
        self.click(self.submit_user)  # 点击确认提交按钮
        time.sleep(1)  # 等待提交操作完成
        allure.attach(self.screenshots_png(), '提交订单页面截屏', attachment_type=allure.attachment_type.PNG)  # 添加提交后的页面截图到报告中

    # 用户状态切换操作方法
    def user_change_state(self):
        self.open_url(self.url)  # 打开用户编辑页面
        allure.attach(self.url, '打开测试页面', attachment_type=allure.attachment_type.TEXT)  # 记录操作日志
        time.sleep(1)  # 等待页面加载
        self.click(self.switch_locator)  # 点击开关按钮切换状态
        time.sleep(1)  # 等待状态切换操作完成
