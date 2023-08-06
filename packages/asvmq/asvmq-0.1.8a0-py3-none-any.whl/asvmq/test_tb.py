import sys
import traceback
import asvmq

def excepthook(exctype, excvalue, exctb):
    err_traceback = traceback.format_exception(exctype, excvalue, exctb)
    asvmq.log_fatal("".join(err_traceback))

sys.excepthook = excepthook

raise Exception("Hello world")
