# Playing with spark on local machine with Docker

Run Docker container with the spark master, and a few workers.
First using Scala, then with Python.

  https://towardsdatascience.com/a-journey-into-big-data-with-apache-spark-part-1-5dfcc2bccdd2

We will create several "machines":
1 master to send the jobs to workers
3 workers (each running executors)
1 machine to create the code and submit to the master

Instead of using real computers or virtual machines, we will use *Docker containers*. Each container behaves like a virtual machine, only much more lightweight.

## Prerequisites
* Docker is installed


First, 
create the docker network:
`docker network create spark_network`

Then,
build the images:
`docker build  -t spark:latest .`
`docker build -t spark_py -f ./Dockerfile_with_python .`

and the Livy docker image as well: TBD

and run the containers:
`docker-compose up --scale spark-worker=3`

**NOTE:
If This is not the first run, and you made some changes, the docker compose might try to use cached values and stopped containers.
If you get an error in the above command, try to remove stopped containers (find the ID with `docker ps -aq`), remove with `docker rm `*id* **

 Check the master web UI:
   http://localhost:8080/

To check using builtin examples:
Run a new container:
 `docker run --rm -it --network spark_spark-network spark /bin/sh`
 
Then in the new container:
```
/spark/bin/spark-submit --master spark://spark-master:7077 --class \
    org.apache.spark.examples.SparkPi \
    /spark/examples/jars/spark-examples_2.11-2.4.5.jar 1000
```
If everything works, you will see a lot of log lines, and after a while: 
```
20/09/06 14:42:09 INFO DAGScheduler: Job 0 finished: reduce at SparkPi.scala:38, took 61.659824 s
Pi is roughly 3.14180503141805
20/09/06 14:42:09 INFO SparkUI: Stopped Spark web UI at http://ae4c528de6a2:4040
```
<br><br>
# Playing with pyspark
Look at https://www.tutorialspoint.com/pyspark/pyspark_sparkcontext.htm (and previous pages)

## Run pyspark locally
When running in docker container (that contains both Spark and Python):
`docker run --rm -it --network spark_spark-network spark_py /bin/sh`

`cd /spark`

### using pyspark console:
`bin/pyspark`

### using a py file:
Create app.py
```
from pyspark import SparkContext
logFile = "file:///spark/README.md" 
sc = SparkContext("local", "first app")
logData = sc.textFile(logFile).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print "Lines with a: %i, lines with b: %i" % (numAs, numBs)
```
Then run it:

`# bin/spark-submit app.py`

## running pyspark on a cluster

Now we will run the python code on our cluster of 3 workers:

**NOTE:
To run pyspark on the workers, the workers must have python installed, hence the modification in the docker-compose.yml**

* Start the cluster
`docker-compose up --scale spark-worker=3`
* in the new docker container change the "local" to "spark://<name of master>:7077"  :

```
from pyspark import SparkContext
logFile = "file:///spark/README.md"
sc = SparkContext("spark://spark-master:7077", "first app")
logData = sc.textFile(logFile).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print "Lines with a: %i, lines with b: %i" % (numAs, numBs)

```

and run it  again: ` bin/spark-submit app.py`
