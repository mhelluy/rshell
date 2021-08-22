from modules.functions import *


class BaseCommands:
    @autoCheckPath
    def touch(self, *args):
        os.system("touch "+" ".join(args))
    touch.help = lambda: os.system("man touch")

    @autoCheckPath
    def mv(self, *args):
        os.system("mv "+" ".join(args))
    mv.help = lambda: os.system("man mv")

    @autoCheckPath
    def cat(self, *args):
        os.system("cat "+" ".join(args))
    cat.help = lambda: os.system("man cat")
    type = cat

    @checkPathDec(1)
    def nano(self, path=None, *args):
        if checkPathExec(path):
            print()
        if len(args) == 0 and path is not None:
            os.system(f"nano -T4 -m -E -b {path}")
        else:
            print("\001"+Fore.RED+"\002{}: nano <{}>\001".format(
                lang["usage"], lang["file_to_edit"])+Style.RESET_ALL+"\002")
    nano.help = lambda: print("\001"+Fore.RED+"\002{}: nano <{}>\001".format(
        lang["usage"], lang["file_to_edit"])+Style.RESET_ALL+"\002")
    edit = nano

    @checkPathDec(2)
    def scp(self, option=None, path=None, *args):
        if option in ("-f", "-t") and len(args) == 0:
            os.system(f"scp {option} {path}")
        else:
            print("\001"+Fore.RED +
                  "\002{}.\001".format(lang["forbidden"])+Style.RESET_ALL+"\002")
    scp.help = lambda: print(lang["no_description"])

    def expire(self, *args):
        print(strftime(lang["expire_access"],
                       localtime(expire)))
    expire.help = lambda: print(lang["no_description"])

    @autoCheckPath
    def cd(self, dir=None, *args):
        if dir is None:
            dir = "~" if checkPath("~") else perms["path"][0]
        try:
            os.chdir(os.path.expanduser(dir))
        except FileNotFoundError:
            print("{} : {} ({})".format(
                lang["error"], lang["unknown_path"], dir))
    cd.help = lambda: print(lang["usage"], ": cd <{}>".format(lang["dir"]))

    def exit(self, *args):
        exit(0)
    exit.help = lambda: print("Exit the terminal.")

    @autoCheckPath
    def cp(self, *args):
        os.system("cp "+" ".join(args))
    cp.help = lambda: os.system("man cp")

    @autoCheckPath
    def rm(self, *args):
        os.system("rm "+" ".join(args))
    rm.help = lambda: os.system("man rm")

    @autoCheckPath
    def mkdir(self, *args):
        os.system("mkdir "+" ".join(args))
        pathargs = getPathArgs(args)
        for patharg in pathargs:
            if not checkPath(patharg):
                print("\001"+Fore.RED+"\002" +
                      lang["dir_forbidden"]+" : "+patharg+"\001"+Style.RESET_ALL+"\002")
                os.system("rmdir "+" ".join([arg for arg in args if arg not in (
                    "-m", "--mode", "-v", "--verbose", "-Z", "--context")]))
                break
    mkdir.help = lambda: os.system("man mkdir")

    @autoCheckPath
    def rmdir(self, *args):
        os.system("rmdir "+" ".join(args))
    rmdir.help = lambda: os.system("man rmdir")

    @autoCheckPath
    def ls(self, *args):
        for arg in args:
            if re.match(r"^-[a-zA-Z\-]$",arg):
                os.system("ls "+" ".join(args))
                return
        if not len(args):
            args = ["."]
        cwd = os.getcwd()
        ls_path = os.path.abspath(os.path.expanduser(args[0]))
        if os.path.exists(ls_path):
            os.chdir(ls_path)
        else:
            print("{} : {} ({})".format(lang["error"], lang["unknown_path"], ls_path))
            return
        for file in sorted(os.listdir()):
            if checkPath(file):
                if os.path.isdir(file):
                    print(Fore.BLUE+file+Style.RESET_ALL)
                else:
                    print(Fore.RED+file+Style.RESET_ALL)
        os.chdir(cwd)
    ls.help = lambda: print("{} : ls <{}>".format(lang["usage"], lang["dir"]))
    dir = ls

    @autoCheckPath
    def rsync(self, *args):
        os.system("rsync "+" ".join(args))
    rsync.help = lambda: os.system("man rsync")

    @autoCheckPath
    def execute(self, *args):
        """Run a command, a script."""
        cmddelimiter = 0
        if len(args) == 0:
            self.execute.help()
            return
        if args[0] == "in":
            if checkPath(args[1]):
                if os.path.isdir(args[1]):
                    os.chdir(args[1])
                else:
                    print("{} : {} ({})".format(lang["error"], lang["unknown_path"], args[1]))
                    return
            else:
                print("\001" + Fore.RED + "\002" +
                      lang["dir_forbidden"] + "\001" + Style.RESET_ALL + "\002")
                return
            cmddelimiter = 2
        if os.path.isfile(os.path.expanduser(args[cmddelimiter])) and checkPathExec(os.path.expanduser(args[cmddelimiter])):
            os.system("{} {}".format(os.path.abspath(os.path.expanduser(
                args[cmddelimiter])), " ".join(args[cmddelimiter+1:])))
        else:
            command = " ".join(args[cmddelimiter:])
            if command != "":
                execute(command, self)
    execute.help = lambda: print("{} : execute [in <{}>] <{}|{}>".format(
        lang["usage"], lang["dir"], lang["command"], lang["file"]))

    def help(self, *args):
        cmds = sorted(perms["commands"])
        if len(args) == 0:
            print(lang["available_commands"]+" :")
            for cmd in cmds:
                print(" - "+cmd)
        elif args[0] in cmds:
            if args[0][0:2] != "__" and args[0] in self.__dir__():
                attr = getattr(self, args[0])
                try:
                    attr.help()
                except AttributeError:
                    help(attr)
            else:
                os.system("man "+args[0])
        else:
            print("{} : help {}\n".format(lang["forbidden"], args[0]))
