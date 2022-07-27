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

    def singleatt_down(self, message, savepath): # 对单个附件eml进行解析得到其附件eml的附件
        attachments = []
        for part in message.walk(): # 循环信件中的每一个mime数据块
            filename = part.get_filename()
            if filename: # 如果附件存在名字, 说明该附件eml还有附件
                filename = self.decode_str(filename)
                data = part.get_payload(decode=True)
                abs_filename = os.path.join(savepath, filename)
                attach = open(abs_filename, 'wb')
                attachments.append(filename)
                attach.write(data)
                attach.close()
        return attachments

    def get_allemlatt(self, dirpath, atteml_subpath): # 基于DFS的eml循环嵌套解析
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
            print('*************************************')
            if any(name.endswith(('.eml')) for name in os.listdir(dirpath)): # 如果目标路径下还有eml文件, 就继续循环, 重复进行解析
                try:
                    self.get_allemlatt(dirpath, atteml_subpath)
                except Exception as e:
                    print(f"eml解析附件失败: {e}")
                    ttp = False
            else:
                print("目标路径下已经没有eml文件")
                ttp = True # ttp=false说明 目标路径下所有eml都已经完成了解析
                return ttp

            if ttp == True:
                break
            else:
                continue
        return ttp

class Unzip_att(object): # 对附件的zip文件进行操作, 解决了中文名称多目录zip文件的循环解析问题
    def __init__(self):
        self.__PATHS = [0 for i in range(100)]
        self.__UNPATHS = [0 for i in range(100)]
        self.__FILE_NUM = 0

    def decode_str(self, str): # 针对中文文件, 先使用cp437编码成bytes, 再以gbk格式解码成中文string
        try:
            string = str.encode('cp437').decode('gbk')
        except:
            string = str.encode('utf-8').decode('gbk')
        return string

    def decode_path(self, path): # 针对中文名称文件夹, 先使用cp437编码成bytes, 再以gbk格式解码成中文string
        try:
            path_name = path.decode('utf-8')
        except:
            path_name = path.encode('cp437').decode('gbk')
            path_name = path_name.encode('utf-8').decode('utf-8')
        return path_name

    def List_FilePATHS(self, target_path): # 递归文件夹下所有文件放入列表PATHS, 获得路径下的所有zip文件
        for base_path, folder_list, file_list in os.walk(target_path): # 遍历文件夹
            for file_name in file_list:
                file_path = os.path.join(base_path, file_name)
                file_ext = file_path.rsplit('.', maxsplit=1)
                if len(file_ext) != 2: # 没有后缀名, 文件夹
                    self.List_FilePATHS(file_path)
                    continue
                elif file_ext[1] == 'zip': # zip文件
                    self.__PATHS[self.__FILE_NUM] = file_path
                    self.__FILE_NUM = self.__FILE_NUM + 1
                    print(">>>已获得第{0}个zip文件{1}".format(self.__FILE_NUM, file_path))
                    continue
        return True

    def single_extract_zip(self, file, target_dir): # 对单个zip文件进行解压操作
        attname = []
        try: # 如果压缩文件zip中含有多目录
            if file.endswith(".zip"):
                with zipfile.ZipFile(file, allowZip64=True) as Z:
                    # print("Z.filelist", Z.filelist)
                    file_iter = (fileone for fileone in Z.filelist if os.path.isfile(file))
                    for file_one in file_iter:
                        file_one.filename = self.decode_path(file_one.filename) # 防止出现乱码
                        # print(file_one)
                        Z.extract(file_one, target_dir)
                        attname.append(file_one)
        except: # zip文件中没有多目录
            try:
                ## 解压方式2: 防止乱码
                azip = zipfile.ZipFile(file, 'r')
                # 返回所有文件夹和文件
                zip_list = azip.namelist()
                for zip_file in zip_list:
                    azip.extract(zip_file, target_dir)
                    attname.append(zip_file)
                azip.close()
            except Exception as e:
                print(f"文件解压失败: {e}")
        return attname

    def get_allzipres(self, dirpath, attzip_subpath): # 基于DFS的zip循环嵌套解压
        os.chdir(dirpath)

        ttp = False  # ttp=false说明 目标路径下还有zip文件没有进行解压
        for i in range(self.__FILE_NUM):
            if self.__PATHS[i] in self.__PATHS:
                time = datetime.datetime.now()  # 系统当前时刻
                if self.__PATHS[i] == 0:
                    pass
                else:
                    try:
                        attach = self.single_extract_zip(self.__PATHS[i], dirpath)
                        print(">>>*zip文件解压所得附件'{0}'成功存入本地目标路径*, time:{1}".format(attach, time))
                        ttp = True
                    except Exception as e:
                        print(">>>*zip文件解压所得附件'{0}'存入本地目标路径失败*, error:{1}".format(attach, e))
            # 将zip文件移动到子目录attzip_subpath中防止二次解压
            try:
                shutil.copy(self.__PATHS[i], attzip_subpath)
                os.remove(self.__PATHS[i])
            except Exception as e:
                print(">>>*zip文件'{0}'移动路径失败*, error:{1}".format(self.__PATHS[i], e))
            # 更新列表PATHS和FILE_NUM
            self.__PATHS.remove(self.__PATHS[i])
            self.__FILE_NUM = 0
            self.List_FilePATHS(dirpath)
            print('*************************************')
            if any(name.endswith(('.zip')) for name in os.listdir(dirpath)):  # 如果目标路径下还有eml文件, 就继续循环, 重复进行解析
                try:
                    self.get_allzipres(dirpath, attzip_subpath)
                except Exception as e:
                    print(f"zip解压失败: {e}")
                    ttp = False
            else:
                print("目标路径下已经没有zip文件")
                ttp = True  # ttp=false说明 目标路径下所有zip都已经完成了解压
                return ttp

            if ttp == True:
                break
            else:
                continue
        return ttp

