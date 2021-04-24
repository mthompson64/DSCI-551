import sys
from pyspark.sql import SparkSession

def printf(p):
    par = list(p)
    print('Partition: ', par)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: spark-submit rdd-b.py country.json city.json")
        sys.exit(1)
    
    spark = SparkSession.builder.appName("RDD-B").getOrCreate()

    # Create RDD's for country and city json data
    country_rdd = spark.read.json(sys.argv[1]).rdd.repartition(4)
    city_rdd = spark.read.json(sys.argv[2]).rdd.repartition(4)

    df1 = country_rdd.map(lambda x: [x['Capital'], x['Name']])
    df2 = city_rdd.map(lambda x: [x['ID'], x['Name']])
    
    # Join the two RDD's on country.Capital = city.ID and display
    # country.Name and city.Name
    df = df1.join(df2).map(lambda x: x[1]).collect()

    print(df)

    spark.stop()