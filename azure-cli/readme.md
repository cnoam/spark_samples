# use az cli to create the spark VMs
Before running any commands, you need to be logged in ( this will use the default subscription)
   
    az login
   

## create a VM
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli
  
    az group create --name myResourceGroup --location eastus
   
TODO: need to open inbound rule to accept connection to port 80
   
    az vm create \
    --resource-group myResourceGroup \
    --name spark-master \
    --image UbuntuLTS \
    --admin-username azureuser \
    --ssh-key-values ~/.ssh/id_rsa.pub
  
NOTE: the returned value is a json file. You can retrieve the public IP address by

    jq -r '.publicIpAddress' the-response-json
   
login to the machine:

    ssh  -o "StrictHostKeyChecking no"  azureuser@<public IP>
   
Install Docker in this machine

     sudo apt update && sudo apt install -y docker.io
   
configure docker to start the service

    sudo systemctl start docker
    sudo systemctl enable docker
   
## install/run Spark MASTER on the VM

see also https://github.com/sdesilva26/docker-spark/blob/master/TUTORIAL.md

### add regular user to docker group
    sudo groupadd docker
    sudo gpasswd -a $USER docker
   
### start the master   

This image already has builtin start-master script so don't copy another one.

    # scp start-master.sh azureuser@<public IP of master>
    TODO  The shell command has to be copied into the container
    docker run -e SPARK_LOCAL_IP=<public IP>  -e SPARK_MASTER_PORT=7077 -e SPARK_MASTER_WEBUI_PORT=8080 -p 80:8080 bde2020/spark-master:3.0.2-hadoop3.2./ # start-master.sh

## install/run Spark WORKER on the second VM
    scp start-worker.sh azureuser@<public IP of worker>: 
    docker run -d  -p 8080:8080 -e SPARK_MASTER=spark://10.0.0.4:7077 -e SPARK_WORKER_WEBUI_PORT=8080 -it bde2020/spark-master:3.0.2-hadoop3.2 /bin/sh
   
connect to the container or run

    docker exec -it    <container ID> ./start-worker.sh

## delete the resource group

    az group delete --name myResourceGroup
   

