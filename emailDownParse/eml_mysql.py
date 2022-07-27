# -*-coding:utf-8-*-
# @Time : 20220124-20220310
# @Author : xieboyu
# @Project : emailDownParse
import os
import pymysql
from email.parser import Parser
import datetime
import shutil
from email.header import decode_header
import email
import json
from email.utils import parseaddr
# from datetime import datetime

class eml_mysql(object):
    def __init__(self):
        self.__PATHS = [0 for i in range(100)] # 用来存储目标路径下eml文件的列表
        self.__UNPATHS = [0 for i in range(100)] # 用来存储目标路径下无法正常读取的eml文件的列表
        self.__FILE_NUM = 0 # 记录目标路径下无法读取的eml文件的总数
        self.__CONN = None

    def connec_mysql(self): # 输入远程ip, 数据库密码, 数据库名称和用户名来 连接mysql8.0数据库
        print("提示: 本邮箱管理器支持的邮件编码方式为: quoted-printable")
        print(">>>正在进行对数据库的连接: ")
        select_ip = float(input(">>>(1)是否需要进行远程提取:(需要请输入1, 不需要输入非1): "))
        if select_ip == 1:
            ip = input("请输入远程IP: ")
        else:
            ip = input(">>>请输入IP: ")
        passwd = input(">>>请输入数据库密码: ")
        db = input("请输入指定数据库: ")
        user = input("请输入选择用户名: ")
        if select_ip == 1:
            print("正在进行远程请求, 请稍等: ")
        else:
            pass
        try:
            self.__CONN = pymysql.connect( # 连接数据库
                host = ip, # 数据库
                user = user, # 用户名
                passwd = passwd, # 数据库密码
                db = db, # 数据库名称
                charset = 'utf8') # 数据库编码
        except Exception as e:
            print("连接数据库失败: ", e)
        else:
            print("连接数据库成功;")
    
    def if_conn(self): # 判断是否连接数据库
        if self.__CONN is None:
            print("请先进行对mysql数据库的连接: ")
            self.connec_mysql()
        else:
            pass
    def List_FilePATHS(self, target_path): # 递归文件夹下所有eml文件放入列表PATHS中
        k = 0
        for base_path, folder_list, file_list in os.walk(target_path): # 遍历文件夹
            for file_name in file_list:
                file_path = os.path.join(base_path, file_name)
                file_ext = file_path.rsplit('.', maxsplit=1)
                if len(file_ext) != 2: # 没有后缀名, 文件夹
                    self.List_FilePATHS(file_path)
                    continue
                elif file_ext[1] == 'eml': # eml文件
                    self.__PATHS[self.__FILE_NUM] = file_path
                    self.__FILE_NUM = self.__FILE_NUM + 1
                    print(">>>已获得第{0}个eml文件{1}".format(self.__FILE_NUM, file_path))
                    continue
        return True
    
    def clean_uneml(self): # 清除目标路径下无法正常读取的eml文件
        try:
            umeml_path = 

