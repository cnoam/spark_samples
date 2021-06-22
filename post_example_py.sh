#!/bin/bash -eu
# run a sample program in the LIVY cluster
curl -k --user "admin:$LIVY_PASS" -v \
-X POST --data '{ "file":"wasbs:///minimal.py" }' \
"https://noam-c3.azurehdinsight.net/livy/batches" \
-H "X-Requested-By: admin" \
-H "Content-Type: application/json" 
