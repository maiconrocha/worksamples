#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    core,
)

import os

class AutoScalingStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")
        
        # For other custom (Linux) images, instantiate a `GenericLinuxImage` with
        # a map giving the AMI to in for each region:

        linux = ec2.GenericLinuxImage({
            "us-east-1": "ami-056907df001eeca0e",
            "eu-west-1": "ami-0063fa0451e11ca13",
            "ap-southeast-2": "ami-0455f9923a0d8e96f",
        })
        
        asg = autoscaling.AutoScalingGroup(
            self, "MyFleet",
            instance_type=ec2.InstanceType("t2.xlarge"),
            machine_image= linux,
            associate_public_ip_address=True,
            update_type=autoscaling.UpdateType.REPLACING_UPDATE,
            desired_capacity=3,
            vpc=vpc,
            vpc_subnets={ 'subnet_type': ec2.SubnetType.PUBLIC },
        )


app = core.App()
AutoScalingStack(app, "AutoScalingStack", env={'account': os.environ['CDK_DEFAULT_ACCOUNT'],'region': os.environ['CDK_DEFAULT_REGION']})
app.synth()
