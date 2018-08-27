from apscheduler.schedulers.blocking import BlockingScheduler
#from dollarial.models import send_email_to_user
from django.core.management import call_command

from finance.management.commands import worker
from subprocess import call

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():

    call(["python", "manage.py", "worker"])
    print('salary paid')


@sched.scheduled_job('interval', minutes=2)
def timed_job2():

    call(["python", "manage.py", "autofail"])
    print('trans')


sched.start()
