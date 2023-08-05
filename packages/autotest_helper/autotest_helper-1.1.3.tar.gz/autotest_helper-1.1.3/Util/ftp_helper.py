#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/3/25 9:16
@Describe: 
"""
import ftplib
import os


class FTP:
    """
        FTP上传下载工具类
    """

    def __init__(self, host="", port=21):
        self.ftp = ftplib.FTP()
        self.ftp.connect(host, port)

    def login(self, username="", password=""):
        """
            登录ftp
        """
        self.ftp.login(username, password)
        print(self.ftp.welcome)

    def download_file(self, local_file, remote_file):
        """
        拉取文件到本地
        :param local_file:
        :param remote_file:
        :return:
        """
        handler = open(local_file, 'wb')
        self.ftp.retrbinary("RETR %s" % remote_file, handler.write)
        handler.close()
        return True

    def upload_file(self, local_file, remote_file):
        """
        上传文件至服务器
        :param local_file:
        :param remote_file:
        :return:
        """
        global file_handler
        if not os.path.isfile(local_file):
            return False
        file_handler = open(file=local_file, mode='rb+')
        try:
            print(remote_file)
            self.ftp.delete(remote_file)
        except Exception as e:
            print(e)
        self.ftp.storbinary('STOR ' + remote_file, file_handler)
        file_handler.close()
        return True

    def upload_file_tree(self, local_dir, remote_dir):
        """
            上传文件夹
        :param local_dir:
        :param remote_dir:
        :return:
        """
        if not os.path.isdir(local_dir):
            return False
        local_file_names = os.listdir(local_dir)
        for Local in local_file_names:
            if Local != "Security":
                src = os.path.join(local_dir, Local)
                self.ftp.cwd(remote_dir)
                if os.path.isdir(src):
                    print("文件夹"+Local)
                    nlst = self.ftp.nlst(remote_dir)
                    if Local in nlst:
                        print("文件存在")
                    else:
                        print(Local+"在服务器上不存在")
                        self.ftp.mkd(Local)
                        print(Local+"在服务器已经创建")
                    self.upload_file_tree(src, remote_dir+"\\"+Local)
                else:
                    print(
                        "-------------------------------上传开始" + Local.__str__() + "-----------------------------------------")
                    self.upload_file(src, Local)
                    print(
                        "-------------------------------上传完毕" + Local.__str__() + "-----------------------------------------")
        return
