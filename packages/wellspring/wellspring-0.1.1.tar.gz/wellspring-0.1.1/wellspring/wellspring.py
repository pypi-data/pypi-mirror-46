# %% import pyspark libraries
from pyspark.sql import functions as F
from pyspark.sql.window import Window as W
from pyspark.sql import DataFrameNaFunctions
from pyspark.sql.types import IntegerType,StringType,DateType,TimestampType,FloatType,DoubleType,LongType

# %% import python libraries
from datetime import datetime as dt
import datetime
import time
import os
import json
import math
from dateutil.rrule import rrule, MONTHLY
import dateutil.parser
import calendar
import re
import pytz
import pandas as pd
from multiprocessing.pool import ThreadPool
import bisect

# %% Get beginning of current month
def beginning_of_current_month():
  """
  Get beginning of current month
  
  Parameters:
  -----------
  None
    
  Returns:
  ----------
  datetime.date

  Example:
  ----------
  df = df.withColumn('first_day',F.lit(ws.beginning_of_current_month()))
  """
  return dt.today().replace(day=1).date()

# %% Get today date with specified hour and minutes
def TodayAt(hh, min=0, sec=0, micros=0):
  """
  Get today date with specified hour and minutes
  
  Parameters:
  -----------
  None
    
  Returns:
  ----------
  datetime.date

  Example:
  ----------
  df = df.withColumn('today_at',F.lit(ws.TodayAt()))
  """
  now = dt.now()
  return now.replace(hour=hh, minute=min, second=sec, microsecond=micros)

# %% Get today's day
def DayToday():
  """
  Get today's day
  
  Parameters:
  -----------
  None
    
  Returns:
  ----------
  datetime.date

  Example:
  ----------
  df = df.withColumn('DayToday',F.lit(ws.DayToday()))
  """
  return calendar.day_abbr[dt.today().weekday()]

# %% Get current time
def TimeNow():
  """
  Get current time
  
  Parameters:
  -----------
  None
    
  Returns:
  ----------
  datetime.date

  Example:
  ----------
  df = df.withColumn('first_day',F.lit(ws.TimeNow()))
  """
  return dt.now()

# %% Get Today's date
def DateToday():
  """
  Get Today's date
  
  Parameters:
  -----------
  None
    
  Returns:
  ----------
  datetime.date

  Example:
  ----------
  df = df.withColumn('first_day',F.lit(ws.DateToday()))
  """
  return dt.today().date()


# %% Convert date to seconds
def convert_date_to_seconds(d):
  """
  This function convert a date object to seconds elapsed from epoch
  
  Parameters:
  -----------
  d : datetime.date

  Returns
  -----------
  new_i  : int

  Example
  ------------
  df = df.withColumn('dateinseconds',ws.convert_date_to_seconds(df['date']))
  """
  t = dt.combine(d, dt.min.time())
  return time.mktime(t.timetuple())


# %% Convert all files with months and year
def CombineAllFilesWithMonths(dirpath,filesep='_',yyyymmorwwsep='.',yyyy_position=1,mmorww_position=2,mm=True):
  """
  Combine multiple parquet files from the same directory and read month or week number from the filename.
  The function creates another date column "snapshot_date" in the spark.dataframe.
  
  Parameters:
  -----------
  dirpath : String
      directory path where to read the files from
      
  filesep : String
      file separators
  
  yyyymmorwwsep : String
      separator for year and month or week
  
  yyyy_position : Boolean
      position after file split on years
  
  mmorww_position : Boolean
      position for month or week
  
  mm : Boolean
      if month then mm=True, if week then mm=False
  
  Returns:
  ----------
  df = spark.DataFrame
  
  Example:
  ----------
  df = ws.CombineAllFilesWithMonths('/landing/internal/bu/l/wellspring/transfer_pricing',filesep='_',yyyymmorwwsep='_',yyyy_position=3,mmorww_position=4,mm=True)
  """
  directory = hdf_path(dirpath)
  files = listFilesByExtension(directory,extension='parquet') #list the files in the given directory
  df = spark.read.parquet(hdf_path(dirpath))
  df = df.withColumn('snapshot_date',F.lit(None))
  column_names = df.columns
  df = spark.createDataFrame([tuple('' for i in column_names)],column_names).where("1=0")
  for file in files:
      data = spark.read.parquet(file)
      file = file.replace('.','_').replace(filesep,'_').replace(yyyymmorwwsep,'_').split('_')
      print(file)
      yyyy = int(file[yyyy_position])
      mmorww = int(file[mmorww_position])
      if mm:
        snapshot_date = get_start_end_dates_month(yyyy,mmorww)[0]
      else:
        snapshot_date = get_start_end_dates(yyyy,mmorww)[0]
      data = data.withColumn('snapshot_date',F.lit(snapshot_date))
      df = df.unionByName(data)
  df = df.withColumn('snapshot_date',F.to_date('snapshot_date','yyyy-MM-dd'))
  return df


