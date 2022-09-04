import requests
from flask import Flask
from flask import request
from flask import make_response
import json

from datetime import date
from datetime import timedelta
import mysql.connector
import time

import os
from dotenv import dotenv_values
db =  mysql.connector.connect(
        host=os.getenv('SERVER_HOST'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB'),
    )
print(db) 

select_Geet = "SELECT user_id FROM user_list_meter WHERE user_id NOT IN (SELECT user_id FROM user_list_meter WHERE create_at >= %(date)s) GROUP BY user_id"
today = date.today().strftime("%Y%m%d")
mycursor = db.cursor()
mycursor.execute(select_Geet ,{'date': today})
Getdata = mycursor.fetchall()
i = 0
ar = []
while i < len(Getdata)  :
    ar.append(','.join(Getdata[i]))
        # TestFn(ar[i])
    i=i+1
    # TestFn(ar)
# y=['U377cab5da50240870dab5b689b463b32','U07ee8d35cb363791ff5c7da807ba978c']
print(ar)
urls = 'https://api.line.me/v2/bot/message/multicast'
linepayload = {} 
linepayload['type'] = 'sticker'
linepayload['packageId'] = '789'
linepayload['stickerId'] = '10866' 
payload = {
            "to": ar,
            "messages":[
                {
                    "type":"text",
                    "text":"ลืมหรือป่าว คุณยังไม่ได้บันทึกค่ามิเตอร์นะคะ \nโปรดบันทึกค่ามิเตอร์เพื่อการใช้งานที่ดีที่สุด "
                },
                    linepayload
            ],
        
            }
accessToken = os.getenv("ACCESSTOKEN");            
headers = {
            'content-type': 'application/json',
            'Authorization':'Bearer '+str(accessToken),
            # 'X-Line-Retry-Key':str((uuid.uuid1()))
            } 
print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
r = requests.post(urls, data=json.dumps(payload), headers=headers)
print(r)