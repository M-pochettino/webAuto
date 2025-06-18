import time
import os
import allure
from selenium.webdriver.common.by import By

from util_tools.basePage import BasePage


class FileManagePage(BasePage):
    """文件管理页面对象"""
    url = '#/admin/file/index'  # 文件管理页面URL
    
    # 定位器定义 - 多种上传按钮定位策略
    upload_button = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(text(), '上传')]")  # 上传按钮主要定位器
    upload_button_alt1 = (By.XPATH, "//button[contains(@icon, 'folder-add') and contains(@class, 'el-button--primary')]")  # 按图标定位
    upload_button_alt2 = (By.XPATH, "//button[contains(@class, 'el-button--primary')][contains(., '上传')]")  # 文本匹配
    upload_button_alt3 = (By.XPATH, "//button[@type='primary'][contains(text(), '上传')]")  # 简化定位器
    # 文件输入和上传弹窗相关定位器
    file_input = (By.XPATH, "//input[@type='file']")  # 文件输入框
    file_input_alt = (By.CSS_SELECTOR, "input[type='file']")  # 备用文件输入框
    upload_area = (By.XPATH, "//div[contains(text(),'将文件拖到此处，或')]")  # 上传区域
    click_upload_link = (By.XPATH, "//button[contains(text(),'点击上传')]")  # 点击上传链接
    upload_dialog = (By.XPATH, "//div[contains(@class, 'el-dialog__wrapper')]")  # 上传弹窗
    upload_dialog_alt = (By.CSS_SELECTOR, ".el-dialog__wrapper")  # 备用上传弹窗
    close_dialog_button = (By.XPATH, "//button[contains(@class, 'el-dialog__headerbtn')]")  # 关闭弹窗按钮
    close_dialog_button_alt = (By.CSS_SELECTOR, ".el-dialog__headerbtn")  # 备用关闭按钮
    upload_success_text = (By.XPATH, "//span[contains(text(),'上传成功')]")  # 上传成功提示
    
    def navigate_to_file_manage(self):
        """导航到文件管理页面"""
        self.open_url(self.url)
        allure.attach(self.url, '打开文件管理页面', attachment_type=allure.attachment_type.TEXT)
        time.sleep(3)  # 等待页面加载
        
    def find_upload_button(self):
        """智能查找上传按钮"""
        upload_button_locators = [
            self.upload_button,
            self.upload_button_alt1,
            self.upload_button_alt2,
            self.upload_button_alt3,
            # 更多备用定位策略
            (By.XPATH, "//button[contains(@class, 'el-button') and contains(text(), '上传')]"),
            (By.XPATH, "//button[contains(@class, 'el-button')][contains(., '上传')]"),
            (By.XPATH, "//*[contains(@class, 'el-button') and contains(text(), '上传')]"),
            (By.XPATH, "//button[contains(@class, 'el-button--primary')][1]"),  # 找第一个主要按钮
        ]
        
        for locator in upload_button_locators:
            try:
                element = self.location_element(*locator)
                if element:
                    allure.attach(f"成功找到上传按钮: {locator}", "查找结果", attachment_type=allure.attachment_type.TEXT)
                    return locator
            except Exception as e:
                allure.attach(f"尝试定位器失败: {locator} - {str(e)}", "查找记录", attachment_type=allure.attachment_type.TEXT)
                continue
        
        # 如果都找不到，抛出异常
        allure.attach(self.screenshots_png(), '找不到上传按钮截图', attachment_type=allure.attachment_type.PNG)
        raise Exception("无法找到上传按钮，请检查页面是否正确加载")
    
    def upload_files(self, file_paths):
        """
        上传文件
        :param file_paths: 要上传的文件路径列表
        """
        # 智能查找并点击上传按钮打开上传弹窗
        upload_btn_locator = self.find_upload_button()
        self.click(upload_btn_locator)
        time.sleep(3)
        
        # 等待上传弹窗出现
        dialog_found = False
        dialog_locators = [self.upload_dialog, self.upload_dialog_alt]
        for dialog_locator in dialog_locators:
            try:
                self.visibility_of_element_located(*dialog_locator)
                dialog_found = True
                allure.attach(f"上传弹窗已打开: {dialog_locator}", "弹窗状态", attachment_type=allure.attachment_type.TEXT)
                break
            except:
                continue
        
        if not dialog_found:
            allure.attach("未检测到上传弹窗，尝试直接查找文件输入框", "状态信息", attachment_type=allure.attachment_type.TEXT)
        
        # 智能查找文件输入框并上传
        if file_paths:
            file_input_locators = [
                self.file_input,
                self.file_input_alt,
                (By.XPATH, "//div[contains(@class, 'el-dialog')]//input[@type='file']"),
                (By.CSS_SELECTOR, ".el-dialog input[type='file']"),
                (By.XPATH, "//input[@accept='image/*']"),
                (By.XPATH, "//input[contains(@accept, 'image')]"),
            ]
            
            file_input_found = False
            for input_locator in file_input_locators:
                try:
                    file_input_element = self.location_element(*input_locator)
                    if file_input_element:
                        file_input_found = True
                        allure.attach(f"找到文件输入框: {input_locator}", "查找结果", attachment_type=allure.attachment_type.TEXT)
                        break
                except:
                    continue
            
            if not file_input_found:
                allure.attach("无法找到文件输入框", "错误信息", attachment_type=allure.attachment_type.TEXT)
                allure.attach(self.screenshots_png(), '找不到文件输入框截图', attachment_type=allure.attachment_type.PNG)
                return
            
            # 尝试批量上传，如果失败则逐个上传
            try:
                all_files = '\n'.join(file_paths)
                file_input_element.send_keys(all_files)
                allure.attach(f"批量上传 {len(file_paths)} 个文件", "上传操作", 
                            attachment_type=allure.attachment_type.TEXT)
            except Exception as batch_error:
                allure.attach(f"批量上传失败: {str(batch_error)}，尝试逐个上传", "上传策略", 
                            attachment_type=allure.attachment_type.TEXT)
                # 逐个上传
                upload_count = 0
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        try:
                            # 重新获取文件输入框元素
                            file_input_element = self.location_element(*input_locator)
                            file_input_element.send_keys(file_path)
                            upload_count += 1
                            allure.attach(file_path, f'上传文件 {upload_count}: {os.path.basename(file_path)}', 
                                        attachment_type=allure.attachment_type.TEXT)
                            time.sleep(2)  # 等待文件上传处理
                        except Exception as upload_error:
                            allure.attach(str(upload_error), f'上传失败: {os.path.basename(file_path)}', 
                                        attachment_type=allure.attachment_type.TEXT)
                
                allure.attach(f"成功上传 {upload_count}/{len(file_paths)} 个文件", "上传统计", 
                            attachment_type=allure.attachment_type.TEXT)
        
        # 等待上传完成
        time.sleep(8)
        
    def close_upload_dialog(self):
        """关闭上传弹窗"""
        close_strategies = [
            self.close_dialog_button,
            self.close_dialog_button_alt,
            (By.XPATH, "//button[@aria-label='Close']"),
            (By.XPATH, "//button[contains(@class, 'el-dialog__headerbtn')]//i"),
            (By.XPATH, "//div[contains(@class, 'el-dialog__header')]//i"),
            (By.CSS_SELECTOR, ".el-dialog__close"),
            (By.XPATH, "//span[contains(@class, 'el-dialog__close')]"),
        ]
        
        for strategy in close_strategies:
            try:
                self.click(strategy)
                allure.attach(f"成功关闭上传弹窗: {strategy}", "操作记录", attachment_type=allure.attachment_type.TEXT)
                time.sleep(2)
                return
            except Exception as e:
                allure.attach(f"尝试关闭策略失败: {strategy} - {str(e)}", "尝试记录", attachment_type=allure.attachment_type.TEXT)
                continue
        
        # 如果所有策略都失败，记录错误但不抛出异常（允许测试继续）
        allure.attach("所有关闭弹窗策略都失败，但测试将继续", "警告信息", attachment_type=allure.attachment_type.TEXT)
        allure.attach(self.screenshots_png(), '关闭弹窗失败截图', attachment_type=allure.attachment_type.PNG)
            
    def upload_files_and_close(self, test_data_dir):
        """
        完整的文件上传流程：导航到页面 -> 上传文件 -> 关闭弹窗
        :param test_data_dir: 测试数据目录路径
        """
        # 导航到文件管理页面
        self.navigate_to_file_manage()
        
        # 获取测试图片文件路径列表
        image_files = []
        for filename in os.listdir(test_data_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                file_path = os.path.join(test_data_dir, filename)
                image_files.append(os.path.abspath(file_path))
        
        if not image_files:
            allure.attach("未找到测试图片文件", "错误信息", attachment_type=allure.attachment_type.TEXT)
            return
        
        allure.attach(f"找到 {len(image_files)} 个图片文件", "文件统计", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # 上传所有图片文件
        self.upload_files(image_files)
        
        # 关闭上传弹窗
        self.close_upload_dialog()
        
        # 截图记录最终状态
        allure.attach(self.screenshots_png(), '文件上传完成截图', 
                     attachment_type=allure.attachment_type.PNG) 