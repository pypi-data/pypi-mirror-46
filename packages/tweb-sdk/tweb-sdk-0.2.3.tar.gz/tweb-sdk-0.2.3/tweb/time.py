import time


# 获取 10 位时间戳，秒
def second():
    return int(time.time())


# 获取 13 位时间戳，毫秒
def millisecond():
    return int(time.time() * 1000)


# 将秒时间戳转化为格式时间
def sec2str(sec):
    tl = time.localtime(sec)
    return time.strftime("%Y-%m-%d %H:%M:%S", tl)


# 将毫秒秒时间戳转化为格式时间
def ms2str(ms):
    mod = ms % 1000
    sec = int(ms / 1000)
    tl = time.localtime(sec)
    return time.strftime(f"%Y-%m-%d %H:%M:%S.{mod}", tl)
