import os
import shutil
import pytest

# 当脚本作为主程序运行时，执行以下代码
if __name__ == '__main__':
    print("=" * 80)
    print("开始执行系统管理流程测试")
    print("测试顺序：角色管理 -> 用户管理 -> 文件管理")
    print("注意：测试将连续执行，不会重新登录")
    print("=" * 80)
    
    # 检查测试数据目录
    test_data_dir = os.path.join(os.getcwd(), 'testcase', 'test_data', 'image')
    if os.path.exists(test_data_dir):
        image_files = [f for f in os.listdir(test_data_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        print(f"找到 {len(image_files)} 个测试图片文件用于文件上传测试")
    
    # 运行系统流程测试 - 连续执行角色、用户、文件管理测试
    # 测试方法按test_01_, test_02_等命名，pytest会按字母顺序自动执行
    pytest.main([
        'testcase/system/test_system_flow.py',  # 执行完整的系统流程测试
        '-v',  # 显示详细输出
        '-s',  # 不捕获输出，显示print信息
        '--tb=short',  # 简化traceback
        '--alluredir=./report/temp'  # 生成allure报告
    ])
    
    print("\n" + "=" * 80)
    print("系统管理流程测试执行完成")
    print("测试包含以下步骤：")
    print("1. 角色添加")
    print("2. 岗位添加") 
    print("3. 用户导入")
    print("4. 用户添加")
    print("5. 用户修改")
    print("6. 用户状态变更")
    print("7. 用户查询")
    print("8. 文件上传（批量上传所有图片文件）")
    print("9. 用户删除")
    print("=" * 80)
    
    # 确保报告目录存在
    os.makedirs('./report/temp', exist_ok=True)
    # 将环境配置文件复制到报告目录
    if os.path.exists('./environment.xml'):
        shutil.copy('./environment.xml', './report/temp')
    
    # 使用系统命令启动Allure报告服务，显示测试报告
    print("\n正在生成并打开测试报告...")
    os.system('allure serve ./report/temp')

