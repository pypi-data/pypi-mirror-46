# coding:utf-8

from enum import Enum
from enum import unique
import config


@unique
class ErrCode(Enum):
    def code(self):
        return int(self.name.split('E')[1])

    def message(self, lang=config.LANG):
        if lang == 'zh':
            return self.value[0]
        return self.value[1]

    E40000 = ('请求参数错误', 'bad request')
    E40001 = ('未设置用户登录名', 'no name')
    E40002 = ('无效的用户标示', 'invalid indicator')
    E40003 = ('无效的email地址', 'invalid email')
    E40004 = ('无效的手机号码，eg. 86-13012345678', 'invalid mobile，eg. 86-13012345678')
    E40005 = ('未设置用户ID', 'no user ID')
    E40006 = ('未设置密码', 'no password')
    E40007 = ('无效用户登录名', 'invalid name')
    E40008 = ('未设置微信授权码CODE', 'no weixin auth CODE')

    E40020 = ('资源已存在，禁止重复添加', 'resource existed, no re-create')
    E40021 = ('非编辑状态禁止更新', 'no update when not in editing status')
    E40022 = ('错误的状态迁移请求', 'wrong status changing request')

    E40100 = ('请求校验失败', 'verify failed')
    E40101 = ('用户不存在', 'user not existed')
    E40102 = ('密码错误', 'wrong password')
    E40103 = ('无效验证码', 'invalid verification code')
    E40104 = ('无效用户ID', 'invalid user ID')

    E40300 = ('访问被拒绝', 'access forbidden')
    E40301 = ('无效access_token', 'invalid access_token')
    E40302 = ('已被注册', 'has been registered')
    E40303 = ('已存在，禁止修改', 'existed，no modify')
    E40304 = ('访问频次限制', 'more frequently accessing')
    E40305 = ('用户不在组织中', 'user not in org')
    E40306 = ('被操作目录不在授权目录下', 'catalog not in the authorized')
    E40307 = ('授权校验失败', 'failed verify license')
    E40308 = ('操作未授权', 'unauthorized operation')
    E40309 = ('授权无效，请重新获取授权', 'authorization invalid, regain license please')
    E40310 = ('授权已过期，请重新获取授权', 'authorization expired, regain license please')
    E40311 = ('超过授权范围', 'exceed authorization range')

    E40400 = ('不存在', 'not found')

    E50000 = ('系统内部错误', 'internal server error')
    E50001 = ('发送邮件失败', 'sending email failed')
    E50002 = ('发送SMS失败', 'sending SMS failed')
    E50003 = ('调用微信API失败', 'weixin API failed')



