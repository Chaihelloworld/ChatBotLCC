import schedule
import time

from getusers import GetUser

def func():
  print("Check schedule")

schedule.every().day.at("16:00").do(GetUser)
schedule.every(60).seconds.do(func)

# schedule.every().day.at("10:30:42").do(job)
while True:
  schedule.run_pending()
  time.sleep(1)