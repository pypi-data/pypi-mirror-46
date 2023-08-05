#!/usr/bin/python
import paramiko, time


def _getsshdata(host, port, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    conn = ssh.connect(host, port=port, username=user, password=passwd, timeout=5, look_for_keys=False)
    remote_conn = ssh.invoke_shell()
    cnt = remote_conn.send(cmd)
    time.sleep(4)
    output = remote_conn.recv(20000)
    return output


def _getsshdata1(host, port, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    conn = ssh.connect(host, port=port, username=user, password=passwd, timeout=5, look_for_keys=False)
    remote_conn = ssh.invoke_shell()
    cnt = remote_conn.send(cmd)
    time.sleep(2)
    output = remote_conn.recv(10000)
    return output


def _getsshdata2(host, port, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    conn = ssh.connect(host, port=port, username=user, password=passwd, timeout=5, look_for_keys=False)
    remote_conn = ssh.invoke_shell()
    cnt = remote_conn.send(cmd)
    time.sleep(1)
    output = remote_conn.recv(5000)
    return output


def _getsshdata3(host, port, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    conn = ssh.connect(host, port=port, username=user, password=passwd, timeout=15, look_for_keys=False)
    remote_conn = ssh.invoke_shell()
    cnt = remote_conn.send(cmd)
    time.sleep(10)
    output = remote_conn.recv(50000)
    return output


def _getsshdata4dnsClearContextGn(host, port, user, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    conn = ssh.connect(host, port=port, username=user, password=passwd, timeout=7, look_for_keys=False)
    remote_conn = ssh.invoke_shell()
    remote_conn.send('context Gn\n')
    time.sleep(1)
    cnt = remote_conn.send('clear dns-client dns-1 cache\n')
    time.sleep(1)
    output = remote_conn.recv(10000)
    return output


def _getsshdata5(host, port, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    conn = ssh.connect(host, port=port, username=user, password=passwd, timeout=5, look_for_keys=False)
    remote_conn = ssh.invoke_shell()
    cnt = remote_conn.send(cmd)
    time.sleep(1)
    output = remote_conn.recv(2000)
    return output
