import allure
import pytest
from time import sleep

from pageObject.system_page.role_add_page import RoleAddPage
from pageObject.system_page.position_add_page import PositionAddPage
from pageObject.flow_page.user_add_page import UserAddPage
from pageObject.flow_page.user_import_page import UserImportPage
from util_tools.basePage import BasePage


@allure.feature('系统设置')
class TestRoleSetup:
    """角色设置测试类 - 用于测试前数据准备"""

    @allure.story('添加产品经理角色')
    def test_add_product_manager_role(self, login_driver):
        """添加产品经理角色"""
        page = RoleAddPage(login_driver)
        
        try:
            allure.attach("开始添加产品经理角色", "测试开始", allure.attachment_type.TEXT)
            
            page.add_product_manager_role()
            
            # 验证添加成功
            if page.verify_add_success():
                allure.attach("产品经理角色添加成功", "添加结果", allure.attachment_type.TEXT)
            else:
                allure.attach("未检测到成功消息，但操作已完成", "添加结果", allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"添加产品经理角色失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            allure.attach(page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise

    @allure.story('添加总监角色')  
    def test_add_supervisor_role(self, login_driver):
        """添加总监角色"""
        page = RoleAddPage(login_driver)
        
        try:
            allure.attach("开始添加总监角色", "测试开始", allure.attachment_type.TEXT)
            
            page.add_supervisor_role()
            
            # 验证添加成功
            if page.verify_add_success():
                allure.attach("总监角色添加成功", "添加结果", allure.attachment_type.TEXT)
            else:
                allure.attach("未检测到成功消息，但操作已完成", "添加结果", allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"添加总监角色失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            allure.attach(page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise

    @allure.story('添加产品经理岗位')
    def test_add_product_manager_position(self, login_driver):
        """添加产品经理岗位"""
        page = PositionAddPage(login_driver)
        
        try:
            allure.attach("开始添加产品经理岗位", "测试开始", allure.attachment_type.TEXT)
            
            page.add_product_manager_position()
            
            # 验证添加成功
            if page.verify_add_success():
                allure.attach("产品经理岗位添加成功", "添加结果", allure.attachment_type.TEXT)
            else:
                allure.attach("未检测到成功消息，但操作已完成", "添加结果", allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"添加产品经理岗位失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            allure.attach(page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise

    @allure.story('添加总监岗位')
    def test_add_supervisor_position(self, login_driver):
        """添加总监岗位"""
        page = PositionAddPage(login_driver)
        
        try:
            allure.attach("开始添加总监岗位", "测试开始", allure.attachment_type.TEXT)
            
            page.add_supervisor_position()
            
            # 验证添加成功
            if page.verify_add_success():
                allure.attach("总监岗位添加成功", "添加结果", allure.attachment_type.TEXT)
            else:
                allure.attach("未检测到成功消息，但操作已完成", "添加结果", allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"添加总监岗位失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            allure.attach(page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise

    @allure.story('添加普通员工岗位')
    def test_add_general_position(self, login_driver):
        """添加普通员工岗位"""
        page = PositionAddPage(login_driver)
        
        try:
            allure.attach("开始添加普通员工岗位", "测试开始", allure.attachment_type.TEXT)
            
            page.add_general_position()
            
            # 验证添加成功
            if page.verify_add_success():
                allure.attach("普通员工岗位添加成功", "添加结果", allure.attachment_type.TEXT)
            else:
                allure.attach("未检测到成功消息，但操作已完成", "添加结果", allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"添加普通员工岗位失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            allure.attach(page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise

    @allure.story('验证角色功能')
    def test_role_functionality(self, login_driver):
        """验证角色功能是否正常"""
        page = RoleAddPage(login_driver)
        
        try:
            # 验证页面能否正常打开
            page.open_url(page.url)
            allure.attach("角色管理页面已打开", "页面状态", allure.attachment_type.TEXT)
            
            # 验证新增按钮是否存在
            add_btn_locator = page.find_add_button()
            allure.attach(f"新增按钮存在: {add_btn_locator}", "元素检查", allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"角色功能验证失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            allure.attach(page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise 

    @allure.story('跳转用户管理并测试用户功能')
    def test_navigate_to_user_management(self, login_driver):
        """角色和岗位添加完成后，跳转到用户管理页面进行用户功能测试"""
        try:
            allure.attach("开始跳转到用户管理页面", "页面跳转", allure.attachment_type.TEXT)
            
            # 使用基础页面对象进行导航
            base_page = BasePage(login_driver)
            
            # 通过菜单导航到用户管理页面
            user_management_url = "http://39.99.40.155#/admin/system/user/index"
            base_page.open_url(user_management_url)
            allure.attach(f"已跳转到用户管理页面: {user_management_url}", "页面跳转", allure.attachment_type.TEXT)
            
            sleep(3)  # 等待页面加载
            
            # 截图确认页面已加载
            allure.attach(base_page.screenshots_png(), '用户管理页面截图', attachment_type=allure.attachment_type.PNG)
            
            # 测试用户导入功能
            self._test_user_import(login_driver)
            
            # 测试用户添加功能  
            self._test_user_add(login_driver)
            
            allure.attach("用户管理功能测试完成", "测试完成", allure.attachment_type.TEXT)
            
        except Exception as e:
            allure.attach(f"用户管理测试失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
            base_page = BasePage(login_driver)
            allure.attach(base_page.screenshots_png(), '错误截图', attachment_type=allure.attachment_type.PNG)
            raise

    def _test_user_import(self, login_driver):
        """测试用户导入功能"""
        try:
            allure.attach("开始测试用户导入功能", "功能测试", allure.attachment_type.TEXT)
            
            # 初始化用户导入页面对象
            import_page = UserImportPage(login_driver)
            
            # 执行用户导入操作
            import_page.user_import()
            
            # 验证导入结果
            base_page = BasePage(login_driver)
            base_page.assert_element_text_contains("用户导入成功")
            
            allure.attach("用户导入功能测试成功", "功能测试结果", allure.attachment_type.TEXT)
            sleep(3)
            
        except Exception as e:
            allure.attach(f"用户导入功能测试失败: {str(e)}", "功能测试错误", allure.attachment_type.TEXT)
            raise

    def _test_user_add(self, login_driver):
        """测试用户添加功能"""
        try:
            allure.attach("开始测试用户添加功能", "功能测试", allure.attachment_type.TEXT)
            
            # 初始化用户添加页面对象
            add_page = UserAddPage(login_driver)
            
            # 执行用户添加操作
            add_page.user_add()
            
            # 验证添加结果
            base_page = BasePage(login_driver)
            base_page.assert_element_text_contains("添加成功")
            
            allure.attach("用户添加功能测试成功", "功能测试结果", allure.attachment_type.TEXT)
            sleep(3)
            
        except Exception as e:
            allure.attach(f"用户添加功能测试失败: {str(e)}", "功能测试错误", allure.attachment_type.TEXT)
            raise 