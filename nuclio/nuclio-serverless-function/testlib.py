import datetime
import pprint
def debug_log(obj=None, msg=None):
    out = str(datetime.datetime.now())
    if obj:
        out += " | " + pprint.pformat(obj)
    if msg:
        out += " | " + msg
    return out
