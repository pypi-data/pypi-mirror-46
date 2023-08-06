from ._logging import logger
from .errors import *
log = logger.getChild('data')
none = type(None)
import re

def Proxy(what,*a,**k):
    if isinstance(what,(int,str,bool,float,tuple,none)):
        return what
    if isinstance(what,dict):
        return DictProxy(what,*a,**k)
    if isinstance(what,list):
        return ListProxy(what,*a,**k)
    raise CustomTypeError(what)

class ProxyType(object):
    __int_re__ = re.compile(r'^[0-9]+$')
    __ascii_re__ = re.compile(r'^\w+$',re.A)
    def __init__(self,data=None,defaults=None,parent=None):
        if data is None:
            data = self.__datatype__()
        if not isinstance(data,self.__datatype__):
            raise TypeError(type(data).__name__)

        if defaults is not None:
            if not isinstance(defaults,ProxyType):
                defaults = Proxy(defaults)
            if not isinstance(defaults,ProxyType):
                raise TypeError(type(defaults).__name__)
        elif parent is not None:
            defaults = parent.__default__

        self.__content__ = data
        self.__default__ = defaults

    @classmethod
    def __parse_key__(cls,key):
        if not cls.__ascii_re__.match(key):
            raise ValueError('Only ascii keys accepted: [0-9a-zA-Z_]')
        if cls.__int_re__.match(key):
            return int(key)
        return str(key)
    @classmethod
    def __parse_keys__(cls,*keys):
        keys = list(keys)
        if len(keys) == 1:
            key = keys[0]
            if isinstance(key,(tuple,list)):
                keys = map(str,key)
            else:
                keys = str(key).split('.')
        keys = [ cls.__parse_key__(key) for key in keys ]
        return keys[0],keys[1:]

    def __get_item_by_key__(self,key):
        if not self.__has_key__(self,key):
            if self.__has_key__(self.__content__,key):
                value = self.__content__.__getitem__(key)
                self.__cache__(key,value)
            elif isinstance(self.__default__,self.__datatype__):
                return self.__default__.__getitem__(key)
            else: # raise content class error
                _ = self.__content__.__getitem__(key)
        return self.__datatype__.__getitem__(self,key)

    def __getitem__(self,*keys):
        key,tail = self.__parse_keys__(*keys)
        val = self.__get_item_by_key__(key)
        if tail:
            return val.__getitem__(*tail)
        return val

    def __set_item_by_key__(self,key,value):
        self.__content__.__setitem__(key,value)
        self.__cache__(key, self.__content__.__getitem__(key))

    def __setitem__(self,key,value):
        key,tail = self.__parse_keys__(key)
        if tail:
            if not self.__has_key__(self,key):
                self.__set_item_by_key__(key,dict())
            obj = self.__datatype__.__getitem__(self,key)
            obj.__setitem__(tuple(tail),value)
        else:
            self.__set_item_by_key__(key,value)

    def __delitem__(self,key):
        self.__content__.__delitem__(key)
        if self.__has_key__(self,key):
            self.__datatype__.__delitem__(self,key)

    def __len__(self):
        return len(self.__content__)

    def __contains__(self,key):
        return self.__content__.__contains__(key)

class DictProxy(ProxyType,dict):
    __datatype__ = dict
    def __init__(self,*a,**k):
        dict.__init__(self)
        ProxyType.__init__(self,*a,**k)

    @staticmethod
    def __has_key__(obj,key):
        return dict.__contains__(obj,key)

    def __cache__(self,key,value):
        dict.__setitem__(self,key,Proxy(value,parent=self))

    def keys(self):
        return (k for k in self.__content__.keys())

    def values(self):
        return (self[k] for k in self.keys())

    def items(self):
        return ((k,self[k]) for k in self.keys())

    def __iter__(self):
        return self.keys()

    def setdefault(self,key,value):
        self.__content__.setdefault(key,value)
        return self[key]

class ListProxy(ProxyType,list):
    __datatype__ = list
    def __init__(self,*a,**k):
        list.__init__(self)
        ProxyType.__init__(self,*a,**k)

    @staticmethod
    def __has_key__(obj,key):
        return isinstance(key,int) \
           and key >= 0            \
           and key < list.__len__(obj)

    def __cache__(self,key,value):
        if not key < self.__datatype__.__len__(self):
            if key > 0:
                self.__cache__(key - 1, self.__content__.__getitem__(key - 1))
            list.append(self, None)
        list.__setitem__(self,key,Proxy(value,parent=self))

    def __iter__(self):
        return (self[k] for k in range(len(self)))

    def append(self,value):
        self.__content__.append(value)

    def extend(self,what):
        self.__content__.extend(what)

__all__ = []
