import sys
from pyspark.sql import SparkSession
import pyspark.sql.functions as fc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: spark-submit dataframe-e.py country.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("DataframeE").getOrCreate()
    
    # Create a dataframe from country.json
    country = spark.read.json(sys.argv[1])

    df = country.groupBy('Continent').agg(fc.avg('LifeExpectancy').alias('avg_le'), fc.count('*').alias('cnt')).filter('cnt >= 20').orderBy(fc.desc('cnt')).limit(1)[['Continent','avg_le']]
    # ordered by cnt desc

    print(df.show())

    spark.stop()
