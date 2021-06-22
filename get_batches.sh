#!/bin/bash -eu
# get the list of batches in the LIVY cluster
curl -k --user "admin:$LIVY_PASS"  -H "Content-Type: application/json"   "https://noam-c3.azurehdinsight.net/livy/batches" -H "X-Requested-By: admin" | jq

