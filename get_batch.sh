#!/bin/bash -eu
curl -k --user "admin:$LIVY_PASS"  -H "Content-Type: application/json"   "https://noam-c3.azurehdinsight.net/livy/batches/$1" -H "X-Requested-By: admin" | jq
