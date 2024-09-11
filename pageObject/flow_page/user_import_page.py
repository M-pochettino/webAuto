import time
import allure
from selenium.webdriver.common.by import By

from util_tools.basePage import BasePage


class UserImportPage(BasePage):
    # 定义页面URL地址
    url = '#/admin/system/user/index'

    # 定位“导入”按钮的定位器，按钮具有类名'el-button--primary'，并且包含文本'span'为“导入”
    file_input_click = (By.XPATH, "//button[contains(@class, 'el-button--primary')][contains(span, '导入')]")
    # 定位文件上传的input元素，通过CSS选择器找到具有类名'el-upload__input'的元素
    file_input_locator = (By.CSS_SELECTOR, "input.el-upload__input")
    # 定位“确认”按钮的定位器，使用XPath找到文本为“确认”的按钮
    submit_import = (By.XPATH, "//button[span[text()='确认']]")

    def user_import(self):
        """上传文件的操作流程"""
        self.open_url(self.url)  # 打开用户管理页面
        allure.attach(self.url, '打开测试页面', attachment_type=allure.attachment_type.TEXT)  # 添加操作日志到报告中
        time.sleep(1)  # 等待页面加载
        self.click(self.file_input_click)  # 点击“导入”按钮，打开文件上传对话框
        time.sleep(1)  # 等待文件上传对话框弹出
        self.send_keys(self.file_input_locator, "E:\\temp.xlsx")  # 在文件上传input元素中输入文件路径，模拟文件上传
        time.sleep(1)  # 等待文件上传完成
        self.click(self.submit_import)  # 点击“确认”按钮提交文件
        time.sleep(1)  # 等待文件上传和导入操作完成

