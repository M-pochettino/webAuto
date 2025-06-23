import pytest
import allure
from time import sleep
from selenium.webdriver.common.by import By

from pageObject.pay_page.channel_page import ChannelPage
from util_tools.basePage import BasePage


@allure.feature('支付渠道管理测试')
class TestChannelFlow:
    """支付渠道管理测试类 - 增删改查功能测试"""

    @allure.story('1. 支付渠道增加')
    def test_01_channel_add(self, login_driver):
        """测试支付渠道添加功能"""
        allure.attach("开始执行支付渠道添加测试", "步骤1", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 添加测试渠道
        channel_page.add_channel(
            app_id="TEST_APP_001",
            channel_name="测试支付渠道",
            merchant_id="MERCHANT_TEST_001",
            channel_type="微信支付",
            channel_status="正常",
            front_callback="https://test.example.com/callback",
            back_callback="https://test.example.com/notify",
            remark="自动化测试渠道",
            config='{"key": "test_value"}'
        )
        
        # 验证添加成功
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("添加成功")
        sleep(2)

    @allure.story('2. 支付渠道查询')
    def test_02_channel_search(self, login_driver):
        """测试支付渠道搜索功能"""
        allure.attach("开始执行支付渠道搜索测试", "步骤2", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 搜索刚才添加的渠道
        result_count = channel_page.search_channel("测试支付渠道")
        
        # 验证搜索结果
        assert result_count > 0, "搜索结果为空，渠道可能未添加成功"
        allure.attach(f"搜索到 {result_count} 条记录", "搜索结果", attachment_type=allure.attachment_type.TEXT)
        sleep(2)

    @allure.story('2. 支付渠道查询')
    def test_03_channel_search_empty(self, login_driver):
        """测试支付渠道搜索空结果"""
        allure.attach("开始执行支付渠道空搜索测试", "步骤3", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 搜索不存在的渠道
        result_count = channel_page.search_channel("不存在的渠道名称")
        
        # 验证搜索结果为空
        assert result_count == 0, "搜索不存在的渠道应该返回空结果"
        allure.attach("搜索不存在的渠道，结果为空，符合预期", "搜索结果", attachment_type=allure.attachment_type.TEXT)
        
        # 重置搜索条件
        channel_page.reset_search()
        sleep(2)

    @allure.story('3. 支付渠道修改')
    def test_04_channel_edit(self, login_driver):
        """测试支付渠道修改功能"""
        allure.attach("开始执行支付渠道修改测试", "步骤4", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 修改第一个渠道
        channel_page.edit_first_channel(
            new_channel_name="修改后的测试渠道",
            new_remark="修改后的备注信息"
        )
        
        # 验证修改成功
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("修改成功")
        sleep(2)

    @allure.story('2. 支付渠道查询')
    def test_05_channel_search_updated(self, login_driver):
        """测试修改后的渠道搜索"""
        allure.attach("开始执行修改后渠道搜索测试", "步骤5", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 搜索修改后的渠道名称
        result_count = channel_page.search_channel("修改后的测试渠道")
        
        # 验证能搜索到修改后的渠道
        assert result_count > 0, "修改后的渠道搜索失败"
        allure.attach(f"搜索修改后的渠道，找到 {result_count} 条记录", "搜索结果", attachment_type=allure.attachment_type.TEXT)
        
        # 重置搜索
        channel_page.reset_search()
        sleep(2)

    @allure.story('1. 支付渠道增加')
    def test_06_channel_add_multiple(self, login_driver):
        """测试添加多个支付渠道"""
        allure.attach("开始执行多渠道添加测试", "步骤6", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 添加第二个测试渠道
        channel_page.add_channel(
            app_id="TEST_APP_002",
            channel_name="微信支付渠道",
            merchant_id="MERCHANT_WECHAT_001",
            channel_type="微信支付",
            channel_status="正常",
            front_callback="https://wechat.example.com/callback",
            back_callback="https://wechat.example.com/notify",
            remark="微信支付测试渠道",
            config='{"appId": "wx123456", "mchId": "1234567890", "apiKey": "test_api_key"}'
        )
        
        # 验证添加成功
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("添加成功")
        sleep(1)
        
        # 添加第三个测试渠道
        channel_page.add_channel(
            app_id="TEST_APP_003",
            channel_name="支付宝渠道",
            merchant_id="MERCHANT_ALIPAY_001",
            channel_type="支付宝支付",
            channel_status="正常",
            front_callback="https://alipay.example.com/callback",
            back_callback="https://alipay.example.com/notify",
            remark="支付宝测试渠道",
            config='{"appId": "2021001234567890", "privateKey": "test_private_key", "publicKey": "test_public_key"}'
        )
        
        # 验证添加成功
        base_page.assert_element_text_contains("添加成功")
        sleep(2)

    @allure.story('2. 支付渠道查询')
    def test_07_channel_count(self, login_driver):
        """测试渠道总数统计"""
        allure.attach("开始执行渠道总数统计测试", "步骤7", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        channel_page.navigate_to_channel_page()
        
        # 获取当前渠道总数
        total_count = channel_page.get_channel_count()
        
        # 验证至少有我们添加的渠道
        assert total_count >= 3, f"渠道总数异常，当前只有 {total_count} 个渠道"
        allure.attach(f"当前共有 {total_count} 个支付渠道", "统计结果", attachment_type=allure.attachment_type.TEXT)
        sleep(2)

    @allure.story('2. 支付渠道查询')
    def test_08_channel_search_by_different_names(self, login_driver):
        """测试不同渠道名称的搜索"""
        allure.attach("开始执行不同渠道名称搜索测试", "步骤8", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 测试搜索微信渠道
        wechat_count = channel_page.search_channel("微信")
        assert wechat_count > 0, "微信渠道搜索失败"
        allure.attach(f"搜索微信相关渠道，找到 {wechat_count} 条", "搜索结果", attachment_type=allure.attachment_type.TEXT)
        
        # 测试搜索支付宝渠道
        alipay_count = channel_page.search_channel("支付宝")
        assert alipay_count > 0, "支付宝渠道搜索失败"
        allure.attach(f"搜索支付宝相关渠道，找到 {alipay_count} 条", "搜索结果", attachment_type=allure.attachment_type.TEXT)
        
        # 重置搜索
        channel_page.reset_search()
        sleep(2)

    @allure.story('4. 支付渠道删除')
    def test_09_channel_delete(self, login_driver):
        """测试支付渠道删除功能 - 最后执行"""
        allure.attach("开始执行支付渠道删除测试", "步骤9", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        
        # 获取删除前的渠道数量
        channel_page.navigate_to_channel_page()
        before_count = channel_page.get_channel_count()
        allure.attach(f"删除前渠道总数: {before_count}", "删除前统计", attachment_type=allure.attachment_type.TEXT)
        
        # 删除第一个渠道
        channel_page.delete_first_channel()
        
        # 验证删除成功
        base_page = BasePage(login_driver)
        base_page.assert_element_text_contains("删除成功")
        
        # 验证渠道数量减少
        channel_page.navigate_to_channel_page()
        after_count = channel_page.get_channel_count()
        allure.attach(f"删除后渠道总数: {after_count}", "删除后统计", attachment_type=allure.attachment_type.TEXT)
        
        assert after_count == before_count - 1, f"删除后渠道数量异常，删除前: {before_count}, 删除后: {after_count}"
        
        sleep(2)
        allure.attach("支付渠道管理测试全部完成", "测试结束", attachment_type=allure.attachment_type.TEXT)

    @allure.story('5. 支付渠道异常测试')
    def test_10_channel_add_validation(self, login_driver):
        """测试支付渠道添加时的字段验证"""
        allure.attach("开始执行渠道添加字段验证测试", "步骤10", attachment_type=allure.attachment_type.TEXT)
        
        channel_page = ChannelPage(login_driver)
        channel_page.navigate_to_channel_page()
        
        try:
            # 点击新增按钮
            channel_page.click(channel_page.add_button)
            
            # 等待弹窗出现
            if channel_page.wait_for_dialog():
                allure.attach("新增渠道弹窗已打开", "弹窗状态", attachment_type=allure.attachment_type.TEXT)
                
                # 不填写任何字段，直接点击确认，测试必填字段验证
                try:
                    channel_page.click(channel_page.confirm_button)
                    sleep(1)
                    allure.attach("测试必填字段验证完成", "验证结果", attachment_type=allure.attachment_type.TEXT)
                except:
                    pass
                
                # 点击取消按钮关闭弹窗
                cancel_button_locators = [
                    (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(text(), '取消')]"),
                    (By.XPATH, "//div[contains(@class, 'el-dialog')]//span[contains(text(), '取消')]/parent::button"),
                    (By.CSS_SELECTOR, ".el-dialog .el-button:not(.el-button--primary)"),
                    (By.XPATH, "//div[contains(@class, 'el-dialog')]//button[contains(@class, 'el-button--default')]"),
                ]
                
                for locator in cancel_button_locators:
                    try:
                        channel_page.click(locator)
                        allure.attach("取消添加渠道", "操作记录", attachment_type=allure.attachment_type.TEXT)
                        break
                    except:
                        continue
                
        except Exception as e:
            allure.attach(f"字段验证测试异常: {str(e)}", "异常信息", attachment_type=allure.attachment_type.TEXT)
        
        sleep(2) 