## Cloud Formation Project for high-availability web-app

This repo contains cloud infrastructure for high-availability web-app<br>
provisioned via cloud formation<br>
as part of Udacity Cloud DevOps Nanodegree.

## Provisioned Architecture
![Architecture-Diagram](cloud_architecture.png)

## Requirements

The code assumes already existing S3 bucket in the account with prepared web-app<br>
which is then automatically downloaded during each app-server-instance initialization<br>
and served by Apache HTTP Server.

## Run instructions

create-stack.cmd [stack-name] network-infra/network.yml network-infra/network-parameters.json<br>
create-stack.cmd [stack-name] ec2-infra/ec2.yml ec2-infra/ec2-parameters.json