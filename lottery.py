# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:23:58 2018

@author: Rob
"""

import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import math
import time
        
class Lottery(object):
    
    def __init__ (self, strfrom, server, participants, emails, username="", password="",lives=1,last=True):
        self.participants = participants
        self.emails = emails
        self.strfrom = strfrom
        self.server = server
        self.lives=lives
        self.full_list = participants*lives
        self.last=last
        self.username = username
        self.password = password
        self.server.ehlo()
        self.server.starttls()
        try: self.server.login(username,password)
        except: pass
        self.server.set_debuglevel(1)
        
    #gets list of people to email depending on participants
    def emaillist(self):
        email_list = dict((key,value) for key, value in self.emails.items() if key in self.participants)
        return list(email_list.values())
    
    def counter(self,list1):
        my_dict = {}
        for x in list(set(self.participants)):
            my_dict[x] = len([elem for elem in list1 if elem == x])
        my_dict = my_dict
        return my_dict
     
    #checks if there is a winner    
    def checkwinner(self):
        win = 0
        if self.last is True:
            if len(self.full_list) == 1:
                win+=1
        else:
            dict1 = self.counter(self.full_list)
            for x in dict1:
                if dict1[x] == 0:
                    win += 1
        return win
    
    #gets table for display
    def gettable(self):
        table = pd.DataFrame(list(self.counter(self.full_list).items()),columns=['Name','Lives'])
        if self.lives==1:
            return table[['Name']]
        else: return table
    
    #sends table in an email to the list of participants
    def sendtable(self,table,message):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = message
        msgRoot['From'] = self.strfrom
        msgRoot['To'] = ','.join(self.emaillist())
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        TEXT = table.to_html(index=False)
        msgText = MIMEText(TEXT, 'html')
        msgAlternative.attach(msgText)
        self.server.sendmail(self.strfrom, self.emaillist(), msgRoot.as_string())
    
    #sends email with the lastest particpant to be removed from the draw    
    def sendmail(self,body):
        self.server.sendmail(self.strfrom, self.emaillist(), body)
        
    def pullout(self):
        d = random.choice(self.full_list)
        self.full_list.remove(d)
        return d

    def run(self,email,subject):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        count = 1
        while True:
            d = self.pullout()
            check = self.checkwinner()
            if check == 0:
                message = "%s" %d
                subj = "Pulled out %s is:" %ordinal(count)
                BODY = '\r\n'.join(['Subject: %s' % subj,
                '', message])
                self.sendmail(BODY)
                time.sleep(15)
                if self.lives != 1:
                    if count%3==0:
                        message = "Lives Update"
                        table = self.gettable()
                        self.sendtable(table,message)
                        time.sleep(15)
                count += 1
            else:
                if self.lives==1:
                    message = "%s" %d
                    subj = "Pulled out last is:"
                    BODY = '\r\n'.join(['Subject: %s' % subj,
                    '', message])
                    self.sendmail(BODY)
                    time.sleep(5)
                    message = '%s! ' %d.upper() + email
                    for values in self.full_list:
                        message = '%s! ' %values.upper() + email
                        BODY = '\r\n'.join(['Subject: %s' % subject,
                        '', message])
                        self.sendmail(BODY)
                else:
                    message = '%s! ' %d.upper() + email
                    BODY = '\r\n'.join(['Subject: %s' % subject,
                    '', message])
                    self.sendmail(BODY)
                break
        self.server.quit()
