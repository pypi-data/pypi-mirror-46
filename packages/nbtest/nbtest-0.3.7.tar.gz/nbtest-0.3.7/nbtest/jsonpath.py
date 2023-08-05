#encoding=utf-8
from __future__ import unicode_literals, print_function, division
from .future2to3 import *

import jsonpath_rw_ext as jpath  # pip install jsonpath_rw_ext
from .Utils import Undef

def jpFinds(jsDc, jsPath, onlyone=None, notNull=False, onlyoneAuto=True, dftRaise=True, dft=Undef):
    """
        print jsFinds({'foo': [{'baz': 1}, {'baz': 2}]}, 'foo[*].baz') #=> [1, 2]
        print jsFinds({'foo': [{'baz': 1}, {'baz': 2}]}, 'foo[0].baz') #=> 1
    """
    #
    if (not jsDc) or (not jsPath):
        raise Exception('#(not jsDc) or (not jsPath), jsDc={!r}, jsPath={!r}'.format(jsDc, jsPath))
    try:
        jsonpath_expr = jpath.parse(jsPath)
        res = [match.value for match in jsonpath_expr.find(jsDc)]
        if len(res) == 0 and notNull:
            raise Exception('#len(res)==0')
        if onlyone or (onlyone == None and onlyoneAuto and (('*' not in jsPath) and ('?' not in jsPath))):
            if len(res) == 1:
                return res[0]
            if dftRaise:
                assert False, 'assert len(res)==1, but res={!r}'.format(res)
            else:
                return dft
        return res
    except Exception as errObj:
        raise Exception('jsPath=%r err=%s' % (jsPath, errObj))