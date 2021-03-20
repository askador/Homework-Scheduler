from pytz import utc
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

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
#scheduler.add_job(show_hw, 'cron', hour=14, minute=13)
#scheduler.add_job(show_hw, 'interval', seconds=5)
# scheduler.start()
