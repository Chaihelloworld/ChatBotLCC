#code by Stackpython
#Import Library
import array


# from asyncio import constants
# from asyncio.windows_events import NULL
import json
from operator import ge
import os
from re import X
from tkinter import W
from tokenize import Number
from types import NoneType
from typing import Any
from flask import Flask
from flask import request
from flask import make_response

from datetime import date
from datetime import timedelta

import uuid

#----Additional from previous file----
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyparsing import empty
from datetime import datetime



scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("Bybot").worksheet('Sheet1') 

from random import randint

import mysql.connector

import os
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
import schedule
import time

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import send_from_directory
import requests

app = Flask(__name__)
@app.route('/favicon.ico')
@app.route('/', methods=['POST']) 

def MainFunction():
    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    # print(date.today().strftime("HH:MM"))
    if date.today().strftime("HH:MM") == "16:00":
      print('now 16.00')

    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป

    return r


def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

def home_view():
        return "connecting ... "
  
def generating_answer(question_from_dailogflow_dict):

    #Print intent ที่รับมาจาก Dailogflow
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #เก็บต่า ชื่อของ intent ที่รับมาจาก Dailogflow
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 
    #ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str == 'คำนวณ':    

        answer_str = menu_recormentation(question_from_dailogflow_dict)
       
    elif intent_group_question_str == 'reportMonth': 
        answer_str = getReport_mounth(question_from_dailogflow_dict)
    
    elif intent_group_question_str == 'คำนวณช่วงเดือน': 
        answer_str = getReportBymonth(question_from_dailogflow_dict)
    elif intent_group_question_str == 'dailyReportCal': 
        answer_str = getReportDay(question_from_dailogflow_dict)

    else: answer_str = "ผมไม่เข้าใจ คุณต้องการอะไร"
    
    #สร้างการแสดงของ dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def initText(data):
    if data is not None:
        for xs in data:
                result = xs
                if not all(result) == True : 
                    return "ไม่มีค่าที่บันทึกของเมื่อวาน"
                else : 
                    y=sum(result)
                    x = "เมื่อวานใช้ไฟ ทั้งหมด"+str(y)+"หน่วย"

                    return x
def menu_recormentation(respond_dict): #ฟังก์ชั่นสำหรับเมนูแนะนำ
    
    user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]

    select_today = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE  user_id  =  %(user_id)s AND create_at BETWEEN %(d1)s AND %(d2)s;"
    d1 = date.today().strftime("%Y/%m/%d")
    yesterday = date.today() - timedelta(days = 1)
    # print(yesterday)
    mycursor = db.cursor()
    mycursor.execute(select_today, { 'user_id': user_id ,'d1': yesterday.strftime("%Y/%m/%d"),'d2':d1  })
    
    myresult = mycursor.fetchall()
    xlist = initText(myresult)
    ylist = SelectValid(user_id)
    meter_value = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["meter.original"]
    
    token = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["replyToken"]
    group_month = date.today().strftime("%Y/%m")
    sheet.insert_row([meter_value,d1],2)
    
    print('---->',ylist,'meter__--->',meter_value)
    print('int(meter_value)---->',int(meter_value))
    print('int(valid)---->',int(ylist))
    if int(meter_value) < int(ylist) :
       answer_function = "ข้อมูลน้อยกว่า ค่าในระบบกรุณากรอกข้อมูลใหม่ \n **โปรดเลือกเมนู > บันทึกข้อมูล" 
    elif int(meter_value) > (int(ylist)+ int(50)):
       answer_function = "ค่ามิเตอร์ที่บันทึก มากกว่า 50 หน่วยกรุณาตรวจสอบใหม่อีกครั้ง \n **โปรดเลือกเมนู > บันทึกข้อมูล" 
    else :
       connect(user_id,meter_value,group_month,d1)
       answer_function = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["meter.original"] + ' บันทึกค่าสำเร็จ' +"\n"+str(xlist)
       MessageReply(token)

    return  answer_function 
  
