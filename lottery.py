# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:23:58 2018

@author: Rob
"""

import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math
import time
      
class Lottery:
    
    def __init__ (self, strfrom, server, participants, emails, full_list, username, password):
        self.participants = participants
        self.emails = emails
        self.strfrom = strfrom
        self.server = server
        self.full_list = full_list
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
    def checkwinner(self,list1):
        win = 0
        dict1 = self.counter(list1)
        for x in dict1:
            if dict1[x] == 0:
                win += 1
            else: win = win
        return win
    
    #gets table for display
    def gettable(self):
        return pd.DataFrame(list(self.counter(self.full_list).items()),columns=['Name','Lives'])
    
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
        import random
        d = random.choice(self.full_list)
        self.full_list.remove(d)
        return d

    def run(self):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        count = 1
        while True:
            d = self.pullout()
            check = self.checkwinner(self.full_list)
            if check == 0:
                message = "%s" %d
                subj = "Pulled out %s is:" %ordinal(count)
                BODY = '\r\n'.join(['Subject: %s' % subj,
                '', message])
                self.sendmail(BODY)
                if count%3==0:
                    message = "Lives Update"
                    table = self.gettable()
                    self.sendtable(table,message)
                    time.sleep(15)
                count += 1
                time.sleep(15)
            else:
                message = "%s! Don't you just hate them" %d.upper()        
                subj = "WE HAVE A WINNER!"
                BODY = '\r\n'.join(['Subject: %s' % subj,
                '', message])
                self.sendmail(BODY)
                break
        self.server.quit()