# %% change string type of columns to date type
def ConvertToDate(df_name,listofcolumns,format='yyyyMMdd'):

  """
  Converts a list of column in a spark dataframe, from string type to date type
  
  Parameters:
  -----------
  df_name : spark.DataFrame
      name of the data frame to change

  listofcolumns : list 
      list of columns to be converted to date
      
  format : str
      specify the format of the input string

  Returns:
  -----------
  df_name : spark.DataFrame
      Output Data Frame

  Example:
  -----------
  listofcolumns = ["column1", "column2", "column3"]
  df_name = ws.ConvertToDate(df_name, listofcolumns)
  """

  for listofcolumn in listofcolumns:
    df_name = df_name.withColumn(listofcolumn, F.to_date(listofcolumn,format))
    print("Column -- %s -- changed to type date..." % listofcolumn)

  return df_name


# %% filter one column with multiple values
def FilterColumnsList(df, column_name, filtervalues):
  
  """
  Filters a spark dataframe on a specific column with list of values.
  
  Parameters:
  -----------
  df : spark.DataFrame
      Initial Data Frame
  
  column_name : Column name String
      Column to filter on
  
  filtervalues : list
      List of values to be filter
  
  Returns:
  -------
  df : spark.DataFrame
      Output Data Frame

  Example:
  -----------
  df = ws.FilterColumnsList(df,column_name,filtervalues)
  """

  df = df.where(F.col(column_name).isin(filtervalues))
  print("Data Frame has been filtered...")
  return df
  
  
# %% combine two tables with unequal schemas
def harmonize_schemas_and_combine(df_left, df_right):

  """
  Harmonize schemas and combine to datasets
  
  Parameters:
  -----------
  df_left : spark.DataFrame
      Input Data Frame 1
  
  df_right : spark.DataFrame
      Input Data Frame 2

  Returns:
  ------------
  df_new : spark.DataFrame
      Output Data Frame
      
  Example:
  -----------
  df_new = ws.harmonize_schemas_and_combine(df_1, df_2)
  """
  left_types = {f.name: f.dataType for f in df_left.schema}
  right_types = {f.name: f.dataType for f in df_right.schema}
  left_fields = set((f.name, f.dataType, f.nullable) for f in df_left.schema)
  right_fields = set((f.name, f.dataType, f.nullable) for f in df_right.schema)

  # First go over left-unique fields
  for l_name, l_type, l_nullable in left_fields.difference(right_fields):
      if l_name in right_types:
          r_type = left_types[l_name]
          if l_type != r_type:
              raise TypeError
              print("Union failed. Type conflict on field %s. left type %s, right type %s" % (l_name, l_type, r_type))
          else:
              raise TypeError
              print("Union failed. Nullability conflict on field %s. left nullable %s, right nullable %s"  % (l_name, l_nullable, not(l_nullable)))
      df_right = df_right.withColumn(l_name, F.lit(None).cast(l_type))

  # Now go over right-unique fields
  for r_name, r_type, r_nullable in right_fields.difference(left_fields):
      if r_name in left_types:
          l_type = right_types[r_name]
          if r_type != l_type:
              raise TypeError
              print("Union failed. Type conflict on field %s. right type %s, left type %s" % (r_name, r_type, l_type))
          else:
              raise TypeError
              print("Union failed. Nullability conflict on field %s. right nullable %s, left nullable %s" % (r_name, r_nullable, not(r_nullable)))
      df_left = df_left.withColumn(r_name, F.lit(None).cast(r_type))    

  # Make sure columns are in the same order
  df_left = df_left.select(df_right.columns)
  return df_left.union(df_right)
  

