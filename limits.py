import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from firebase_service import reset_limits

day_in_sec = 60 * 60 * 24
week_in_sec = day_in_sec * 7
month_in_sec = day_in_sec * 30


def reset_day_limits():
    reset_limits('day')


def reset_week_limits():
    reset_limits('week')


def reset_month_limits():
    reset_limits('month')


scheduler = BackgroundScheduler()
scheduler.add_job(func=reset_day_limits, trigger="interval", seconds=day_in_sec)
scheduler.add_job(func=reset_week_limits, trigger="interval", seconds=week_in_sec)
scheduler.add_job(func=reset_month_limits, trigger="interval", seconds=month_in_sec)
scheduler.start()


atexit.register(lambda: scheduler.shutdown())
