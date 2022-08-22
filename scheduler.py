from datetime import date

from flask import request
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import dotenv_values

from app import GetUser

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)

def Sometime():
    GetUser()

sched.start()