# %% Return the latest update date and time for a specific folder or file
def LatestUpdateTime(path,HDF_landing=False):
  """
  Return the latest update date and time for a specific folder or file
  
  Parameters:
  -----------
  path : str
      path of the directory

  Returns:
  ------------
  date : str
      latest update date of the source table
      
  Example:
  -----------
  1. landingpath = hdf_path("/landing/internal/edw10/HORDEO16/")
  2. trustedpath = hdf_path("/trusted/internal/edw10/HORDEO16_B_L_ORDER_ITEMS_OTC.parquet/")
  3. print(ws.LatestUpdateTime('/landing/internal/edw10/HORDEO12/'))
  """
  URI           = sc._gateway.jvm.java.net.URI
  Path          = sc._gateway.jvm.org.apache.hadoop.fs.Path
  FileSystem    = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
  Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration
  fs = FileSystem.get(URI('hdf.azuredatalakestore.net'), Configuration())

  if HDF_landing:
    # for landing folder, find newest path and find all parquet files
    path = hdf_newest_path(hdf_path(path))
    files = listFilesByExtension(hdf_path(path),extension="parquet")
  else:
    # for HDF trusted folder, no listing of parquet files are needed
    files = [hdf_path(path)]

  modifiedDateTime = []
  for file in files:
      status = fs.listStatus(Path(hdf_path(file)))[0]
      x = dt.fromtimestamp(status.getModificationTime()/1000.0)
      modifiedDateTime.append(x)
  return max(modifiedDateTime)


# %% Read cleaned table by renaming and droping specific columns
def ReadParquet(f_name,data_path,dict_json):

  """
  Read a parquet directory and create a spark dataframe
  
  Parameters:
  -----------
  f_name : str
      name of the folder/table to be cleaned
  data_path : str
      directly where the folder/table is located
  dict_json : str
      location of the json file that has the data regarding the table cleaning 

  Returns:
  ------------
  df_new : spark.DataFrame
      Output Data Frame
      
  Example:
  -----------
  f_name = "HZORGX01"
  data_path = "/lab/_projects/wellspring/edw10_copy/"
  json_path = ws_root+"/data_dictionary/edw10/renames/region.json"
  df_name = ws.ReadParquet(f_name,data_path,json_path)
  """
  
  f_path = hdf_path(data_path + "%s.parquet" % f_name)
  df_name = spark.read.parquet(f_path)
  print('Parquet files are loaded into the Data Frame successfully...')
  
  json_path = hdf_path(ws_root+config_path+'/references/data_dictionary/'+dict_json,local=True,is_file=True)
  my_json = pd.read_excel(json_path)
  my_json = my_json.values.tolist()
  print('Data dictionary for table %s loaded successfully...' % f_name)
  
  renames = [
              [x[0], x[1]]
              for x in my_json
            ]
  print('Rename columns list for %s generated successfully...' % f_name)
  columns = [x[1]
              for x in my_json
              if x[2] == True
              ]
  
  print('Selected columns list for %s generated successfully...' % f_name)
  print('There are %d columns to keep for %s...' % (len(columns),f_name))

  if len(df_name.columns) == len(renames):
    df_name = RenameColumns(df_name, renames)
    df_name = df_name.select(columns)
    print('Selected columns are kept for the table %s...' % f_name)
    return df_name
  else :
    df_name = RenameColumns(df_name, renames)
    df_name = df_name.select(columns)
    print('Number of columns in data dictionary are incorrect!')
    print('Number of Columns in df is %f and in config file is %f' % (len(df_name.columns),len(renames)))
    return df_name


# %% Read data by providing alias
def ReadData(alias):
  
  """
  Just provide alias nad supply the rest in the configuration file.
  
  Parameters:
  -----------
  alias : string
      Input string

  Returns:
  ------------
  df : spark.DataFrame
      Output Data Frame 
  """
  table_name = cfg['input_path'][alias]['table_name']
  data_dir_path = cfg['input_path'][alias]['data_dir_path']
  dict_json = cfg['input_path'][alias]['dict_json']
  df = ws.ReadParquet(table_name, data_dir_path, dict_json)
  return df


