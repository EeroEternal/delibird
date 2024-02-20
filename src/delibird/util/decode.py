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


def common_decode(data):
    """通用解析函数.

    解析从大模型获取的数据，返回其中的 content 字段。
    数据一般是这样的：
    1. 从 choices 中获取 delta，然后从 delta 中获取 content
    2. choices 有个 finish_reason 字段表示该条内容是最后一条
    3. [DONE] 表示结束。这个是可选，有些没有结束标记
    4. 一段可解析内容开始的标记是 data:，结束的标记是 \n\n

    Args:
        data: 待解析的数据
    Returns:
        True,message: 是否成功，消息内容(str)
    """

    start = "data:"
    last = "\n\n"
    end_tag = "[DONE]"

    if not data.startswith(start):
        return False, ""

    # 去掉开头的 data: 字符串
    data = data.lstrip(start)

    # 去掉结尾的标记字符
    data = data.rstrip(last)

    # 检查是否是结束标记
    if data == end_tag:
        return True, data

    # 将 json 字符串转换为字典
    try:
        data = json.loads(data)
    except json.JSONDecodeError as e:
        return False, ""

    # 检查 choices 下面是否有 finish_reason 字段
    # 如果有，说明是最后一条消息。在返回的消息后面加上 [DONE]
    # 让调用者知道已经结束了
    if "choices" in data and "finish_reason" in data:
        return True, data["choices"][0]["delta"]["content"] + end_tag

    # 返回 choices 下面的 delta 下的 content 字段，就是消息内容
    return True, data["choices"][0]["delta"]["content"]
