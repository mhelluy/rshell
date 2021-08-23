#!/usr/bin/env python3

from sys import argv, path
from os import listdir, chdir, system
from os import path as ospath

def dataload(path):
    import re, json, yaml
    path = re.sub(r"\.(?:yaml|yml|json)$","",path)
    if ospath.isfile(path+".yaml"):
        return yaml.safe_load(open(path+".yaml","r").read())
    elif ospath.isfile(path+".yml"):
        return yaml.safe_load(open(path+".yml","r").read())
    elif ospath.isfile(path+".json"):
        return json.loads(open(path+".json","r").read())

chdir(path[0])

config = dataload("config")

if len(argv) <= 1:
    print("You have to specify the public key to add :\nThe command should look like : {} ssh-rsa XXX..XXX user@example.fr".format(argv[0]))
    exit()

while True:
    print("Which permission file you want to apply to the user ?")
    permfiles = [".".join(f.split(".")[0:-1]) for f in sorted(listdir("perms"))]

    for i,permf in enumerate(permfiles):
        print(" [{}] {}".format(i+1,permf))

    try:
        perm = permfiles[int(input("? (1--{}) ".format(len(permfiles)))) - 1]
    except IndexError:
        print("Incorrect ID.\n\n")
    except ValueError:
        print("Incorrect ID.\n\n")
    except EOFError:
        print()
        exit()
    else:
        break

while True:
    print("Which user do you want to assign to this key ?")
    userfiles = [".".join(f.split(".")[0:-1]) for f in sorted(listdir(ospath.expanduser(config["paths"]["userpath"].replace("$$",path[0]))))]

    for i,userf in enumerate(userfiles):
        print(" [{}] {}".format(i+1,userf))

    try:
        user = userfiles[int(input("? (1--{}) ".format(len(userfiles)))) - 1]
    except IndexError:
        print("Incorrect ID.\n\n")
    except ValueError:
        print("Incorrect ID.\n\n")
    except EOFError:
        print()
        exit()
    else:
        break

chdir(ospath.expanduser("~"))

system("mkdir -p .ssh/")
system("touch .ssh/authorized_keys")

open(".ssh/authorized_keys","a").write('\ncommand="python3 {0}/rshell.py {1} {2}" {3}'.format(path[0],perm,user," ".join(argv[1:])))
print("The key has been written is authorized keys.")