# %% Save (overwrite) parquet file with partition
def SaveParquetwithPartition(df,fpath,partitioncols):
  """
  Save dataframe as parquet files and partition col
  
  Parameters:
  -----------
  df: spark.DataFrame
      Input dataframe
  
  fpath : str
      path to save at
  
  partitioncols : List
      list of columns to partition on
  
  Returns:
  -------
  None
  
  Example:
  -----------
  ws.SaveParquetwithPartition(df,fpath,partitioncols)
  """
  dbutils.fs.rm(fpath,recurse=True)

  newpartitioncols = []
  for column in partitioncols:
    newcol = 'partBy_'+column
    newpartitioncols.append(newcol)
    df = df.withColumn(newcol,F.col(column))

  count = df.count()
  parts = math.ceil((count * len(df.columns)) / 50000000)
  print('Number of rows are : '+str(count))
  print('Number of files : '+str(parts))
  fpath = hdf_path(fpath+".parquet")
  df.repartition(parts).write.mode('overwrite').partitionBy(*newpartitioncols).parquet(fpath)
  return None


# %% Save (overwrite) parquet file without partition
def SaveParquet(df,fpath):
  """
  Save data frame as parquet files without partition
  Parameters:
  -----------
  df: spark.DataFrame
      Input data frame
  
  fpath : str
    path to save output parquet files at
  
  Returns:
  -------
  None
  
  Example:
  -----------
  ws.SaveParquet(df,fpath)
  """
  dbutils.fs.rm(fpath,recurse=True)
  count = df.count()
  parts = math.ceil((count * len(df.columns)) / 50000000)
  print('Number of rows are : '+str(count))
  print('Number of files : '+str(parts))
  df = df.repartition(parts)
  fpath = hdf_path(fpath+".parquet")
  df.write.mode('overwrite').parquet(fpath)
  print('Writing to database successful!')
  return None


# %% Rename the column headers for a spark dataframe
def RenameColumns(df_old, renames):
  
  """
  Rename the column headers for a spark dataframe
  
  Parameters:
  -----------
  df_old : spark.DataFrame
      Initial Data Frame
  
  renames : list
      List of columns to rename, like:

  Returns:
  -------
  None
  
  Example:
  -----------
  df_new = ws.RenameColumns(df_old,renames)
  """

  df_new = df_old
  
  for rename in renames:
      df_new = df_new.withColumnRenamed(rename[0], rename[1])
  print("Column headers are renamed successfully...")
  return df_new


# %% call a notebook to run for another notebook
def run_notebook(notebook):

  """
  Parameters:
  -----------
  notebook : string 
      relative path to the notebook to run

  Returns:
  ------------
  None
  
  Example:
  -----------
  ws.run_notebook('4_customer')
  """

  return dbutils.notebook.run(path=notebook, timeout_seconds=0)


# %% call list of notebooks to run in parallel
def RunParallelNotebooks(notebooks,ThreadPoolCount=25):
  
  """
  Run parallel notebooks with a specified thread pook count.
  
  Parameters:
  -----------
  notebooks : list
      list of notebooks to run in parallel 
      relative path is taken automatically only the notebook name to run in a list
      notebooks = ['3_shipment','4_customer']

  Returns:
  ------------
  None
  
  Example:
  -----------
  notebooks = ['3_shipment','4_customer']
  ws.RunParallelNotebooks(notebooks,ThreadPoolCount=30)
  """

  pool_x = ThreadPool(ThreadPoolCount)
  results = pool_x.map(lambda notebook: run_notebook(notebook=notebook), notebooks)
  pool_x.close()
  return results


# %% save a temporary CSV File
def SaveTempCsv(df_csv,fpath):
  """
  Saving a spark dataframe as csv
  Parameters
  -----------
  df_csv : spark.DataFrame
      Data Frame to be saved in CSV
      
  filename : str
      FileName to be saved at the temp location
  
  Returns
  -----------
  None
  
  Example:
  -----------
  ws.SaveTempCsv(dataframe,filename as string)
  """
  df_csv.coalesce(1).write.format("com.databricks.spark.csv").save(
  hdf_path(fpath),
  header=True,
  mode="overwrite",
  )
  print('CSV file saved successfully at '+hdf_path(fpath))
  return None


