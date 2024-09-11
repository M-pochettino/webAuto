import base64
import hashlib
import hmac
import time
import urllib.parse

import requests

from config import setting


# 用于生成加签信息的函数
def generate_sign():
    """
    生成加签计算
    :return: 返回生成的时间戳和签名
    """
    # 获取当前时间的时间戳，并将其转换为毫秒级的字符串格式
    timestamp = str(round(time.time() * 1000))
    # 从配置中获取钉钉机器人的加签秘钥
    secret = setting.secret
    # 将加签秘钥转换为utf-8编码的字节类型
    secret_enc = secret.encode('utf-8')
    # 组合时间戳和加签秘钥，形成待签名的字符串，格式为 "timestamp\nsecret"
    str_to_sign = f"{timestamp}\n{secret}"
    # 将待签名字符串转换为utf-8编码的字节类型
    str_to_sign_enc = str_to_sign.encode('utf-8')
    # 使用 HMAC 算法和 SHA256 加密方式生成加密后的二进制数据
    hmac_code = hmac.new(secret_enc, str_to_sign_enc, digestmod=hashlib.sha256).digest()
    # 使用 base64 对加密后的数据进行编码，并通过 urllib.parse.quote_plus 对其进行 URL 编码
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 返回时间戳和加密生成的签名
    return timestamp, sign


# 用于向钉钉群发送消息的函数
def send_dd_msg(content_str, at_all=True):
    """
    向钉钉群发送消息
    :param content_str: 发送的消息内容，字符串格式
    :param at_all: 是否 @ 全员，默认为 True
    :return: 钉钉机器人接口返回的响应文本
    """
    # 调用 generate_sign 函数，生成当前时间戳和签名
    timestamp, sign = generate_sign()
    # 构造包含 webhook 地址、时间戳和签名的完整 URL
    url = f"{setting.webhook}&timestamp={timestamp}&sign={sign}"
    # 定义请求头信息，设置为发送 JSON 数据
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    # 构造发送给钉钉机器人的消息体，msgtype 为 'text'，消息内容为 content_str
    # 'at' 字段用来指定是否 @ 全员（通过 isAtAll 字段控制）
    data = {
        'msgtype': 'text',
        'text': {
            'content': content_str
        },
        'at': {
            'isAtAll': at_all
        }
    }
    # 发送 HTTP POST 请求到钉钉机器人接口，发送的数据为 JSON 格式
    res = requests.post(url=url, json=data, headers=headers)
    # 返回钉钉机器人接口的响应文本
    return res.text
