from datetime import date, datetime, timedelta
from threading import Timer
import requests
import uuid
import json
import mysql.connector
import os
# from app import CountInsertData



db =  mysql.connector.connect(
        host=os.getenv('SERVER_HOST'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB'),
    )

def GetUser():
    select_Geet = "SELECT user_id FROM user_list_meter GROUP BY user_id"
    mycursor = db.cursor()
    mycursor.execute(select_Geet ,{})
    Getdata = mycursor.fetchall()
    print(len(Getdata))
    # print(FormatStr(Getdata[0]),FormatStr(Getdata[1]),FormatStr(Getdata[2]))
    i = 0
    CountInsertData("U377cab5da50240870dab5b689b463b32")
    while i < len(Getdata)  :
        
        print(FormatStr(Getdata[i]))
        i=i+1
    # for x in Getdata :
    #     # lis = FormatStr(x)
    #     lis = 'U377cab5da50240870dab5b689b463b32'
    #     print(lis)
    # #   CountInsertData
    #     CountInsertData(lis)
    
    

def FormatStr(data):
    if data is not None:
        for xs in data:
                result = xs
                if not all(result) == True : 
                    return 0
                else : 
                    x = result
                    return str(x)


    # START OF ADMIN CONVERSATION HANDLER TO REPLACE THE DATABASE 
def CountInsertData(user_id):
    # print(datetime.now().strftime("%H:%M:%S"))
    xDate = datetime.now().strftime("%H:%M:%S")
    select_insert = "SELECT meter_value FROM user_list_meter WHERE  user_id  =  %(user_id)s AND create_at >= %(date)s"
    mycursor = db.cursor()
    #  m2
    mycursor.execute(select_insert, { 'user_id': user_id ,'date': date.today().strftime("%Y%m%d") } )
    select_insertFetch = mycursor.fetchall()
    x = sumMin(select_insertFetch)
    print('in fn---------> ',x)
    if x == 0:
        urls = 'https://api.line.me/v2/bot/message/broadcast'
        linepayload = {} 
        linepayload['type'] = 'sticker'
        linepayload['packageId'] = '789'
        linepayload['stickerId'] = '10858'


        payload = {
        "messages":[
            {
                "type":"text",
                "text":"ลืมหรือป่าว คุณยังไม่ได้บันทึกค่ามิเตอร์นะคะ "
            },
                  linepayload
        ],
      
        }
        accessToken = os.getenv("ACCESSTOKEN");

        headers = {
          'content-type': 'application/json',
          'Authorization':'Bearer '+str(accessToken),
          'X-Line-Retry-Key':str((uuid.uuid1()))
          } 
        r = requests.post(urls, data=json.dumps(payload), headers=headers)
        print(r)

        print(x)
def sumMin(data):
    if data is not None:
        for xs in data:
                result = xs
                if not all(result) == True : 
                    return 0
                else : 
                    x = result
                    return sum(x)


