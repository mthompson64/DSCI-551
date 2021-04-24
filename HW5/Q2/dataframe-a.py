import sys
from pyspark.sql import SparkSession
from pyspark import SparkContext


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: spark-submit dataframe-a.py country.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("DataframeA").getOrCreate()

    # Create a dataframe from country.json
    country = spark.read.json(sys.argv[1])
    df = country[['Name']].filter('Continent = "North America"')
    
    print(df.show())

    spark.stop()
