#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付渠道测试运行脚本
单独运行支付渠道模块的测试用例
"""

import os
import pytest
import sys
from datetime import datetime

def run_channel_tests():
    """运行支付渠道测试用例"""
    
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置测试报告目录
    report_dir = os.path.join(current_dir, 'report', 'pay_channel')
    os.makedirs(report_dir, exist_ok=True)
    
    # 生成时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 设置pytest参数
    pytest_args = [
        # 测试文件路径
        'testcase/biz/pay/test_channel_flow.py',
        
        # 生成allure报告
        f'--alluredir={report_dir}/allure_results_{timestamp}',
        
        # 详细输出
        '-v',
        
        # 显示测试进度
        '--tb=short',
        
        # 输出实时日志
        '-s',
        
        # 失败时停止（可选，调试时使用）
        # '--maxfail=1',
        
        # 并行执行（如果安装了pytest-xdist）
        # '-n=2',
    ]
    
    print("=" * 60)
    print("🚀 开始执行支付渠道测试用例")
    print("=" * 60)
    print(f"测试文件: testcase/biz/pay/test_channel_flow.py")
    print(f"报告目录: {report_dir}")
    print("=" * 60)
    
    # 运行测试
    result = pytest.main(pytest_args)
    
    # 输出结果
    print("\n" + "=" * 60)
    if result == 0:
        print("✅ 支付渠道测试执行完成 - 全部通过")
    else:
        print("❌ 支付渠道测试执行完成 - 存在失败用例")
    
    print(f"📊 Allure报告已生成到: {report_dir}/allure_results_{timestamp}")
    print("📋 查看报告命令:")
    print(f"   allure serve {report_dir}/allure_results_{timestamp}")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    # 确保当前目录在Python路径中
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # 运行测试
    exit_code = run_channel_tests()
    sys.exit(exit_code) 