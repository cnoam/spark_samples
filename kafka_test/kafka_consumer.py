"""
Example code: consuming KAFKA data stream.

The Kafka server is located in Azure and has no security
It contains preloaded weather data.

"""
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.spark:spark-sql-kafka_-0-10_2.12:3.1.1 pyspark-shell"

#os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.spark:spark-sql-kafka_-0-10_2.12:3.1.1 pyspark-shell"
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import *

def init_spark(app_name: str):
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    sc = spark.sparkContext
    return spark, sc

def main():
    kafka_server = 'dds2020s-kafka_.eastus.cloudapp.azure.com:9092'
    # Subscribe to multiple topics
    kafka_raw_df = spark \
        .read \
        .format("kafka_") \
        .option("kafka_.bootstrap.servers", kafka_server) \
        .option("subscribe", "EZ") \
        .option("startingOffsets", "earliest") \
        .load()

    noaa_schema = StructType([StructField('StationId', StringType(), False),
                                StructField('Date', IntegerType(), False),
                                StructField('Variable', StringType(), False),
                                StructField('Value', IntegerType(), False),
                                StructField('M_Flag', StringType(), True),
                                StructField('Q_Flag', StringType(), True),
                                StructField('S_Flag', StringType(), True),
                                StructField('ObsTime', StringType(), True)])


    kafka_value_df = kafka_raw_df.selectExpr("CAST(value AS STRING)")
    json_df = kafka_value_df.select(F.from_json(F.col("value"), schema=noaa_schema).alias('json'))
    # Flatten the nested object:
    kafka_df = json_df.select("json.*")
    kafka_df.show()


if __name__ == '__main__':
    spark, sc = init_spark('demo')
    main()
