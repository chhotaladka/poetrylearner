
from time import localtime, strftime

def print_log(msg):
    timestamp = strftime("%d/%m/%Y %H:%M:%S", localtime())
    print("[" + timestamp + "] DBG: " + msg)