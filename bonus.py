# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 07:19:36 2017

@author: collinr
"""
#This lottery gives each participant 3 lives, first person drawn out 3 times wins
import random
import time
import smtplib
import math
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

#enter list of competitors here
lott = []

#dictionary of participant names and email addresses
Man = {}

email_list = dict((key,value) for key, value in Man.items() if key in lott)

strfrom = 'email'
strto = list(email_list.values())
server = smtplib.SMTP()
server.ehlo()
server.starttls()
server.set_debuglevel(1)

def counter(list1,list2):
    my_dict = {}
    for x in list(set(list1)):
        my_dict[x] = len([elem for elem in list2 if elem == x])
    return my_dict
    
def checkwinner(dict1):
    win = 0
    for x in dict1:
        if dict1[x] == 0:
            win += 1
        else: win = win
    return win

def gettable(list1,list2):
    return pd.DataFrame(list(counter(list1,list2).items()),columns=['Name','Lives'])
        
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

lottery  = lott*3

#each player pays 250 to particpate
prize = len(lott)*250

display = gettable(lott,lottery)

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = "Bonus Day Lottery, prize is %s Big Ones" %prize
msgRoot['From'] = strfrom
msgRoot['To'] = ','.join(strto)
msgRoot.preamble = 'This is a multi-part message in MIME format.'
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)
TEXT = display.to_html(index=False)
msgText = MIMEText(TEXT, 'html')
msgAlternative.attach(msgText)
server.sendmail(strfrom, strto, msgRoot.as_string())

time.sleep(15)
count = 1
while True:
    d=random.choice(lottery)
    lottery.remove(d)
    check = checkwinner(counter(lott,lottery))
    if check == 0:
        message = "%s" %d
        subj = "Pulled out %s is:" %ordinal(count)
        BODY = '\r\n'.join(['Subject: %s' % subj,
        '', message])
        server.sendmail(strfrom, strto, BODY)
        count +=1
        time.sleep(15)
        if (count-1)%3==0:
            display = gettable(lott,lottery)
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = "Lives Update"
            msgRoot['From'] = strfrom
            msgRoot['To'] = ','.join(strto)
            msgRoot.preamble = 'This is a multi-part message in MIME format.'
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)
            TEXT = display.to_html(index=False)
            msgText = MIMEText(TEXT, 'html')
            msgAlternative.attach(msgText)
            server.sendmail(strfrom, strto, msgRoot.as_string())
            time.sleep(15)
    else:
        message = "%s! Don't you just hate them" %d.upper()        
        subj = "WE HAVE A WINNER!"
        BODY = '\r\n'.join(['Subject: %s' % subj,
        '', message])
        server.sendmail(strfrom, strto, BODY)
        break

server.quit()