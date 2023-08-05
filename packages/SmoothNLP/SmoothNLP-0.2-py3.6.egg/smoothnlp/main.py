global __name__
__name__ = "SmoothNLP"

import smoothnlp.jvm as jvm
from smoothnlp.jvm import initJVMConnection
from server import smoothNlpRequest

smoothnlp_local = jvm.LazyLoadingJClass("com.smoothnlp.nlp.SmoothNLP")
smoothnlp_server = smoothNlpRequest()


def set_property(*args):
    def decorate_func(func):
        for i in range (0, len(args),2):
            setattr(func, args[i], args[i+1])
        return func
    return decorate_func


########################
## smoothnlp function ##
########################

@set_property("name":"segment")
def _segment(text:str,module='server'):
     if module == 'server':
        return smoothnlp_server.
     else
        try:
            return smoothnlp.segment(text)
