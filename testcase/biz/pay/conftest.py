import time
import pytest

from util_tools.connectMysql import ConnectMysql
from util_tools.logs_util.recordlog import logs


@pytest.fixture(scope='session', autouse=True)
def pay_data_cleaning():
    """
    支付模块测试结束后清理测试数据
    """
    # 创建一个数据库连接实例
    conn = ConnectMysql()
    # 使用yield关键字，分隔fixture的准备和清理阶段
    yield
    # 清理阶段代码，执行测试数据清理的操作
    logs.info('正在清理支付渠道测试数据...')
    
    try:
        # 清理测试渠道数据
        sql_list = [
            "DELETE FROM pay_channel WHERE channel_name LIKE '%测试%'",
            "DELETE FROM pay_channel WHERE channel_name LIKE '%微信支付渠道%'",
            "DELETE FROM pay_channel WHERE channel_name LIKE '%支付宝渠道%'",
            "DELETE FROM pay_channel WHERE channel_name LIKE '%修改后的测试渠道%'",
            "DELETE FROM pay_channel WHERE app_id LIKE 'TEST_APP_%'"
        ]
        
        # 执行清理SQL
        for sql in sql_list:
            try:
                conn.delete(sql)
                logs.info(f'执行清理SQL: {sql}')
            except Exception as e:
                logs.warning(f'清理数据异常: {str(e)}, SQL: {sql}')
                
    except Exception as e:
        logs.error(f'支付渠道数据清理失败: {str(e)}')
    
    logs.info('支付渠道测试数据清理完成') 