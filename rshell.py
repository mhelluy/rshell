#!/usr/bin/env python3
import os
import sys
import modules.autodestroy as autodestroy
try:
    from genericpath import isdir
    from posix import listdir
    import readline
    import glob
    from socket import gethostname
    from commands import expire,checkPath, commands, perms, Fore, Style, strftime, localtime, time, re, execute, exit, lang, config


    if int(time()) > int(expire):
        print(Fore.RED+strftime("{} :\n{}".format(lang["access_denied"], lang["expired_access"]) +
                                Style.RESET_ALL, localtime(expire)))
        exit(0)

    running = True


    def completer(text, state):
        listdirv = [path+"/" if os.path.isdir(path) else path for path in glob.glob(os.path.expanduser(text)+"*") if path.startswith(text) and checkPath(path)]
        options = [i for i in perms["commands"] if i.startswith(text)] + listdirv if len(listdirv) < 50 else []
        if state < len(options):
            return options[state]
        else:
            return None


    readline.set_completer_delims('\t\n `!@#$%^&*()-=+[{]}\\|;:\'",<>?')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    prefix = os.getlogin()+"@"+gethostname()

    if len(perms["path"]) == 0:
        raise ValueError("Users must have at least one directory allowed in permission file.")

    while running:
        if not checkPath(os.getcwd()):
            os.chdir(perms["path"][0])
        if len(sys.argv) > 3:
            command = " ".join(sys.argv[3:])
            running = False
        else:
            sys.stdout.flush()
            try:
                command = input("\001"+Fore.CYAN+Style.BRIGHT+"\002"+prefix+"\001"+Fore.RESET+"\002"+":"+"\001"+Fore.BLUE+"\002" +
                                re.sub(r"^"+os.path.expanduser("~"), "~", os.getcwd())+"\001"+Style.RESET_ALL+"\002""$ ").strip()
                autodestroy.cancel(autodestroy.ADID)
                autodestroy.ADID = autodestroy.configure(autodestroy.DELAY)
            except KeyboardInterrupt:
                sys.stdout.write("\n")
                continue
            except EOFError:
                sys.stdout.write("\n")
                exit(0)
            if not command:
                continue
        
        execute(command,commands)
except Exception as e:
    #delete autodestroy task on error
    os.system("rm -rf {}/.temp{}".format(sys.path[0],os.getpid()))
    autodestroy.cancel(autodestroy.ADID)
    raise e

os.system("rm -rf {}/.temp{}".format(sys.path[0],os.getpid()))
autodestroy.cancel(autodestroy.ADID)