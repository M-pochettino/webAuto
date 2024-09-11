import os
import sys

# 获取当前脚本所在目录的上级目录，即项目根目录，并将该目录添加到Python模块搜索路径中
DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_PATH)
# 设置隐式等待时间，默认为10秒，用于等待元素出现等操作
WAIT_TIME = 10
# 设置浏览器类型为Chrome
browser_type = 'chrome'
# 钉钉机器人相关配置
# 钉钉机器人密钥（用于身份验证）
secret = "SECb163daa45904540212492d8ad7bf7c3ce428fae5211c2e94b1f0926be0778191"
# 钉钉机器人Webhook URL（用于发送消息）
webhook = ("https://oapi.dingtalk.com/robot/send?access_token"
           "=df849617e1f9593fd9c31f75ce4fdf2fea8fec39c7b714a65f20413444f5cea5")
# 设置是否发送钉钉群消息的开关
is_dd_msg = False
# 定义文件路径字典
# 日志文件的存储路径
FILE_PATH = {
    'log': os.path.join(DIR_PATH, 'log'),
    # 截图文件的存储路径
    'screenshot': os.path.join(DIR_PATH, 'screenshot'),
    # 配置文件的路径
    'ini': os.path.join(DIR_PATH, 'config', 'config.ini')
}
