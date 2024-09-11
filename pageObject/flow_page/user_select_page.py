import time
import allure
from selenium.webdriver.common.by import By

from util_tools.basePage import BasePage
from util_tools.connectMysql import ConnectMysql


class UserSelectPage(BasePage):
    # 定义页面URL地址
    url = '#/admin/system/user/index'

    # 定位用户名输入框的定位器，通过XPath找到具有指定placeholder的输入框元素
    username_input = (By.XPATH, "//div[contains(@class, 'el-input__wrapper')]//input[@placeholder='请输入用户名']")
    # 定位“查询”按钮的定位器，通过XPath找到具有指定类名和文本内容的按钮元素
    search = (By.XPATH, "//button[contains(@class, 'el-button--primary')]//span[text()='查询']")
    # 定位显示用户总数的span元素，通过XPath找到具有指定类名和包含“共”字样的span元素
    total_span = (By.XPATH, '//span[contains(@class, "el-pagination__total") and contains(text(), "共")]')

    def user_select(self):
        """查询用户操作流程"""

        self.open_url(self.url)  # 打开用户管理页面
        allure.attach(self.url, '打开测试页面', attachment_type=allure.attachment_type.TEXT)  # 将页面URL附加到报告中
        time.sleep(1)  # 等待页面加载
        self.send_keys(self.username_input, "t")  # 在用户名输入框中输入字母't'，用于查询以't'开头的用户名
        time.sleep(1)  # 等待输入完成
        self.click(self.search)  # 点击“查询”按钮，执行查询操作
        time.sleep(1)  # 等待查询结果加载
        # 获取显示总用户数的span元素
        total_span_element = self.location_element(*self.total_span)
        # 获取span元素的文本内容
        total_text = total_span_element.text
        # 从文本中提取用户总数的数值（假设文本格式为"共 N 条"）
        page_value = int(total_text.split()[1])
        # 初始化数据库连接
        conn = ConnectMysql()
        # 构造SQL查询语句，查询用户名以't'开头且未被标记为删除的用户总数
        sql = "SELECT count(*) FROM sys_user WHERE username like 't%' and del_flag = 0"
        result = conn.query(sql)  # 执行SQL查询
        # 对查询结果进行处理
        if result:
            print("Query successful:", result)  # 查询成功并输出结果
        else:
            print("No data found")  # 未找到匹配的数据
        # 从查询结果中取出count(*)的值
        count_value = result['count(*)']
        # 返回页面上显示的用户总数和数据库查询的用户总数
        return page_value, count_value

