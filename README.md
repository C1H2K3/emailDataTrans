## 项目说明
<br/>
<font face = "黑体" color=black size=2>对满足时间要求的指定邮箱的邮件及其附件进行解析、下载以及eml元数据的入库</font>
<br/>

## 版本信息
```python
mysql: 8.0
python: 3.6.x
主要用到的包：
poplib, email, zipfile, patoolib, datetime, pymysql, os, shutil
```
## 目录结构
<br/>


## 接口说明
**（一）class_download.py**
<br/>
<font face = "黑体" color=black size=2>功能主要是下载满足时间要求的邮件及其附件。</font>

<table>
  <tr>
    <td>No</td>
    <td>接口名</td>
    <td>接口说明</td>
    <td>参数说明</td>
    <td>返回值</td>
  </tr>
  <tr>
    <td rowspan="1">1</td>
    <td>downeml</td>
    <td>以eml格式下载指定邮箱邮件到本地</td>
    <td>
      :param mail_adress: str, <br/> 邮箱账号, eg.xxxxxxx@qq.com<br/>
      :param mail_passwd: str, <br/> 邮箱密码, eg.xxxxxxx<br/>
      :param pop3_server: str, <br/> 收件服务器, eg.pop.exmail.qq.com<br/>
      :param time_judge: str, <br/> 时间阈值, 下载晚于该时间的邮件, 输入格式: '%Y-%m-%d %H:%M:%S'<br/>
    </td>
    <td>
      -
    </td>
  </tr>
  <tr>
    <td rowspan="1">2</td>
    <td>downatt</td>
    <td>读取本地eml的原始文本, 从中解析出附件并保存到本地中</td>
    <td>:param target_path: str,<br/> 本地eml存储路径, eg./xxxxxxx/xxxxx/xxx
    <td>
      -
    <td/>
  <tr/>
</table>

**（二）class_attparse.py**
<br/>
<font face = "黑体" color=black size=2>功能主要是解析eml格式的附件、解压zip格式的附件。</font>

<table>
  <tr>
    <td>No</td>
    <td>接口名</td>
    <td>接口说明</td>
    <td>参数说明</td>
    <td>返回值</td>
  </tr>
  <tr>
    <td rowspan="1">1</td>
    <td>uneml_run</td>
    <td>基于DFS的eml循环嵌套解析</td>
    <td>
      :param target_path: str, <br/> eml格式附件文件本地存储路径, eg./xxxxxxx/xxxxx/xxx</td>
    <td>
      -
    </td>
  </tr>
  <tr>
    <td rowspan="1">2</td>
    <td>unzip_run</td>
    <td>基于DFS的zip循环解压</td>
    <td>
      :param target_path: str, <br/> zip格式附件文件本地存储路径, eg./xxxxxxx/xxxxx/xxx</td>
    <td>
      -
    </td>
  </tr>
</table>
    
**（三）eml_mysql.py**
<br/>
<font face = "黑体" color=black size=2>功能主要是在指定数据库中创建email表, 并将获取的eml文件的元数据存入email表中。</font>
<br/>
<font face = "黑体" color=black size=2>针对email表, 除标记次序的email_id外, 其存储了6种信息, 分别是'From', 'Date', 'To', 'Subject', 'eml文件所带附件名称', 'eml文件本地存储路径'。其中'Date'信息格式化为: '%Y-%m-%d %H:%M:%S'[eg.2022-02-14 09:13:00], 其他信息均为直接从eml原始文本解析所得。</font>
<table>
  <tr>
    <td>No</td>
    <td>接口名</td>
    <td>接口说明</td>
    <td>参数说明</td>
    <td>返回值</td>
  </tr>
  <tr>
    <td rowspan="1">1</td>
    <td>emlsql_run</td>
    <td>获取eml文件元数据并将元数据存储入库</td>
    <td>
      :param ip: str, <br/> 远程IP, eg.xxx.xxx.x.xx<br/>
      :param passwd: str, <br/> 数据库密码, eg.xxxxxxx<br/>
      :param db: str, <br/> 数据库名称, eg.xxxxxxx<br/>
      :param user: str, <br/> 数据库用户名, eg.xxxx<br/>
      :param target_pat: str <br/> 数据库中email表中起始文件的编号<br/>
    </td>
    <td>
      -
    </td>
  </tr>
</table>

## 使用示例
## (1).导入class_download, 下载满足时间要求的邮件和附件到本地
##### 示例代码
```python
# -*-coding:utf-8-*-
from emailDownParse import class_download
# 下载邮件到本地
class_download.downeml_run()
# 下载附件到本地
class_download.downatt_run()

```
##### 输入过程示例
##### (1).class_download.downeml_run()输入示例
```python
>>>请输入邮箱账号: xxxxxxx@qq.com
>>>请输入邮箱密码: xxxxxxx
>>>请输入邮箱收件服务器端口: pop.exmail.qq.com
>>>请输入一个日期(早于该日期的邮件将不会被下载)[输入格式: '%Y-%m-%d %H:%M:%S']: 2022-02-14 09:13:00
+OK QQMail POP3 Server v1.0 Service Ready(QQMail v2.0)
*cmd* 'USER xxxxxxx@qq.com'
*cmd* 'PASS xxxxxxx'
*cmd* 'STAT'
*stat* [b'+OK', b'xx', b'xxxxxxx']
Messages: xx. Size: xxxxxxx
*cmd* 'LIST'
>>>请输入邮件本地存储路径[若无该路径则会在当前路径下新建一个]: /xxxxxxx/xxxxx/xxx
```

##### (2).class_download.Downatt_run()输入示例
```python
>>>请输入eml文件本地存储路径: /xxxxxxx/xxxxx/xxx
>>>[1].目录存在, 准备读文件:
>>>已获得第1个eml文件/xxxxxxx/xxxxx/xxx/Steam农历新年特卖现已盛大开幕!还有专门为您推荐的特别优惠!.eml
>>>已获得第2个eml文件/xxxxxxx/xxxxx/xxx/感谢您在Steam上的购买!.eml
>>>已获得第3个eml文件/xxxxxxx/xxxxx/xxx/已收到您的退款申请.eml
>>>已获得第4个eml文件/xxxxxxx/xxxxx/xxx/您的退款申请.拒绝.eml
...
>>>[2].已成功得到目标路径下的所有eml文件
>>>开始下载邮件附件到本地
>>>请输入附件保存路径: /xxxxxxx/xxxxx/xxx
```

##### 运行结果
##### (1).class_download.downeml_run运行结果
```python
2022-03-06 14:26:20 比给定时间阈值更晚, 进行邮件下载
>>>邮件'<Hollow Knight 购买成功>'存入本地成功*, time:2022-02-14 14:26:20
*cmd* 'RETR 7'
2022-02-28 15:36:28 比给定时间阈值更晚, 进行邮件下载
>>>邮件'<Sekiro: Shadows Die Twice 购买成功>'存入本地成功*, time:2022-02-28 15:36:28
*cmd* 'RETR 6'
...
2022-02-11 17:15:33 比给定时间阈值更早, 不进行邮件下载
*cmd* 'RETR 3'
2022-02-01 00:00:00 比给定时间阈值更早, 不进行邮件下载
*cmd* 'RETR 2'
```
##### (2).class_download.downatt_run运行结果
```python
>>>*邮件附件/xxxxxxx/xxxxx/xxx/.eml成功存入本地目标路径*, time:

```


    
    
    
    
    
