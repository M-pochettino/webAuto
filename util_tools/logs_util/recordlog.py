# -*- coding:utf-8 -*-
import logging
import os
import time
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份

import colorlog

from config import setting

log_path = setting.FILE_PATH['log']
if not os.path.exists(log_path):
    os.mkdir(log_path)

logfile_name = log_path + r"\test.{}.log".format(time.strftime("%Y%m%d"))


# 定义一个记录日志的类
class RecordLog:

    # 初始化方法，目前没有需要在初始化时处理的内容，所以使用 pass
    def __init__(self):
        pass

    # 类方法，用于配置日志的颜色输出
    @classmethod
    def log_color(cls):
        # 定义一个字典，指定不同日志级别对应的颜色
        log_color_config = {
            'DEBUG': 'cyan',  # DEBUG 级别日志的颜色为青色
            'INFO': 'green',  # INFO 级别日志的颜色为绿色
            'WARNING': 'yellow',  # WARNING 级别日志的颜色为黄色
            'ERROR': 'red',  # ERROR 级别日志的颜色为红色
            'CRITICAL': 'red'  # CRITICAL 级别日志的颜色为红色
        }

        # 创建一个带有颜色格式的日志格式器（formatter）
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s %(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s',
            # 配置日志级别对应的颜色
            log_colors=log_color_config
        )

        # 返回配置好的日志格式器
        return formatter

    # 定义一个输出日志的方法
    def output_logging(self):
        # 获取一个名为当前模块名称的 logger 实例
        logger = logging.getLogger(__name__)
        # 调用 log_color 方法获取带颜色的日志格式
        stream_format = self.log_color()
        # 防止重复添加处理器（handlers）导致日志重复输出
        if not logger.handlers:
            # 设置日志的最低级别为 DEBUG
            logger.setLevel(logging.DEBUG)
            # 定义一个标准的日志格式器，不带颜色
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s'
            )
            # 创建一个 StreamHandler，将日志输出到控制台
            sh = logging.StreamHandler()
            # 设置控制台输出的日志级别为 DEBUG
            sh.setLevel(logging.DEBUG)
            # 为控制台日志输出设置带颜色的格式
            sh.setFormatter(stream_format)
            # 为 logger 添加这个控制台处理器
            logger.addHandler(sh)

            # 创建一个 RotatingFileHandler，用于将日志保存到文件中
            # 设置文件路径为 logfile_name，日志文件最大大小为 5MB（5242880 字节），备份最多 7 个日志文件
            fh = RotatingFileHandler(filename=logfile_name, mode='a', maxBytes=5242880, backupCount=7, encoding='utf-8')
            # 设置文件输出的日志级别为 DEBUG
            fh.setLevel(logging.DEBUG)
            # 为文件日志输出设置标准的日志格式
            fh.setFormatter(log_format)
            # 为 logger 添加这个文件处理器
            logger.addHandler(fh)

        # 返回配置好的 logger 实例
        return logger


# 创建 RecordLog 类的实例
rec = RecordLog()
# 调用 output_logging 方法，获取配置好的 logger 实例，并赋值给 logs
logs = rec.output_logging()

