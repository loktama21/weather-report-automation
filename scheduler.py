import schedule
import time
import datetime
import os


def job():
    os.system(
        'python "C:\\Users\\Lok Tamang\\Desktop\\home\\Learn javascript-python\\Python Projects\\scrap-weather-data\\script.py"'
    )


schedule.every(15).minutes.do(job)

while True:

    next_job_time = schedule.next_run()
    current_time = datetime.datetime.now()
    remaining_time = next_job_time - current_time

    print(f"Next job scheduled at {next_job_time}. Time remaining: {remaining_time}")

    schedule.run_pending()
    time.sleep(30)
