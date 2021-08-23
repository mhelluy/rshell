# rshell
A restricted shell to use with SSH

# Description
Rshell is a python shell that ains at being used with SSH to give users a stricter access to a remote terminal. With rshell, you can configure permissions about commands which can be runned, but also the paths you want the user to access, the files which can be executed, etc.

## Quick start
First, create a SSH key on **your computer** which will connect to the server through SSH. You can use [ssh-keygen](https://docs.oracle.com/en/cloud/cloud-at-customer/occ-get-started/generate-ssh-key-pair.html) for this.  
Then, copy the content of the public key generated in the `.pub` file. **Don't put it on the server at this point**

Clone the repository on your **remote server** and run the `install_key.py` script:
```bash
git clone https://github.com/mhelluy/rshell.git
python3 rshell/install_key.py
```
You will be asked for which permission file you want to apply and which user configuration to load. For default settings, choose 1 for both.

You need to add a config entry on your local computer to bind your key to the host you want to connect in [~/.ssh/config](https://www.cloudsavvyit.com/4274/how-to-manage-an-ssh-config-file-in-windows-linux). Don't forget to set `IdentitiesOnly` to `yes` if you have several keys set for the same host.

Then, simply connect with the ssh command, and the shell should open !
