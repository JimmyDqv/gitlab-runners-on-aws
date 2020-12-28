FROM amazon/aws-lambda-provided:al2

WORKDIR /var/runtime/
COPY bootstrap bootstrap
RUN chmod 755 bootstrap

WORKDIR /var/task/
COPY start.sh start.sh
RUN chmod 755 start.sh

RUN yum update -y
RUN yum install jq -y
RUN yum install unzip -y
RUN curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh" | bash
RUN export GITLAB_RUNNER_DISABLE_SKEL=true
RUN yum install -y gitlab-runner

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

CMD [ "start.sh.handler" ]
