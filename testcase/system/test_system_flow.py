import os
from time import sleep
import pytest
import allure

from pageObject.system_page.role_add_page import RoleAddPage
from pageObject.system_page.position_add_page import PositionAddPage
from pageObject.system_page.user_add_page import UserAddPage
from pageObject.system_page.user_del_page import UserDelPage
from pageObject.system_page.user_edit_page import UserEditPage
from pageObject.system_page.user_import_page import UserImportPage
from pageObject.system_page.user_select_page import UserSelectPage
from pageObject.system_page.file_manage_page import FileManagePage
from util_tools.basePage import BasePage


@allure.feature('系统管理流程测试')
class TestSystemFlow:
    """系统管理流程测试类 - 连续执行角色、用户、文件管理测试"""

    @allure.story('1. 角色管理')
    def test_01_role_add(self, login_driver):
        """测试角色添加功能"""
        allure.attach("开始执行角色添加测试", "步骤1", attachment_type=allure.attachment_type.TEXT)
        
        page = RoleAddPage(login_driver)
        page.role_add()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("添加成功")
        sleep(2)

    @allure.story('1. 角色管理')
    def test_02_position_add(self, login_driver):
        """测试岗位添加功能"""
        allure.attach("开始执行岗位添加测试", "步骤2", attachment_type=allure.attachment_type.TEXT)
        
        page = PositionAddPage(login_driver)
        page.position_add()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("添加成功")
        sleep(2)

    @allure.story('2. 用户管理')
    def test_03_user_import(self, login_driver):
        """测试用户导入功能"""
        allure.attach("开始执行用户导入测试", "步骤3", attachment_type=allure.attachment_type.TEXT)
        
        page = UserImportPage(login_driver)
        page.user_import()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("用户导入成功")
        sleep(2)

    @allure.story('2. 用户管理')
    def test_04_user_add(self, login_driver):
        """测试用户添加功能"""
        allure.attach("开始执行用户添加测试", "步骤4", attachment_type=allure.attachment_type.TEXT)
        
        page = UserAddPage(login_driver)
        page.user_add()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("添加成功")
        sleep(2)

    @allure.story('2. 用户管理')
    def test_05_user_edit(self, login_driver):
        """测试用户修改功能"""
        allure.attach("开始执行用户修改测试", "步骤5", attachment_type=allure.attachment_type.TEXT)
        
        page = UserEditPage(login_driver)
        page.user_edit()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("修改成功")
        sleep(2)

    @allure.story('2. 用户管理')
    def test_06_user_change_state(self, login_driver):
        """测试用户启用禁用功能"""
        allure.attach("开始执行用户状态变更测试", "步骤6", attachment_type=allure.attachment_type.TEXT)
        
        page = UserEditPage(login_driver)
        page.user_change_state()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("操作成功")
        sleep(2)

    @allure.story('2. 用户管理')
    def test_07_user_select(self, login_driver):
        """测试用户查询功能"""
        allure.attach("开始执行用户查询测试", "步骤7", attachment_type=allure.attachment_type.TEXT)
        
        page = UserSelectPage(login_driver)
        total, count = page.user_select()
        assert total == count
        sleep(2)

    @allure.story('3. 文件管理')
    def test_08_file_upload(self, login_driver):
        """测试文件上传功能"""
        allure.attach("开始执行文件上传测试", "步骤8", attachment_type=allure.attachment_type.TEXT)
        
        # 初始化文件管理页面对象
        file_page = FileManagePage(login_driver)
        
        # 获取测试数据目录路径
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_data_dir = os.path.join(current_dir, 'test_data', 'image')
        
        allure.attach(test_data_dir, '测试数据目录', attachment_type=allure.attachment_type.TEXT)
        
        # 验证测试数据目录是否存在
        assert os.path.exists(test_data_dir), f"测试数据目录不存在: {test_data_dir}"
        
        # 获取图片文件列表
        image_files = [f for f in os.listdir(test_data_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        allure.attach(f"找到 {len(image_files)} 个图片文件", "文件统计", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # 执行完整的文件上传流程
        try:
            file_page.upload_files_and_close(test_data_dir)
            allure.attach("文件上传流程执行完成", "上传结果", 
                         attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(str(e), "上传异常", attachment_type=allure.attachment_type.TEXT)
            # 截图记录错误状态
            base_page = BasePage(login_driver)
            allure.attach(base_page.screenshots_png(), '错误截图', 
                         attachment_type=allure.attachment_type.PNG)
            raise
        
        # 等待操作完成并截图
        sleep(3)
        base_page = BasePage(login_driver)
        allure.attach(base_page.screenshots_png(), '最终状态截图', 
                     attachment_type=allure.attachment_type.PNG)

    @allure.story('2. 用户管理')
    def test_09_user_del(self, login_driver):
        """测试用户删除功能 - 最后执行"""
        allure.attach("开始执行用户删除测试", "步骤9", attachment_type=allure.attachment_type.TEXT)
        
        page = UserDelPage(login_driver)
        page.user_del()
        
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("删除成功")
        sleep(2)
        
        allure.attach("系统管理流程测试全部完成", "测试结束", 
                     attachment_type=allure.attachment_type.TEXT) 