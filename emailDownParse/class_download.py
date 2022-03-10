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
  
  def get_email_headers(self, msg): # 得到eml文件的
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
  
  def get_email_file(self, server, judgetime):
    server.set_debuglevel(1)
    
    print(server.getwelcome().decode('utf-8'))
    
    server.user(self.mail_address)
    server.pass_(self.mail_passwd)
    
    print('Messages: %s. Size: %s' % server.stat())
    
    resp, mails, octets = server.list()
    index = len(mails)
    format_pattern = '%Y-%m-%d %H:%M:%S'
    
    savepath = input(">>>请输入邮件本地存储路径[若无该路径则会在当前目录下创建一个]: ")
    if not os.path.exists(savepath):
      os.makedirs(savepath)
    os.chdir(savepath) 
    for i in range(index, 0, -1):
      
      resp, lines, octets = server.retr(i)
      
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
      try:
        try:
          time_new = datetime.datetime.strptime(time[5,25], '%d %b %Y %H:%M:%S')
        except Exception as e:
          time_new = datetime.datetime.strptime(time[5,24], '%d %b %Y %H:%M:%S')
      except Exception as e:
        try:
          time_new = datetime.datetime.strptime(time[0,20], '%d %b %Y %H:%M:%S')
        except Exception as e:
          time_new = datetime.datetime.strptime(time[0,19], '%d %b %Y %H:%M:%S')
      
      filename = subject + '.eml'
      msg_content = bytes(msg_content, encoding="utf-8")
      
      time_new = str(time_new)
      difference = (datetime.datetime.strptime(time_new, format_pattern) - datetime.datetime.strptime(judgetime, format_pattern))
      if difference.days < 0:
        print(time_new, "比给定时间阈值更早, 不进行邮件下载")
      else:
        print(time_new, "比给定时间阈值更晚, 进行邮件下载")
        try:
          
          if os.path.exists(filename):
            time_new = str(time_new)
            email_file = open(subject + time_new + '.eml', 'wb')
            email_file.write(msg_content)
            email_file.close()
          else:
            email_file = open(filename, 'wb')
            email_file.write(msg_content)
            email_file.close()
        except Exception as e:
          print(">>>邮件'<{0}>'存入本地失败, 失败原因:{1}".format(subject, e))
        else:
          print(">>>邮件'<{0}>'存入本地成功, time:{1}".format(subject, time_new))
    
    server.quit()

class Downatt(object):
  def __init__(self):
    self.__PATHS = [0 for i in range(100)]
    self.__FILE_NUM = 0
    self.__UNFILE_NUM = 0
    
  def decode_str(self, s): # 字符编码转换
    value, charset = decode_header(s)[0]
    if charset:
      value = value.decode(charset)
    return value
  
  def List_FilePATHS(self, target_path):
    k = 0
    for base_path, folder_list, file_list in os.walk(target_path):
      for file_name in file_list:
        file_path = os.path.join(base_path, file_name)
        file_ext = file_path.rsplit('.', maxsplit=1)
        if len(file_ext) != 2:
          self.List_FilePATHS(file_path)
          continue
        elif file_ext[1] == 'eml':
          self.__PATHS[self.__FILE_NUM] = file_path
          self.__FILE_NUM = self.__FILE_NUM + 1
          print(">>>已获得第{0}个eml文件{1}".format(self.__FILE_NUM, file_path))
          continue
          
      return True
    
  def get_message(self, path):
    if os.path.exists(path):
      fp = self.open_file(path)
      return email.message_from_file(fp)
    else:
      print('文件不存在')
      
  def open_file(self, path):
    if os.path.exists(path):
      return open(path, 'r')
    else:
      print('文件不存在')
      
  def singleatt_down(self, message, savepath):
    attachments = []
    for part in message.walk():
      filename = part.get_filename()
      if filename:
        filename = self.decode_str(filename)
        data = part.get_payload(decode=True)
        abs_filename = os.path.join(savepath, filename)
        attach = open(abs_filename, 'wb')
        attachments.append(filename)
        attach.write(data)
        attach.close()
    return attachments
  
  def down_allatt(self):
    ttp = False
    dirpath = input(">>>请输入附件保存路径: ")
    for i in range(self.__FILE_NUM):
      time = datetime.datetime.now()
      if self.__PATHS[i] == 0:
        pass
      else:
        try:
          msg = self.get_message(self.__PATHS[i])
          attach = self.singleatt_down(msg, dirpath)
          print(">>>*邮件附件{0}成功存入本地目标路径*, time:{1}".format(self.__PATHS[i], time))
          ttp = True
        except Exception as e:
          print(">>>*邮件附件{0}成功存入本地目标失败*, 失败原因:{1}".format(self.__PATHS[i], e))
    return ttp
def downeml_run():
  testmail_address = input(">>>请输入邮箱账号: ")
  
  
  
  
      
   


        
      
          

        
    
    
            
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
