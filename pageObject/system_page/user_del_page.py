import time
import allure
from selenium.webdriver.common.by import By

from util_tools.basePage import BasePage


class UserDelPage(BasePage):  # 定义一个名为UserDelPage的类，继承自BasePage，表示删除用户页面的操作类
    url = '#/admin/system/user/index'  # 定义用户管理页面的URL，作为类的属性

    # 定义删除按钮的定位器，通过XPATH定位第一个可用的删除按钮
    del_button = (By.XPATH, "//button[not(@disabled) and @aria-disabled='false'][span[text()='删除']][1]")
    # 定义确认删除按钮的定位器，定位弹出确认框中的确认按钮
    submit_user = (By.XPATH, "//div[contains(@class, 'el-overlay-message-box')]//button[contains(@class, 'el-button--primary') and span[text()='确认']]")

    def user_del(self):  # 定义删除用户的方法
        # 打开用户管理页面
        self.open_url(self.url)
        # 将页面URL附加到Allure报告中，用于记录
        allure.attach(self.url, '打开测试页面', attachment_type=allure.attachment_type.TEXT)
        # 暂停1秒，等待页面加载完成
        time.sleep(1)
        # 点击删除按钮，尝试删除第一个用户
        self.click(self.del_button)
        # 暂停1秒，等待删除确认框弹出
        time.sleep(1)
        # 点击确认按钮，确认删除操作
        self.click(self.submit_user)
        # 暂停1秒，等待删除操作完成
        time.sleep(1)

        # 截取当前页面的屏幕截图并附加到Allure报告中，用于记录删除后的页面状态
        allure.attach(self.screenshots_png(), '提交用户删除页面截屏', attachment_type=allure.attachment_type.PNG)

