import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util_tools.basePage import BasePage


class RoleAddPage(BasePage):
    """角色管理页面类"""
    # 定义角色管理页面的URL地址
    url = '#/admin/system/role/index'

    # 定位"新增"按钮的定位器 - 使用多种方式定位
    add_button = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., '新') and contains(., '增')]")
    add_button_alt = (By.XPATH, "//button[contains(@class, 'el-button--primary')]")
    
    # 弹窗相关定位器
    dialog = (By.CSS_SELECTOR, ".el-dialog")
    dialog_title = (By.CSS_SELECTOR, ".el-dialog__title")
    
    # 定位角色名称输入框的定位器 - 使用更通用的方式
    role_name_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '角色名称') or contains(@placeholder, '请输入角色名称')]")
    role_name_input_alt = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[@type='text']")
    
    # 定位角色标识输入框的定位器
    role_code_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '角色标识') or contains(@placeholder, '请输入角色标识')]")
    
    # 定位角色描述输入框的定位器
    role_desc_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//textarea[contains(@placeholder, '角色描述') or contains(@placeholder, '请输入角色描述')]")
    
    # 定位数据权限下拉框的定位器 - 修复定位器
    data_authority_select = (By.XPATH, "//div[contains(@class, 'el-dialog')]//label[text()='数据权限']/following-sibling::div//el-select")
    data_authority_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//label[text()='数据权限']/following-sibling::div//input")
    data_authority_input_alt = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[@placeholder='请选择']")
    data_authority_input_alt2 = (By.XPATH, "//div[contains(@class, 'el-dialog')]//el-select//input")
    
    # 数据权限选项 - 修复定位器，使用更通用的方式
    data_authority_options = {
        "全部": [
            (By.XPATH, "//div[contains(@class, 'el-select-dropdown')]//span[text()='全部']"),
            (By.XPATH, "//div[contains(@class, 'el-select-dropdown')]//span[contains(text(), '全部')]"),
            (By.XPATH, "//*[contains(@class, 'el-select-dropdown')]//span[text()='全部']"),
            (By.XPATH, "//*[text()='全部']"),
            (By.XPATH, "//li//span[text()='全部']"),
            (By.XPATH, "//span[text()='全部']")
        ],
        "自定义": [
            (By.XPATH, "//div[contains(@class, 'el-select-dropdown')]//span[text()='自定义']"),
            (By.XPATH, "//*[text()='自定义']")
        ],
        "本级及子级": [
            (By.XPATH, "//div[contains(@class, 'el-select-dropdown')]//span[text()='本级及子级']"),
            (By.XPATH, "//*[text()='本级及子级']")
        ],
        "本级": [
            (By.XPATH, "//div[contains(@class, 'el-select-dropdown')]//span[text()='本级']"),
            (By.XPATH, "//*[text()='本级']")
        ],
        "本人": [
            (By.XPATH, "//div[contains(@class, 'el-select-dropdown')]//span[text()='本人']"),
            (By.XPATH, "//*[text()='本人']")
        ]
    }
    
    # 定位确认按钮的定位器 - 修复定位器
    confirm_button = (By.XPATH, "//div[contains(@class, 'el-dialog')]//span[contains(@class, 'dialog-footer')]//button[contains(@class, 'el-button--primary')]")
    confirm_button_alt = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--primary')]")
    confirm_button_alt2 = (By.XPATH, "//button[contains(@class, 'el-button--primary') and not(@disabled)]")
    
    # 定位取消按钮的定位器
    cancel_button = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '取消')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver  # 添加driver属性以便访问

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

    def find_add_button(self):
        """尝试多种方式找到新增按钮"""
        locators = [self.add_button, self.add_button_alt]
        
        for locator in locators:
            try:
                element = self.location_element(*locator)
                if element:
                    return locator
            except:
                continue
        
        raise Exception("无法找到新增按钮")

    def find_input_element(self, primary_locator, alt_locator=None):
        """尝试多种方式找到输入框元素"""
        try:
            return self.location_element(*primary_locator)
        except:
            if alt_locator:
                try:
                    return self.location_element(*alt_locator)
                except:
                    pass
            raise Exception(f"无法找到输入框元素: {primary_locator}")

    def select_data_authority(self, authority_type="全部"):
        """选择数据权限类型"""
        # 尝试多种方式找到数据权限输入框
        data_input_locators = [
            self.data_authority_input,
            self.data_authority_input_alt,
            self.data_authority_input_alt2
        ]
        
        clicked = False
        for locator in data_input_locators:
            try:
                self.click(locator)
                clicked = True
                allure.attach(f"成功点击数据权限输入框: {locator}", "操作记录", attachment_type=allure.attachment_type.TEXT)
                break
            except Exception as e:
                allure.attach(f"尝试点击数据权限输入框失败: {locator} - {str(e)}", "尝试记录", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not clicked:
            allure.attach("无法找到数据权限输入框", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '无法找到数据权限输入框截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("无法找到数据权限输入框")
        
        time.sleep(3)  # 增加等待时间，让下拉选项完全加载
        
        # 使用有效的定位方式选择选项（基于测试结果，//*[text()='全部'] 是有效的）
        option_selectors = [
            # 最有效的通用文本匹配
            f"//*[text()='{authority_type}']",
            f"//*[contains(text(), '{authority_type}')]",
            # span元素匹配
            f"//span[text()='{authority_type}']",
            f"//span[contains(text(), '{authority_type}')]",
            # div元素匹配
            f"//div[text()='{authority_type}']",
            f"//div[contains(text(), '{authority_type}')]"
        ]
        
        selected = False
        for selector in option_selectors:
            try:
                option_locator = (By.XPATH, selector)
                self.click(option_locator)
                selected = True
                allure.attach(f"成功选择数据权限: {authority_type} 使用定位器: {selector}", "操作记录", attachment_type=allure.attachment_type.TEXT)
                break
            except Exception as e:
                allure.attach(f"尝试选择失败: {selector} - {str(e)}", "尝试记录", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not selected:
            # 最后的兜底策略：截图并选择第一个选项
            allure.attach(self.screenshots_png(), '无法找到具体选项，尝试选择第一个选项', attachment_type=allure.attachment_type.PNG)
            try:
                # 尝试选择第一个可见的下拉选项
                first_option_selectors = [
                    "//li[contains(@class, 'el-select-dropdown__item')][1]",
                    "//*[contains(@class, 'el-select-dropdown__item')][1]",
                    "//div[contains(@class, 'el-select-dropdown')]//*[1]"
                ]
                
                for first_selector in first_option_selectors:
                    try:
                        first_option = (By.XPATH, first_selector)
                        self.click(first_option)
                        allure.attach(f"选择第一个下拉选项: {first_selector}", "兜底操作", attachment_type=allure.attachment_type.TEXT)
                        selected = True
                        break
                    except:
                        continue
                        
                if not selected:
                    allure.attach(f"完全无法选择数据权限选项: {authority_type}", "错误信息", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(self.screenshots_png(), '选择数据权限选项完全失败截图', attachment_type=allure.attachment_type.PNG)
                    raise Exception(f"完全无法选择数据权限选项: {authority_type}")
            except Exception as e:
                allure.attach(f"兜底策略也失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
                raise Exception(f"无法选择数据权限选项: {authority_type}")
        
        time.sleep(1)

    def click_confirm_button(self):
        """点击确认按钮"""
        confirm_selectors = [
            # 标准确认按钮定位器
            "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--primary')]",
            "//div[contains(@class, 'el-dialog')]//span[contains(@class, 'dialog-footer')]//button[contains(@class, 'el-button--primary')]",
            # 按钮文本匹配
            "//div[contains(@class, 'el-dialog')]//button[contains(text(), '确')]",
            "//div[contains(@class, 'el-dialog')]//button[contains(text(), '确定')]",
            "//div[contains(@class, 'el-dialog')]//button[contains(text(), '确认')]",
            "//div[contains(@class, 'el-dialog')]//button[contains(text(), '保存')]",
            "//div[contains(@class, 'el-dialog')]//button[contains(text(), '提交')]",
            # 更通用的定位器
            "//button[contains(@class, 'el-button--primary') and not(@disabled)]",
            "//button[contains(@class, 'el-button--primary')]",
            # 弹窗底部按钮
            "//div[contains(@class, 'el-dialog__footer')]//button[contains(@class, 'el-button--primary')]",
            "//div[contains(@class, 'dialog-footer')]//button[contains(@class, 'el-button--primary')]",
            # 直接匹配按钮
            "//button[contains(text(), '确')]",
            "//button[contains(text(), '确定')]",
            "//button[contains(text(), '确认')]",
            "//button[contains(text(), '保存')]"
        ]
        
        clicked = False
        for selector in confirm_selectors:
            try:
                confirm_locator = (By.XPATH, selector)
                self.click(confirm_locator)
                clicked = True
                allure.attach(f"成功点击确认按钮: {selector}", "操作记录", attachment_type=allure.attachment_type.TEXT)
                break
            except Exception as e:
                allure.attach(f"尝试点击确认按钮失败: {selector} - {str(e)}", "尝试记录", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not clicked:
            allure.attach("无法找到确认按钮", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '无法找到确认按钮截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("无法找到确认按钮")

    def add_role(self, role_name, role_code, role_desc="", data_authority="全部"):
        """添加角色的方法"""
        self.open_url(self.url)  # 打开角色管理页面
        allure.attach(self.url, '打开角色管理页面', attachment_type=allure.attachment_type.TEXT)
        time.sleep(3)  # 等待页面加载完成
        
        # 点击新增按钮
        try:
            add_btn_locator = self.find_add_button()
            self.click(add_btn_locator)
            allure.attach("成功点击新增按钮", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"点击新增按钮失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '点击新增按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise
        
        # 等待弹窗出现
        if not self.wait_for_dialog():
            allure.attach(self.screenshots_png(), '弹窗未出现截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("新增角色弹窗未出现")
        
        allure.attach("弹窗已打开", "弹窗状态", attachment_type=allure.attachment_type.TEXT)
        time.sleep(1)  # 等待弹窗完全加载
        
        # 输入角色名称
        try:
            self.send_keys(self.role_name_input, role_name)
            allure.attach(f"输入角色名称: {role_name}", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            try:
                self.send_keys(self.role_name_input_alt, role_name)
                allure.attach(f"使用备用定位器输入角色名称: {role_name}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            except Exception as e2:
                allure.attach(f"输入角色名称失败: {str(e2)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
                raise
        
        # 输入角色标识
        try:
            self.send_keys(self.role_code_input, role_code)
            allure.attach(f"输入角色标识: {role_code}", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"输入角色标识失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            raise
        
        # 输入角色描述（可选）
        if role_desc:
            try:
                self.send_keys(self.role_desc_input, role_desc)
                allure.attach(f"输入角色描述: {role_desc}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"输入角色描述失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
                # 描述是可选的，不抛出异常
        
        # 选择数据权限（必填）
        try:
            self.select_data_authority(data_authority)
            allure.attach(f"选择数据权限: {data_authority}", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"选择数据权限失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '选择数据权限失败截图', attachment_type=allure.attachment_type.PNG)
            raise
        
        # 截图
        allure.attach(self.screenshots_png(), '填写角色信息完成', attachment_type=allure.attachment_type.PNG)
        
        # 点击确认按钮
        try:
            self.click_confirm_button()
            allure.attach("点击确认按钮", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"点击确认按钮失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '点击确认按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise
        
        # 等待弹窗关闭
        if not self.wait_for_dialog_close(timeout=15):
            allure.attach(self.screenshots_png(), '提交失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("角色添加可能失败，弹窗未关闭")
        
        time.sleep(2)  # 等待操作完成
        allure.attach(self.screenshots_png(), '添加角色完成', attachment_type=allure.attachment_type.PNG)

    def add_product_manager_role(self):
        """添加产品经理角色"""
        self.add_role(
            role_name="产品经理",
            role_code="PRODUCT_MANAGER", 
            role_desc="产品经理角色，负责产品规划和管理",
            data_authority="全部"
        )
    
    def add_supervisor_role(self):
        """添加总监角色"""
        self.add_role(
            role_name="部门总监",
            role_code="SUPERVISOR", 
            role_desc="总监角色，负责部门管理",
            data_authority="全部"
        )
        
    def check_role_exists(self, role_name):
        """检查角色是否已存在 - 简化版本，如果找不到就返回False"""
        try:
            self.open_url(self.url)
            time.sleep(2)
            # 使用更准确的定位器检查角色是否存在
            role_locator = (By.XPATH, f"//table//td[contains(text(), '{role_name}')]")
            self.location_element(*role_locator)
            return True
        except:
            # 如果找不到，直接返回False，不影响主流程
            return False

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