# -*coding:utf-8-*-
import poplib
import time
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
form datetime import datetime
import os, re
import calendar
import shutil
import datetime
# custom Pycharm properties
#idea.max.intellisense.filesize = 20000
#idea.max.content.load.filesize = 20000
# 将IDEA关于代码解压的文件大小阈值调大到20MB[主要是eml附件文件较大]

# 将foxmail中的邮件以eml格式保存到本地
class Downeml(object):
  def __init__(self, mail_address, mial_passwd, server):
    self.mail_address = mail_address # 邮箱账号
    self.mail_passwd = mail_passwd # 邮箱账号
    self.server = server
   
  def decode_str(self, s): # 字符编码转换
    value, charset = decode_header(s)[0]
    if charset:
      value = value.decode(charset)
    return value
  
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
  
  def get_email_file(self, server, judgetime): # 将符合条件的eml文件导入到本地中
    server.set_debuglevel(1)
    # 打印POP3服务器的欢迎文字
    print(server.getwelcome().decode('utf-8'))
    # 身份认证
    server.user(self.mail_address)
    server.pass_(self.mail_passwd)
    # 返回邮件总量和所占用空间
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号
    resp, mails, octets = server.list()
    index = len(mails)
    format_pattern = '%Y-%m-%d %H:%M:%S' # 日期格式化模板，用于后续时间判断
    
    savepath = input(">>>请输入邮件本地存储路径[若无该路径则会在当前目录下创建一个]: ")
    if not os.path.exists(savepath):
      os.makedirs(savepath) # 将默认目录更改为savepath所在路径，方便后续邮件的本地存储
    os.chdir(savepath) 
    for i in range(index, 0, -1):
      # 倒序遍历邮件
      resp, lines, octets = server.retr(i)
      # msg_content为邮件的原始文本
      msg_content = b'\r\n'.join(lines).decode('utf-8')
      
      new_msg = Parser().parsestr(msg_content)
      headers = self.get_email_headers(new_msg)
      if 'Subject' in headers:
        subject = headers['Subject']
      else:
        subject = None
        
      if 'Date' in headers:
        time = headers['Date']
      else:
        time = None
      try: # 得到eml文件的'Date'信息并将其格式化为datetime类型，总共有以下4种情况
        try:
          time_new = datetime.datetime.strptime(time[5,25], '%d %b %Y %H:%M:%S')
        except Exception as e:
          time_new = datetime.datetime.strptime(time[5,24], '%d %b %Y %H:%M:%S')
      except Exception as e:
        try:
          time_new = datetime.datetime.strptime(time[0,20], '%d %b %Y %H:%M:%S')
        except Exception as e:
          time_new = datetime.datetime.strptime(time[0,19], '%d %b %Y %H:%M:%S')
      
      filename = subject + '.eml' # 修改下载文件名称，可以指定中文
      msg_content = bytes(msg_content, encoding="utf-8") # str to bytes, 将字符串类型转换为字节类型
      # 这里可增加 邮件下载判断条件，这里输入时间阈值，晚于该时间的邮件才进行下载
      time_new = str(time_new)
      difference = (datetime.datetime.strptime(time_new, format_pattern) - datetime.datetime.strptime(judgetime, format_pattern))
      if difference.days < 0:
        print(time_new, "比给定时间阈值更早, 不进行邮件下载")
      else:
        print(time_new, "比给定时间阈值更晚, 进行邮件下载")
        try:
          # 判断是否有同名文件
          if os.path.exists(filename): # 说明存在同名文件，一般是同一封邮件发了2次，考虑通过在eml文件名称中增加发送时间来进行区分
            time_new = str(time_new)
            email_file = open(subject + time_new + '.eml', 'wb') # 通过增加发送时间对同名文件进行区别
            email_file.write(msg_content) # 保留文件
            email_file.close()
          else: # 说明不存在同名文件
            email_file = open(filename, 'wb')
            email_file.write(msg_content) # 保存文件
            email_file.close()
        except Exception as e:
          print(">>>邮件'<{0}>'存入本地失败, 失败原因:{1}".format(subject, e))
        else:
          print(">>>邮件'<{0}>'存入本地成功, time:{1}".format(subject, time_new))
    
    server.quit()
