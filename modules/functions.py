from enum import auto
import os,sys
import re
import yaml
from colorama import Fore,Style
from time import time, strftime, localtime
from json import loads as jsload
from json import dumps as jsdump
import modules.autodestroy as autodestroy
import stat
import filecmp

os.system("mkdir {}/.temp{}".format(sys.path[0],os.getpid()))

def dataload(path):
    path = re.sub(r"\.(?:yaml|yml|json)$","",path)
    if os.path.isfile(path+".yaml"):
        return yaml.safe_load(open(path+".yaml","r").read())
    elif os.path.isfile(path+".yml"):
        return yaml.safe_load(open(path+".yml","r").read())
    elif os.path.isfile(path+".json"):
        return jsload(open(path+".json","r").read())
    else:
        print(path)

def datadump(path,data):
    ext = path.split(".")[-1]
    if ext == "yaml" or ext == "yml":
        open(path,"w").write(yaml.safe_dump(data))
    elif ext == "json":
        open(path,"w").write(jsdump(data))


def adDec(func):
    """Decorator for canceling autodestroy at task"""
    def newFunc(*args,**kwargs):
        os.system("rm -rf {}/.temp{}".format(sys.path[0],os.getpid()))
        autodestroy.cancel(autodestroy.ADID)
        return func(*args,**kwargs)
    return newFunc

pathInterpreter = lambda path: os.path.expanduser(path).replace("$$",sys.path[0])


exit = adDec(exit)

stdir = os.getcwd()
os.chdir(sys.path[0])

#load config
config = dataload("config")

if config["timeout_delay"] != "disabled":
    autodestroy.DELAY = config["timeout_delay"]
    autodestroy.ADID = autodestroy.configure(autodestroy.DELAY)

#load lang
lang = dataload("lang/{}".format(config["lang"]))
for instr in lang:
    lang[instr] = lang[instr].strip()

#load perms
perms = dataload("perms/{}".format(sys.argv[1]))
def execute(command,commands):
    history = dataload(pathInterpreter(config["paths"]["cmdhistory"]))
    if history is None:
        history = {}
    if history.get(sys.argv[2]) is None:
        history[sys.argv[2]] = []
    history[sys.argv[2]].append(command.strip())
    datadump(pathInterpreter(config["paths"]["cmdhistory"]),history)
    del history

    if "<" in command or ";" in command or "|" in command or "&" in command or ">" in command:
        print("\001"+Fore.RED+Style.BRIGHT+"\002{}\001".format(lang["invalid_character"])+Style.RESET_ALL+"\002")
        return
    cmd_comp = re.split(r"\s+", command)
    if cmd_comp[0] in perms["commands"]:
        if cmd_comp[0] in commands.__dir__() and cmd_comp[0][0:2] != "__":
            getattr(commands, cmd_comp[0])(*cmd_comp[1:])
        else:
            os.system(command)
    else:
        sys.stdout.write(
            "{} : {}\n".format(lang["forbidden"],command))
    sys.stdout.flush()

    #verify if executable files have been modified
    for i,exec in enumerate(perms["path_executable"]):
        sav_filename = perms["path_executable"][i].replace("/",".")
        if (not os.path.exists(perms["path_executable"][i])) or (not filecmp.cmp(perms["path_executable"][i],"{}/.temp{}/{}".format(sys.path[0],os.getpid(),sav_filename))):
            print("\001"+Fore.RED+Style.BRIGHT+"\002"+lang["error_edit_exec"]+"\001"+Style.RESET_ALL+"\002")
            os.system("cp {}/.temp{}/{} {}".format(sys.path[0],os.getpid(),sav_filename,perms["path_executable"][i]))

os.chdir(stdir)
del stdir

for i,path in enumerate(perms["path"]):
    perms["path"][i] = os.path.abspath(os.path.expanduser(path))

for i,path in enumerate(perms["path_executable"]):
    perms["path_executable"][i] = os.path.abspath(os.path.expanduser(path))
    os.system("cp {} {}/.temp{}/{}".format(perms["path_executable"][i],sys.path[0],os.getpid(),perms["path_executable"][i].replace("/",".")))


expire = dataload("{}/{}".format(pathInterpreter(config["paths"]["userpath"]),sys.argv[2])).get("consoleAccess")
if expire is None:
    expire = 0
def checkPathExec(path):
    for paths in perms["path_executable"]:
        if os.path.abspath(os.path.expanduser(path)).startswith(paths):
            return True
    return False

def checkPath(path):
    for paths in perms["path"]:
        if os.path.abspath(os.path.expanduser(path)).startswith(paths):
            return True
    return False



def getPathArgs(args: list):
    """In a list of args, return the args which are existing path"""
    indexes = []
    for arg in args:
            if type(arg) is str and (os.path.exists(os.path.expanduser(arg)) or os.path.exists(os.path.dirname(os.path.expanduser(arg)))):
                indexes.append(arg)
    return indexes
def autoCheckPath(func):
    """Decorator automatically checking if path specified in command is allowed to user, denies access if it is not.
    WARNING: Experimental feature."""
    def newFunc(*args,**kwargs):
        for arg in args + tuple(kwargs[arg] for arg in kwargs):
            if type(arg) is str:
                filepath = os.path.expanduser(arg)
                dirpath = os.path.dirname(os.path.expanduser(arg))
                if os.path.exists(filepath) or os.path.exists(dirpath):
                    if checkPath(arg):
                        continue
                    else:
                        print("\001"+Fore.RED+"\002"+lang["dir_forbidden"]+" : "+arg+"\001"+Style.RESET_ALL+"\002")
                        return
        return func(*args,**kwargs)
    return newFunc

def checkPathDec(*verifargs):
    def decorator(func):
        def newFunc(*args,**kwargs):
            access = []
            if len(args)==1:
                func(*args,**kwargs)
            else:
                for i in verifargs:
                    if checkPath(args[i]):
                        access.append(1)
                if sum(access) == len(verifargs):
                    func(*args,**kwargs)
                else:
                    print(Fore.RED+lang["dir_forbidden"]+Style.RESET_ALL)
        return newFunc
    return decorator