def MessageReply(token):
  urls = 'https://api.line.me/v2/bot/message/reply'
  linepayload = {} 
  linepayload['type'] = 'sticker'
  linepayload['packageId'] = '789'
  linepayload['stickerId'] = '10869'
  payload = {
        "replyToken":token,
        "messages":[
            {
                "type":"text",
                "text":" บันทึกค่าของวันนี้เรียบร้อยแล้ว \n เก่งมากๆค่า \n \n เพื่อการใช้งานที่มีประสิทธิภาพสูงสุด \n กรุณาบันทึกค่าอย่างต่อเนื่องนะคะ "
            },
                  linepayload
        ],
      
        }
        
  accessToken = os.getenv("ACCESSTOKEN")

  headers = {
              'content-type': 'application/json',
              'Authorization':'Bearer '+str(accessToken),
              # 'X-Line-Retry-Key':str((uuid.uuid1()))
              } 
  r = requests.post(urls, data=json.dumps(payload), headers=headers)
  print(r)
  
#Flask
def SelectValid(user_id):
    mycursor = db.cursor()
    
    validate = "SELECT MAX(meter_value) FROM user_list_meter WHERE  user_id  =  %(user_idValid)s ;"
    mycursor.execute(validate, { 'user_idValid': user_id  })
    myresultValid = mycursor.fetchall()
    if myresultValid is not None:
         for xs in myresultValid:
                result = xs
                if not all(result) == True : 
                    return 0
                else : 
                    x = result
                    return sum(x)









def GetUser():
    select_Geet = "SELECT user_id FROM user_list_meter GROUP BY user_id"
    mycursor = db.cursor()
    mycursor.execute(select_Geet ,{})
    Getdata = mycursor.fetchall()
    print(len(Getdata))
    # print(FormatStr(Getdata[0]),FormatStr(Getdata[1]),FormatStr(Getdata[2]))
    i = 0
    # CountInsertData("U377cab5da50240870dab5b689b463b32")
    while i < len(Getdata)  :
        
        print(FormatStr(Getdata[i]))
        i=i+1
        
    for x in Getdata :
        lis = FormatStr(x)
        # lis = 'U377cab5da50240870dab5b689b463b32'
        print(lis)
    #   CountInsertData
        CountInsertData(lis)
    
def sumMin(data):
    if data is not None:
        for xs in data:
                result = xs
                if not all(result) == True : 
                    return 0
                else : 
                    x = result
                    return sum(x)    

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
    print('select_insertFetch--------------->',select_insertFetch)
    xSchedule = sumMin(select_insertFetch)
    print('in fn---------> ',xSchedule)
    if xSchedule == None:
        urls = 'https://api.line.me/v2/bot/message/broadcast'
        linepayload = {} 
        linepayload['type'] = 'sticker'
        linepayload['packageId'] = '789'
        linepayload['stickerId'] = '10866'


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

        print(xSchedule)

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=GetUser, trigger="cron", hour='16', minute='30')
scheduler.start()






