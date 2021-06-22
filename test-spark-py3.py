# code by Afik Bar, from email 2021-06-04

import sys
import random

major = sys.version_info[0]
if major != 3:
    raise Exception("Please use Python 3")
    

from pyspark.sql import SparkSession
from pyspark.mllib.random import RandomRDDs

def init_spark(app_name):
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    sc = spark.sparkContext
    return spark, sc



def main():
    if len(sys.argv) == 2:
        length = sys.argv[1]
    else:
        length = 10**3
    print("26")
    data0_1  = RandomRDDs.uniformVectorRDD(sc, length, 3) \
        .map(lambda a : a.round(3).tolist()) \
            .toDF()
    print("30")
    name = "random_data{}.parquet".format( 333 ) # random.randrange(200))
    print("using name="+ name)
    data0_1.write.parquet(name)
    print("33")

    read_df = spark.read.parquet(name)
#    print(f"Read {read_df.count()} records. Should be {length} records.") # for python 3
    print("Read {} records. Should be {} records.".format(read_df.count(),length) ) # for python 3
#    print "Read %d records. Should be %d records." % (read_df.count(),length ) 

if __name__ == '__main__':
    spark, sc = init_spark('demo222')
    print ("before calling main")
    main()
    print ("after main returned")
    
