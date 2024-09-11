from time import sleep

import allure

from pageObject.flow_page.user_add_page import UserAddPage
from pageObject.flow_page.user_del_page import UserDelPage
from pageObject.flow_page.user_edit_page import UserEditPage
from pageObject.flow_page.user_import_page import UserImportPage
from pageObject.flow_page.user_select_page import UserSelectPage
from util_tools.basePage import BasePage


# 定义一个Allure特性标签，用于标识用户管理模块的测试
@allure.feature('用户管理')
class TestUserFlow:

    # 定义一个Allure故事标签，表示这是“导入用户”功能的测试
    @allure.story('导入用户')
    def test_user_import(self, login_driver):
        # 初始化用户导入页面对象，并传入登录后的浏览器驱动实例
        page = UserImportPage(login_driver)
        # 调用页面对象中的用户导入方法，执行导入操作
        page.user_import()
        # 重新初始化一个基础页面对象，用于进行通用的页面操作
        page = BasePage(login_driver)
        # 断言页面上是否包含“用户导入成功”这段文本，以验证导入操作是否成功
        page.assert_element_text_contains("用户导入成功")
        # 等待3秒，确保页面操作完成并稳定
        sleep(3)

    # 定义一个Allure故事标签，表示这是“添加用户”功能的测试
    @allure.story('添加用户')
    def test_user_add(self, login_driver):
        # 初始化用户添加页面对象，并传入登录后的浏览器驱动实例
        page = UserAddPage(login_driver)
        # 调用页面对象中的添加用户方法，执行添加操作
        page.user_add()
        # 重新初始化一个基础页面对象，用于进行通用的页面操作
        page = BasePage(login_driver)
        # 断言页面上是否包含“添加成功”这段文本，以验证添加操作是否成功
        page.assert_element_text_contains("添加成功")
        # 等待3秒，确保页面操作完成并稳定
        sleep(3)

    # 定义一个Allure故事标签，表示这是“修改用户”功能的测试
    @allure.story('修改用户')
    def test_user_edit(self, login_driver):
        # 初始化用户编辑页面对象，并传入登录后的浏览器驱动实例
        page = UserEditPage(login_driver)
        # 调用页面对象中的修改用户方法，执行编辑操作
        page.user_edit()
        # 重新初始化一个基础页面对象，用于进行通用的页面操作
        page = BasePage(login_driver)
        # 断言页面上是否包含“修改成功”这段文本，以验证修改操作是否成功
        page.assert_element_text_contains("修改成功")
        # 等待3秒，确保页面操作完成并稳定
        sleep(3)

    # 定义一个Allure故事标签，表示这是“启用禁用”功能的测试
    @allure.story('启用禁用')
    def test_change_state(self, login_driver):
        # 初始化用户编辑页面对象，并传入登录后的浏览器驱动实例
        page = UserEditPage(login_driver)
        # 调用页面对象中的启用/禁用用户状态方法，执行状态变更操作
        page.user_change_state()
        # 重新初始化一个基础页面对象，用于进行通用的页面操作
        page = BasePage(login_driver)
        # 断言页面上是否包含“操作成功”这段文本，以验证状态变更操作是否成功
        page.assert_element_text_contains("操作成功")
        # 等待3秒，确保页面操作完成并稳定
        sleep(3)

    # 定义一个Allure故事标签，表示这是“删除用户”功能的测试
    @allure.story('删除用户')
    def test_user_del(self, login_driver):
        # 初始化用户删除页面对象，并传入登录后的浏览器驱动实例
        page = UserDelPage(login_driver)
        # 调用页面对象中的删除用户方法，执行删除操作
        page.user_del()
        # 重新初始化一个基础页面对象，用于进行通用的页面操作
        page = BasePage(login_driver)
        # 断言页面上是否包含“删除成功”这段文本，以验证删除操作是否成功
        page.assert_element_text_contains("删除成功")
        # 等待3秒，确保页面操作完成并稳定
        sleep(3)

    # 定义一个Allure故事标签，表示这是“查询用户列表”功能的测试
    @allure.story('查询用户列表')
    def test_user_select(self, login_driver):
        # 初始化用户查询页面对象，并传入登录后的浏览器驱动实例
        page = UserSelectPage(login_driver)
        # 调用页面对象中的查询用户方法，执行用户列表查询操作
        total, count = page.user_select()
        # 断言查询到的用户总数是否与预期相符，以验证查询操作是否成功
        assert total == count
        # 等待3秒，确保页面操作完成并稳定
        sleep(3)

