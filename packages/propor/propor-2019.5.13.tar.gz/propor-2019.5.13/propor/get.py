from paramiko import SSHClient, SFTPClient, AutoAddPolicy
from pathlib import Path
import stat
import sys


def download(host, username, password, local_path, remote_path):
    """
    Download files or folders from other MacOS/Linux (not windows).
    :param host: remote host.
    :param username: remote user.
    :param password: remote login password.
    :param local_path: download to the specified directory.
    :param remote_path: download the specified file or directory from a remote host.
    :return: 'Successfully!' or raise exception.
    """
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        with SFTPClient.from_transport(ssh.get_transport()) as sftp:
            is_dir = ssh.exec_command(f'file -b {remote_path}')[1].read().decode().strip() == 'directory'
            _transferring(sftp, remote_path, is_dir, Path(local_path))
    return 'Successfully!'


def _transferring(sftp, file_path, is_dir, local_path):
    """
    Transfer each file and folder.
    :param sftp: sftp client object.
    :param file_path: file or folders that need to be transferred.
    :param local_path: Current local path.
    """
    file_name = file_path.split('/')[-1]
    local_path = local_path / file_name
    print(local_path)
    if is_dir:
        local_path.mkdir(parents=True, exist_ok=True)
        for file_attr in sftp.listdir_attr(file_path):
            _transferring(sftp, f'{file_path}/{file_attr.filename}', stat.S_ISDIR(file_attr.st_mode), local_path)
    else: sftp.get(file_path, local_path)


def _get():
    """Command call interface."""
    params = sys.argv[1:]
    if len(params) == 4: host, username, password, remote_path = params
    else: return 'Error: please check the command (propor-get <host> <username> <password> <remote_path>).'
    return download(host, username, password, Path.cwd(), remote_path)
