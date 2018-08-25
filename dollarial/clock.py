from apscheduler.schedulers.blocking import BlockingScheduler
#from dollarial.models import send_email_to_user
from django.core.management import call_command

from finance.management.commands import worker
from subprocess import call

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():


    print('This job is run every 1 minutes$$$$')

    #cmd = worker.Command()
    #opts = {}  # kwargs for your command -- lets you override stuff for testing...
    #cmd.handle_noargs(**opts)

    #call_command('worker')
    call(["python", "manage.py", "worker"])
    #send_email_to_user('salam', 'parand1997@gmail.com', 'parand1997@gmail.com', 'bother')
    print('This job is run every 1 minutes.')

sched.start()
