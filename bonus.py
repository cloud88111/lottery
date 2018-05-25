# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:26:34 2018

@author: Rob
"""

import lottery as lt
import time
import smtplib

#enter list of competitors here
lott = ['Name1','Name2']

#dictionary of participant names and email addresses
Man = {'Name1': 'name1@email.com',
       'Name2': 'name2@email.com'}

strfrom = 'email'
server = smtplib.SMTP('')
pwd = ''

draw = lott*3

conn = lt.Lottery(strfrom,server,lott,Man,draw,strfrom,pwd)
strto = lt.Lottery.emaillist(conn)

#each player pays 250 to particpate
prize = len(lott)*250

table = lt.Lottery.gettable(conn)

message = "Prize is %s Big Ones" %prize
lt.Lottery.sendtable(conn,table,message)

time.sleep(15)

lt.Lottery.run(conn)