def uneml_run():
    test_uneml = Uneml_att()
    target_path = input(">>>请输入附件eml文件本地存储路径: ")
    # 创建同级目录来存放解析完成的eml
    os.chdir(os.path.abspath(os.path.dirname(target_path)))
    newpath = "sorted_att"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    subemlpath = "att_eml"
    if not os.path.exists(subemlpath):
        os.makedirs(subemlpath)
    # subemlpath即为存储父本eml的子目录路径
    subemlpath = os.path.abspath(os.path.dirname(target_path)) + '/' + newpath + '/' + subemlpath
    print(subemlpath)
    if os.path.exists(target_path):
        print(">>>[1].目录存在, 准备读文件: \n")
        if test_uneml.List_FilePATHS(target_path):
            print(">>>[2].已成功得到所有eml文件: \n")
            print("开始下载邮件附件到本地")
            if test_uneml.get_allemlatt(target_path, subemlpath) == False:
                print("目标路径下存在 解析失败 的eml文件 \n")
            else:
                print("目标路径下所有eml文件都已完成解析 \n")

        else:
            print(">>>[-2].未成功得到所有eml文件: \n")
    else:
        print(">>>[-1].目录不存在, 请重新输入目录路径 \n")
        print("=======================================\n")

def unzip_run():
    test_unzip = Unzip_att()
    target_path = input(">>>请输入附加zip文件本地存储路径: ")
    # 创建同级目录来存放解压完成的zip文件
    os.chdir(os.path.abspath(os.path.dirname(target_path)))
    newpath = "sorted_att"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    subzippath = "att_zip"
    if not os.path.exists(subzippath):
        os.makedirs(subzippath)
    # subzippath即为存储父本zip的子目录路径
    subzippath = os.path.abspath(os.path.dirname(target_path)) + '/' + newpath + '/' + subzippath
    print(subzippath)
    if os.path.exists(target_path):
        print(">>>[1].目录存在, 准备读文件: \n")
        if test_unzip.List_FilePATHS(target_path):
            print(">>>[2].已成功得到所有zip文件: \n")
            print("开始解压zip到本地")
            if test_unzip.get_allzipres(target_path, subzippath) == False:
                print("目标路径下存在 解压失败 的zip文件 \n")
            else:
                print("目标路径下所有zip文件都已完成解析 \n")

        else:
            print(">>>[-2].未成功得到所有zip文件: \n")
    else:
        print(">>>[-1].目录不存在, 请重新输入目录路径 \n")
        print("=======================================\n")


