#Use jenkins image as base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# Add Jenkins user to Docker group (creat eif it doesnt exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create docker dir and volume for DinD (Docker in Docker)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to jenkins user
USER jenkins


