from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("DeltaTest")
    .enableHiveSupport()
    .getOrCreate()
)

data = [
    (1, "Chennai", 35),
    (2, "London", 18),
    (3, "New York", 22)
]

df = spark.createDataFrame(data, ["id", "city", "temperature"])

df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("path", "s3a://bronze/weather_test") \
    .saveAsTable("default.weather_test")

print("Delta table written successfully!")

spark.stop()