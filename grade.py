#!/usr/bin/python
# -*- coding:utf-8 -*-
from urllib import request,parse
import http.cookiejar as cookielib
import re
from log import Log
# import threading
# from queue import Queue
from mail import send_email
from config import username,password,sleep_time
import time

url1='https://passport.ustc.edu.cn/login'
url2='https://jw.ustc.edu.cn/ucas-sso/login'
url3='https://jw.ustc.edu.cn/for-std/grade/sheet/getSemesters'
url4='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?trainTypeId=1&semesterIds='
headers={
    'Connection': 'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
pattern1=re.compile("\"id\":(.+?),")
pattern2=re.compile("{(.+?)}")
pattern3=re.compile("\"courseNameCh\":\"(.+?)\",")
pattern4=re.compile("\"score\":\"(.+?)\",")
# def read_url(url,queue):
#     data=request.urlopen(url).read()
#     queue.put(data)
# def fetch_parallel(urls):
#     result=Queue()
#     threads=[threading.Thread(target=read_url,args=(url,result)) for url in urls]
#     for t in threads:
#         t.start()
#     for t in threads:
#         t.join()
#     return result
def login():
    logger.info('loging...')
    cookie=cookielib.CookieJar()
    opener=request.build_opener(request.HTTPCookieProcessor(cookie))
    request.install_opener(opener)
    login_data=parse.urlencode([
        ('username',username),
        ('password',password)
    ])
    req1=request.Request(url=url1,headers=headers)
    result1=request.urlopen(req1,data=login_data.encode('utf-8'))
    req2=request.Request(url=url2,headers=headers)
    result2=request.urlopen(req2)
    logger.info('log in complete!')


def get_grade():
    url4='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?trainTypeId=1&semesterIds='    
    GETID=request.urlopen(url3)
    IDs=GETID.read().decode('utf-8')
    IDs=re.findall(pattern1,IDs)
    IDs=list(map(int,IDs))
    max_ID=max(IDs)
    url4+=str(max_ID)
    Grades=request.urlopen(url4).read().decode('utf-8')
    sheet=re.findall(pattern2,Grades)
    return sheet
def parse_grade(sheet):
    grades=[]
    for i in range(1,len(sheet)):
        courseName=re.findall(pattern3,sheet[i])
        courseName=courseName[0]
        score=re.findall(pattern4,sheet[i])
        score=int(score[0])
        grades.append((courseName,score))
    return grades
    

grade_len=0
grades=[]
first_access=True
logger=Log(__name__).getlog()
logger.info("Started")
while True:
    logger.info('Query...')
    try:
        if(first_access):
            login()
            first_access=False
        sheet=get_grade()
        if(len(sheet)==grade_len): # no new grade
            pass
        else:
            new_grades=parse_grade(sheet)
            new_grade=list(set(new_grades)-set(grades))
            logger.info("new_grades!")
            for k,v in new_grade:
                logger.info(k+': '+str(v))
            logger.info('sending Email...')
            send_email(new_grade)
            grades=new_grades
            grade_len=len(sheet)
    except Exception as e:
        if not isinstance(e, KeyboardInterrupt):
           logger.info('Error: '+ str(e))
        else:
            break
    logger.info('sleeping...')
    time.sleep(sleep_time)