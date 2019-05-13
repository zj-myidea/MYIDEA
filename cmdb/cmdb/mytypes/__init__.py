import importlib
import ipaddress

classes_cache = {}
instance_cache = {}

def get_class(type:str):

    cls = classes_cache.get(type)
    if cls:
        return cls
    raise TypeError(f'wrong type {type}. not subclass of BaseType')

def get_instance(type:str,**option):
    key = ','.join('{}={}'.format(k,v) for k, v in sorted(option.items()))
    key = '{}|{}'.format(type,key)
    instance = instance_cache.get(key)
    if instance:
        return instance
    obj = get_class(type)(**option)
    instance_cache[key] = obj
    return obj

def inject_class_cache():
    mod = globals().get('__package__')
    print(mod)
    for k,v in globals().items():
        if type(v) == type and k != 'BaseType' and issubclass(v,BaseType):
            classes_cache[k] = v
            classes_cache['.'.join((mod,k))] = v
    print(classes_cache)

class BaseType:

    def __init__(self,**option):
        self.option = option

    def __getattr__(self, item):
        return self.option.get(item)

    def stringfy(self,value):
        raise NotImplementedError

    def destringfy(self,value):
        return NotImplementedError

class Int(BaseType):

    def stringfy(self, value):
        val = int(value)
        min = self.min
        if min and val < min:
            raise ValueError('too small')
        max = self.val
        if max and val > max:
            raise ValueError('too big')
        return str(int(value))

    def destringfy(self, value):
        return value

class Ip(BaseType):

    def stringfy(self, value):
        prefix = self.prefix
        if prefix and not str(value).startswith(prefix):
            raise ValueError(f'{value} is not start with {prefix}')
        return str(ipaddress.ip_address(value))

    def destringfy(self, value):
        return value

inject_class_cache()