# %% Tracker for tracking update date and times
def Tracker(definition,landingpath='',trustedpath='',fromHDF=False):
  """
  This is used to track schedules for different workflows in wellspring
  
  Parameters
  -----------
  definition : str
      if Local extraction then use the definition coming from Excel file
      if HDF, then its free text field
      
  landingpath : str
      path in HDF Landing area, only required when fromHDF = True
  
  trustedpath : str
      path in HDF Trusted area, only required when fromHDF = True
  
  fromHDF : bool
      Default False, True if definition tracking is from HDF
  
  Returns
  -----------
  df : spark.DataFrame
  
  Example
  -----------
  1. example for Tracking with Excel uploads
  df = ws.Tracker('Inventory Daily (EU28)',landingpath)

  2. example for Tracking with HDF as source Data
  definition = 'end-to-end'
  landingpath = hdf_path('/landing/internal/edw10/HORDEO16')
  trustedpath = hdf_path('/trusted/internal/edw10/HORDEO16_B_L_ORDER_ITEMS_OTC.parquet')
  df = ws.Tracker(definition,landingpath,trustedpath,fromHDF=True)
  """
  
  if not fromHDF:
    # Read all tracker Files
    f_path = hdf_path("/landing/internal/bu/l/wellspring/update_date_time_tracker/*.parquet")
    df = spark.read.parquet(f_path)
  
    # Filter on the definition
    df = df.filter(df.definition==definition)
    df = df.withColumn('source',F.when(df.source=='KNIME','Manipulation')
                                 .when(df.source !='KNIME','Extraction')
                                 .otherwise(df.source)
                      )
    df = df.withColumn('execution_place',F.when(df.source=='Manipulation','Wellspring').otherwise(df.execution_place))
    df = df.withColumn('planned',F.to_date('planned_date_utc'))
    df = df.withColumn('planned',F.concat(df.planned,F.lit(" "),df.planned_time_utc))
    df = df.withColumn('planned',df.planned.cast(TimestampType()))
    df = df.withColumn('actual',df.actual_date_utc.cast(TimestampType()))
    df = df.drop(*['description','region','planned_date_utc','planned_time_utc','actual_date_utc','actual_time_utc','__index_level_0__'])

    # add another row for reading update date in landing
    myjson = [{
                  "definition": definition,
                  "source": "Ingestion",
                  "execution_place": "Docker",
                  "planned": str(TimeNow())
              }]

    json_dump=[json.dumps(myjson)]
    jsonRDD = sc.parallelize(json_dump)
    df1 = spark.read.json(jsonRDD)

    df1 = df1.withColumn('actual',F.lit(LatestUpdateTime(landingpath,HDF_landing=False)))

    df = df.unionByName(df1)

    df = df.withColumn('actual',F.when((df.source=='Manipulation') & (df.definition==definition),F.current_timestamp())
                                 .otherwise(df.actual)
                      )

    df = df.withColumn('flag',F.when(
                                      (df.planned>df.actual) & 
                                      (F.to_date(df.planned)==F.to_date(df.actual))
                                      ,1).otherwise(0)
                      )
    df = df.withColumn('planned',F.to_timestamp('planned'))
    return df
  else:

    # add another row for reading update date in landing
    myjson = [{
                  "definition": definition,
                  "source": "Extraction",
                  "execution_place": "HDF",
                  "planned": str(TimeNow())
              }]

    json_dump=[json.dumps(myjson)]
    jsonRDD = sc.parallelize(json_dump)
    df1 = spark.read.json(jsonRDD)

    landingUpdateTime = LatestUpdateTime(landingpath,HDF_landing=True)
    df1 = df1.withColumn('actual',F.lit(landingUpdateTime))

    # add another row for reading update date in landing
    myjson = [{
                  "definition": definition,
                  "source": "Ingestion",
                  "execution_place": "HDF",
                  "planned": str(landingUpdateTime)
              }]

    json_dump=[json.dumps(myjson)]
    jsonRDD = sc.parallelize(json_dump)
    df2 = spark.read.json(jsonRDD)

    trustedUpdateTime = LatestUpdateTime(trustedpath,HDF_landing=False)
    df2 = df2.withColumn('actual',F.lit(trustedUpdateTime))

    df3 = df1.unionByName(df2)

    myjson = [{
                  "definition": definition,
                  "source": "Manipulation",
                  "execution_place": "Wellspring",
                  "planned": str(trustedUpdateTime)
              }]

    json_dump=[json.dumps(myjson)]
    jsonRDD = sc.parallelize(json_dump)
    df4 = spark.read.json(jsonRDD)

    df4 = df4.withColumn('actual',F.lit(F.current_timestamp()))

    df5 = df3.unionByName(df4)

    df = df5.withColumn('flag',F.when(
                                        (df5.source == 'Extraction') & 
                                        (F.to_date(df5.planned)==F.to_date(df5.actual))
                                    ,1)
                                .when(
                                        (df5.planned<df5.actual) & 
                                        (F.to_date(df5.planned)==F.to_date(df5.actual))
                                   ,1)
                                .otherwise(0)
                        )
    df = df.withColumn('planned',F.to_timestamp('planned'))
    return df


