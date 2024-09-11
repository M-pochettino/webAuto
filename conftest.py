import time

import pytest

from config.setting import is_dd_msg
from util_tools.connectMysql import ConnectMysql
from util_tools.dingRebot import send_dd_msg
from util_tools.logs_util.recordlog import logs


# 定义一个pytest fixture，作用范围是整个测试会话，且自动使用
@pytest.fixture(scope='session', autouse=True)
def data_cleaning():
    """
    测试结束后清理测试数据
    """
    # 创建一个数据库连接实例
    conn = ConnectMysql()
    # 使用yield关键字，分隔fixture的准备和清理阶段
    yield
    # 清理阶段代码，执行测试数据清理的操作
    logs.info('正在清理测试数据...')
    # 定义要执行的SQL删除语句
    sql = "delete from sys_user where phone = '17689876523'"
    # 执行SQL删除操作
    conn.delete(sql)


# 定义pytest钩子函数，用于在测试会话结束时自动执行
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    pytest预定义的钩子函数，用于自动收集测试结果
    """
    # 从terminalreporter对象中获取已收集的测试用例总数
    total = terminalreporter._numcollected
    # 从terminalreporter对象中获取通过的测试用例数量
    passed = len(terminalreporter.stats.get('passed', []))
    # 从terminalreporter对象中获取失败的测试用例数量
    failed = len(terminalreporter.stats.get('failed', []))
    # 从terminalreporter对象中获取错误的测试用例数量
    error = len(terminalreporter.stats.get('error', []))
    # 从terminalreporter对象中获取被跳过的测试用例数量
    skipped = len(terminalreporter.stats.get('skipped', []))
    # 计算测试会话的持续时间
    duration = round(time.time() - terminalreporter._sessionstarttime, 2)
    # 构建测试结果的摘要信息
    summary = f"""
    自动化测试结果，通知如下，具体执行结果如下：
    测试用例总数：{total}
    测试通过数：{passed}
    测试失败数：{failed}
    错误数量：{error}
    跳过执行数量：{skipped}
    执行总时长：{duration}s
    """
    # 打印测试结果摘要
    print(summary)
    # 如果需要发送钉钉消息，则发送摘要信息
    if is_dd_msg:
        send_dd_msg(summary)
