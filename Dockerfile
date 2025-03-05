# Use Python slim base image
FROM python:3.12-slim
# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y gnupg2 curl && \
    curl -fsSL https://ftp-master.debian.org/keys/archive-key-12.asc | gpg --batch --no-tty --dearmor -o /tmp/debian-archive-keyring.gpg && \
    mv /tmp/debian-archive-keyring.gpg /usr/share/keyrings/debian-archive-keyring.gpg && \
    curl -fsSL https://ftp-master.debian.org/keys/archive-key-12-security.asc | gpg --batch --no-tty --dearmor -o /tmp/debian-security-archive-keyring.gpg && \
    mv /tmp/debian-security-archive-keyring.gpg /usr/share/keyrings/debian-security-archive-keyring.gpg
RUN apt-get update && \
    apt-get install -y git gcc python3-dev libhdf5-dev pkg-config swig g++ build-essential libboost-all-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
#RUN apt-get update && apt-get install -y curl
RUN pip install uvicorn fastapi
# Set build arguments for Git username and access token
ARG GIT_USERNAME
ARG GIT_ACCESS_TOKEN
# Set working directory
WORKDIR /app
# Configure Git with provided credentials
RUN git config --global credential.helper store && \
    printf "https://${GIT_USERNAME}:${GIT_ACCESS_TOKEN}@github.com" > ~/.git-credentials
# Clone your repository
RUN git clone https://github.com/paradimdata/project_chameleon.git .
# # Install project dependencies 
RUN pip install matplotlib numpy hyperspy py4dstem pandas xylib-py htmdec_formats openpyxl
RUN pip install adjustText 

RUN set -x \
    && add-apt-repository ppa:mc3man/trusty-media \
    && apt-get update \
    && apt-get dist-upgrade \
    && apt-get install -y --no-install-recommends \
        ffmpeg \ 

EXPOSE 5020
EXPOSE 8080
#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5020"]