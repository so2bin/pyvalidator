##################################################################
#    Validate the format of parameter and transfer to the correct
#    data with the specified format
#
#    ref: validator.js  [https://github.com/chriso/validator.js]
#
import re
import json

_STR_IPV4 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

_RE_EMAIL = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
_RE_PHONE = re.compile("^[1][34578][0-9]{9}$")
_RE_URL = re.compile(r"".join([
        r'^(?:http|ftp)s?://', # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|', #domain...
        r'localhost|', #localhost...
        _STR_IPV4 + r')', # ...or ip
        r'(?::\d+)?', # optional port
        r'(?:/?|[/?]\S+)$']), re.IGNORECASE)
_RE_MONGOID = re.compile(r'^[a-f0-9]{24}$')
_RE_IPV4 = re.compile(_STR_IPV4)

__all__ = ['isEmail', 'isPhone', 'isUrl', 'isMongoId', 'isIPV4', 'VType', 'Validator']

def isEmail(s):
    if isinstance(s, str):
        if _RE_EMAIL.match(s):
            return True
    return False


def isPhone(s):
    if isinstance(s, int):
        s = str(s)
    if isinstance(s, str):
        if _RE_PHONE.match(s):
            return True
    return False


def isUrl(s):
    if isinstance(s, str):
        if _RE_URL.match(s):
            return True
    return False


def isMongoId(s):
    if isinstance(s, str):
        if _RE_MONGOID.match(s):
            return True
        else:
            return False


def isIPV4(s):
    if isinstance(s, str):
        if _RE_IPV4.match(s):
            return True
        else:
            return False


class VType(object):
    """
    define the formats constant that can be validated
    """
    STRING = 0
    INT = 1
    FLOAT = 2
    BOOLEAN = 3
    LIST = 4
    DICT = 5
    EMAIL = 6
    URL = 7
    JSON = 8
    MOBILEPHONE = 9
    MONGOID = 10
    IPV4 = 11
    IPV6 = 12


class Validator(object):
    def __init__(self):
        self.data = {}
        self.error = []

    def isValid(self, data, key, _format):
        """
        validate value of data[key] with format, like:
            validator.isValid(data, 'name', {'type':VType.STRING, 'default':'', 'must': True})
            validator.isValid(data, 'account', {'default':'', 'test': [isEmail, isIPV4]})

        'must' in format default as: True

        :param data: origin data
        :param key:
        :param _format: object, {'type', 'default', 'test': [validate functions]}
        :return:
        """
        if not data or not (key and _format):
            raise ValueError('参数错误')
        if key not in data:
            if 'default' in _format:
                self.data[key] = _format.get('default', None)
                return
            else:
                if _format.get('must') is True:
                    self.error.append('缺少参数：%s' % key)
                    return
        v = data[key]
        if 'type' in _format:
            vtype = _format['type']
            if vtype == VType.INT:
                try:
                    v = int(v)
                except ValueError:
                    self.error.append('参数非整型：%s' % key)
                else:
                    self.data[key] = v
            elif vtype == VType.STRING:
                try:
                    v = str(v)
                except ValueError:
                    self.error.append('参数非字符串：%s' % key)
                else:
                    self.data[key] = v
            elif vtype == VType.FLOAT:
                try:
                    v = float(v)
                except ValueError:
                    self.error.append('参数非字符串：%s' % key)
                else:
                    self.data[key] = v
            elif vtype == VType.BOOLEAN:
                if v in ['true', 'True', 'TRUE', True]:
                    self.data[key] = True
                elif v == ['false', 'False', 'FALSE', False]:
                    self.data[key] = False
                else:
                    try:
                        v = bool(v)
                    except ValueError:
                        self.error.append('参数非bool：%s' % key)
                    else:
                        self.data[key] = v
            elif vtype == VType.LIST:
                if isinstance(v, list):
                    self.data[key] = v
                if isinstance(v, str):
                    try:
                        v = json.loads(v)
                    except json.JSONDecodeError:
                        self.error.append('参数非数组：%s' % key)
                    else:
                        if isinstance(v, list):
                            self.data[key] = v
                        else:
                            self.error.append('参数非数组：%s' % key)
                else:
                    self.error.append('参数非数组：%s' % key)
            elif vtype == VType.DICT:
                if isinstance(v, dict):
                    self.data[key] = v
                if isinstance(v, str):
                    try:
                        v = json.loads(v)
                    except json.JSONDecodeError:
                        self.error.append('参数非对象：%s' % key)
                    else:
                        if isinstance(v, dict):
                            self.data[key] = v
                        else:
                            self.error.append('参数非对象：%s' % key)
                else:
                    self.error.append('参数非对象：%s' % key)
            elif vtype == VType.EMAIL:
                if isinstance(v, str):
                    if isEmail(v):
                        self.data[key] = v
                    else:
                        self.error.append('参数非email：%s' % key)
            elif vtype == VType.URL:
                if isinstance(v, str):
                    if isUrl(v):
                        self.data[key] = v
                    else:
                        self.error.append('参数非url：%s' % key)
            elif vtype == VType.JSON:
                if isinstance(v, object):
                    self.data[key] = v
                if isinstance(v, str):
                    try:
                        v = json.loads(v)
                    except json.JSONDecodeError:
                        self.error.append('参数非json：%s' % key)
                    else:
                        self.data[key] = v
                else:
                    self.error.append('参数非json：%s' % key)
            elif vtype == VType.MOBILEPHONE:
                if isPhone(v):
                    self.data[key] = v
                else:
                    self.error.append('参数非手机号：%s' % key)
            elif vtype == VType.MONGOID:
                if isMongoId(v):
                    self.data[key] = v
                else:
                    self.error.append('参数非mongoId：%s' % key)
            elif vtype == VType.IPV4:
                if isIPV4(v):
                    self.data[key] = v
                else:
                    self.error.append('参数非IPV4：%s' % key)
            elif vtype == VType.IPV6:
                # TODO xxxx
                self.data[key] = v
                pass
            else:
                raise ValueError('无效验证参数类型：%s' % key)
        if 'test' in _format:
            test = _format['test']
            if isinstance(test, object) and callable(test):
                if test(v):
                    self.data[key] = v
                else:
                    self.error.append('参数验证失败：%s' % key)
            elif issubclass(test, list):
                for tf in test:
                    if callable(tf):
                        if tf(v):
                            self.data[key] = v
                        else:
                            self.error.append('参数验证失败：%s' % key)
