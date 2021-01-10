# Create an AMI
For fast startup make sure to prepare an AMI with the following installed.  
For starting, registering, un-registering, and terminating runners this is important.

## Base
This project has been developed with Ubuntu 18.04 as the base.

## Install requirements

### Install and Start Docker

```bash
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

###  Install wildq for parsing toml files

```bash
VERSION=$(curl -s "https://api.github.com/repos/ahmet2mir/wildq/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
curl -sL https://github.com/ahmet2mir/wildq/releases/download/v${VERSION}/wildq_${VERSION}-1_amd64.deb -o wildq_${VERSION}-1_amd64.deb
sudo dpkg -i wildq_${VERSION}-1_amd64.deb
```

###  Install unzip

```bash
sudo apt install unzip
```

###  Install AWS CLI V2

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

###  Install GitLab Runner

```bash
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
export GITLAB_RUNNER_DISABLE_SKEL=true; sudo -E apt-get install gitlab-runner
```