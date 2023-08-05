import datetime
from pyspark.sql.types import IntegerType,StringType,DateType,TimestampType,FloatType,DoubleType,LongType
from pyspark.sql import functions as F

def beginning_of_current_month():
  return datetime.datetime.today().replace(day=1).date()

def udf_beginning_of_current_month():
    return F.udf(lambda d:beginning_of_current_month(), DateType())

udf_beginning = F.udf(lambda d:beginning_of_current_month(), DateType())