# %% Cleaning a html to simple text - parse HTML
def cleanhtml(raw_html):
  """
  Parse HTML tags and return simple text
  
  Parameters:
  -----------
  raw_html : str

  Returns:
  -----------
  re : str

  Example:
  ------------
  df = df.withColumn('raw_html',ws.udf_cleanhtml(df['raw_html']))
  """
  try:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
  except:
    cleantext = ""
  return cleantext


# %% Get differnce between two date time objects  
def datetimediff(d2_ts,d1_ts):
  """
  To find difference between two date time objects in days, hours, min, seconds
  
  Parameters
  -----------
  d2_ts: str
  d1_ts: str

  Returns
  -----------
  difference: Tuple (days, hours, min, sec)

  Example
  ------------
  1. example to get date time difference in hour
  df = df.withColumn('delta_hour',ws.udf_date_time_diff_hour(df['d2'], df['d1']))
  """
  try:
    fmt = '%Y-%m-%d %H:%M:%S'
    d1_ts = dt.strptime(d1_ts, fmt)
    d2_ts = dt.strptime(d2_ts, fmt)

    # Convert to Unix timestamps
    d1_ts = time.mktime(d1_ts.timetuple())
    d2_ts = time.mktime(d2_ts.timetuple())

    # They are now in seconds, just subtract
    delta_days = int((d2_ts-d1_ts) / (24*60*60))
    delta_hour = int((d2_ts-d1_ts) / (60*60))
    delta_min = int((d2_ts-d1_ts) / (60))
    delta_sec = int((d2_ts-d1_ts))
    return delta_days,delta_hour,delta_min,delta_sec
  
  except:
    return None,None,None,None


# %% Yield all combinations of valid date formats for EDW
def DateFormatsEDW():
  """Yield all combinations of valid date formats."""
  from itertools import permutations
  formats = []
  date = ("%Y%m%d")
  hours = ("%H","",)
  minutes = ("%M","",)
  seconds = ("%S","",)

  for hour in hours:
          for minute in minutes:
              for second in seconds:
                  for combo in permutations([second, minute, hour]):
                      time = "".join(combo).strip(":")
                      formats.append((date+" "+time).strip(" ")) 
  formats = list(dict.fromkeys(formats))
  formats = sorted(formats, key=len, reverse=True)
  formats = ['%Y%m%d %H%M%S']+formats
  return formats

# %% Concatenate EDW Date and EDW time column to give date time
def ConcatenateEDWDateTime(dateAsString,timeAsString,formats=DateFormatsEDW()):
  """
  Concatenate EDW Date and EDW time column to give date time
  
  Parameters:
  -----------
  dateAsString : str
  timeAsString : str
  formats : getting list of formats from DateFormatsEDW() function

  Returns:
  -----------
  date : datetime.datetime

  Example:
  ------------
  
  """
  if not timeAsString.strip():
    date = dateAsString
  else:
    date = dateAsString+" "+timeAsString
  
  for fmt in formats:
    try:
      date = dt.strptime(date, fmt)
      return date
    except:
      pass


# %% Yield all combinations of valid date formats for dates with - as separator
def DateFormatswithDashes():
  """Yield all combinations of valid date formats."""
  from itertools import permutations
  formats = []
  date = ("%Y-%m-%d")
  hours = ("%H","",)
  minutes = ("%M","",)
  seconds = ("%S","",)

  for hour in hours:
          for minute in minutes:
              for second in seconds:
                  for combo in permutations([second, minute, hour]):
                      time = ":".join(combo).strip(":")
                      formats.append((date+" "+time).strip(" ")) 
  formats = list(dict.fromkeys(formats))
  formats = sorted(formats, key=len, reverse=True)
  formats = ['%Y-%m-%d %H:%M:%S']+formats
  return formats


