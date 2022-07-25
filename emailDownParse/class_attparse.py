# -*-coding:utf-8-*-
# @Time : 20220124-20220310
# @Author : xieboyu
# @Project : emailDownParse
import os
import shutil
import datetime
from email.header import decode_header
from email.parser import Parser
import email
import patoolib
import zipfile
import py7zr

class Uneml_att(object):
    def __init__(self):
        self.__PATHS = [0 for i in range(100)]
        self.__UNPATHS = [0 for i in range(100)]
        self.__FILE_NUM = 0
    def decode_str(self, s): #字符编码转换
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    def List_FilePATHS(self, target_path): # 递归文件夹下所有文件放入列表PATHS, 获得路径下的所有eml文件
        for base_path, folder_list, file_list in os.walk(target_path): # 遍历文件夹
            for file_name in file_list:
                file_path = os.path.join(base_path, file_name)
                file_ext = file_path.rsplit('.', maxsplit=1)
                if len(file_ext) != 2: # 没有后缀名, 说明是文件夹
                    self.List_FilePATHS(file_path)
                    continue
                elif file_ext[1] == 'eml': # 说明是eml文件
                    self.__PATHS[self.__FILE_NUM] = file_path
                    self.__FILE_NUM = self.__FILE_NUM + 1
                    print(">>>已获得第{0}个eml文件{1}".format(self.__FILE_NUM, file_path))
                    continue
        return True

    def get_message(self, path): # 创建消息对象
        if os.path.exists(path):
            fp = self.open_file(path)
            return email.message_from_file(fp)
        else:
            print('文件不存在!')

    def open_file(self, path): # 打开一个文件
        if os.path.exists(path):
            return open(path, 'r')
        else:
            print('文件不存在!')

    def singleatt_down(self, dirpath, atteml_subpath): # 基于DFS的eml循环嵌套解析
        os.chdir(dirpath)

        ttp = False # ttp=false说明 目标路径下还有eml文件没有进行解析
        # dirpath = input(">>>请输入附件保存路径: ")
        for i in range(self.__FILE_NUM):
            if self.__PATHS[i] in self.__PATHS:
                time = datetime.datetime.now() # 系统当前时刻
                if self.__PATHS[i] == 0:
                    pass
                else:
                    try:
                        msg = self.get_message(self.__PATHS[i])
                        text = open(self.__PATHS[i], 'r').read()
                        msg_content = text
                        new_msg = Parser.parsestr(msg_content)
                        attach = self.singleatt_down(msg, dirpath)
                        print(">>>*邮件附件'{0}'成功存入本地目标路径*, time:{1}".format(attach, time))
                        ttp = True
                    except Exception as e:
                        print(">>>*邮件附件'{0}'存入本地目标路径失败*, error:{1}".format(attach, e))
            #将父本eml文件移动到子目录atteml_subpath中防止二次解析
            try:
                shutil.copy(self.__PATHS[i], atteml_subpath)
                os.remove(self.__PATHS[i])
            except Exception as e:
                print(">>>*邮件'{0}'移动路径失败*, error:{1}".format(self.__PATHS[i], e))
            # 更新列表PATHS和FILE_NUM
            self.__PATHS.remove(self.__PATHS[i])
            self.__FILE_NUM = 0
            self.List_FilePATHS(dirpath)
            




