from datetime import date
from datetime import datetime as dt

def log_error(file, function, error):
    today = date.today()
    with open(f'searchengine/logs/{today}.txt', 'a') as log:
        log.write(
            f"\n{dt.now().strftime('%H:%M:%S')}: Error in File \"{file}\" in {function}:  {error}")