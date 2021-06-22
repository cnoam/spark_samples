#!/bin/bash -eu
# delete a  batch in the LIVY cluster
# usage: ./delete_batch 0
curl -k --user "admin:$LIVY_PASS" -v -H "Content-Type: application/json" \
-X DELETE\
 "https://noam-c3.azurehdinsight.net/livy/batches/$1" \
 -H "X-Requested-By: admin"
