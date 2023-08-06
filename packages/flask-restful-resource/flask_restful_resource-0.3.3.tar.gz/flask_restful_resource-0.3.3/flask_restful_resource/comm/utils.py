import logging
import time
from datetime import datetime

from schema import Schema, SchemaError


def move_space(data: dict):
    if data:
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = str.strip(v)
        return data
    return {}


def validate_schema(schema: Schema, data: dict, remove_blank=False):
    """schema验证,验证成功返回数据，验证失败返回错误信息
    Parameters
    ----------
    schema:Schema: 验证规则
    data: 验证数据
    remove_blank : 是否去除空白字段

    Returns (data,errors)
    -------

    """
    if not isinstance(data, dict):
        return {}, "Not found params"
    d = {}
    if remove_blank:
        for k, v in data.items():
            if v != "":
                d[k] = v
    else:
        d = data
    try:
        validate_data = schema.validate(d)
        return validate_data, []
    except SchemaError as e:
        return {}, str(e.autos)
    else:
        return validate_data, []


def utc_timestamp():
    """返回utc时间戳（秒）"""
    return int(datetime.now().timestamp())


def utc_strftime(fmt):
    return datetime.now().strftime(fmt)


def print_run_time(func):
    """计算时间函数"""

    def wrapper(*args, **kw):
        local_time = int(time.time() * 1000)
        result = func(*args, **kw)
        logging.info("current Function [%s] run time is %s ms" % (func.__name__, int(time.time() * 1000) - local_time))
        return result

    return wrapper
