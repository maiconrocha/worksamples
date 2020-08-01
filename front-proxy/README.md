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

To be Continued...
