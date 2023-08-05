import datetime

def beginning_of_current_month():
  return datetime.datetime.today().replace(day=1).date()