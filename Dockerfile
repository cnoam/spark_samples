
# you can override the argument value by calling
# docker build --build-arg SPARK_VER=spark-2.7 -t some_label .
FROM openjdk:8-alpine
RUN apk --update add wget tar bash


ENV SPARK_VERSION 2.4.7
ENV HADOOP_VERSION 2.7
ENV SPARK_FILE spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION
ENV SPARK_DOWNLOAD_URL https://downloads.apache.org/spark/spark-$SPARK_VERSION/$SPARK_FILE.tgz


# Download and unzip Spark
RUN wget $SPARK_DOWNLOAD_URL && \
    tar xvf $SPARK_FILE.tgz && \
    mv $SPARK_FILE /spark && \
    rm $SPARK_FILE.tgz
    
COPY start-master.sh /start-master.sh
COPY start-worker.sh /start-worker.sh

