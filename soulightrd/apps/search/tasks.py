from celery.task import PeriodicTask
from celery.task.schedules import crontab
from celery.decorators import periodic_task 

from soulightrd.settings import ROOT_PATH 

from sys import path

import os

@periodic_task(run_every=crontab(minute=0, hour='*/3'))
def update_search_index():  
	path.append(ROOT_PATH)
	cmd = "python manage.py update_index"
	os.system(cmd)


