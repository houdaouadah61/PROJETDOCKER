from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, avg, sum as _sum
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType


def main():
    spark = (
        SparkSession.builder
        .appName("WeatherAggregation")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    kafka_bootstrap = "kafka:29092"
    source_topic = "weather_transformed"

    schema = StructType([
        StructField("time", StringType(), True),
        StructField("interval", DoubleType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("windspeed", DoubleType(), True),
        StructField("winddirection", DoubleType(), True),
        StructField("is_day", DoubleType(), True),
        StructField("weathercode", DoubleType(), True),
        StructField("temp_f", DoubleType(), True),
        StructField("high_wind_alert", BooleanType(), True),
    ])

    raw = (
        spark.read
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap)
        .option("subscribe", source_topic)
        .option("startingOffsets", "earliest")
        .load()
    )

    df = (
        raw.selectExpr("CAST(value AS STRING) AS json_str")
        .select(from_json(col("json_str"), schema).alias("data"))
        .select("data.*")
    )

    df_ts = df.withColumn("event_time", col("time").cast("timestamp"))

    agg = (
        df_ts.groupBy(window(col("event_time"), "1 minute"))
        .agg(
            avg(col("temperature")).alias("avg_temp_c"),
            _sum(col("high_wind_alert").cast("int")).alias("alert_count"),
        )
        .orderBy(col("window").asc())
    )

    # Affichage console (optionnel)
    agg.show(truncate=False)

    # Export HDFS (CSV)
    hdfs_output = "hdfs://namenode:9000/user/jovyan/weather_csv"

    (
        agg.select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("avg_temp_c"),
            col("alert_count"),
        )
        .coalesce(1)
        .write
        .mode("append")
        .option("header", "true")
        .csv(hdfs_output)
    )

    print("Saved to HDFS: %s" % hdfs_output)

    spark.stop()


if __name__ == "__main__":
    main()

