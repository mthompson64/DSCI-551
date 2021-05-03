import sys
import os
import time
from pyspark.sql import SparkSession

tic = time.perf_counter()

def printf(p):
    par = list(p)
    print('Partition: ', par)

def toCSV(data):
  return ','.join(str(d) for d in data)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: spark-submit parallel-processing.py <path/to/data>")
        sys.exit(1)

    spark = SparkSession.builder.appName("DSCI551").getOrCreate()

    list_of_files = []

    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    
    print(list_of_files)

    for name in list_of_files:
        if name.endswith("commute_info.csv"):
            commute = spark.read.option("header", "true").csv(name).rdd.repartition(10)

        elif name.endswith("zip_codes.csv"):
            zip_code = spark.read.option("header", "true").csv(name).rdd.repartition(10)
            zip_codes = zip_code.map(lambda x: [x['zip_code'], (x['state'], x['population'], x['house_value'], x['household_income'])])

        elif name.endswith("restaurant_data.json"):
            restaurants = spark.read.option("multiline", "true").json(name).rdd.repartition(10)
    
    close_zips = commute.filter(lambda x: x['duration'] is not None).filter(lambda x: "hour" not in x['duration'])\
        .map(lambda x: [x['zip_code'], (x['latitude'], x['longitude'], x['distance'], x['duration'])])
    
    veg_restaurant = restaurants.groupBy(lambda x: x['ZIP_code']).mapValues(lambda vals: len(vals))
    veg_restaurants = veg_restaurant.map(lambda x: (str(x[0]), x[1]))
    # print(veg_restaurants.collect())

    zips = close_zips.join(zip_codes)
    # print(zips.collect())
    final_join = zips.join(veg_restaurants)
    final = final_join.map(lambda x: (x[0], x[1][0][0][0], x[1][0][0][1], x[1][0][0][2], x[1][0][0][3], x[1][0][1][0], \
        x[1][0][1][1], x[1][0][1][2], x[1][0][1][3], x[1][1])).toDF(('zip', 'latitude', 'longitude', 'distance', \
            'duration', 'state', 'population', 'house_value', 'household_income', 'count_veg_restaurants'))
 
    print(final.show())

    # lines = final.map(toCSV).collect()
    final.toPandas().to_csv('output.csv')

    spark.stop()

print(f"Code successfully compiled in {time.perf_counter() - tic:0.4f} seconds")