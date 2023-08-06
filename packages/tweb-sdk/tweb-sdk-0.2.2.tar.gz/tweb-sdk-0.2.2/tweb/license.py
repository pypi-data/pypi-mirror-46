from tweb.error_exception import ErrException, ERROR
from tweb import tools, rdpool, time
import os
import base64
import re
from bitarray import bitarray
import json


class License:
    def __init__(self, profiles, display, **kwargs):
        """
        :param profile: 配置清单，示例如下

        'catalog': {
            'switches': [
                "sample_sw1",  # 0
                "sample_sw2"
            ],

            # 共6个数值域可用
            'numbers': [
                "sample_num1",
                "sample_num2"
            ],

            # 共4个范围域可用
            'ranges': [
                "sample_range1",
                "sample_range2"
            ]
        }
        :param display: 显示字典，示例如下

        'zh': {
            'catalog': '分类节点控制',
            'catalog.switches': '权限开关',
            'catalog.switches.sample_sw1': '示例开关1',
            'catalog.switches.sample_sw2': '示例开关2',
            'catalog.numbers': '数量限制',
            'catalog.numbers.sample_num1': '示例数量1',
            'catalog.numbers.sample_num2': '示例数量2',
            'catalog.ranges': '范围控制',
            'catalog.ranges.sample_range1': '示例范围1',
            'catalog.ranges.sample_range2': '示例范围2',
        },
        'en': {
            'catalog': 'Catalog Node',
            'catalog.switches': 'Switches',
            'catalog.switches.sample_sw1': 'Sample SW1',
            'catalog.switches.sample_sw2': 'Sample SW2',
            'catalog.numbers': 'Number Limit',
            'catalog.numbers.sample_num1': 'Sample Num1',
            'catalog.numbers.sample_num2': 'Sample Num2',
            'catalog.ranges': 'Range Limit',
            'catalog.ranges.sample_range1': 'Sample Range1',
            'catalog.ranges.sample_range2': 'Sample Range2',
        }
        :param kwargs:
        """
        # license支持的授权项配置
        self.profiles = profiles
         # 配置项显示字典，多语言支持
        self.display = display
        # 发证机构代码，一般在子类中修改
        self._authority = kwargs['authority'] if 'authority' in kwargs else 'world'
        # 发证机构代签名密码
        self._secret = kwargs['secret'] if 'secret' in kwargs else 'Lic123!@#'
        # 有效性超时时间, 秒
        self._timeout = kwargs['timeout'] if 'timeout' in kwargs else 604800
        # 闲置超时时间, 秒
        self._idle_time = kwargs['idle_time'] if 'idle_time' in kwargs else 86400

        # 资源节点标示，即资源树路径，如"world/google/dev"
        self.node = None
        # 被授权主体ID，组织ID或者个人用户ID
        self.owner = None

        # 分域解析对象字典
        self.parser_dic = dict()
        # 分域序列文本字典
        self.text_dic = dict()
        # License的json描述对象
        self._json = dict()
        for k, v in self.profiles.items():
            p = Parser(v)
            self.parser_dic[k] = p
            self.text_dic[k] = p.text
            self._json[k] = p.json

        # License序列化后的文本
        self.text = '|'.join(['{}:{}'.format(k, txt) for k, txt in sorted(self.text_dic.items())])

    @property
    def json(self):
        temp = self._json.copy()
        for k, v in list(temp.items()):
            if len(v) == 0:
                temp.pop(k)
        return temp

    def parse(self, text):
        if text is None or text == '':
            return self

        self.text = text

        domains_text = self.text.split('|')
        for item in domains_text:
            dt = item.split(':')
            if len(dt) != 2:
                raise ErrException(ERROR.E50000, extra='wrong format of license string')

            domain = dt[0]
            lic_txt = dt[1]
            self.text_dic[domain] = lic_txt
            if domain in self.profiles:
                lic = Parser(self.profiles[domain]).parse(lic_txt)
                self.parser_dic[domain] = lic
                self._json[domain] = lic.json

        return self

    def update(self, node, owner, json, my_lic=None):
        """
        :param node: 资源节点标示，即资源树路径，如"world/google/dev"
        :param owner: 被授权主体ID，组织ID或者个人用户ID
        :param json: License的json描述对象
        :param my_lic: 我所拥有的授权（License对象），我有授权，才能给其他主体授权
        :return: self
        """
        if owner is None:
            owner = ''

        if my_lic is not None and owner == my_lic.owner:
            raise ErrException(ERROR.E40300, extra='can not update yourself, should be done by your parents')

        self.node = node
        self.owner = owner

        for domain, lic in sorted(json.items()):
            if domain in self.profiles:
                if my_lic is None:
                    the_parser = None
                elif domain in my_lic.parser_dic:
                    the_parser = my_lic.parser_dic[domain]
                else:
                    continue

                p = self.parser_dic[domain]
                # 授权其他主体，范围限定在我的授权范围之内
                p.update(lic, the_parser)
                self._json[domain] = p.json
                self.text_dic[domain] = p.text

        lst = list()
        for kv in sorted(self.text_dic):
            lst.append(':'.join(kv))

        text = '|'.join(['{}:{}'.format(k, txt) for k, txt in sorted(self.text_dic.items())])

        # 如果新的授权串与原来不一样则更新
        if text != self.text:
            self.text = text

            # 使某资源对某拥有者的授权签名全部失效
            self.invalidate_signed(self.node, self.owner)

        return self

    def signed(self, resource, owner, nonce):
        """
        获取签名的授权字符串
        :param resource: 受保护的资源标示, 为节点node值，如'root/product'
        :param owner: 权限授予对象标示, 如组织ID，或者用户ID
        :param nonce: 临时一致性标示，如可以使用用户的access_token
        """
        if owner is None:
            owner = ''
        if nonce is None:
            nonce = ''

        self.node = resource
        self.owner = owner

        key = self._key(self.node, self.owner, nonce)
        lic_token = rdpool.rds.get(key)
        if lic_token is None:
            lic_token = {'random': os.urandom(9).hex(), 'ts': time.second()}
            rdpool.rds.set(key, json.dumps(lic_token), self._idle_time)
        else:
            lic_token = json.loads(lic_token)

        sign = tools.gen_md5(self.text + self.node + self.owner + nonce + lic_token['random'])

        expired = lic_token['ts'] + self._timeout;

        temp = '{}&{}&{}&{}&{}'.format(self.text, self.node, self.owner, sign, expired)
        return str(base64.b64encode(str.encode(temp)), encoding="utf8")

    def verify(self, *auth_args):
        """
        校验授权签名的合法性
        :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
        :return: 授权对象
        """
        signed = auth_args[0]
        nonce = auth_args[1]
        if nonce is None:
            nonce = ''

        if signed is None:
            raise ErrException(ERROR.E40000, extra='no signed license')

        try:
            signed = str(base64.b64decode(signed), encoding="utf8")
        except Exception:
            raise ErrException(ERROR.E40000, extra='wrong signed license')

        fields = signed.split('&')
        if len(fields) != 5:
            raise ErrException(ERROR.E40307, extra='wrong format of signed license')

        text = fields[0]
        self.node = fields[1]
        self.owner = fields[2]
        sign = fields[3]
        expired = int(fields[4])

        if time.second() > expired:
            raise ErrException(ERROR.E40310)

        key = self._key(self.node, self.owner, nonce)
        lic_token = rdpool.rds.get(key)
        if lic_token is None:
            raise ErrException(ERROR.E40309)
        else:
            lic_token = json.loads(lic_token)

        # 重置lic_token超时时间
        rdpool.rds.expire(key, self._idle_time)

        dynamic_sign = tools.gen_md5(text + self.node + self.owner + nonce + lic_token['random'])
        if dynamic_sign != sign:
            raise ErrException(ERROR.E40307)

        return self.parse(text)

    @staticmethod
    def invalidate_signed(node, owner):
        """
        使签名无效
        """
        if node is not None and owner is not None:
            key = License._key(node, owner, '')
            issued_list = rdpool.rds.keys('{}*'.format(key))
            for k in issued_list:
                rdpool.rds.delete(k)

    def operable(self, cur_resource, *actions):
        """
        检查是否允许进行指定操作
        :param cur_resource: 将被操作的资源路径，如'root/club/table'
        :param actions: 操作列表(逻辑与的关系)，格式：DOMAIN.ACTION，如org.create, catalog.read...
        """
        # 判断操作目录是否是授权目录，或者授权目录的子目录
        if cur_resource.find(self.node) != 0:
            raise ErrException(ERROR.E40306)

        # 对授权节点本身禁止操作
        if cur_resource == self.node:
            raise ErrException(ERROR.E40306, extra='forbid operate the current node')

        group = dict()
        for item in actions:
            temp = item.split('.')
            if len(temp) != 2:
                raise ErrException(ERROR.E50000, extra='action string format is "DOMAIN.ACTION"')
            domain = temp[0]
            action = temp[1]
            if domain not in group:
                group[domain] = list()
            group[domain].append(action)

        for d, lst in group.items():
            if d in self.parser_dic:
                self.parser_dic[d].operable(lst)

        return self

    def number(self, cur_resource, key):
        """
        查询授权数值
        :param cur_resource: 将被操作的资源路径，如'root/club/table'
        :param key: 字段名, 格式：DOMAIN.KEY，如org.num1, catalog.num2...
        """
        # 判断操作目录是否是授权目录，或者授权目录的子目录
        if cur_resource.find(self.node) != 0:
            raise ErrException(ERROR.E40306)

        temp = key.split('.')
        if len(temp) != 2:
            raise ErrException(ERROR.E50000, extra='action string format is "DOMAIN.KEY"')

        domain = temp[0]
        if domain in self.parser_dic:
            return self.parser_dic[domain].number(temp[1])
        else:
            raise ErrException(ERROR.E40000, extra='wrong domain license of %s' % domain)

    def range(self, cur_resource, key):
        """
        查询授权的数值范围
        :param domain: 权限域的名字
        :param cur_resource: 将被操作的资源路径，如'root/club/table'
        :param key: 字段名, 格式：DOMAIN.KEY，如org.range1, catalog.range2...
        """
        # 判断操作目录是否是授权目录，或者授权目录的子目录
        if cur_resource.find(self.node) != 0:
            raise ErrException(ERROR.E40306)

        temp = key.split('.')
        if len(temp) != 2:
            raise ErrException(ERROR.E50000, extra='action string format is "DOMAIN.KEY"')

        domain = temp[0]
        if domain in self.parser_dic:
            return self.parser_dic[domain].range(temp[1])
        else:
            raise ErrException(ERROR.E40000, extra='wrong domain license of %s' % domain)

    @staticmethod
    def _key(node, owner, nonce):
        return 'license/{}/{}/{}'.format(node, owner, nonce)


