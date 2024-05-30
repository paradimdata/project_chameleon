# Use Python slim base image
FROM python:3.12-slim
# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y git gcc python3-dev libhdf5-dev pkg-config swig g++ build-essential libboost-all-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y curl
RUN pip install uvicorn fastapi flask
RUN pip install poetry numpy
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
# # Install project dependencies with Poetry
RUN poetry install

#RUN pip install matplotlib numpy hyperspy py4dstem pandas xylib-py
#EXPOSE 5020
#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5020"]