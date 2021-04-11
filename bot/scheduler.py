from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from bot.utils.methods.scheduler.scheduled_hw import show_daily_hw

from bot.data import config


jobstores = {
    'mongo': MongoDBJobStore(client=MongoClient(config.mongodb_url))
}

executors = {
    'processpool': ProcessPoolExecutor(24)
}

#scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone='Europe/Kiev')
scheduler = AsyncIOScheduler(timezone='Europe/Kiev')

# print('scheduling')
for time in range(24):
    scheduler.add_job(show_daily_hw, 'cron', args=[time], hour=time)
    # scheduler.add_job(show_hw, 'cron', hour=10, minute=42)
# scheduler.add_job(show_daily_hw, 'cron', args=[14], hour=20, minute=8)
# scheduler.add_job(show_daily_hw, 'interval', args=[12],  seconds=5)
scheduler.start()
