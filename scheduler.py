from datetime import date

from flask import request
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import dotenv_values

from app import GetUser

sched = BlockingScheduler()

sched.add_job(GetUser, 'cron', month='1-12', day='*', hour='22', minute='05')

sched.start()
