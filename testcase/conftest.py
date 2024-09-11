import allure
import pytest
from selenium import webdriver

from config.setting import browser_type, WAIT_TIME
from pageObject.login_page.login_page import LoginPage
from util_tools.logs_util.recordlog import logs


# 使用 pytest.fixture 装饰器来定义一个自动应用的fixture，所有测试用例执行前后都会执行此代码块
@pytest.fixture(autouse=True)
def log_outputs():
    # 在测试用例开始执行前记录一条日志信息
    logs.info('-------测试用例开始执行-------')
    yield  # yield 之前的代码在测试用例执行前运行
    # 在测试用例执行完毕后记录一条日志信息
    logs.info('-------测试用例执行完毕-------')
    # yield 之后的代码在测试用例执行后运行


# 初始化浏览器驱动程序的函数
def init_driver():
    # 定义一个映射，关联浏览器名称与其对应的 WebDriver 类
    browser_mapping = {
        'Chrome': webdriver.Chrome,  # 谷歌浏览器的 WebDriver
        'Edge': webdriver.Edge,  # Edge 浏览器的 WebDriver
        'Firefox': webdriver.Firefox  # 火狐浏览器的 WebDriver
    }
    # 判断全局变量 browser_type 是否在映射中
    if browser_type.capitalize() in browser_mapping:
        # 返回对应的 WebDriver 实例，用于启动相应的浏览器
        return browser_mapping.get(browser_type.capitalize())()


# 定义一个用于测试类级别的 fixture，用于初始化并提供浏览器驱动
@pytest.fixture(scope='class')
def get_driver():
    # 调用 init_driver 函数，初始化一个浏览器驱动实例
    driver = init_driver()
    # 设置一个全局的隐式等待时间，等待页面元素的加载
    driver.implicitly_wait(WAIT_TIME)
    # 最大化浏览器窗口（注释掉的代码行表示该操作可能是可选的）
    # driver.maximize_window()
    # 使用 yield 将 driver 实例提供给测试类，在测试类执行完毕后执行后续清理操作
    yield driver
    # 关闭浏览器并退出 WebDriver 实例，释放资源
    driver.quit()


# 定义一个用于登录状态的 fixture，在类级别使用
@pytest.fixture(scope='class')
def login_driver(get_driver):
    # 从 get_driver fixture 中获取浏览器驱动实例
    driver = get_driver
    # 初始化登录页面对象
    login_page = LoginPage(driver)
    # 执行登录操作，传入用户名和密码
    login_page.login('', '')
    # 返回登录后的浏览器驱动实例
    return driver


# 定义一个用于未登录状态的 fixture，应用于单个测试用例
@pytest.fixture()
def not_login_driver():
    global driver  # 声明全局变量 driver，用于在整个模块中访问
    driver = init_driver()  # 调用初始化驱动程序的函数，返回一个 WebDriver 实例
    driver.implicitly_wait(WAIT_TIME)  # 设置隐式等待时间，确保在查找元素时的超时等待
    driver.maximize_window()  # 最大化当前浏览器窗口，以便能够显示更多内容或确保一致的测试环境
    yield driver  # 将 driver 传递给测试用例，在测试执行完成后继续执行后续清理操作
    driver.quit()  # 关闭浏览器并退出 WebDriver 实例，释放资源


# 定义一个 pytest 钩子函数，用于对失败的测试用例进行截图
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    # 执行测试用例并获取结果
    outcome = yield
    result = outcome.get_result()  # 获取测试结果对象
    # 检查测试用例是否在执行阶段（'call'），确保只在该阶段进行处理
    if result.when == 'call':
        # 检查是否有被标记为预期失败的情况
        xfail = hasattr(result, 'wasxfail')
        # 如果测试用例失败且不是预期的失败（即未被 xfail 标记），则进行截图操作
        if (result.skipped and xfail) or (result.failed and not xfail):
            driver = item.funcargs.get('driver')  # 从测试用例的参数中获取 driver 实例
            if driver:  # 如果获取到 driver 实例
                with allure.step('测试用例失败截图'):  # 创建一个 Allure 步骤，用于记录失败截图
                    # 附加当前页面的截图到 Allure 报告中
                    allure.attach(driver.get_screenshot_as_png(), '失败截图',
                                  attachment_type=allure.attachment_type.PNG)
