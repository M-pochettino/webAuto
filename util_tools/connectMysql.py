import pymysql

from util_tools.handle_data.configParse import ConfigParse
from util_tools.logs_util.recordlog import logs

conf = ConfigParse()


# 定义一个连接 MySQL 数据库的类
class ConnectMysql:

    # 初始化方法，用于设置数据库连接配置并建立连接
    def __init__(self):
        # 从配置文件中读取数据库连接参数，并将其存储在字典中
        self.conf = {
            'host': conf.get_section_mysql('host'),  # 数据库主机地址
            'port': int(conf.get_section_mysql('port')),  # 数据库端口号，需要转换为整数类型
            'user': conf.get_section_mysql('username'),  # 数据库用户名
            'password': conf.get_section_mysql('password'),  # 数据库密码
            'database': conf.get_section_mysql('database')  # 数据库名称
        }
        try:
            # 使用 pymysql 连接到数据库，并传入配置信息
            self.conn = pymysql.connect(**self.conf)
            # 获取游标对象，用于执行 SQL 语句
            # cursor=pymysql.cursors.DictCursor：结果以字典形式返回，每一行数据为一个字典
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 记录成功连接数据库的日志信息
            logs.info(f'成功连接到数据库，数据库IP：{self.conf.get("host")}')
        except Exception as e:
            # 如果连接数据库失败，记录错误日志信息
            logs.error(f'连接数据库失败，错误信息：{e}')

    # 关闭数据库连接和游标的方法
    def close(self):
        if self.conn and self.cursor:  # 如果连接和游标对象存在
            self.conn.close()  # 关闭数据库连接
            self.cursor.close()  # 关闭游标
        return True  # 返回 True 表示关闭成功

    # 查询数据库的方法
    def query(self, sql, fetchall=False):
        """
        查询数据库数据
        :param sql: 查询的SQL语句
        :param fetchall: 查询全部数据，默认为False则查询单条数据
        :return:
        """
        try:
            # 执行传入的 SQL 查询语句
            self.cursor.execute(sql)
            # 提交事务（对于查询语句一般不需要，但部分数据库可能需要）
            self.conn.commit()
            if fetchall:
                # 如果 fetchall 为 True，则获取所有查询结果
                res = self.cursor.fetchall()
            else:
                # 否则只获取一条结果
                res = self.cursor.fetchone()
            return res  # 返回查询结果
        except Exception as e:
            # 如果查询时出现异常，记录错误日志
            logs.error(f'查询数据库内容出现异常，错误信息：{e}')
        finally:
            # 不管是否异常，都关闭数据库连接
            self.close()

    # 删除数据库内容的方法
    def delete(self, sql):
        """
        删除数据库内容
        :param sql: 删除的SQL语句
        :return:
        """
        try:
            # 执行传入的 SQL 删除语句
            self.cursor.execute(sql)
            # 提交事务，确保删除操作生效
            self.conn.commit()
            # 记录删除成功的日志信息
            logs.info('数据库数据删除成功')
        except Exception as e:
            # 如果删除时出现异常，记录错误日志
            logs.error(f'删除数据库数据出现异常，错误信息：{e}')
        finally:
            # 无论是否异常，都关闭数据库连接
            self.close()
