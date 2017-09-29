sudo yum update -y
sudo yum install -y \
	bzip2 \
    bzip2-devel \
	ca-certificates \
	ncurses-devel \
	docker \
	gcc \
	gcc-c++ \
	git \
	make \
    nano \
	python-devel \
	tar \
	wget \
	zlib-devel

# Add new user
USER=jake
sudo adduser $USER
sudo mkdir /home/$USER/.ssh
sudo chmod 700 /home/$USER/.ssh/
sudo nano /home/$USER/.ssh/authorized_keys
# add pub key manually...
sudo chmod 400 /home/$USER/.ssh/authorized_keys

# Docker
sudo service docker start
sudo usermod -a -G docker steve

# Mount drives
# ephemeral0 already mounted
sudo mkdir /media/ephemeral1
sudo mount /dev/xvdc /media/ephemeral1

# Scratch and raw dirs
sudo mkdir /media/ephemeral0/scratch
sudo chmod 777 /media/ephemeral0/scratch/
sudo ln --symbolic /media/ephemeral0/scratch/ /scratch
sudo mkdir /media/ephemeral1/raw
sudo chmod 777 /media/ephemeral1/raw
sudo ln --symbolic /media/ephemeral1/raw /raw

# Reference dir (synced from S3)
sudo mkdir /media/ephemeral1/reference
sudo chmod 777 /media/ephemeral1/reference
sudo ln --symbolic /media/ephemeral1/reference /reference

## OR

# Reference dir (EBS)
sudo mkfs -t ext4 /dev/xvdd
sudo mount /dev/xvdd /mnt/reference

# Anaconda
wget https://repo.continuum.io/archive/Anaconda3-5.0.0-Linux-x86_64.sh
bash Anaconda3-5.0.0-Linux-x86_64.sh

# NGS tools. Use /opt/tools for anything that can't be dumped into /usr/local/bin
sudo mkdir -p /opt/tools
sudo chmod 777 tools

pip install multiqc

cd /tmp
wget https://github.com/samtools/samtools/releases/download/1.3/samtools-1.3.tar.bz2
tar -xvjf samtools-1.3.tar.bz2
cd samtools-1.3
make
chmod 777 samtools
sudo mv samtools /usr/local/bin

cd /opt/tools
wget https://github.com/broadinstitute/picard/releases/download/2.8.3/picard.jar

