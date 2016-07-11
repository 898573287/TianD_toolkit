#coding:utf-8
'''
Created on 2016年7月8日 下午3:13:55

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:

'''

from functools import wraps
import maya.cmds as mc

def undo(func):
    """ Puts the wrapped `func` into a single Maya Undo action, then 
        undoes it when the function enters the finally: block """
    @wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunkw
            mc.undoInfo(ock=True)
            return func(*args, **kwargs)
        finally:
            # after calling the func, end the undo chunk and undo
            mc.undoInfo(cck=True)
            mc.undo()

    return _undofunc