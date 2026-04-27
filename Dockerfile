FROM python:3.13-slim
# Set build arguments for user and group IDs
ARG USER=app
ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
#install dependencies
RUN apt-get update && apt-get install -y \
    gnupg \
    git \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
# Create a non-root user to run the application
RUN groupadd -g ${GID} ${USER} \
    && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER}
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Change ownership of the application files to the non-root user
RUN chown -R ${USER}:${USER} /app
# Switch to the non-root user
USER ${USER}