# ustc-new-grade-auto-notification

USTC新成绩自动通知脚本



## 参考

本脚本参考了[ustc-grade-automatic-notification](https://github.com/zzh1996/ustc-grade-automatic-notification)（一个旧版教务系统上的成绩通知脚本）的框架，在新版教务系统上用python3重新实现了一个成绩通知脚本。

## 项目简述

本脚本会根据config.py中的配置文件，登录教务系统，获取**最新学期**的成绩，并不断检测是否有更新。一旦有新成绩，会登录配置文件中的发送方邮箱，给一个或多个接收方邮箱发送邮件。

邮件的格式为：

**标题:** 您有新成绩！

**正文：**

新成绩：

xxxx:xxx

xxxx:xxx



## 虽然没啥用但是写了的feature

1. 自动在console输出带时间的log，并存入"running.log"中，log的设置还算详细。
2. 在运行的过程中会保存已有的成绩，下次执行时直接读取，类似于**“断点续传”**。
3. 在没有输入发件方、没有输入接收方或者用户密码错误时会报错并退出，**防止连续5次登陆失败账户被锁定**
4. 运行过程中**检测是否还在登陆状态**，不在的话会重新登录，适合长时间挂载。
5. **使用requests**替换最开始的urllib，因为最开始实现的时候后者明显比前者慢很多。



## 依赖库

requests

re

time

pickle

os

smtplib

email

logging



## 使用方法

1. 安装git和python3

2. 安装依赖库，python3不自带的应该只有requests

   ```shell
   pip3 install requests
   #使用anaconda3的不需要安装，自带
   ```

3. 下载本仓库

   ```shell
   git clone https://github.com/Sinon02/ustc-new-grade-auto-notification.git
   ```

4. 进入目录，修改配置文件

   ```shell
   cd ustc-new-grade-auto-notification
   vim config.py
   ```

   配置文件的格式为：

   ```python
   #!/usr/bin/python
   # -*- coding:utf-8 -*-
   #login
   username = 'PBxxxxxxxx'
   password = ''

   #sender_email
   mail_host = 'smtp.qq.com' #以qq邮箱为例
   mail_user = 'xx@qq.com'
   mail_passwd = ''  #这里填密码或授权码
   use_ssl = True
   ssl_port = 465 #根据情况修改

   #receiver_email
   receivers = ['xx@qq.com','xx@mail.ustc.edu.cn']

   #time
   sleep_time = 120  #second
   ```

   sender_email下填写**发送方**的信息，receiver_email下方填写**接收方**的信息，接收方可多个。

   login下为**统一身份认证系统**中的用户名和密码。

   time为执行间隔，以**秒**为单位，推荐设置大一点。

5. 执行grade.py

   ```python
   python grade.py
   ```



## 反馈bug

欢迎提issue。
