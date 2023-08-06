

def filter_keys(src, keys_dict):
    """
    保留或者去除指定的字段
    :param src: 原始字典对象
    :param keys_dict: 指定过滤字段，如：{'name': 1, 'age': 1},
    :return: 过滤后的对象
    """
    result = dict()
    for (key, value) in src.items():
        if key in keys_dict:
            result[key] = value
    return result
