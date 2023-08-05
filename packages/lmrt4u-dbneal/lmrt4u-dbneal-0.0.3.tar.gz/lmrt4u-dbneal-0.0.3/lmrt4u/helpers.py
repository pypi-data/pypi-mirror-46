# -*- coding unix -*-

from datetime import datetime

to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
