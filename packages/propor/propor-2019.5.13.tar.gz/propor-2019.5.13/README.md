# Propor
Project porter, easy and quick command-based startup, support file and folder transfer. 

## Install
```
pip3 install propor --upgrade
```

## Usage
First, enter the project directory and open the command line interface, then enter the command:
```
# propor-get 192.168.0.1 root 123456 project
>>> propor-get <host> <username> <password> <remote_path>
>>> propor-put <host> <username> <password> <remote_path>

```
- only remote host systems are supported: `Linux/MacOS`
- `propor-get`: transfer the remote host specified directory to the current directory.
- `propor-put`: transfer the current directory to the remote host specified directory.
- `host`: remote host.
- `username`: remote user.
- `password`: remote login password.
- `remote_path`: remote host specified directory.
- in the program, you can use the `from propor import download, upload` import method.
