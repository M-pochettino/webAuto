import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util_tools.basePage import BasePage


class PositionAddPage(BasePage):
    """岗位管理页面类"""
    # 定义岗位管理页面的URL地址
    url = '#/admin/system/post/index'

    # 定位"新增"按钮的定位器
    add_button = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., '新') and contains(., '增')]")
    
    # 弹窗相关定位器
    dialog = (By.CSS_SELECTOR, ".el-dialog")
    
    # 定位岗位编码输入框
    position_code_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '岗位编码') or contains(@placeholder, '请输入岗位编码')]")
    
    # 定位岗位名称输入框
    position_name_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '岗位名称') or contains(@placeholder, '请输入岗位名称')]")
    
    # 定位岗位排序输入框
    position_sort_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[@type='number' or contains(@placeholder, '排序')]")
    
    # 定位岗位描述输入框
    position_desc_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//textarea[contains(@placeholder, '岗位描述') or contains(@placeholder, '请输入岗位描述')]")
    
    # 定位确认按钮
    confirm_button = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--primary')]")
    
    # 定位取消按钮
    cancel_button = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '取消')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def wait_for_dialog(self, timeout=10):
        """等待弹窗出现"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.dialog)
            )
            return True
        except:
            return False

    def wait_for_dialog_close(self, timeout=10):
        """等待弹窗关闭"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.dialog)
            )
            return True
        except:
            return False

    def add_position(self, position_code, position_name, position_sort=0, position_desc=""):
        """添加岗位的方法"""
        self.open_url(self.url)  # 打开岗位管理页面
        allure.attach(self.url, '打开岗位管理页面', attachment_type=allure.attachment_type.TEXT)
        time.sleep(3)  # 等待页面加载完成
        
        # 点击新增按钮
        try:
            self.click(self.add_button)
            allure.attach("成功点击新增按钮", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"点击新增按钮失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '点击新增按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise
        
        # 等待弹窗出现
        if not self.wait_for_dialog():
            allure.attach(self.screenshots_png(), '弹窗未出现截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("新增岗位弹窗未出现")
        
        allure.attach("弹窗已打开", "弹窗状态", attachment_type=allure.attachment_type.TEXT)
        time.sleep(1)  # 等待弹窗完全加载
        
        # 输入岗位编码
        try:
            self.send_keys(self.position_code_input, position_code)
            allure.attach(f"输入岗位编码: {position_code}", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"输入岗位编码失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            raise
        
        # 输入岗位名称
        try:
            self.send_keys(self.position_name_input, position_name)
            allure.attach(f"输入岗位名称: {position_name}", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"输入岗位名称失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            raise
        
        # 输入岗位排序
        try:
            self.send_keys(self.position_sort_input, str(position_sort))
            allure.attach(f"输入岗位排序: {position_sort}", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"输入岗位排序失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            # 排序是可选的，不抛出异常
        
        # 输入岗位描述（可选）
        if position_desc:
            try:
                self.send_keys(self.position_desc_input, position_desc)
                allure.attach(f"输入岗位描述: {position_desc}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"输入岗位描述失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
                # 描述是可选的，不抛出异常
        
        # 截图
        allure.attach(self.screenshots_png(), '填写岗位信息完成', attachment_type=allure.attachment_type.PNG)
        
        # 点击确认按钮
        try:
            self.click(self.confirm_button)
            allure.attach("点击确认按钮", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"点击确认按钮失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '点击确认按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise
        
        # 等待弹窗关闭
        if not self.wait_for_dialog_close(timeout=15):
            allure.attach(self.screenshots_png(), '提交失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("岗位添加可能失败，弹窗未关闭")
        
        time.sleep(2)  # 等待操作完成
        allure.attach(self.screenshots_png(), '添加岗位完成', attachment_type=allure.attachment_type.PNG)

    def add_product_manager_position(self):
        """添加产品经理岗位"""
        self.add_position(
            position_code="PRODUCT_MANAGER_POST",
            position_name="产品经理", 
            position_sort=1,
            position_desc="产品经理岗位，负责产品规划和管理"
        )
    
    def add_supervisor_position(self):
        """添加总监岗位"""
        self.add_position(
            position_code="SUPERVISOR_POST",
            position_name="部门总监", 
            position_sort=2,
            position_desc="部门总监岗位，负责部门管理"
        )

    def add_general_position(self):
        """添加普通员工岗位"""
        self.add_position(
            position_code="GENERAL_STAFF",
            position_name="普通员工", 
            position_sort=3,
            position_desc="普通员工岗位"
        )

    def get_success_message(self):
        """获取成功消息"""
        try:
            # Element UI 的消息提示
            message_locator = (By.CSS_SELECTOR, ".el-message--success")
            element = self.location_element(*message_locator)
            return element.text
        except:
            return None

    def verify_add_success(self):
        """验证添加成功"""
        try:
            # 等待成功消息出现
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".el-message--success"))
            )
            return True
        except:
            return False 