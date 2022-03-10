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
**(一) class_download.py**
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
    <td>:param mail_adress: str, <br/> 邮箱账号, eg.xxxxxxx@qq.com<br/>
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

**(一) class_attparse.py**
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
    <td>:param target_path: str, <br/> eml格式附件文件本地存储路径, eg./xxxxxxx/xxxxx/xxx</td>
    <td>
      -
    </td>
  </tr>
  <tr>
    <td rowspan="1">2</td>
    <td>unzip_run</td>
    <td>基于DFS的zip循环解压</td>
    <td>:param target_path: str, <br/> zip格式附件文件本地存储路径, eg./xxxxxxx/xxxxx/xxx</td>
    <td>
      -
    </td>
  </tr>
</table>
    
    
    
    
    
    
    
    
    
    
