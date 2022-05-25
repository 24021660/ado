from crontab import CronTab
import os,pytz
from apscheduler.schedulers.background import BackgroundScheduler



def host_alive():
    print('cron_host_alive')
    os.system('python3 /home/project/app/cron/host_alive.py')



if __name__ == '__main__':
    scheduler = BackgroundScheduler()

    scheduler.add_job(host_alive,'cron',minute='*/1',timezone=pytz.utc)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('error')

'''
cron = CronTab(user='root')
cron.remove_all()
job = cron.new(command='python3 /home/project/app/cron/host_alive.py')
job.minute.every(1)
cron.write()
'''
