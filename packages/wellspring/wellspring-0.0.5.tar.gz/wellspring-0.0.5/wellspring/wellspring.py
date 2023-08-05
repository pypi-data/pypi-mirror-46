import datetime
from pyspark.sql.types import IntegerType,StringType,DateType,TimestampType,FloatType,DoubleType,LongType
from pyspark.sql import functions as F

def beginning_of_current_month():
  return datetime.datetime.today().replace(day=1).date()

def udf_beginning_of_current_month():
    return F.udf(lambda d:beginning_of_current_month(d), DateType())

udf_beginning = F.udf(lambda d:beginning_of_current_month(), DateType())

 # Convert date to seconds
def convert_date_to_seconds(d):
  """
  -------------
  this function returns the seconds from a date object
  """
  import datetime, time
  t = datetime.datetime.combine(d, datetime.datetime.min.time())
  return time.mktime(t.timetuple())

udf_date_to_seconds = F.udf(lambda d:convert_date_to_seconds(d), FloatType())


def udf_date_to_seconds_indef():
    return F.udf(lambda d:convert_date_to_seconds(d), FloatType())
