from paramiko import SSHClient, SFTPClient, AutoAddPolicy
from pathlib import Path
import sys


def upload(host, username, password, local_path, remote_path):
    """
    Upload files or folders to other MacOS/Linux (not windows).
    :param host: remote host.
    :param username: remote user.
    :param password: remote login password.
    :param local_path: upload the specified file or directory from a local host.
    :param remote_path: upload to the specified directory.
    :return: 'Successfully!' or raise exception.
    """
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        with SFTPClient.from_transport(ssh.get_transport()) as sftp:
            _transferring(ssh, sftp, Path(local_path).resolve(), remote_path)
    return 'Successfully!'


def _transferring(ssh, sftp, file_path, remote_path):
    """
    Transfer each file and folder.
    :param ssh: ssh client object.
    :param sftp: sftp client object.
    :param file_path: file or folders that need to be transferred.
    :param remote_path: Current remote path.
    """
    remote_path = f'{remote_path}/{file_path.name}'
    print(remote_path)
    if file_path.is_dir():
        ssh.exec_command(f'mkdir -p {remote_path}')[1].read()
        for f in file_path.iterdir():
            _transferring(ssh, sftp, file_path / f.name, remote_path)
    else: sftp.put(file_path, remote_path)


def _put():
    """Command call interface."""
    params = sys.argv[1:]
    if len(params) == 4: host, username, password, remote_path = params
    elif len(params) == 3:
        host, username, password = params
        remote_path = '.'
    else: return 'Error: please check the command (propor-put <host> <username> <password> <remote_path>).'
    return upload(host, username, password, Path.cwd(), remote_path)
