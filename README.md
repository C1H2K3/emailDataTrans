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
** (一) class_download.py**
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
        :param time_judge: str, <br/> 时间阈值, 下载晚于该时间的邮件, 输入格式: '%Y-%m-%d %H:%M:%S'<br/>
    </td>
    <td>
      -
    </td>
  </tr>
</table>
    
    
    
    
    
    
    
    
    
    
    
    
