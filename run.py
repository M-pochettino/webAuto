import os
import shutil

import pytest

# 当脚本作为主程序运行时，执行以下代码
if __name__ == '__main__':
    # 调用pytest的main函数，启动pytest测试
    pytest.main()
    # 将环境配置文件复制到报告目录
    shutil.copy('./environment.xml', './report/temp')
    # 使用系统命令启动Allure报告服务，显示测试报告
    os.system('allure serve ./report/temp')

