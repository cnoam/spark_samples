#!/bin/bash -eux
LIVY_PASS="%Qq12345678"
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=noamc3hdistorage;AccountKey=fdFdbbGwF3Siw1FSpj9w+gAFhQ+Ie/vS152mv0ZAEb23GXUILHUYX1kIJuMs8IzOLZ+YafVORHGiWGeSu0hTWA==;EndpointSuffix=core.windows.net"
SRC_FILE=$1
CLUSTER_NAME=noam-c3
CONTAINER_NAME=noam-c3-2021-04-06t10-05-57-099z

# upload the file to storage
az storage blob upload -f $SRC_FILE -c $CONTAINER_NAME -n $SRC_FILE


# send to spark for processing
curl -k --user "admin:$LIVY_PASS" -v \
-X POST --data "{ \"file\":\"wasbs:///$SRC_FILE\" , \
\"conf\": { \"spark.yarn.appMasterEnv.PYSPARK_PYTHON\" : \"/usr/bin/anaconda/envs/py35/bin/python\", \
\"spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON\" : \"/usr/bin/anaconda/envs/py35/bin/python\" } \
 }" \
"https://$CLUSTER_NAME.azurehdinsight.net/livy/batches" \
-H "X-Requested-By: admin" \
-H "Content-Type: application/json" \
   | jq
   



#we should get the batch ID from the above reply. (TODO)

#BATCH_ID=0
# check the status of the batch
#curl -k --user "admin:$LIVY_PASS"  -H "Content-Type: application/json"   "https://$CLUSTER_NAME.azurehdinsight.net/livy/batches/$BATCH_ID" -H "X-Requested-By: admin" | jq

