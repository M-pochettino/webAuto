import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from util_tools.basePage import BasePage


class ChannelPage(BasePage):
    """支付渠道管理页面类"""
    # 定义支付渠道页面的URL地址
    url = '#/biz/pay/channel/index'

    # 定位"新增"按钮的定位器
    add_button = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., '新') and contains(., '增')]")
    
    # 弹窗相关定位器
    dialog = (By.CSS_SELECTOR, ".el-dialog")
    dialog_title = (By.CSS_SELECTOR, ".el-dialog__title")
    
    # 新增/编辑表单字段定位器
    app_id_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, 'AppID') or contains(@placeholder, '请输入应用ID')]")
    channel_name_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '渠道名称') or contains(@placeholder, '请输入渠道名称')]")
    merchant_id_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '商户ID') or contains(@placeholder, '请输入商户ID')]")
    
    # 渠道类型下拉选择器 (根据标签定位)
    channel_type_select = (By.XPATH, "//div[contains(@class, 'el-dialog')]//label[contains(text(), '渠道类型')]/following-sibling::div//div[contains(@class, 'el-select')]")
    
    # 渠道状态下拉选择器 (根据标签定位)  
    channel_status_select = (By.XPATH, "//div[contains(@class, 'el-dialog')]//label[contains(text(), '渠道状态')]/following-sibling::div//div[contains(@class, 'el-select')]")
    
    # 前端回调地址和后端回调地址
    front_callback_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '前端回调') or contains(@placeholder, '请输入前端回调地址')]")
    back_callback_input = (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[contains(@placeholder, '后端回调') or contains(@placeholder, '请输入后端回调地址')]")
    
    # 备注文本域
    remark_textarea = (By.XPATH, "//div[contains(@class, 'el-dialog')]//textarea[contains(@placeholder, '备注') or contains(@placeholder, '请输入备注')]")
    
    # 配置参数文本域
    config_textarea = (By.XPATH, "//div[contains(@class, 'el-dialog')]//textarea[contains(@placeholder, '配置参数') or contains(@placeholder, '请输入配置参数')]")
    
    # 对话框按钮
    confirm_button = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--primary')]")
    cancel_button = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '取消')]")
    
    # 列表页面操作按钮
    edit_button = (By.XPATH, "//button[contains(@class, 'el-button') and contains(.,'修 改')]")
    delete_button = (By.XPATH, "//button[contains(@class, 'el-button') and contains(.,'删除')]")
    
    # 确认删除弹窗
    delete_confirm_button = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(text(), '确定')]")
    
    # 搜索相关
    search_input = (By.XPATH, "//input[contains(@placeholder, '渠道名称') or contains(@placeholder, '请输入渠道名称')]")
    search_button = (By.XPATH, "//button[contains(@class, 'el-button--primary') and not(contains(text(), '新增'))]")
    reset_button = (By.XPATH, "//button[contains(@class, 'el-button') and contains(.,'重置')]")
    
    # 表格相关
    table_rows = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    table_no_data = (By.CSS_SELECTOR, ".el-table__empty-text")

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

    def navigate_to_channel_page(self):
        """导航到支付渠道页面"""
        self.open_url(self.url)
        allure.attach(self.url, '打开支付渠道管理页面', attachment_type=allure.attachment_type.TEXT)
        time.sleep(3)  # 等待页面加载完成

    def add_channel(self, app_id, channel_name, merchant_id, channel_type="微信支付", channel_status="正常",
                   front_callback="", back_callback="", remark="", config='{"default": "config"}'):
        """添加支付渠道"""
        self.navigate_to_channel_page()
        
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
            raise Exception("新增渠道弹窗未出现")

        allure.attach("弹窗已打开", "弹窗状态", attachment_type=allure.attachment_type.TEXT)
        time.sleep(1)

        # 填写表单字段
        try:
            # AppID
            self.send_keys(self.app_id_input, app_id)
            allure.attach(f"输入AppID: {app_id}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 渠道名称
            self.send_keys(self.channel_name_input, channel_name)
            allure.attach(f"输入渠道名称: {channel_name}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 商户ID
            self.send_keys(self.merchant_id_input, merchant_id)
            allure.attach(f"输入商户ID: {merchant_id}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 选择渠道类型
            self.select_channel_type(channel_type)
            
            # 选择渠道状态
            self.select_channel_status(channel_status)
            
            # 前端回调地址（可选）
            if front_callback:
                self.send_keys(self.front_callback_input, front_callback)
                allure.attach(f"输入前端回调地址: {front_callback}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 后端回调地址（可选）
            if back_callback:
                self.send_keys(self.back_callback_input, back_callback)
                allure.attach(f"输入后端回调地址: {back_callback}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 备注（可选）
            if remark:
                self.send_keys(self.remark_textarea, remark)
                allure.attach(f"输入备注: {remark}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 配置参数（必填）- 确保总是填写配置参数
            if not config or config.strip() == "":
                config = '{"default": "config"}'  # 如果配置为空，使用默认配置
            self.send_keys(self.config_textarea, config)
            allure.attach(f"输入配置参数: {config}", "操作记录", attachment_type=allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(f"填写表单失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '填写表单失败截图', attachment_type=allure.attachment_type.PNG)
            raise

        # 截图
        allure.attach(self.screenshots_png(), '填写渠道信息完成', attachment_type=allure.attachment_type.PNG)

        # 点击确认按钮（使用成功的定位策略）
        try:
            locator = (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--primary')]")
            self.click(locator)
            allure.attach("成功点击确认按钮", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"确认按钮点击失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '确认按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("无法定位确认按钮")

        # 等待弹窗关闭
        if not self.wait_for_dialog_close(timeout=15):
            allure.attach(self.screenshots_png(), '提交失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("渠道添加可能失败，弹窗未关闭")

        time.sleep(2)
        allure.attach(self.screenshots_png(), '添加渠道完成', attachment_type=allure.attachment_type.PNG)

    def select_channel_type(self, channel_type):
        """选择渠道类型"""
        # 使用成功的定位策略（根据日志，策略4成功）
        try:
            locator = (By.XPATH, "//div[contains(@class, 'el-dialog')]//div[contains(@class, 'el-select')][1]")
            self.click(locator)
            time.sleep(1)
            
            # 使用成功的选项定位策略（根据日志，span策略成功）
            option_locator = (By.XPATH, f"//span[contains(text(), '{channel_type}')]")
            self.click(option_locator)
            allure.attach(f"成功选择渠道类型: {channel_type}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
        except Exception as e:
            allure.attach(f"渠道类型选择失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '渠道类型选择失败截图', attachment_type=allure.attachment_type.PNG)
            raise

    def select_channel_status(self, channel_status):
        """选择渠道状态"""
        # 使用成功的定位策略（根据日志，策略3成功）
        try:
            locator = (By.XPATH, "//div[contains(@class, 'el-dialog')]//div[contains(@class, 'el-select')][2]")
            self.click(locator)
            time.sleep(1)
            
            # 使用成功的选项定位策略（根据日志，span策略成功）
            option_locator = (By.XPATH, f"//span[contains(text(), '{channel_status}')]")
            self.click(option_locator)
            allure.attach(f"成功选择渠道状态: {channel_status}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
        except Exception as e:
            allure.attach(f"渠道状态选择失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '渠道状态选择失败截图', attachment_type=allure.attachment_type.PNG)
            raise

    def search_channel(self, channel_name):
        """搜索支付渠道 - 使用多种定位策略"""
        self.navigate_to_channel_page()
        
        # 搜索输入框的多种定位策略
        search_input_locators = [
            (By.XPATH, "//input[contains(@placeholder, '渠道名称') or contains(@placeholder, '请输入渠道名称')]"),
            (By.XPATH, "//input[contains(@placeholder, '请输入')]"),
            (By.CSS_SELECTOR, "input[placeholder*='渠道']"),
            (By.CSS_SELECTOR, ".el-input__inner"),
            (By.XPATH, "//div[contains(@class, 'search') or contains(@class, 'query')]//input"),
        ]
        
        # 查询按钮定位（根据HTML结构和测试日志）
        search_button_locators = [
            # 使用成功的策略（从日志看这个成功了）
            (By.XPATH, "//button[contains(@class, 'el-button--primary') and not(contains(text(), '新增'))]"),
            # 通过内部span文本定位
            (By.XPATH, "//button[contains(@class, 'el-button--primary')]//span[contains(text(), '查询')]/parent::button"),
            # 直接通过span文本找父按钮
            (By.XPATH, "//span[contains(text(), '查询')]/ancestor::button[contains(@class, 'el-button--primary')]"),
            # 更精确的定位
            (By.XPATH, "//button[contains(@class, 'el-button--primary') and .//span[contains(text(), '查询')]]"),
        ]
        
        # 尝试输入搜索条件
        input_success = False
        for i, locator in enumerate(search_input_locators, 1):
            try:
                allure.attach(f"尝试搜索输入框定位策略 {i}", "定位策略", attachment_type=allure.attachment_type.TEXT)
                self.send_keys(locator, channel_name)
                allure.attach(f"成功输入搜索条件: {channel_name} (使用策略 {i})", "操作记录", attachment_type=allure.attachment_type.TEXT)
                input_success = True
                break
            except Exception as e:
                allure.attach(f"搜索输入框定位策略 {i} 失败: {str(e)}", "定位失败", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not input_success:
            allure.attach("所有搜索输入框定位策略都失败了", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '搜索输入失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("无法定位搜索输入框")
        
        # 点击查询按钮（使用成功的策略）
        try:
            # 根据测试日志，这个策略是成功的
            locator = (By.XPATH, "//button[contains(@class, 'el-button--primary') and not(contains(text(), '新增'))]")
            self.click(locator)
            allure.attach("成功点击查询按钮", "操作记录", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"查询按钮点击失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '查询按钮失败截图', attachment_type=allure.attachment_type.PNG)
            # 如果查询按钮点击失败，尝试按回车键
            try:
                from selenium.webdriver.common.keys import Keys
                # 在搜索框中按回车
                element = self.location_element(*search_input_locators[0])
                element.send_keys(Keys.ENTER)
                allure.attach("通过回车键执行搜索", "备选操作", attachment_type=allure.attachment_type.TEXT)
            except:
                raise Exception("查询按钮点击失败且回车键备选方案也失败")
        
        time.sleep(2)
        allure.attach(self.screenshots_png(), '搜索结果', attachment_type=allure.attachment_type.PNG)
        
        return self.get_search_results()

    def get_search_results(self):
        """获取搜索结果数量"""
        try:
            # 先尝试获取表格行数
            rows = self.driver.find_elements(*self.table_rows)
            if len(rows) > 0:
                return len(rows)
            
            # 如果没有行，再检查是否显示了"暂无数据"
            try:
                no_data_element = self.driver.find_element(*self.table_no_data)
                if no_data_element.is_displayed():
                    return 0
            except:
                pass
            
            return 0
        except:
            return 0

    def edit_first_channel(self, new_channel_name, new_remark=""):
        """编辑第一个渠道 - 使用多种定位策略"""
        self.navigate_to_channel_page()
        
        # 编辑按钮的多种定位策略（按钮文本是"修 改"，注意中间有空格）
        edit_button_locators = [
            # 主要策略 - 根据前端代码的实际文本
            (By.XPATH, "//button[contains(@class, 'el-button') and contains(.,'修 改')]"),
            # 通过icon属性定位（前端代码中有 icon="edit-pen"）
            (By.XPATH, "//button[contains(@class, 'el-button') and @icon='edit-pen']"),
            # 表格第一行的编辑按钮
            (By.XPATH, "//tbody/tr[1]//button[contains(.,'修 改')]"),
            (By.XPATH, "//table//tr[1]//button[contains(.,'修 改')]"),
            # 更精确的定位 - 通过span文本
            (By.XPATH, "(//span[contains(text(), '修 改')]/ancestor::button)[1]"),
            (By.XPATH, "//tbody/tr[1]//span[contains(text(), '修 改')]/ancestor::button"),
            # 备选策略 - 处理可能的变化
            (By.XPATH, "(//button[contains(text(), '修改') or contains(text(), '修 改')])[1]"),
            (By.XPATH, "(//button[contains(@class, 'el-button') and (.//span[contains(text(), '修 改')] or .//span[contains(text(), '修改')])])[1]"),
        ]
        
        edit_success = False
        for i, locator in enumerate(edit_button_locators, 1):
            try:
                allure.attach(f"尝试编辑按钮定位策略 {i}", "定位策略", attachment_type=allure.attachment_type.TEXT)
                self.click(locator)
                allure.attach(f"成功点击编辑按钮 (使用策略 {i})", "操作记录", attachment_type=allure.attachment_type.TEXT)
                edit_success = True
                break
            except Exception as e:
                allure.attach(f"编辑按钮定位策略 {i} 失败: {str(e)}", "定位失败", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not edit_success:
            allure.attach("所有编辑按钮定位策略都失败了", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '编辑按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("无法定位编辑按钮")
        
        try:
            # 等待弹窗出现
            if not self.wait_for_dialog():
                raise Exception("编辑弹窗未出现")
                
            time.sleep(1)
            
            # 修改渠道名称
            self.send_keys(self.channel_name_input, new_channel_name, is_clear=True)
            allure.attach(f"修改渠道名称为: {new_channel_name}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 修改备注（可选）
            if new_remark:
                self.send_keys(self.remark_textarea, new_remark, is_clear=True)
                allure.attach(f"修改备注为: {new_remark}", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            # 截图
            allure.attach(self.screenshots_png(), '修改渠道信息完成', attachment_type=allure.attachment_type.PNG)
            
            # 点击确认按钮 - 使用多种定位策略
            confirm_button_locators = [
                # 基础策略
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--primary')]"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '确定')]"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '提交')]"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '保存')]"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '确')]"),
                
                # 通过span文本定位父按钮
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//span[contains(text(), '确定')]/parent::button"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//span[contains(text(), '提交')]/parent::button"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//span[contains(text(), '保存')]/parent::button"),
                
                # CSS选择器策略
                (By.CSS_SELECTOR, ".el-dialog .el-button--primary"),
                (By.CSS_SELECTOR, ".el-dialog .el-button.el-button--primary"),
                (By.CSS_SELECTOR, ".el-dialog__wrapper .el-button--primary"),
                
                # 对话框footer区域
                (By.XPATH, "//div[contains(@class, 'el-dialog-footer') or contains(@class, 'dialog-footer')]//button[contains(@class, 'el-button--primary')]"),
                (By.XPATH, "//div[contains(@class, 'el-dialog__footer')]//button[contains(@class, 'el-button--primary')]"),
                
                # 最后的备选策略
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[position()=last()]"),
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[last()]"),
            ]
            
            confirm_success = False
            for i, locator in enumerate(confirm_button_locators, 1):
                try:
                    allure.attach(f"尝试编辑确认按钮定位策略 {i}", "定位策略", attachment_type=allure.attachment_type.TEXT)
                    self.click(locator)
                    allure.attach(f"成功点击确认按钮 (使用策略 {i})", "操作记录", attachment_type=allure.attachment_type.TEXT)
                    confirm_success = True
                    break
                except Exception as e:
                    allure.attach(f"编辑确认按钮定位策略 {i} 失败: {str(e)}", "定位失败", attachment_type=allure.attachment_type.TEXT)
                    continue
            
            if not confirm_success:
                allure.attach("所有编辑确认按钮定位策略都失败了", "错误信息", attachment_type=allure.attachment_type.TEXT)
                allure.attach(self.screenshots_png(), '编辑确认按钮失败截图', attachment_type=allure.attachment_type.PNG)
                raise Exception("无法定位编辑确认按钮")
            
            # 等待弹窗关闭
            if not self.wait_for_dialog_close(timeout=15):
                raise Exception("渠道修改可能失败，弹窗未关闭")
                
            time.sleep(2)
            allure.attach(self.screenshots_png(), '修改渠道完成', attachment_type=allure.attachment_type.PNG)
            
        except Exception as e:
            allure.attach(f"编辑渠道失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '编辑渠道失败截图', attachment_type=allure.attachment_type.PNG)
            raise

    def delete_first_channel(self):
        """删除第一个渠道 - 使用多种定位策略"""
        self.navigate_to_channel_page()
        
        # 删除按钮的多种定位策略（根据前端代码和成功的编辑按钮经验）
        delete_button_locators = [
            # 主要策略 - 根据前端代码的实际文本（类似编辑按钮的成功策略）
            (By.XPATH, "//button[contains(@class, 'el-button') and contains(.,'删除')]"),
            # 通过icon属性定位（前端代码中有 icon="delete"）
            (By.XPATH, "//button[contains(@class, 'el-button') and @icon='delete']"),
            # 表格第一行的删除按钮
            (By.XPATH, "//tbody/tr[1]//button[contains(.,'删除')]"),
            (By.XPATH, "//table//tr[1]//button[contains(.,'删除')]"),
            # 更精确的定位 - 通过span文本
            (By.XPATH, "(//span[contains(text(), '删除')]/ancestor::button)[1]"),
            (By.XPATH, "//tbody/tr[1]//span[contains(text(), '删除')]/ancestor::button"),
            # 备选策略
            (By.XPATH, "(//button[contains(text(), '删除') or contains(@title, '删除')])[1]"),
            (By.XPATH, "(//button[contains(@class, 'el-button') and .//span[contains(text(), '删除')]])[1]"),
            # 危险按钮样式
            (By.XPATH, "//table//tr[1]//button[contains(@class, 'danger')]"),
            (By.XPATH, "//tbody/tr[1]//button[contains(@class, 'el-button--danger')]"),
        ]
        
        delete_success = False
        for i, locator in enumerate(delete_button_locators, 1):
            try:
                allure.attach(f"尝试删除按钮定位策略 {i}", "定位策略", attachment_type=allure.attachment_type.TEXT)
                self.click(locator)
                allure.attach(f"成功点击删除按钮 (使用策略 {i})", "操作记录", attachment_type=allure.attachment_type.TEXT)
                delete_success = True
                break
            except Exception as e:
                allure.attach(f"删除按钮定位策略 {i} 失败: {str(e)}", "定位失败", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not delete_success:
            allure.attach("所有删除按钮定位策略都失败了", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '删除按钮失败截图', attachment_type=allure.attachment_type.PNG)
            raise Exception("无法定位删除按钮")
        
        try:
            time.sleep(1)
            
            # 确认删除 - 使用多种定位策略
            delete_confirm_locators = [
                (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(text(), '确定')]"),
                (By.XPATH, "//span[contains(text(), '确定')]/parent::button"),
                (By.XPATH, "//button[contains(text(), '确认')]"),
                (By.XPATH, "//div[contains(@class, 'el-message-box')]//button[contains(@class, 'el-button--primary')]"),
                (By.CSS_SELECTOR, ".el-message-box .el-button--primary"),
                (By.XPATH, "//div[contains(@class, 'el-popconfirm')]//button[contains(@class, 'el-button--primary')]"),
            ]
            
            confirm_delete_success = False
            for i, locator in enumerate(delete_confirm_locators, 1):
                try:
                    allure.attach(f"尝试删除确认按钮定位策略 {i}", "定位策略", attachment_type=allure.attachment_type.TEXT)
                    self.click(locator)
                    allure.attach(f"成功确认删除 (使用策略 {i})", "操作记录", attachment_type=allure.attachment_type.TEXT)
                    confirm_delete_success = True
                    break
                except Exception as e:
                    allure.attach(f"删除确认按钮定位策略 {i} 失败: {str(e)}", "定位失败", attachment_type=allure.attachment_type.TEXT)
                    continue
            
            if not confirm_delete_success:
                allure.attach("所有删除确认按钮定位策略都失败了", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach("确认删除", "操作记录", attachment_type=allure.attachment_type.TEXT)
            
            time.sleep(2)
            allure.attach(self.screenshots_png(), '删除渠道完成', attachment_type=allure.attachment_type.PNG)
            
        except Exception as e:
            allure.attach(f"删除渠道失败: {str(e)}", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '删除渠道失败截图', attachment_type=allure.attachment_type.PNG)
            raise

    def reset_search(self):
        """重置搜索条件"""
        # 重置按钮定位策略（根据前端HTML结构和国际化文本）
        reset_button_locators = [
            # 主要策略 - 根据前端代码结构
            (By.XPATH, "//button[contains(@class, 'el-button') and contains(.,'重置')]"),
            # 更精确的策略 - 包含图标的按钮
            (By.XPATH, "//button[contains(@class, 'el-button') and @icon='Refresh']"),
            # 通过span文本查找
            (By.XPATH, "//button[contains(@class, 'el-button')]//span[contains(text(), '重置')]/parent::button"),
            (By.XPATH, "//span[contains(text(), '重置')]/ancestor::button[contains(@class, 'el-button')]"),
            # 更通用的策略
            (By.XPATH, "//button[contains(text(), '重置')]"),
            (By.XPATH, "//button[contains(@class, 'el-button') and .//span[contains(text(), '重置')]]"),
            # 表单区域内的重置按钮
            (By.XPATH, "//div[contains(@class, 'el-form-item__content')]//button[contains(.,'重置')]"),
            (By.XPATH, "//el-form-item//button[contains(.,'重置')]"),
        ]
        
        reset_success = False
        for i, locator in enumerate(reset_button_locators, 1):
            try:
                allure.attach(f"尝试重置按钮定位策略 {i}: {locator}", "定位策略", attachment_type=allure.attachment_type.TEXT)
                self.click(locator)
                allure.attach(f"成功点击重置按钮 (使用策略 {i})", "操作记录", attachment_type=allure.attachment_type.TEXT)
                reset_success = True
                break
            except Exception as e:
                allure.attach(f"重置按钮定位策略 {i} 失败: {str(e)}", "定位失败", attachment_type=allure.attachment_type.TEXT)
                continue
        
        if not reset_success:
            allure.attach("所有重置按钮定位策略都失败了", "错误信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(self.screenshots_png(), '重置按钮失败截图', attachment_type=allure.attachment_type.PNG)
            # 如果重置按钮找不到，直接清空搜索框作为备选方案
            try:
                self.send_keys(self.search_input, "", is_clear=True)
                allure.attach("通过清空搜索框实现重置", "备选操作", attachment_type=allure.attachment_type.TEXT)
            except:
                raise Exception("无法定位重置按钮且清空搜索框备选方案也失败")
        
        time.sleep(1)
        allure.attach(self.screenshots_png(), '重置搜索完成', attachment_type=allure.attachment_type.PNG)

    def get_channel_count(self):
        """获取渠道总数"""
        try:
            if self.is_element_present(self.table_no_data):
                return 0
            rows = self.driver.find_elements(*self.table_rows)
            return len(rows)
        except:
            return 0 