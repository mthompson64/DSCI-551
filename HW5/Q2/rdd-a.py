import sys
from pyspark.sql import SparkSession

def printf(p):
    par = list(p)
    print('Partition: ', par)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: spark-submit rdd-a.py country.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("RDD-A").getOrCreate()

    # Create an RDD from country.json
    country_rdd = spark.read.json(sys.argv[1]).rdd.repartition(4)

    df = country_rdd.filter(lambda x: x['Continent'] == 'North America').map(lambda x: x['Name']).collect()
    print(df)

    spark.stop()