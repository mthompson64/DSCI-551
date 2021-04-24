import sys
from pyspark.sql import SparkSession


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: spark-submit dataframe-d.py countrylanguage.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("DataframeD").getOrCreate()

    # Create a dataframe from countrylanguage.json
    cl = spark.read.json(sys.argv[1])

    df = cl[['Language']].filter('CountryCode = "CAN"')
    
    print(df.show())

    spark.stop()
