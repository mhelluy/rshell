# rshell
A restricted shell to use with SSH

# Description
Rshell is a python shell that ains at being used with SSH to give users a stricter access to a remote terminal. With rshell, you can configure permissions about commands which can be runned, but also the paths you want the user to access, the files which can be executed, etc.

## Quick start
First, create a SSH key on **your computer** which will connect to the server through SSH. You can use [ssh-keygen](https://docs.oracle.com/en/cloud/cloud-at-customer/occ-get-started/generate-ssh-key-pair.html) for this.  
Then, copy the content of the public key generated in the `.pub` file. **Don't put it on the server at this point.**

Clone the repository on your **remote server** and run the `install_key.py` script:
```bash
git clone https://github.com/mhelluy/rshell.git
python3 rshell/install_key.py "<paste your public key here (with quotes)>"
```
*Note: if an exception `ModuleNotFoundError` is raised, run `python3 -m pip install <module name>`.*

You will be asked for which permission file you want to apply and which user configuration to load. For default settings, choose 1 for both.

You need to add a config entry on your local computer to bind your key to the host you want to connect in [~/.ssh/config](https://www.cloudsavvyit.com/4274/how-to-manage-an-ssh-config-file-in-windows-linux). Don't forget to set `IdentitiesOnly` to `yes` if you have several keys set for the same host.

Then, simply connect with the ssh command, and the shell should open !

## Configuration
Rshell supports YML/YAML and JSON data format for configuration. To switch to another data format you just need to change the file extension (obviously, the content has to be in the corresponding format to be correctly decoded).

### config.yaml
default file content:
```yaml
paths:
  # $$ is the directory where rshell.py is
  userpath: $$/users
  cmdhistory: $$/cmdhistory.yaml
lang: "en-US" #langs are in the langs folder. currently only fr-FR and en-US are available
timeout_delay: 1 hour #'disabled' to disable the delay.
```

### Permissions files
You can create several permissions files that give access to commands and paths.  
The permission file which is loaded is specified when you add the ssh-key with the `install_key.py` script.
Content of defaut permission file :
```yaml
commands:
  - date
  - ls
  - exit
  - scp
  - rsync
  - expire
  - cd
  - execute
  - nano
  - edit
  - cp
  - mkdir
  - rm
  - rmdir
  - help
  - touch
  - mv
  - cat
  - type
  - dir
path:
  - ~/testpath
path_executable: []
```
Commands are either existing UNIX commands, or new commands that can be added in the `commands.py` file. The commands in `commands.py` overwrite the UNIX commands.  
The path_executable entry must contains all the paths of the scripts that you want the user to be able to execute. The executable files cannot be edited, they can only be read, and executed using `execute <file>`.

**WARNING :** by default, the UNIX commands are not configured to consider the paths specified in permission file. You'll need to overwrite them in `commands.py`. (See `base_commands.py` for an example). Most time, a method executing...
```python
os.system("<command> +" ".join(args))
```
...decorated with `@autoCheckPath` will work.

### Users files
Users files currently only contain the ssh-access expiration date. The `consoleAccess` entry must be an integer that represents the time in UNIX format (number of seconds since 1970.01.01). 
