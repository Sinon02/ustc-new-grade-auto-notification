#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import re
from log import Log
from mail import send_email
from config import username,password,sleep_time
import time
import os
import pickle
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

def login(s):
    logger.info('loging...')
    data={'username':username,'password':password}
    r1=s.post(url1,data=data,headers=headers)
    if(r1.text==''):
        logger.info('username or password wrong!')
        os._exit(0)
    s.get(url2,headers=headers)
    logger.info('log in complete!')

def get_ID(s):
    logger.info('getting the max ID...')
    GETID=s.get(url3)
    IDs=GETID.text
    IDs=re.findall(pattern1,IDs)
    IDs=list(map(int,IDs))
    max_ID=max(IDs)
    return max_ID

def get_grade(s,max_ID):
    logger.info('getting the grades')
    url4='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?trainTypeId=1&semesterIds='    
    url4+=str(max_ID)
    Grades=s.get(url4).text
    if '统一身份认证登录' in Grades:
        logger.info('Not login')
        login(s)
        return get_grade(s,max_ID)
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
if os.path.exists('grades.pickle') and os.path.getsize('grades.pickle'):
    logger.info('Find the old data,reading...')
    f=open('grades.pickle','rb')
    grades=pickle.load(f)
    grade_len=len(grades)
    f.close()
s=requests.Session()
while True:
    logger.info('Query...')
    try:
        if(first_access):
            login(s)
            max_ID=get_ID(s)
            first_access=False
        sheet=get_grade(s,max_ID)
        if(len(sheet)==grade_len+1): # no new grade
            pass
        else:
            f=open('grades.pickle','wb')
            new_grades=parse_grade(sheet)
            new_grade=list(set(new_grades)-set(grades))
            logger.info("new_grades!")
            for k,v in new_grade:
                logger.info(k+': '+str(v))
            grades=new_grades
            grade_len=len(grades)
            logger.info('writing to file...')
            pickle.dump(grades,f)
            f.close()
            logger.info('sending Email...')
            send_email(new_grade)
    except Exception as e:
        if not isinstance(e, KeyboardInterrupt):
           logger.info('Error: '+ str(e))
        else:
            break
    logger.info('sleeping...')
    time.sleep(sleep_time)