Based on the Blog Article: https://aws.amazon.com/blogs/compute/setting-up-an-envoy-front-proxy-on-amazon-ecs/

Steps to Deploy to ECS:

1) Clone the Repository on your local machine.
go to front-proxy folder

2) Create ECR Repo service and push image to the repository

docker build -t service --file Dockerfile-service . 
docker tag service:latest <account id>.dkr.ecr.<region>.amazonaws.com/service:latest 
docker push <account id>.dkr.ecr.<region>.amazonaws.com/service:latest  

3) Create ECR Repo envoy
docker build -t envoy --file Dockerfile-envoy . 
docker tag envoy:latest <account id>.dkr.ecr.<region>.amazonaws.com/envoy:latest 
docker push <account id>.dkr.ecr.<region>.amazonaws.com/envoy:latest 

4) Create ECR Repo frontenvoy

docker build -t frontenvoy --file Dockerfile-frontenvoy . 
docker tag frontenvoy:latest <account id>.dkr.ecr.<region>.amazonaws.com/frontenvoy:latest 
docker push <account id>.dkr.ecr.<region>.amazonaws.com/frontenvoy:latest 

5) Create Task Definitions

Edit files task-definition-envoy.json and task-definition-frontproxy.json
and specify the correct region and aws account, also the correct ARN for ECR Repository

Register task definition through the console or through the CLI command:
aws ecs register-task-definition --cli-input-json file://<path_to_json_file>/task-definition-envoy.json
aws ecs register-task-definition --cli-input-json file://<path_to_json_file>/task-definition-frontproxy.json

6) Create ECS Cluster

Go to ECS Console > Create Cluster > EC2 Linux + Networking > Cluster Name: envoy, create new VPC


7) Create ECS Services

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

8) Test Envoy

Create an EC2 instance on the same VPC than ECS Cluster

$ curl (front-proxy-private-ip):80/service
Hello from behind Envoy! 

