import os
import shutil

import pytest

# 当脚本作为主程序运行时，执行以下代码
if __name__ == '__main__':
    # 运行系统设置测试，其中包含角色数据准备和用户管理功能测试
    # 这样确保在同一个浏览器会话中完成所有测试，避免重复登录
    pytest.main([
        'testcase/system/test_role_setup.py',  # 执行角色设置和用户管理集成测试
        '-v'  # 显示详细输出
    ])
    # 确保报告目录存在
    os.makedirs('./report/temp', exist_ok=True)
    # 将环境配置文件复制到报告目录
    shutil.copy('./environment.xml', './report/temp')
    # 使用系统命令启动Allure报告服务，显示测试报告
    os.system('allure serve ./report/temp')

