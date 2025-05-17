FROM jenkins/jenkins:lts
USER root
# Install prerequisites for Docker, Python, and Google Cloud SDK
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common python3 python3-venv python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python
# Install Docker for DinD
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean
# Install Google Cloud SDK
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/google-cloud-sdk.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-cloud-sdk.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update -y && \
    apt-get install -y google-cloud-sdk
# Create directory for Docker daemon
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker
# Add Jenkins user to Docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins
USER jenkins