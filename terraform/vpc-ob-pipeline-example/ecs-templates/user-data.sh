#!/bin/bash
 
# ECS config
{
  echo "ECS_CLUSTER=${cluster_name}"
} >> /etc/ecs/ecs.config

################## Pre-provision the host #####################

# Stop Docker before mounting new drives
service docker stop

# Mount half of host memory to /mnt and create scratch and reference folders in there
mkdir -p /mnt
mount -t tmpfs -o size=50% tmpfs /mnt
mkdir -p /mnt/scratch /mnt/reference
chmod 777 /mnt/scratch /mnt/reference

echo "Defaults secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin" >> /etc/sudoers

yum update
yum install -y python36 python36-virtualenv python36-pip htop vim python-setuptools
easy_install pip
pip install awscli

# Start Docker back
service docker start

sleep 3

# Login to the ECR
$(aws ecr get-login --no-include-email --region us-east-1) || :

##############################################################

start ecs
 
echo "Done"
