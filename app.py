#code by Stackpython
#Import Library
import array
from asyncio import constants
from asyncio.windows_events import NULL
import json
import os
from types import NoneType
from flask import Flask
from flask import request
from flask import make_response

from datetime import date


#----Additional from previous file----
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pyparsing import empty


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("Bybot").worksheet('Sheet1') 


from random import randint

import mysql.connector

import os
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
# print()
#123#123

# Flask

# import mysql.connector

# db =  mysql.connector.connect(
#     host="http://128.199.208.244/",
#     user="root",
#     password="Password.lcc2030",
#     database="meter"
# )
# mycursor = db.cursor()
# text = request.get_json(silent=True, force=True)
# sql = "INSERT INTO req_question (question, result) VALUES (%s, %s)"
# val = (text["queryResult"]["intent"]["displayName"] , "Highway 21")
# mycursor.execute(sql,val )

# db.commit()


# print(request.get_json(silent=True, force=True))
# print(mycursor.rowcount, "record inserted.")
app = Flask(__name__)
@app.route('/', methods=['POST']) 
def MainFunction():

    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
  
    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป

    return r



 
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
    
    elif intent_group_question_str == 'GetselectMonthMeter': 
        answer_str = getReportBymonth(question_from_dailogflow_dict)

    else: answer_str = "ผมไม่เข้าใจ คุณต้องการอะไร"

    #สร้างการแสดงของ dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot


def menu_recormentation(respond_dict): #ฟังก์ชั่นสำหรับเมนูแนะนำ
    answer_function = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["meter.original"] + ' บันทึกค่าสำเร็จ'
    
    meter_value = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["meter.original"]
    user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    d1 = date.today().strftime("%Y/%m/%d")
    # token = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["replyToken"]
    group_mouth = date.today().strftime("%Y/%m")
    sheet.insert_row([meter_value,d1],2)
    connect(user_id,meter_value,group_mouth,d1)

# dd/mm/YY
    
    return  answer_function 

#Flask




db =  mysql.connector.connect(
        host=os.getenv('SERVER_HOST'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB'),
    )
def connect(userId,data,group_mouth,date):
    
    mycursor = db.cursor()
    sql = "INSERT INTO user_list_meter (user_id, meter_value, group_mouth, create_at) VALUES (%s, %s, %s,%s)"
    val = (userId , int(data),group_mouth, date)
    mycursor.execute(sql,val)

    db.commit()
    return  val 

   
# def sum_meter(myresult):
#     for x in myresult:
#         i=0
#         m1=int(x[i])
#         # xray= xray+ x[i]
       
#     #     sum += x
#         i = i+1 
#         return m1

# def sumMax(data):
#     Max = 0 
#     if data is None :
#         Max = 0
#     else :
#         for xs in data:
#          Max=sum(xs)
#     return Max

def sumMin(data):
    if data is not None:
        for xs in data:
                result = xs
                if not all(result) == True : 
                    return 0
                else : 
                    x = result
                    return sum(x)
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
    if data == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9:
      return '0'+data
    elif data == 10 or 11 or 12:
      return data

def getReportBymonth(respond_dict):
    user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    Smonth = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["start_month.original"]
    Emonth = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["end_month.original"]
    # select_m1 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m2 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE  user_id  =  %(user_id)s AND group_mouth >= %(group1)s and group_mouth <= %(group2)s"
    d1 = date.today().strftime("%Y")+'/'+calGroup(Smonth)
    d2 = date.today().strftime("%Y")+'/'+calGroup(Emonth)
    mycursor = db.cursor()
    #  m2
    mycursor.execute(select_m2, { 'user_id': user_id ,'group1': d1 ,'group2':d2} )
    myresult_m2 = mycursor.fetchall()
    result = monthrange(myresult_m2)
    # m1 = calMonth(Smonth)
    # m2 = calMonth(Emonth)
    # print(calGroup(Smonth),calGroup(Emonth))
    
    answer_function = 'ช่วงเดือน '+ calGroup(Smonth)  +' - '+ calGroup(Emonth)+ '\nใช้ทั้งหมด '+ str(result)+' หน่วย'
    return answer_function


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
    select_m1 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m2 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m3 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m4 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m5 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m6 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m7 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m8 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m9 = "SELECT MAX(meter_value) - MIN(meter_value)FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m10 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m11 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
    select_m12 = "SELECT MAX(meter_value) - MIN(meter_value) FROM user_list_meter WHERE user_id  =  %(user_id)s AND group_mouth  = %(group)s"
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
       answer_function = "ข้อมูลมิเตอร์ตั้งแต่ เดือน ม.ค. จนถึง ธ.ค. ของปีนี้ คือ \n" + text1 +"\n" + text2+"\n" + text3+"\n" + text4+"\n" + text5+"\n" + text6+"\n" + text7+"\n" + text8+"\n" + text9+"\n" + text10+"\n" + text11+"\n" + text12
       
    # meter_value = respond_dict["queryResult"]["outputContexts"][1]["parameters"]["meter.original"]
    # user_id = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    d1 = date.today().strftime("%Y/%m/%d")
    token = respond_dict["originalDetectIntentRequest"]["payload"]["data"]["replyToken"]
    # sheet.insert_row([meter_value,d1],2)
    # connect(user_id,meter_value,token,d1)
    return  answer_function 
 
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)

