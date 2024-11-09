from datetime import datetime, timezone

import pytz


def get_datetime_kst():
    utc_now = datetime.now(timezone.utc)
    kst = pytz.timezone("Asia/Seoul")
    kst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(kst)
    return kst_now
