from pytz import utc
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from bot.utils.methods.scheduler.scheduled_hw import show_daily_hw

from bot.data import config


jobstores = {
    #'mongo': MongoDBJobStore(database=config.mongodb_setting1["Database"], collection='jobs', host=config.mongodb_setting1["Host"], port=27017)
    'mongo': MongoDBJobStore(client=MongoClient(config.mongodb_url))
}

executors = {
    'processpool': ProcessPoolExecutor(24)
}



#scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone='Europe/Kiev')
scheduler = AsyncIOScheduler()


def show_hw():
    print('Пришло дз')


# print('scheduling')
for time in range(24):
    scheduler.add_job(show_daily_hw, 'cron', args=[time], hour=time)
#scheduler.add_job(show_daily_hw, 'interval', args=[12],  seconds=5)
scheduler.start()
