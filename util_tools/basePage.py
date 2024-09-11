import os
import time
from datetime import datetime

import pytesseract
from PIL import Image
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from config import setting
from util_tools.handle_data.configParse import ConfigParse
from util_tools.logs_util.recordlog import logs


class BasePage(object):
    """
    封装浏览器的一些操作，对象webDriver里面的一些方法进行二次开发
    此类封装所有的操作，所有页面继承该类
    """

    def __init__(self, driver):
        # 初始化浏览器对象
        self.__driver = driver
        # 初始化显式等待，等待时间从配置中获取
        self.__wait = WebDriverWait(self.__driver, setting.WAIT_TIME)
        # 初始化配置解析对象
        self.conf = ConfigParse()

    def window_max(self):
        """浏览器窗口最大化"""
        # 调用浏览器对象的方法将窗口最大化
        self.__driver.maximize_window()

    def window_full(self):
        """全屏窗口"""
        # 调用浏览器对象的方法将窗口全屏
        self.__driver.fullscreen_window()

    def screenshot(self):
        """浏览器截屏"""
        # 调用浏览器对象的方法截取当前屏幕，并以PNG格式保存
        self.__driver.get_screenshot_as_png()

    def refresh(self):
        """页面刷新"""
        # 调用浏览器对象的方法刷新当前页面
        self.__driver.refresh()

    def scroll_to_button(self):
        """
        使用JavaScript滚动页面到最底部
        :return:
        """
        # 使用JavaScript将页面滚动到最底部
        self.__driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    @property
    def current_url(self):
        """获取当前页面的URL"""
        # 返回当前页面的URL
        return self.__driver.current_url

    @property
    def title(self):
        """获取页面标题"""
        # 返回当前页面的标题
        return self.__driver.title

    def open_url(self, url):
        """打开测试页面"""
        if url.startswith('http') or url.startswith('https'):
            # 如果URL以http或https开头，直接打开该URL
            self.__driver.get(url)
            logs.info(f'打开页面：{url}')
        else:
            # 否则，从配置中获取主机地址，并拼接URL后打开
            new_url = self.conf.get_host('host') + url
            self.__driver.get(new_url)
            logs.info(f'打开页面：{new_url}')

    def get_tag_text(self, locator: tuple):
        """获取页面标签文本内容"""
        try:
            # 定位元素
            element = self.location_element(*locator)
            # 获取元素文本内容
            element_text = element.text
            logs.info(f'获取标签文本内容：{element_text}')
            return element_text
        except Exception as e:
            # 捕获异常并记录日志
            logs.error(f'获取标签文本内容出现异常，{str(e)}')

    @property
    def switch_to(self):
        """切换switch_to"""
        # 返回浏览器对象的switch_to属性，用于切换框架、窗口等
        return self.__driver.switch_to

    def iframe(self, frame):
        """切换到iframe内联框架中"""
        try:
            # 切换到指定的iframe框架中
            self.switch_to.frame(frame)
            logs.info(f'切换到{frame}--iframe内部框架中')
        except:
            # 捕获异常并记录日志
            logs.error('切换iframe框架失败！')

    def switch_to_new_tab(self):
        """浏览器打开新的标签页，切换窗口句柄"""
        try:
            # 获取当前窗口的句柄作为原始窗口
            original_window = self.__driver.window_handles[0]
            # 获取所有窗口的句柄列表
            all_window = self.__driver.window_handles
            new_window = None
            for window in all_window:
                if window != original_window:
                    # 找到不等于原始窗口句柄的新窗口句柄
                    new_window = window
                    break

            if new_window:
                # 切换到新窗口，以便在新窗口上执行后续操作
                self.switch_to.window(new_window)
                logs.info('成功切换到新标签页')
        except TimeoutException:
            # 捕获超时异常并记录日志
            logs.error('等待新标签打开超时')
        except NoSuchElementException:
            # 捕获未找到元素异常并记录日志
            logs.error('未找到新标签页句柄')
        except Exception as e:
            # 捕获其他异常并记录日志
            logs.error(f'切换窗口时发生异常：{str(e)}')

    def switch_to_tab_by_index(self, index):
        """
        当需要切换多个标签页时
        :param index: 标签页的索引，从0开始
        :return:
        """
        try:
            all_window = self.__driver.window_handles  # 获取所有窗口的句柄列表
            if 0 <= index < len(all_window):  # 检查索引是否在有效范围内
                target_window = all_window[index]  # 获取目标窗口句柄
                self.switch_to.window(target_window)  # 切换到目标窗口
                logs.info(f'成功切换到第{index + 1}个标签页')  # 记录切换成功日志
            else:
                logs.error('指定的窗口索引超出范围')  # 记录错误日志
        except Exception as e:
            logs.error(f'切换窗口时发生异常：{str(e)}')  # 记录异常日志

    def exit_iframe(self):
        """退出iframe框架"""
        self.switch_to.default_content()  # 切换到默认内容

    @property
    def alert(self):
        """alert弹框处理"""
        return self.__wait.until(ec.alert_is_present())  # 等待直到页面上出现弹框，存在就返回Alert对象，不存在就返回False

    def alert_confirm(self):
        """点击alert弹框中确定操作"""
        self.alert.accept()  # 点击确定按钮

    def alert_cancel(self):
        """点击alert弹框中取消操作"""
        self.alert.dismiss()  # 点击取消按钮

    def location_element(self, by, value):
        """
        二次封装find_element方法，定位页面元素
        :param by: 定位方式，比如By.ID，By.XPATH
        :param value: 定位表达式
        :return:
        """
        try:
            element = self.__wait.until(ec.presence_of_element_located((by, value)))  # 等待元素出现并返回元素对象
            logs.info(f"找到元素：{by} = {value}")  # 记录找到元素的日志
            return element
        except Exception as e:
            logs.error(f"未找到元素：{by} = {value}")  # 记录未找到元素的错误日志
            raise e

    def location_elements(self, by, value):
        """
        二次封装find_elements方法，定位页面元素列表
        :param by: 定位方式，比如By.ID，By.XPATH
        :param value: 定位表达式
        :return:
        """
        try:
            self.__wait.until(ec.presence_of_all_elements_located((by, value)))  # 等待所有元素出现
            elements = self.__driver.find_elements(by, value)  # 返回元素列表
            logs.info(f"找到元素列表：{by} = {value}")  # 记录找到元素列表的日志
            return elements
        except Exception as e:
            logs.error(f"未找到元素列表：{by} = {value}")  # 记录未找到元素列表的错误日志
            raise e

    def visibility_of_element_located(self, by, value):
        """
        等待元素可见性
        :param by:
        :param value:
        :return:
        """
        try:
            element = self.__wait.until(ec.visibility_of_element_located((by, value)))  # 等待元素可见并返回元素对象
            logs.info(f"找到元素：{by} = {value}")  # 记录找到元素的日志
            return element
        except Exception as e:
            logs.error(f"在设定时间内未找到元素：{by} = {value}")  # 记录未找到元素的错误日志
            raise e

    def click(self, locator: tuple, force=False):
        """
        封装点击操作
        :param locator: （tuple）定位元素信息，等于(By.ID,'j_idt88:j_idt93')
        :param force: 可选参数，表示是否使用强制点击，默认为False
        :return:
        """
        try:
            element = self.location_element(*locator)  # 定位元素
            if not force:
                self.__driver.execute_script("arguments[0].click()", element)  # 执行JavaScript点击操作
            else:
                self.__driver.execute_script("arguments[0].click({force:true})", element)  # 执行JavaScript强制点击操作
            logs.info(f"元素被点击：{locator}")  # 记录点击元素的日志
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")  # 记录无法定位元素的错误日志
            raise e

    def click_actions(self, locator: tuple):
        """
        封装模拟鼠标点击操作
        :param locator: （tuple）定位元素信息，等于(By.ID,'j_idt88:j_idt93')
        :return:
        """
        element = self.visibility_of_element_located(*locator)  # 定位并等待元素可见
        ActionChains(self.__driver).click(element).perform()  # 执行模拟鼠标点击操作

    def send_keys(self, locator: tuple, data, is_clear=False):
        """
        封装输入操作，对send_keys方法进行二次封装
        :param locator: （tuple）定位元素信息，例如(By.ID, 'input_id')
        :param data: 输入的内容
        :param is_clear: （bool）是否在输入前清空输入框，默认为False
        :return:
        """
        try:
            element = self.location_element(*locator)  # 定位元素
            if is_clear:
                element.clear()  # 如果clear_first为True，则清空输入框
                logs.info(f"输入框内容已清空：{locator}")  # 记录清空输入框的日志
            element.send_keys(data)  # 输入内容
            logs.info(f"元素被输入内容：{locator}，输入的内容为：{data}")  # 记录输入内容的日志
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")  # 记录无法定位元素的错误日志
            raise e

    def send_keys_actions(self, locator: tuple, data):
        """
        模拟键盘的输入操作
        :param locator: （tuple）定位元素信息，等于(By.ID,'j_idt88:j_idt93')
        :param data: 输入的内容
        :return:
        """
        try:
            element = self.location_element(*locator)  # 定位元素
            ActionChains(self.__driver).move_to_element(element).click().send_keys(data).perform()  # 执行模拟键盘输入操作
            logs.info(f"元素被输入内容：{locator}，输入的内容为：{data}")  # 记录输入内容的日志
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")  # 记录无法定位元素的错误日志
            raise e

    def selects_by_single_level(self, trigger_locator: tuple, option_text: str):
        """
        封装非标准下拉菜单选择
        :param option_text: 要选择的选项文本
        :param trigger_locator: （tuple）定位下拉菜单触发器的元素
        :return:
        """
        try:
            # 点击触发器以展开下拉菜单
            self.click(trigger_locator)
            time.sleep(1)  # 等待下拉菜单展开

            # 构造定位下拉选项的XPath表达式
            options_xpath = f"//div[contains(@class, 'el-select-dropdown')]//ul/li//*[contains(text(), '{option_text}')]"
            option_locator = (By.XPATH, options_xpath)
            time.sleep(1)  # 等待选项可点击

            # 点击选择指定的选项
            self.click(option_locator)
            logs.info(f'成功选择下拉菜单中名称为"{option_text}"的选项')
        except Exception as e:
            logs.error(f"操作失败：{e}, 无法选择下拉菜单中名称为'{option_text}'的选项")
            raise e

    def selects_by_multi_level(self, trigger_locator: tuple, option_texts: list):
        """
        封装多级下拉菜单选择
        :param trigger_locator: （tuple）定位下拉菜单触发器的元素
        :param option_texts: （list）包含每一级菜单的选项文本
        :return:
        """
        try:
            # 点击触发器以展开下拉菜单
            self.click(trigger_locator)
            time.sleep(1)  # 等待下拉菜单展开

            # 遍历每一级菜单的选项文本
            for i, option_text in enumerate(option_texts):
                if i < len(option_texts) - 1:
                    # 不是最后一个元素，点击旁边的 <i> 标签
                    options_xpath = f'//li[span[text()="{option_text}"]]/preceding-sibling::i'
                else:
                    # 最后一个元素，直接点击它自身
                    options_xpath = f'//li[span[text()="{option_text}"]]'

                option_locator = (By.XPATH, options_xpath)
                time.sleep(1)  # 等待选项可点击

                # 点击选择指定的选项
                self.click(option_locator)
                time.sleep(1)  # 等待下一级菜单展开

            print(f'成功选择下拉菜单中名称为"{option_texts}"的选项')
        except Exception as e:
            print(f"操作失败：{e}, 无法选择下拉菜单中名称为'{option_texts}'的选项")
            raise e

    def enter(self):
        """
        封装键盘回车的操作
        :return:
        """
        try:
            # 执行回车键操作
            ActionChains(self.__driver).send_keys(Keys.ENTER).perform()
            logs.info('按下回车键')
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")
            raise e

    def right_click(self, locator: tuple):
        """
        封装右键点击操作
        :param locator: （tuple）定位页面元素
        :return:
        """
        try:
            # 定位元素
            element = self.location_element(*locator)
            # 执行右键点击操作
            ActionChains(self.__driver).context_click(element).perform()
            logs.info('执行右键点击操作')
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")
            raise e

    def double_click(self, locator: tuple):
        """
        封装双击操作
        :param locator: （tuple）定位页面元素
        :return:
        """
        try:
            # 定位元素
            element = self.location_element(*locator)
            # 执行双击操作
            ActionChains(self.__driver).double_click(element).perform()
            logs.info('执行双击操作')
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")
            raise e

    def mouse_hover_actions(self, locator: tuple):
        """
        封装鼠标悬停展示内容或弹框
        :param locator: （tuple）定位页面元素
        :return:
        """
        try:
            # 定位元素
            move_element = self.location_element(*locator)
            # 执行鼠标悬停操作
            ActionChains(self.__driver).move_to_element(move_element).perform()
            logs.info('鼠标悬停')
        except Exception as e:
            logs.error(f"鼠标悬停出现异常：{e}")
            raise e

    def screenshots(self, image_name):
        """
        封装截图的方法
        :param image_name: 文件名
        :return:
        """
        # 获取当前的时间并格式化
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        # 构造文件名
        file_name = f'{image_name}-{current_time}.png'
        # 构造文件路径
        file_path = os.path.join(setting.FILE_PATH.get('screenshot'), file_name)
        # 截图并保存到指定路径
        self.__driver.get_screenshot_as_file(file_path)

    def screenshots_png(self):
        """
        页面截屏，保存为PNG格式
        :return:
        """
        # 返回页面截图的PNG格式数据
        return self.__driver.get_screenshot_as_png()

    def clear(self, locator: tuple):
        """
        清空文本框内容
        :param locator: 定位方式
        :return:
        """
        try:
            # 定位元素
            element = self.location_element(*locator)
            # 清空文本框内容
            element.clear()
            logs.info('清空文本')
        except NoSuchElementException as e:
            logs.error(f"元素无法定位：{e}")
            raise e

    def ocr_captcha(self, locator: tuple):
        """
        1）定位到图形验证码，保存图片
        2）调用Image去打开图像
        3）调用pytesseract模块进行OCR识别
        :param locator: 定位方法和定位表达式，（tuple）元组
        :return:
        """
        # 定位到图形验证码元素
        captcha_element = self.location_element(*locator)
        # 截取图形验证码并保存图片到指定路径
        captcha_path = setting.FILE_PATH['screenshot'] + '/captcha.png'
        captcha_element.screenshot(captcha_path)
        # 调用Image模块打开图像
        captcha_image = Image.open(captcha_path)
        try:
            # 调用pytesseract进行OCR识别
            captcha_text = pytesseract.image_to_string(captcha_image)
            # 记录识别到的验证码
            logs.info(f'识别到的验证码为：{captcha_text}')
            return captcha_text
        except pytesseract.pytesseract.TesseractNotFoundError:
            # 捕获Tesseract引擎未找到的异常并记录错误日志
            logs.error("找不到tesseract,这是因为pytesseract模块依赖于TesseractOCR引擎来进行图像识别！")

    def is_element_present(self, locator: tuple):
        """判断元素是否存在"""
        try:
            # 使用显式等待判断元素是否存在
            self.__wait.until(ec.presence_of_element_located(*locator))
            return True
        except:
            # 捕获异常并记录错误日志
            logs.error(f'{locator}元素未找到或不存在')
            return False

    def assert_is_element_present(self, locator: tuple):
        """
        断言元素存在
        :param locator: 元素定位表达式
        :return:
        """
        try:
            # 查找元素并断言其是否显示
            element = self.__driver.find_element(*locator)
            assert element.is_displayed(), '元素不存在'
        except NoSuchElementException as e:
            # 捕获元素未找到的异常并记录错误日志
            logs.error(f'元素未找到，{e}')
            raise AssertionError('元素不存在')

    def assert_element_not_visible(self, locator: tuple):
        """
        断言元素不可见或不存在
        :param locator:
        :return:
        """
        try:
            # 使用显式等待判断元素是否不可见
            self.__wait.until(ec.invisibility_of_element_located(locator))
        except TimeoutException:
            # 捕获超时异常并记录错误日志
            logs.error('元素可见')

    def assert_title(self, expect_title):
        """
        断言预期标题文本是否包含在实际文本页面的标题中
        :param expect_title: 预期文本标题
        :return:
        """
        # 断言预期标题是否包含在实际页面标题中
        assert expect_title in self.title

    def assert_element_to_be_clickable(self, locator: tuple):
        """
        断言元素是否可被点击操作
        :param locator: （tuple）元素定位表达式
        :return:
        """
        try:
            # 使用显式等待判断元素是否可点击
            element = self.__wait.until(
                ec.element_to_be_clickable(locator)
            )
            # 断言元素是否启用交互
            assert element.is_enabled(), "元素未启用交互"
            logs.info('断言结果：元素是可点击的，并且可以进行交互')
            # 点击元素
            element.click()
        except Exception as e:
            # 捕获异常并记录错误日志
            logs.error(f"发生错误: {e}")

    def assert_alert_present(self):
        """
        断言页面是否出现alert弹框
        :return:
        """
        try:
            # 使用显式等待判断alert是否存在
            alert = self.__wait.until(ec.alert_is_present())
            return True
        except TimeoutException:
            # 捕获超时异常并返回False
            return False

    def assert_is_url_present(self):
        try:
            # 获取当前URL
            current_url = self.current_url
            # 预期登录后的URL
            expected_url_after_login = 'http://localhost:8888/#/home'
            # 断言当前URL是否与预期URL不一致
            assert current_url != expected_url_after_login, f"Expected URL: {expected_url_after_login}, but got: {current_url}"
        except Exception as e:
            # 捕获异常并记录错误日志
            logs.error(f'URL未找到，{e}')
            raise AssertionError('URL不存在')

    def assert_element_text_contains(self, expected_text: str):
        """
        断言元素文本内容是否与预期文本一致
        :param expected_text: 预期文本内容
        :return:
        """
        try:
            # 定位成功消息的元素
            success_message_locator = (
                By.XPATH, "//div[contains(@class, 'el-message--success')]//p[contains(@class, 'el-message__content')]")
            # 使用显式等待确保元素可见
            element = self.visibility_of_element_located(*success_message_locator)
            # 获取实际文本内容
            actual_text = element.text
            # 断言实际文本内容是否包含预期文本
            assert expected_text in actual_text, f"Expected text to contain: {expected_text}, but got: {actual_text}"
            logs.info(f"断言结果：元素文本内容包含预期文本，实际文本内容为：{actual_text}")
        except NoSuchElementException as e:
            # 捕获元素未找到的异常并记录错误日志
            logs.error(f"元素未找到，{e}")
            raise AssertionError('元素不存在')
        except AssertionError as e:
            # 捕获断言失败的异常并记录错误日志
            logs.error(f"文本断言失败，{e}")
            raise e

    def visibility_of_element_located(self, by, value):
        """
        等待元素可见性
        :param by:
        :param value:
        :return:
        """
        try:
            # 使用显式等待判断元素是否可见
            element = self.__wait.until(ec.visibility_of_element_located((by, value)))
            logs.info(f"找到元素：{by} = {value}")
            return element
        except Exception as e:
            # 捕获异常并记录错误日志
            logs.error(f"在设定时间内未找到元素：{by} = {value}")
            raise e