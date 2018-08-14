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

yum update
yum install -y python36 python36-virtualenv python36-pip htop
/usr/bin/pip-3.6 install --upgrade awscli

# Start Docker back
service docker start

##############################################################

start ecs
 
echo "Done"
