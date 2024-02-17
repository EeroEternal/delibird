"""Common functions for the project."""
import json


def decode_data(data, start="data:", last="\n\n", end_tag="[DONE]"):
    """解析返回的 messages

    通用的消息解析。去掉开头的 start_tag，去掉结尾的 end_tag 字符串。
    例如  data:....\n\n

    Args:
        data: 返回的消息
        start: 开头的标志
        last: 结尾的字符
        end_tag: 发送消息结束的标记

    Returns:
        True,message: 是否成功，消息内容(已经转为 json 字典)
    """

    if not data.startswith(start):
        return False, {}

    # 去掉开头的 data: 字符串
    data = data[len(start) :]

    # 去掉结尾的 end_tag 字符串
    data = data.rstrip(last)

    # 检查是否是结束标记
    if data == end_tag:
        return True, data

    # 将 json 字符串转换为字典
    try:
        data = json.loads(data)
        return True, data
    except json.JSONDecodeError as e:
        return False, {}