# %% Return short abbreviation of day from any date 
def GetDayFromDate(date,formats=DateFormatswithDashes()):
  """
  Get Day from Date
  
  Parameters:
  -----------
  dt : str
      date as string

  Returns:
  -----------
  day : str
      day from date

  Example :
  -----------
  df = df.withColumn('day',ws.udf_get_day_from_date(df['date']))
  """
  
  for fmt in formats:
    try:
      date = dt.strptime(date, fmt)
      day = calendar.day_abbr[dt.weekday()]
      return day
    except:
      pass


# %% Get End of month date
def get_eom(date):
  """
  Get End of the month date from a given date
  
  Parameters:
  -----------
  date : datetime.date
      any date

  Returns:
  -----------
  date : datetime.date
      end of the month

  Example:
  -----------
  df = df.withColumn('date',ws.udf_eom(df['date']))
  """
  date = date.replace(day=1)
  date = date + dt.timedelta(32)
  date = date.replace(day=1)
  date = date-dt.timedelta(1)
  return date


# %% Get Start of the month date
def get_som(date):
  """
  Get Start of the month date from a given date
  
  Parameters
  -----------
  date : datetime.date

  Returns
  -----------
  date : datetime.date

  Example
  ------------
  df = df.withColumn('date',ws.udf_som(df['date']))
  """
  return date.replace(day=1)


# %% Return hour from a datetime
def GetHour(dt,formats=DateFormatswithDashes()):
  """
  Get hour from the current date
  
  Parameters
  -----------
  dt: str
      date in the form of string

  Returns
  -----------
  hh: int
      returns the hour

  Example:
  -----------
  df = df.withColumn('hour',ws.udf_get_hour_from_datetime(df['datetime']))
  """
  for fmt in formats:
    try:
      dt = dt.strptime(dt, fmt)
      hh = int(dt.strftime(dt,'%H'))
      return hh
    except:
      pass


# %% Return minute from a datetime
def GetMin(date,formats=DateFormatswithDashes()):
  """
  Get min from the current date
  
  Parameters
  -----------
  date: str

  Returns
  -----------
  min: int
  
  Example:
  -----------
  df = df.withColumn('min',ws.udf_get_min_from_datetime(df['datetime']))
  """
  for fmt in formats:
    try:
      date = dt.strptime(date, fmt)
      min = int(dt.strftime(date,'%M'))
      return min
    except:
      pass


# %% Get beginning of quarter
def get_quarter_begin(datecol):
  """
  Get beginning of quarter from the date provided
  
  Parameters
  -----------
  datecol : datetime.date

  Returns
  -----------
  date : datetime.date

  Example:
  ------------
  df = df.withColumn('date',ws.udf_soq(df['date']))
  """
  qbegins = [dt.date(datecol.year, month, 1) for month in (1,4,7,10)]
  idx = bisect.bisect(qbegins, datecol)
  return qbegins[idx-1]
  
  
# %% Get end date of the quarter
def get_quarter_end(datecol):
  """
  Get end date of the quarter
  
  Parameters:
  -----------
  datecol : datetime.date

  Returns:
  -----------
  date : datetime.date

  Example:
  ------------
  df = df.withColumn('date',ws.udf_eoq(df['date']))
  """
  qbegins = [dt.date(datecol.year, month, 1) for month in (3,6,9,12)]
  gends = list(map(get_eom,qbegins))
  idx = bisect.bisect(gends, datecol)
  if idx>3:
    idx=3
  return gends[idx]


# %% Get date for Start and End of the week
def get_start_end_dates_week(year, week):
  """
  Get date for Start and End of the week
  
  Parameters:
  -----------
  year  : int
  week  : int

  Returns
  -----------
  start_date  : datetime.date
  end_date  : datetime.date

  Example
  ------------
  df = df.withColumn('first_day',ws.udf_first_day(df['year'],df['ww']))
  df = df.withColumn('last_day',ws.udf_last_day(df['year'],df['ww']))
  """
  d = dt.date(year,1,1)
  if(d.weekday()<= 3):
    d = d - dt.timedelta(d.weekday())
  else:
    d = d + dt.timedelta(7-d.weekday())
  dlt = dt.timedelta(days = (week-1)*7)
  start_date = d + dlt
  end_date = d + dlt + dt.timedelta(days=6)
  return start_date, end_date