class Parser:
    """
    资源授权证书
    """

    def __init__(self, profile):
        """
        :param profile: 字段定义，如：
        {
            'switch': [
                "sample_sw1",  # 0
                "sample_sw2",
                "NA",
                "NA"
            ],

            # 共6个数值域可用
            'number': [
                "sample_num1",
                "NA"
            ],

            # 共4个范围域可用
            'range': [
                "sample_range1",
                "NA"
            ]
        }
        """

        if profile is None:
            raise ErrException(ERROR.E50000, extra='license profile is None')

        # 开关类
        self.SWITCH = profile['switch'] if 'switch' in profile else []
        # 数值类
        self.NUMBER = profile['number'] if 'number' in profile else []
        # 数值范围类
        self.RANGE = profile['range'] if 'range' in profile else []

        sw_tpl_str = '0' * len(self.SWITCH)
        num_tpl_str = ','.join(['0'] * len(self.NUMBER))
        ran_tpl_str = ','.join(['0~0'] * len(self.RANGE))
        self.text = '{};{};{}'.format(sw_tpl_str, num_tpl_str, ran_tpl_str)

        self._json = dict()

        for i, k in enumerate(self.SWITCH):
            if k != 'NA':
                if 'switch' not in self._json:
                    self._json['switch'] = dict()

                self._json['switch'][k] = 0
        for i, k in enumerate(self.NUMBER):
            if k != 'NA':
                if 'number' not in self._json:
                    self._json['number'] = dict()

                self._json['number'][k] = 0
        for i, k in enumerate(self.RANGE):
            if k != 'NA':
                if 'range' not in self._json:
                    self._json['range'] = dict()

                self._json['range'][k] = [0, 0]

    @property
    def json(self):
        temp = self._json.copy()
        switches = temp['switch']
        for k, v in list(switches.items()):
            if v == 0:
                switches.pop(k)
        if len(switches) == 0:
            return {}
        return temp


    def parse(self, text):
        """
        :param text: 格式: "若干位0/1开关串;任意个数的数值列表;任意个数的范围列表",
        示例: 1100010010111010000100001000011100100110;12,30,100;0~100,20~50
        :return:
        """
        if text is None:
            return self

        if not re.match(r'[0-1]*;[\-0-9,]*;[\-0-9~,]*', text):
            raise ErrException(ERROR.E40000, extra='wrong format, template')

        self.text = text
        fields = self.text.split(';')

        # 开关相关
        sw_str = fields[0]
        sw_obj = self._json.get('switch')
        if sw_obj is not None:
            for i, k in enumerate(self.SWITCH):
                if k == 'NA':
                    continue
                if i < len(sw_str):
                    sw_obj[k] = int(sw_str[i])
                else:
                    sw_obj[k] = 0
        # END

        # 数值相关
        num_str = fields[1]
        nums = num_str.split(',')
        nums_len = len(nums)
        if num_str == '':
            nums_len = 0

        num_obj = self._json.get('number')
        if num_obj is not None:
            for i, k in enumerate(self.NUMBER):
                if k == 'NA':
                    continue
                if i < nums_len:
                    num_obj[k] = int(nums[i])
                else:
                    num_obj[k] = 0
        # END

        # 范围相关
        ran_str = fields[2]
        ranges = ran_str.split(',')
        ran_len = len(ranges)
        if ran_str == '':
            ran_len = 0

        ran_obj = self._json.get('range')
        if ran_obj is not None:
            for i, k in enumerate(self.RANGE):
                if k == 'NA':
                    continue

                if i < ran_len:
                    mm = ranges[i].split('~')
                    if len(mm) != 2:
                        low = 0
                        up = 0
                    else:
                        try:
                            low = int(mm[0])
                            up = int(mm[1])

                            if low > up:
                                up = low
                        except ValueError:
                            low = 0
                            up = 0

                    ran_obj[k] = [low, up]
                else:
                    ran_obj[k] = [0, 0]
        # END

        return self

    def update(self, json, shader=None):
        """
        更新
        :param json: 新授权json描述对象
        :param shader: 限定授权范围的License对象，一般为操作者自己获得的授权对象
        :return:
        """
        fields = self.text.split(';')

        # 开关相关
        if 'switch' in self._json:
            sw_len = len(self.SWITCH)
            sw_obj = json.get('switch')
            sw_str = fields[0]

            # 因为profile升级，导致原有串位数不够，此时扩展多出来的位数
            if len(sw_str) < sw_len:
                sw_str += '0' * (sw_len - len(sw_str))

            if sw_obj is not None and sw_len > 0:
                ba = bitarray(sw_str)
                for i, k in enumerate(self.SWITCH):
                    if k == 'NA' or k not in sw_obj:
                        continue

                    if shader and sw_obj[k]:
                        # 不能超过shader限定的范围
                        try:
                            shader.operable([k])
                        except ErrException as e:
                            raise ErrException(ERROR.E40311, extra='exceed your own territory--%s' % e.extra)

                    sw = 1 if sw_obj[k] else 0
                    ba[i] = sw
                    self._json['switch'][k] = sw

                sw_str = ba.to01()
        else:
            sw_str = ''
        # END

        # 数值相关
        if 'number' in self._json:
            num_len = len(self.NUMBER)
            num_obj = json.get('number')
            num_str = fields[1]
            if num_obj is not None and num_len > 0:
                nums = num_str.split(',')
                # 因为profile升级，导致原有串位数不够，此时扩展多出来的位数
                if len(nums) < num_len:
                    nums += ['0'] * (num_len - len(nums))

                for i, k in enumerate(self.NUMBER):
                    if k == 'NA':
                        continue
                    val = num_obj.get(k)
                    if val is None:
                        continue

                    if shader:
                        # 不能超过shader限定的范围
                        self_limit = shader.number(k)
                        if val > self_limit:
                            raise ErrException(ERROR.E40311, extra='exceed your own limit %s' % self_limit)

                    nums[i] = str(val)
                    self._json['number'][k] = val

                num_str = ','.join(nums)
        else:
            num_str = ''
        # END

        # 范围相关
        if 'range' in self._json:
            ran_len = len(self.RANGE)
            ran_obj = json.get('range')
            ran_str = fields[2]
            if ran_obj is not None and ran_len > 0:
                rans = ran_str.split(',')
                # 因为profile升级，导致原有串位数不够，此时扩展多出来的位数
                if len(rans) < ran_len:
                    rans += ['0~0'] * (ran_len - len(rans))

                for i, k in enumerate(self.RANGE):
                    if k == 'NA':
                        continue
                    vals = ran_obj.get(k)
                    if vals is None:
                        continue
                    if len(vals) != 2:
                        continue

                    if shader:
                        # 不能超过shader限定的范围
                        self_range = shader.range(k)
                        if vals[0] < self_range[0] or vals[1] > self_range[1]:
                            raise ErrException(ERROR.E40311, extra='exceed your own range %s' % self_range)

                    rans[i] = '{}~{}'.format(vals[0], vals[1])
                    self._json['range'][k] = vals

                ran_str = ','.join(rans)
        else:
            ran_str = ''
        # END

        # 拼接
        self.text = '{};{};{}'.format(sw_str, num_str, ran_str)

        return self

    def operable(self, actions):
        """
        判断是否有操作权限（开关是否为1）
        :param actions: 操作列表（逻辑与的关系）
        """
        for action in actions:
            if 'switch' not in self._json or action not in self._json['switch']:
                raise ErrException(ERROR.E40000, extra='wrong action of %s' % action)

            if self._json['switch'][action] == 0:
                raise ErrException(ERROR.E40308, extra=f'you can not {action}')

        return self

    def number(self, key):
        if 'number' not in self._json or key not in self._json['number']:
            raise ErrException(ERROR.E40000, extra='wrong number key of %s' % key)

        return self._json['number'][key]

    def range(self, key):
        if 'range' not in self._json or key not in self._json['range']:
            raise ErrException(ERROR.E40000, extra='wrong range key of %s' % key)

        return self._json['range'][key]
