import redis

from util_tools.handle_data.configParse import ConfigParse


# 定义一个用于连接 Redis 数据库并执行操作的类
class ConnectRedis:
    """
    连接到 Redis 数据库并执行操作。
    """

    # 初始化方法，用于创建 Redis 连接客户端
    def __init__(self):
        """
        初始化 Redis 连接客户端。
        """
        try:
            # 使用 ConfigParse 类从配置文件获取 Redis 连接信息
            self.redis_client = redis.StrictRedis(
                host=ConfigParse().get_redis_conf('host'),  # 获取 Redis 主机地址
                port=ConfigParse().get_redis_conf('port'),  # 获取 Redis 端口号
                db=ConfigParse().get_redis_conf('db')  # 获取 Redis 数据库编号
            )
        except Exception as e:
            # 如果连接 Redis 失败，打印错误信息
            print(f"Failed to connect to Redis: {e}")

    # 定义一个用于从 Redis 获取键对应值的方法
    def get(self, key):
        """
        获取指定键的值。
        :param key: Redis 键名
        :return: 键对应的值，如果键不存在则返回 None
        """
        try:
            # 查询 Redis 中指定键的值
            value = self.redis_client.get(key)
            if value:
                # 如果键存在，解码为字符串并返回
                return value.decode('utf-8')
            else:
                # 如果键不存在则返回 None
                return None
        except redis.RedisError as e:
            # 如果查询 Redis 时出现异常，打印错误信息
            print(f"Redis error: {e}")
            return None

    # 定义一个用于关闭 Redis 连接的方法
    def close(self):
        """
        关闭 Redis 连接。
        """
        # 关闭 Redis 连接
        self.redis_client.close()