# %% Get dates for Start and End of the month
def get_start_end_dates_month(year, month):
  """
  Get date for Start and End of the month
  
  Parameters:
  -----------
  year  : int
  month  : int

  Returns
  -----------
  start_date  : datetime.date
  end_date  : datetime.date

  Example
  ------------
  df = df.withColumn('first_day',ws.udf_first_day_month(df['year'],df['ww']))
  df = df.withColumn('last_day',ws.udf_last_day_month(df['year'],df['ww']))
  """
  d = dt.date(year,month,1)
  start_date = get_som(d)
  end_date = get_eom(d)
  return start_date, end_date


# %% Removes the leading zeros from any string
def remove_leading_zero(i):
  """
  This function remove leading zeros
  
  Parameters:
  -----------
  i : string

  Returns
  -----------
  new_i : string

  Example
  ------------
  df = df.withColumn('mat_num',ws.remove_leading_zero(df['mat_num']))
  """
  try:
    new_i = i.lstrip('0')
    return new_i
  except:
    pass


# %% Change Time Zone from UTC to Local
def utc_to_local(utc_dt,tz):
  """
  This function converts utc date to local date
  
  Parameters
  -----------
  utc_dt  : datetime.timezone
  tz  : str
      timezone

  Returns
  -----------
  local_dt  : datetime.timezone

  Example
  ------------
  df = df.withColumn('dt_local',ws.udf_utc_to_local(df['dt_utc'], df['timezone']))
  """
  try:
    utc_dt = dt.strptime(utc_dt,'%Y-%m-%d %H:%M:%S')
    local_tz = pytz.timezone(tz)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    local_dt = local_dt.replace(tzinfo=None)
    local_dt = dt.strftime(local_dt,'%Y-%m-%d %H:%M:%S')
    return local_dt  
  except:
    return utc_dt


# %% Declaring lambda functions based on above functions
udf_wk_mnt_format = F.udf(lambda x:'{0:0>2}'.format(x),StringType())
udf_format_plant = F.udf(lambda x: '{0:0>4}'.format(x), StringType())
udf_utc_to_local = F.udf(lambda x,y:utc_to_local(x,y), StringType())
udf_beginning_of_current_month = F.udf(lambda d:beginning_of_current_month(), DateType())
udf_convert_date_to_seconds = F.udf(lambda d:convert_date_to_seconds(d), FloatType())
udf_cleanhtml = F.udf(lambda x:cleanhtml(x), StringType())
udf_date_time_diff_days = F.udf(lambda d2,d1:datetimediff(d2,d1)[0], IntegerType())
udf_date_time_diff_hour = F.udf(lambda d2,d1:datetimediff(d2,d1)[1], IntegerType())
udf_date_time_diff_min = F.udf(lambda d2,d1:datetimediff(d2,d1)[2], IntegerType())
udf_date_time_diff_sec = F.udf(lambda d2,d1:datetimediff(d2,d1)[3], IntegerType())
udf_EDWDateTime = F.udf(lambda d,tm:ConcatenateEDWDateTime(d,tm), TimestampType())
udf_day_from_date = F.udf(lambda d:GetDayFromDate(d), StringType())
udf_eom = F.udf(lambda x:get_eom(x), DateType())
udf_som = F.udf(lambda x:get_som(x), DateType())
udf_get_hour_from_datetime = F.udf(lambda d:GetHour(d), IntegerType())
udf_get_min_from_datetime = F.udf(lambda d:GetMin(d), IntegerType())
udf_soq = F.udf(lambda x:get_quarter_begin(x), DateType())
udf_eoq = F.udf(lambda x:get_quarter_end(x), DateType())
udf_first_day = F.udf(lambda x,y:get_start_end_dates_week(x,y)[0], DateType())
udf_last_day = F.udf(lambda x,y:get_start_end_dates_week(x,y)[1], DateType())
udf_first_day_month = F.udf(lambda x,y:get_start_end_dates_month(x,y)[0], DateType())
udf_last_day_month = F.udf(lambda x,y:get_start_end_dates_month(x,y)[1], DateType())
udf_remove_leading_zero = F.udf(lambda x: remove_leading_zero(x), StringType())
udf_date_to_seconds = F.udf(lambda d:convert_date_to_seconds(d), FloatType())