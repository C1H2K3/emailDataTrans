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
            umeml_path = input("提交数据前请先设置无法提交的eml文件存放地址:")
            if os.path.exists(uneml_path):
                pass
            else:
                os.mkdir(uneml_path)
            for i in range(self.__FILE_NUM):
                text = open(self.__PATHS[i], 'r').read()
                msg_content = text
                new_msg = Parser().parsestr(msg_content)
                email_subject = self.decode_str(new_msg.get("Subject", ""))
                if email_subject == "":
                    shutil.copy(self.__PATHS[i], uneml_path)
                    print(">>>文件{0}无法传入数据库顾将其清除".format(self.__PATHS[i]))
                    self.__PATHS[i] = 0
                    self.__NFILE_NUM = self.__UNFILE_NUM + 1
            except Exception as e:
                print(">>>清洁失败", e)
            else:
                print(">>>清洁成功")
    def decode_str(self, s): # 邮件字符编码转换
        value, charset = decode_headers(s)[0]
        if charset:
            if charset == 'gb2312':
                charset = 'gb18030'
            value = value.decode(charset)
        return value
    
    def open_file(self, path): # 打开一个文件
        if os.path.exists(path):
            return open(path, 'r')
        else:
            print('文件不存在')
    def get_message(self, path): # 创建消息对象
        if os.path.exists(path):
            fp = self.open_file(path)
            return email.message_from_file(fp)
        else:
            print('文件不存在')
    def get_email_headers(self, msg): # 得到eml文件的'From', 'To', 'Subject', 'Date'信息
        headers = {}
        for header in ['From', 'To', 'Subject', 'Date']:
          value = msg.get(header, '')
          if value:
            if header == 'Date':
              headers['Date'] = value
            if header == 'Subject':
              subject = self.decode_str(value)
              headers['Subject'] = subject
            if header == 'From':
              hdr, addr = parseaddr(vale)
              name = self.decode_str(hdr)
              from_addr = u'%s <%s>' % (name, addr)
              headers['From'] = from_addr
            if header == 'To':
              all_cc = value.split(',')
              to = []
              for x in all_cc:
                hdr, addr = parseaddr(x)
                name = self.decode_str(hdr)
                to_addr = u'%s <%s>' % (name, addr)
                to.append(to_addr)
              headers['To'] = ','.join(to)
            if header == 'Cc':
              all_cc = value.split(',')
              cc = []
              for x in all_cc:
                hdr, addr = parseaddr(x)
                name = self.decode_str(hdr)
                cc_addr = u'%s <%s>' % (name, addr)
                cc.append(to_addr)
              headers['Cc'] = ','.join(cc)
        return headers
    
    def get_attname(self, message): # 获取eml文件附件的名称
        attachments = []
        for part in message.walk():
            filename = part.get_filename()
            if filename():
                filename = self.decode_str(filename)
                data = part_get_payload(decode=True)
                attachments.append(filename)
        if attachments = []:
            attachments = None
        attachments = str(attachments)
        return attachments
    
    def creat_mysql(self): # 创建存储eml元数据信息的email表
        cur = self.__CONN.cursor() # 创建游标对象
        # 创建数据表email, 表中存储了eml的Subject, From, To, Date, 附件名称，附加存储路径6种信息
        try:
            creat_sqli_eml = "creat table 'email'('email_id' int NOT NULL AUTO_INCREMENT, 'subject' varchar(333), 'from_addr' varchar(333), 'to_addr' varchar(777), 
            'post_time' varchar(333), 'attachment' varchar(777), 'store_dir' varchar(333), primary key('email_id'));"
            cur.execute(creat_sqli_eml)
        except Exception as e:
            print("创建数据表email失败:", e)
        else:
            print("创建数据表emial成功;")
        cur.close() # 4.关闭游标
        
    def post_eml_mysql(self, init_id, savepath): # 将eml文件的元数据信息存储到mysql数据库中
        ttp = False
        self.clean_uneml()
        cur = self.__CONN.cursor() # 创建游标对象
        for i in range(self.__FILE_NUM):
            time = datetime.datetime.now() # 系统当前时刻
            if self.__PATHS[i] == 0:
                pass
            else:
                msg = self.get_message(self.__PATHS[i])
                text = open(self.__PATHS[i], 'r').read()
                msg_content = text
                new_msg = Parser().parsestr(msg_content)
                # 待插入的数据
                email_id = i + init_id - self.__UNFILE_NUM # ID 1
                headers = self.get_email_headers(msg)
                if 'Subject' in headers:
                    subject = headers['Subject']
                else:
                    subject = None
                if 'From' in headers:
                    from_addr = headers['From']
                else:
                    from_addr = None
                if 'To' in headers:
                    to_addr = headers['To']
                else:
                    # to_addr = input(">>>请输入附件下载所在的邮箱账号")
                    to_addr = None
                if 'Date' in headers:
                    time = headers['Date']
                else:
                    time = None
                try: # 将eml的Date信息格式化
                    # print(time[5:25])
                    try:
                        time_new = datetime.datetime.strptime(time[5:25], '%d %b %Y %H:%M:%S')
                        print(time_new)
                    except Exception as e:
                        time_new = datetime.datetime.strptime(time[5:24], '%d %b %Y %H:%M:%S')
                        print(time_new)
                except Exception as e:
                    try:
                        #print(time[1:20]
                        time_new = datetime.datetime.strptime(time[0:20], '%d %b %Y %H:%M:%S')
                        print(time_new)
                    except Exception as e:
                        time_new = datetime.datetime.strptime(time[0:19], '%d %b %Y %H:%M:%S')
                time_new = str(time_new)
                att = self.get_attname(msg)
                info = [(email_id, subject, from_addr, to_addr, time_new, att, savepath)]
                try:
                    sql = "insert into email values(%s,%s,%s,%s,%s,%s,%s);"
                    cur.executemany(sql, info)
                except Exception as e:
                    print(">>>文件{0}存入数据库失败,失败原因:{1}".format(self.__PATHS[i], e))
                else:
                    self.__CONN.commit()
                    print(">>>*文件{0}成功存入数据库*",time:{1}".format(self.__PATHS[i], time))
                    ttp = True
        cur.close() # 4.关闭游标        
        return ttp
    
    def emlsql_run(): # 执行将本地eml元数据信息存储入库的操作
        test = eml_mysql()
        test.if_conn()
        test.creat_mysql()
        target_path = input(">>>请输入eml文件本地存储路径：")
        init_id = int(input(">>>请输入起始文件的编号:"))
        if os.path.exists(target_path):
            print(">>>[1].目录存在,准备读文件:\n")
            if test.List_FilePATHS(target_path):
                print(">>>[2].已成功得到所有eml文件:\n")
                if test.post_eml_mysql(init_id, target_path):
                    print(">>>*[3].已成功将数据库存入mysql*:\n")
                    print("===========================================\n")
                else:
                    print(">>>*[-3].未成功将数据库存入mysql*:\n")
            else:
                print(">>>[-2].未成功得到所有eml文件:\n")
        else:
            print(">>>[-1].目录不存在,请重新输入目录路径\n")
            print("===========================================\n")            
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
        
