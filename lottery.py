# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:23:58 2018

@author: Rob
"""

class Lottery:
    
    def __init__ (self, strfrom, server, participants, emails):
        self.participants = participants
        self.emails = emails
        self.strfrom = strfrom
        self.server = server
        
    #gets list of people to email depending on participants
    def emaillist(self):
        self.email_list = dict((key,value) for key, value in self.emails.items() if key in self.participants)
        return list(self.email_list.values())
    
    def counter(self,list1,list2):
        my_dict = {}
        for x in list(set(list1)):
            my_dict[x] = len([elem for elem in list2 if elem == x])
        my_dict = my_dict
        return my_dict
        
    def checkwinner(self,list1,list2):
        win = 0
        dict1 = self.counter(list1,list2)
        for x in dict1:
            if dict1[x] == 0:
                win += 1
            else: win = win
        return win
    
    def gettable(self,list1,list2):
        import pandas as pd
        return pd.DataFrame(list(self.counter(list1,list2).items()),columns=['Name','Lives'])
    
    def sendtable(self,table,message):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        self.server.ehlo()
        self.server.starttls()
        self.server.set_debuglevel(1)
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = message
        msgRoot['From'] = self.strfrom
        msgRoot['To'] = ','.join(self.emaillist)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        TEXT = table.to_html(index=False)
        msgText = MIMEText(TEXT, 'html')
        msgAlternative.attach(msgText)
        self.server.sendmail(self.strfrom, self.email_list, msgRoot.as_string())
        self.server.quit()
        
    def sendmail(self, body):
        self.server.ehlo()
        self.server.starttls()
        self.server.set_debuglevel(1)
        self.server.sendmail(self.strfrom, self.emaillist, body)
        self.server.quit()
        
    def pullout(self,list1):
        import random
        d = random.choice(list1)
        list1.remove(d)
        return d