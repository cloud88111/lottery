# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:26:34 2018

@author: Rob
"""

import lotto as lt
import time
import smtplib

#enter list of competitors here
lott = ['name1','name2']

#dictionary of potential participant names and email addresses
Man = {'name1': 'name1@email.com',
        'name2': 'name2@email.com',
        'name3': 'name3@email.com'}

strfrom = 'me@email.com'
server = smtplib.SMTP('')
pwd = ''

conn = lt.Lottery(strfrom,server,lott,Man)
strto = lt.Lottery.emaillist(conn)

#each player pays 250 to particpate
prize = len(lott)*250

table = lt.Lottery.gettable(conn)

message = "Prize is %s Big Ones" %prize
lt.Lottery.sendtable(conn,table,message)

time.sleep(15)

message = "Congratulations"        
subj = "WE HAVE A WINNER!"

lt.Lottery.run(conn,message,subj)