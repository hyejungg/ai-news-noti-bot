from datetime import datetime
import pytz

def datetime_kst():
    utc_now = datetime.utcnow()
    kst = pytz.timezone('Asia/Seoul')
    kst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(kst)
    return kst_now
