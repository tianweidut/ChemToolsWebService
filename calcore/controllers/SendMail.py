#!usr/bin/env python
#coding=utf-8
#-*- coding:utf8 -*-
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText

mail_host="smtp.qq.com"
mail_user="563944525@qq.com"
mail_pass="songyang8464"
mail_postfix="mail.qq.com"
to_list={"563944525@qq.com","563944525@qq.com"}
def sendmail(to_list,sub,attachment):
    # translation
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEMultipart('related')
    msg['Subject'] = email.Header.Header(sub,'utf-8')
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgText = MIMEText(open(attachment,'rb').read(), 'plain', 'UTF-8')
    msgText["Content-Type"]='application/octet-stream'
    msgText["Content-Disposition"]='attachment;filename="'+attachment+'"'
    msgAlternative.attach(msgText)
    msg.attach(msgAlternative)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.quit()    
    except Exception,e:
        return False

    return True

if __name__ == '__main__':
    if sendmail(to_list,"your request message from server","Mopac.py"):
        print "Success!"
    else:
        print "Fail!"