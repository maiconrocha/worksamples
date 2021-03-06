Based on the Blog Article: https://aws.amazon.com/blogs/compute/setting-up-an-envoy-front-proxy-on-amazon-ecs/

Steps to Deploy to ECS:

### 1) Clone the Repository on your local machine.
go to front-proxy folder

### 2) Create ECR Repo service and push image to the repository
```sh
docker build -t service --file Dockerfile-service . 
docker tag service:latest <account id>.dkr.ecr.<region>.amazonaws.com/service:latest 
docker push <account id>.dkr.ecr.<region>.amazonaws.com/service:latest  
```

### 3) Create ECR Repo envoy
```sh
docker build -t envoy --file Dockerfile-envoy . 
docker tag envoy:latest <account id>.dkr.ecr.<region>.amazonaws.com/envoy:latest 
docker push <account id>.dkr.ecr.<region>.amazonaws.com/envoy:latest 
```
### 4) Create ECR Repo frontenvoy
```sh
docker build -t frontenvoy --file Dockerfile-frontenvoy . 
docker tag frontenvoy:latest <account id>.dkr.ecr.<region>.amazonaws.com/frontenvoy:latest 
docker push <account id>.dkr.ecr.<region>.amazonaws.com/frontenvoy:latest 
```
### 5) Create Task Definitions

Edit files task-definition-envoy.json and task-definition-frontproxy.json
and specify the correct region and aws account, also the correct ARN for ECR Repository

Register task definition through the console or through the CLI command:
```sh
aws ecs register-task-definition --cli-input-json file://<path_to_json_file>/task-definition-envoy.json
aws ecs register-task-definition --cli-input-json file://<path_to_json_file>/task-definition-frontproxy.json
```

Console:

Create new Task Revision envoy:
Network Mode: awsvpc
Add Container: Container Name: Service
Image: <aws account>.dkr.ecr.<region>.amazonaws.com/service:latest
Memory Limits (MiB) : 128 Mb
Port Mappings: 8080
CPU units: 256
Auto-configure CloudWatch Logs

Add Container: Container Name: Envoy
Image: <aws account>.dkr.ecr.<region>.amazonaws.com/envoy:latest
Memory Limits (MiB) : 128 Mb
Port Mappings: 80
CPU units: 256
Auto-configure CloudWatch Logs

click on Create

Create new Task Revision frontenvoy:
Network Mode: awsvpc
Add Container: Container Name: frontenvoy
Image: <aws account>.dkr.ecr.<region>.amazonaws.com/frontenvoy:latest
Memory Limits (MiB) : 128 Mb
CPU units: 256
Auto-configure CloudWatch Logs

Click on Create

### 6) Create ECS Cluster

Go to ECS Console > Create Cluster > EC2 Linux + Networking > Cluster Name: envoy, create new VPC


### 7) Create ECS Services

Create ECS Service serviceenvoy
Task Definition > envoy
Choose the VPC from the cluster
Service discovery endpoint testservice.ecs
DNS Record Type A
TTL 60
Namespace ecs (PRIVATE)

Create ECS Service frontenvoy
Task Definition > frontenvoy
Choose the VPC from the cluster

### 8) Test Envoy

Create an EC2 instance on the same VPC than ECS Cluster
```sh
$ curl (front-proxy-private-ip):80/service
Hello from behind Envoy! 
```
