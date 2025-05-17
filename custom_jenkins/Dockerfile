# ## This dockerfile is for the jenkins docker img/container (Dockerfile for the proj container is in ../)

# #Use jenkins image as base image
# FROM jenkins/jenkins:lts

# # Switch to root user to install dependencies
# USER root

# # Install prerequisites and docker
# RUN apt-get update -y && \
#     apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
#     curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
#     echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
#     apt-get update -y && \
#     apt-get install -y docker-ce docker-ce-cli containerd.io && \
#     apt-get clean

# # Add Jenkins user to Docker group (creat eif it doesnt exist)
# RUN groupadd -f docker && \
#     usermod -aG docker jenkins

# # Create docker dir and volume for DinD (Docker in Docker)
# RUN mkdir -p /var/lib/docker
# VOLUME /var/lib/docker

# # Switch back to jenkins user
# USER jenkins

## New code to assign GID 974 while creation as 995 and 994 mismatch restricts jenkins user from docker usage on my host kernel (vdnt)
FROM jenkins/jenkins:lts
USER root
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common python3 python3-venv python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/google-cloud-sdk.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-cloud-sdk.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update -y && \
    apt-get install -y google-cloud-sdk
RUN groupadd -g 974 docker && \
    usermod -aG docker jenkins
USER jenkins

#### GEN code to get G-cloud as well:
# FROM jenkins/jenkins:lts
# USER root
# RUN apt-get update -y && \
#     apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
#     curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
#     echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
#     apt-get update -y && \
#     apt-get install -y docker-ce docker-ce-cli containerd.io && \
#     apt-get clean
# RUN apt-get update -y && \
#     apt-get install -y python3 python3-venv python3-pip && \
#     ln -s /usr/bin/python3 /usr/bin/python
# RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/google-cloud-sdk.gpg && \
#     echo "deb [signed-by=/usr/share/keyrings/google-cloud-sdk.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
#     apt-get update -y && \
#     apt-get install -y google-cloud-sdk
# RUN groupadd -f docker && \
#     usermod -aG docker jenkins
# RUN mkdir -p /var/lib/docker
# VOLUME /var/lib/docker
# USER jenkins