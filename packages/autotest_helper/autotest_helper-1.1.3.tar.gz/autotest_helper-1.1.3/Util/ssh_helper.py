#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/3/25 9:16
@Describe: 
"""

import paramiko


class SSH:
    """
        ssh方式上传文件至linux工具类
    """

    def __init__(self, ip="", port=22):
        self.transport = paramiko.Transport((ip, port))
        self.ssh = None

    def login(self, username="", password=""):
        """
            登录linux
        :param username:
        :param password:
        """
        self.transport.connect(username=username, password=password)
        self.ssh = paramiko.SFTPClient.from_transport(self.transport)

    def upload_file(self, local_path="", linux_path=""):
        """
            上传文件至linux
        :param local_path:
        :param linux_path:
        """
        dir_names = linux_path.split("/")
        dir_path = "/"
        war_name = dir_names[len(dir_names) - 1]
        for dir_name in dir_names:
            if dir_name != war_name and dir_name != "":
                dir_path = dir_path + dir_name + "/"
        print("需要判断的路径为：" + dir_path)
        listdir = self.ssh.listdir(dir_path)
        if war_name in listdir:
            print("linux已经存在了该文件，进行删除操作")
            self.ssh.remove(linux_path)
            print("移除" + linux_path)
        self.ssh.put(local_path, linux_path)

    def close_ssh(self):
        """
            关闭ssh连接
        """
        self.transport.close()


class SSHClient:
    """
        远程执行linux命令工具类
    """

    def __init__(self, ip="", username="", password=""):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(ip, 22, username=username, password=password, timeout=20)

    def exe_command(self, cmd=""):
        """
            远程执行linux终端命令
        :param cmd: cd /home/zdtest/release;./jar_test.sh status pushCenter.jar
        :return: 返回命令执行的返回值
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)
        # 获取命令执行结果,返回的数据是一个list
        result = stdout.readlines()
        for i in result:
            print(i)
        return result

    def ssh_client_close(self):
        """
            关闭终端进程
        """
        self.client.close()
