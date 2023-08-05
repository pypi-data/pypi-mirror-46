#encoding=utf-8
from __future__ import unicode_literals, print_function

# use "".format() insted ""%()
# use six.text_type insted basestring
import six
import chardet

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from codecs import open

def encode_get(s):
    if not s:
        return "unicode"
    if not isinstance(s, basestring):
        return None
    if isinstance(s, unicode):
        return "unicode"
    else:
        return chardet.detect(s).get('encoding', None)  # s==''时，会return None

def encode_toCn(s):
    if (not isinstance(s, basestring)): return s
    if (encode_get(s) in ['unicode', 'utf-8']):
        return s.encode('GBK')
    else:
        try:
            ret = s.decode('GBK').encode('GBK')
        except Exception as eObj:
            print(str(eObj))
            raise Exception("encode_toCn: {%s}.decode('GBK').encode('GBK'), error={%s}" % (s, eObj))
        return ret


def encode_to(s, typeNew='utf-8', __Encoding__=''):
    if not isinstance(s, basestring):
        return s
    typeNew = __Encoding__ or typeNew
    typeOld = encode_get(s)
    if not typeOld or typeOld==typeNew:
        return s

    if typeOld != 'unicode':
        s = encode_toU(s)

    try:
        ret = s.encode(typeNew)
    except Exception as eObj:
        raise Exception("encode_toU: {%s}.decode(%s), error={%s}" % (s, typeNew, eObj))
    return ret

def encode_toU(s):
    if not isinstance(s, basestring):
        return s
    codeType = encode_get(s)
    if not codeType:
        return codeType  # return ''
    if codeType in ['unicode']:
        return s

    try:
        ret = s.decode(codeType)
    except Exception as eObj:
        raise Exception("encode_toU: {%s}.decode(%s), error={%s}" % (s, codeType, eObj))
    return ret

def str_fmt(fmt=None, *args, **kwargs):
    if not args and not kwargs:
        return '{}'.format(fmt) if not isinstance(fmt, basestring) else encode_toU(fmt)
    if args:
        return fmt.format(*[encode_toU(i) for i in args])
    else:
        return fmt.format(**{k: encode_toU(v) for k, v in kwargs.items()})

def str_fmtB(fmt=None, *args, **kwargs):
    strFmt = str_fmt(fmt, *args, **kwargs)
    __Encoding__ = kwargs.get('__Encoding__', 'utf-8')
    return encode_to(strFmt, __Encoding__=__Encoding__)

def printB(fmt=None, *args, **kwargs):
    if not isinstance(fmt, basestring):
        print(fmt)
    else:
        strFmtB = str_fmtB(fmt, *args, **kwargs)
        print(strFmtB)