# 将本地eml文件的附件解析出来保存到本地
class Downatt(object):
  def __init__(self):
    self.__PATHS = [0 for i in range(100)] # 存储eml文件的列表
    self.__FILE_NUM = 0 # 记录目标路径下的eml文件总数
    self.__UNFILE_NUM = 0 # 记录损坏（无法进行读取解析）的eml文件
    
  def decode_str(self, s): # 字符编码转换
    value, charset = decode_header(s)[0]
    if charset:
      value = value.decode(charset)
    return value
  
  def List_FilePATHS(self, target_path): # 递归文件夹下所有文件放入列表PATHS，获得路径下的所有eml文件
    k = 0
    for base_path, folder_list, file_list in os.walk(target_path): # 遍历文件夹
      for file_name in file_list:
        file_path = os.path.join(base_path, file_name)
        file_ext = file_path.rsplit('.', maxsplit=1)
        if len(file_ext) != 2: # 没有后缀名，文件夹
          self.List_FilePATHS(file_path)
          continue
        elif file_ext[1] == 'eml': # eml文件
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
      print('文件不存在')
      
  def open_file(self, path): # 打开一个文件
    if os.path.exists(path):
      return open(path, 'r')
    else:
      print('文件不存在')
      
  def singleatt_down(self, message, savepath): # 下载单个eml文件的附件
    attachments = []
    for part in message.walk(): # 循环信件中的每一个mime的数据块
      filename = part.get_filename()
      if filename: # 如果附件存在名字，说明该eml文件有附件
        filename = self.decode_str(filename)
        data = part.get_payload(decode=True)
        abs_filename = os.path.join(savepath, filename)
        attach = open(abs_filename, 'wb')
        attachments.append(filename)
        attach.write(data)
        attach.close()
    return attachments
  
  def down_allatt(self): # 对PATHS列表中所有eml文件的附件进行解析
    ttp = False
    dirpath = input(">>>请输入附件保存路径: ")
    for i in range(self.__FILE_NUM):
      time = datetime.datetime.now() # time为系统当前时刻
      if self.__PATHS[i] == 0:
        pass
      else:
        try:
          msg = self.get_message(self.__PATHS[i])
          attach = self.singleatt_down(msg, dirpath) # 得到单个eml的附件
          print(">>>*邮件附件{0}成功存入本地目标路径*, time:{1}".format(self.__PATHS[i], time))
          ttp = True
        except Exception as e:
          print(">>>*邮件附件{0}成功存入本地目标失败*, 失败原因:{1}".format(self.__PATHS[i], e))
    return ttp
  
def downeml_run(): # Downeml, 将foxmail目标邮箱最近一个月的所有邮件存储到本地中
  testmail_address = input(">>>请输入邮箱账号: ")
  testmail_passwd = input(">>>请输入邮箱密码: ")
  pop3_server = input("请输入邮箱服务器端口: ")
  testserver = poplib.POP3_SSL(pop3_server)
  test_downeml = Downeml(testmail_address, testmail_passwd, testserver)
  time_judge = input(">>>请输入一个日期(早于该日期的邮件将不会被下载)[输入格式: '%Y-%m-%d %H:%M:%S']: ")
  test_downeml.get_email_file(testserver, time_judge)
  
 def Downatt_run(): # Downatt. 将本地eml文件的附件解析提取出来保存到本地中
  test_att = Downatt()
  target_path = input(">>>请输入eml文件本地存储路径: ")
  if os.path.exists(target_path):
    print(">>>[1].目录存在, 准备读文件: \n")
    if test_att.List_FilePATHS(target_path):
      print(">>>[2].已成功得到所有eml文件: \n")
      print(">>>开始下载邮件附件到本地")
      if test_att.down_allatt():
        print(">>>*[3].已成功将所有目标邮件附件存入本地*: \n")
        print("=====================================\n")
      else:
        print(">>>*[-3].未成功将所有目标邮件附件存入本地*: \n")

    else:
      print(">>>*[-2].未成功得到所有eml文件: \n")
  else:
    print(">>>[-1].目录不存在, 请重新输入目录路径 \n")
    print("=====================================\n")
  
  
    
    
    
