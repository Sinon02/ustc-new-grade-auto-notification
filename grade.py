from urllib import request,parse
import http.cookiejar as cookielib
import re
username=''
password=''
url1='https://passport.ustc.edu.cn/login'
url2='https://jw.ustc.edu.cn/ucas-sso/login'
url3='https://jw.ustc.edu.cn/for-std/grade/sheet'
url4='https://jw.ustc.edu.cn/for-std/grade/sheet/getSemesters'
url5='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?trainTypeId=1&semesterIds='
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
pattern1=re.compile("\"courseNameCh\":\"(.+?)\",")
pattern2=re.compile("\"score\":\"(.+?)\",")
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
req3=request.Request(url=url3,headers=headers)
result4=request.urlopen(url4)
html4=result4.read().decode('utf-8')
IDs=re.findall("\"id\":(.+?),",html4)
IDs=list(map(int,IDs))
max_ID=max(IDs)
url5+=str(max_ID)
result5=request.urlopen(url5)
html5=request.urlopen(url5).read().decode('utf-8')
sheet=re.findall("{(.+?)}",html5)
courseName=re.findall(pattern1,sheet[1])
courseName=courseName[0]
score=re.findall(pattern2,sheet[1])
print(courseName,score)