db =  mysql.connector.connect(
        host=os.getenv('SERVER_HOST'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB'),
    )
print(db)      
def connect(userId,data,group_month,date):
    mycursor = db.cursor()
    sql = "INSERT INTO user_list_meter (user_id, meter_value, group_month, create_at) VALUES (%s, %s, %s,%s)"
    val = (userId , int(data),group_month, date)
    mycursor.execute(sql,val)

    db.commit()
    return  val 


def monthrange(data):
     if data is not None:
        for xs in data:
                result = xs
                if not all(result) == True : 
                    return 0
                else : 
                    x = result
                    # print(x)
                    return sum(x)
def calDay(data):
    if data == 1 or 3 or 5 or 7 or 8 or 10 or 12:
      return data+'/31'
    elif data == 2:
      return data+'/28' 
    elif data == 4 or 6 or 9 or 11:
      return data+'/30'
   
def calGroup(data): 
    if int(data) < 10:


      return '0'+data
    else :
      return data

def getReportBymonth(respond_dict):
    user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    Smonth = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["start_month.original"]
    Emonth = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["end_month.original"]

    select_m2 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE  user_id  =  %(user_id)s AND group_month >= %(group1)s and group_month <= %(group2)s"
    d1 = date.today().strftime("%Y")+'/'+calGroup(Smonth)
    d2 = date.today().strftime("%Y")+'/'+calGroup(Emonth)
    mycursor = db.cursor()
    #  m2
    mycursor.execute(select_m2, { 'user_id': user_id ,'group1': d1 ,'group2':d2} )
    myresult_m2 = mycursor.fetchall()
    result = monthrange(myresult_m2)

    
    answer_function = 'ช่วงเดือน '+ calGroup(Smonth)  +' - '+ calGroup(Emonth)+ '\nใช้ทั้งหมด '+ str(result)+' หน่วย'
    return answer_function

# def Getmont(month):
#     if month == "มกราคม":
#         text = "01" 
#         return text
#     elif month == "กุมภาพันธ์":
#         text = "02" 
#         return text 
#     elif month == "มีนาคม":
#         text = "03" 
#         return text   
#     elif month == "เมษายน":
#         text = "04" 
#         return text   
#     elif month == "พฤษภาคม":
#         text = "05" 
#         return text   
#     elif month == "มิถุนายน":
#         text = "06" 
#         return text   
#     elif month == "กรกฎาคม":
#         text = "07" 
#         return text   
#     elif month == "สิงหาคม":
#         text = "08" 
#         return text   
#     elif month == "กันยายน":
#         text = "09" 
#         return text   
#     elif month == "ตุลาคม":
#         text = "10" 
#         return text   
#     elif month == "พฤศจิกายน":
#         text = "11" 
#         return text   
#     elif month == "ธันวาคม":
#         text = "12" 
#         return text   
#     else :
#         text = "99" 
#         return text 

def getReportDay(respond_dict):
    user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    text_month = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["date-time.original"]
    Sd = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["date-time"]["startDate"]
    Ed = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["date-time"]["endDate"]

    # datamonth = Getmont(text_month)
    d1 = date.today().strftime("%Y")
    # month = datamonth
# +'/'+
    print('d1---------->',d1)
    # print('month---------->',datamonth)
    if text_month != False :
        mycursor = db.cursor()
       
        selectDay= "SELECT meter_value,create_at FROM `user_list_meter` WHERE user_id = %(user_id)s AND (create_at BETWEEN %(Sd)s AND %(Ed)s);"
        # selectDay= "SELECT meter_value,create_at FROM `user_list_meter` WHERE user_id = %(user_id)s  AND YEAR(create_at) = %(year)s AND MONTH(create_at) = %(month)s;"
        mycursor.execute(selectDay, { 'user_id': user_id ,'Sd': Sd ,'Ed': Ed} )

        # mycursor.execute(selectDay, { 'user_id': user_id ,'year': d1 ,'month': month} )
        resDays = mycursor.fetchall()
        print(len(resDays))
        x=FormatStr(resDays)
        i=0
        while i < len(resDays)  :
          if i != len(resDays) :
            i=i+1
        return  str(x)
          # print(FormatStr(resDays[i]))
          
          
          # text = str(resDays[i][1])+" " + str(resDays[i][0]) 
        # while i < len(resDays)  :
        #  print(resDays[i])
        #  i=i+1
         
          
      # for x in resDays :

      #   print('resDays---------->',x)
      #   print('d1---------->',d1)
      #   print('month---------->',month)
      #   text1 =  str(x[4]) +"ใช้ทั้งหมด "+ str(x[2]) + " หน่วย"
      # x='ทดสอบ'
        # return 0


    

def FormatStr(data):
    if not all(data) == True : 
        return 0
    else : 
      x = []  
      i=0
      while i < len(data):
        x.append (""+str(data[i][1])+ " ใช้ไฟ "  + str(data[i][0])+ " หน่วย "  ) 
        print(x)
        i=i+1

      # text = '\n'.join('{}: {}'.format(*val) for val in enumerate(x))
      
      if len(data) == 0 :
        x.append(str('ไม่พบข้อมูล'))
      text = ' \n'.join(map(str, x))
      return str(text)                                                                             

def getReport_mounth(respond_dict):
    user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    
    d1 = date.today().strftime("%Y")+'/01'
    d2 = date.today().strftime("%Y")+'/02'
    d3 = date.today().strftime("%Y") +'/03'
    d4 = date.today().strftime("%Y")+'/04'
    d5 = date.today().strftime("%Y")+'/05'
    d6 = date.today().strftime("%Y")+'/06'
    d7 = date.today().strftime("%Y")+'/07'
    d8 = date.today().strftime("%Y")+'/08'
    d9 = date.today().strftime("%Y")+'/09'
    d10 = date.today().strftime("%Y")+'/10'
    d11 = date.today().strftime("%Y")+'/11'
    d12 = date.today().strftime("%Y")+'/12'
    mycursor = db.cursor()
    

    # mycursor.execute()

    select_m1 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m2 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m3 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m4 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m5 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m6 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m7 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m8 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m9 = "SELECT MAX(meter_value) - MIN(meter_value)FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m10 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m11 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    select_m12 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_month  = %(group)s"
    mycursor.execute(select_m1, { 'user_id': user_id ,'group': d1 } )
    myresult_m1 = mycursor.fetchall()

    #  m2
    mycursor.execute(select_m2, { 'user_id': user_id ,'group': d2 } )
    myresult_m2 = mycursor.fetchall()

    #  m3
    mycursor.execute(select_m3, { 'user_id': user_id ,'group': d3 } )
    myresult_m3 = mycursor.fetchall()

      #  m4
    mycursor.execute(select_m4, { 'user_id': user_id ,'group': d4 } )
    myresult_m4 = mycursor.fetchall()

      #  m5
    mycursor.execute(select_m5, { 'user_id': user_id ,'group': d5 } )
    myresult_m5 = mycursor.fetchall()
    
      #  m6
    mycursor.execute(select_m6, { 'user_id': user_id ,'group': d6 } )
    myresult_m6 = mycursor.fetchall()

      #  m7
    mycursor.execute(select_m7, { 'user_id': user_id ,'group': d7 } )
    myresult_m7 = mycursor.fetchall()

      #  m2
    mycursor.execute(select_m8, { 'user_id': user_id ,'group': d8 } )
    myresult_m8 = mycursor.fetchall()

      #  m2
    mycursor.execute(select_m9, { 'user_id': user_id ,'group': d9 } )
    myresult_m9 = mycursor.fetchall()
      #  m2
    mycursor.execute(select_m10, { 'user_id': user_id ,'group': d10 } )
    myresult_m10 = mycursor.fetchall()
      #  m2
    mycursor.execute(select_m11, { 'user_id': user_id ,'group': d11 } )
    myresult_m11 = mycursor.fetchall()
      #  m2
    mycursor.execute(select_m12, { 'user_id': user_id ,'group': d12 } )
    myresult_m12 = mycursor.fetchall()
    
    m1_x1 = sumMin(myresult_m1)
    m2_x1 = sumMin(myresult_m2)
    m3_x1 = sumMin(myresult_m3)
    m4_x1 = sumMin(myresult_m4)
    m5_x1 = sumMin(myresult_m5)
    m6_x1 = sumMin(myresult_m6)
    m7_x1 = sumMin(myresult_m7)
    m8_x1 = sumMin(myresult_m8)
    m9_x1 = sumMin(myresult_m9)
    m10_x1 = sumMin(myresult_m10)
    m11_x1 = sumMin(myresult_m11)
    m12_x1 = sumMin(myresult_m12)
 
    answer_functionx = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["message"]["text"]
    if answer_functionx == "ข้อมูลรายเดือน" :
    #    m1 = sum_meter(myresultSUM) - 19
    # # sum = 0
    #    print(m1)
       result1 = m1_x1
       result2 = m2_x1
       result3 = m3_x1
       result4 = m4_x1
       result5 = m5_x1
       result6 = m6_x1
       result7 = m7_x1
       result8 = m8_x1
       result9 = m9_x1
       result10 = m10_x1
       result11 = m11_x1
       result12 = m12_x1
       xMax = max(result1,result2,result3,result4,result5,result6,result7,result8,result9,result10,result11,result12)
       print(xMax)
       if xMax == result1:
          textMax = "เดือน ม.ค."
       elif xMax == result2:
          textMax = "เดือน ก.พ."
       elif xMax == result3:
          textMax = "เดือน มี.ค."
       elif xMax == result4:
          textMax = "เดือน เม.ย."
       elif xMax == result5:
          textMax = "เดือน พ.ค."
       elif xMax == result6:
          textMax = "เดือน มิ.ย."
       elif xMax == result7:
          textMax = "เดือน ก.ค."
       elif xMax == result8:
          textMax = "เดือน ส.ค."
       elif xMax == result9:
          textMax = "เดือน ก.ย."
       elif xMax == result10:
          textMax = "เดือน พ.ย."
       elif xMax == result11:
          textMax = "เดือน ธ.ค."
       elif xMax == result12:
          textMax = "เดือน ก.พ."


       text1 = "เดือน ม.ค. ใช้ทั้งหมด "+ str(result1) + " หน่วย"
       text2 = "เดือน ก.พ. ใช้ทั้งหมด "+ str(result2) + " หน่วย"
       text3 = "เดือน มี.ค. ใช้ทั้งหมด "+ str(result3) + " หน่วย"
       text4 = "เดือน เม.ย. ใช้ทั้งหมด "+ str(result4) + " หน่วย"
       text5 = "เดือน พ.ค. ใช้ทั้งหมด "+ str(result5) + " หน่วย"
       text6 = "เดือน มิ.ย. ใช้ทั้งหมด "+ str(result6) + " หน่วย"
       text7 = "เดือน ก.ค. ใช้ทั้งหมด "+ str(result7) + " หน่วย"
       text8 = "เดือน ส.ค. ใช้ทั้งหมด "+ str(result8) + " หน่วย"
       text9 = "เดือน ก.ย. ใช้ทั้งหมด "+ str(result9) + " หน่วย"
       text10 = "เดือน ต.ค. ใช้ทั้งหมด "+ str(result10) + " หน่วย"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
       text11 = "เดือน พ.ย. ใช้ทั้งหมด "+ str(result11) + " หน่วย"
       text12 = "เดือน ธ.ค. ใช้ทั้งหมด "+ str(result12) + " หน่วย"
       answer_function = "ข้อมูลมิเตอร์ตั้งแต่ เดือน ม.ค. จนถึง ธ.ค. ของปีนี้ คือ \n" + text1 +"\n" + text2+"\n" + text3+"\n" + text4+"\n" + text5+"\n" + text6+"\n" + text7+"\n" + text8+"\n" + text9+"\n" + text10+"\n" + text11+"\n" + text12 +"\n" +"เดือนที่มีการใช้ไฟฟ้ามากที่สุดคือ " + "\n"+str(textMax) +" ใช้ "+str(xMax)+" หน่วย "
       
    # meter_value = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["meter.original"]
    # user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    d1 = date.today().strftime("%Y/%m/%d")
    token = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["replyToken"]
    # sheet.insert_row([meter_value,d1],2)
    # connect(user_id,meter_value,token,d1)
    return  answer_function 

    # END OF ADMIN CONVERSATION HANDLER TO BROADCAST MESSAGE

 
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000) )
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)





