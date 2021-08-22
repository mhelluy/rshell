"""Make the user disconnect automatically if no commands are issued within the delay specified
Comment all the file or comment the line "import modules.autodestroy as autodestroy" in functions.py to disable this feature"""
import os
import re
from subprocess import Popen as pop
from subprocess import PIPE
import signal

ADID = None
DELAY = None

def timeouthandler(a,b):
    print(f"Connection timed out : no interaction from user within {DELAY}.")
    exit()
signal.signal(signal.SIGTERM,timeouthandler)

def configure(tps):
    p = pop("at now + {}".format(tps).split(" "),stdin=PIPE,stdout=PIPE,stderr=PIPE)
    return int(re.search(r"job\s+([0-9]+)\s+at",p.communicate(input="kill -15 {0}\n".format(os.getpid()).encode())[1].decode()).group(1))

def cancel(id):
    if id is not None:
        pop(["atrm",str(id)],stdout=PIPE,stderr=PIPE).communicate()