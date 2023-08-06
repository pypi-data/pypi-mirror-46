import hashlib
import base64
import uuid

version_info = (1, 0, 0)


def gen_md5(msg):
    # 创建md5对象
    md5 = hashlib.md5()
    md5.update(msg.encode(encoding='utf-8'))
    return md5.hexdigest()


def gen_sha256(msg):
    sha256 = hashlib.sha256()
    sha256.update(msg.encode(encoding='utf-8'))
    return sha256.hexdigest()


def gen_id0():
    """
    标准分段uuid格式
    """
    return uuid.uuid4().__str__()


def gen_id1():
    """
    uuid以hex输出
    """
    return uuid.uuid4().hex


def gen_id2():
    """
    对uuid进行base32编码，且去掉等号
    """
    guid = str(base64.b32encode(uuid.uuid4().bytes), encoding="utf8")
    return guid.replace('======', '')


def gen_id3():
    """
    对uuid进行base64编码，且去掉等号、替换'+'和'/'
    """
    guid = str(base64.b64encode(uuid.uuid4().bytes), encoding="utf8")
    return guid.replace('==', '').replace('+', 'AD').replace('/', 'DS')
