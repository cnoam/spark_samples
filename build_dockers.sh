#!/bin/bash -xue

docker build -t spark:247 .
docker build -t spark_py:247 -f ./Dockerfile_with_python .
pushd ../docker-livy
docker build -t livy-spark .
popd
echo DONE

