import configparser

from config.setting import FILE_PATH
from util_tools.logs_util.recordlog import logs


# 定义一个用于解析 .ini 配置文件的类
class ConfigParse:
    """
    解析.ini配置文件
    """

    # 类的初始化方法，接受一个可选的配置文件路径参数
    def __init__(self, file_path=FILE_PATH['ini']):
        # 创建一个 ConfigParser 实例，用于读取和解析配置文件
        self.config = configparser.ConfigParser()
        # 将传入的文件路径保存为实例属性
        self.file_path = file_path
        # 调用读取配置文件的方法，初始化时即加载配置文件内容
        self.read_config()

    # 定义一个方法用于读取配置文件
    def read_config(self):
        # 使用 configparser 的 read 方法读取指定路径的配置文件，并指定编码为 utf-8
        self.config.read(self.file_path, encoding='utf-8')

    # 定义一个方法获取指定 section 和 option 的值
    def get_value(self, section, option):
        try:
            # 尝试从配置文件中获取指定 section 和 option 对应的值
            value = self.config.get(section, option)
            # 返回获取到的值
            return value
        except Exception as e:
            # 如果发生异常，记录错误日志并输出异常信息
            logs.error(f'解析配置文件出现异常，原因：{e}')

    # 定义一个方法获取 HOST section 中的配置项
    def get_host(self, option):
        # 通过调用 get_value 方法获取 HOST section 中的指定配置项的值
        return self.get_value('HOST', option)

    # 定义一个方法获取 MYSQL section 中的配置项
    def get_section_mysql(self, option):
        # 通过调用 get_value 方法获取 MYSQL section 中的指定配置项的值
        return self.get_value('MYSQL', option)

    # 定义一个通用方法来获取指定 section 和 option 的值
    def get_conf(self, conf, option):
        """
        获取配置文件中指定 section 和 option 的值的简化方法。
        :param conf: 配置文件中的 section 名称
        :param option: 配置文件中的 option 名称
        :return: 对应 option 的值，如果获取失败则返回 None
        """
        # 通过调用 get_value 方法获取指定 section 和 option 对应的值
        return self.get_value(conf, option)

    # 定义一个方法获取 Redis section 中的配置项
    def get_redis_conf(self, option):
        """
        获取Redis数据库的配置参数值。
        :param option: Redis配置参数的名称
        :return: 对应 option 的值，如果获取失败则返回 None
        """
        # 通过调用 get_value 方法获取 Redis section 中的指定配置项的值
        return self.get_value('Redis', option)
