import sys
from pyspark.sql import SparkSession


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: spark-submit dataframe-c.py country.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("DataframeC").getOrCreate()

    # Create a dataframe from country.json
    country = spark.read.json(sys.argv[1])

    df = country[['Continent']].distinct()
    
    print(df.show())

    spark.stop()
