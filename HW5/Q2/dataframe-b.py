import sys
from pyspark.sql import SparkSession


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: spark-submit dataframe-b.py country.json city.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("DataframeB").getOrCreate()

    # Create a dataframe from country.json
    country = spark.read.json(sys.argv[1])
    # Create a dataframe from city.json
    city = spark.read.json(sys.argv[2])

    df = country.withColumnRenamed('Name', 'CountryName').join(city, country.Capital == city.ID)[['CountryName', 'Name']]
    
    print(df.show())

    spark.stop()
