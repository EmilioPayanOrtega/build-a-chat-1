#!/bin/bash

# --- Configuration Variables ---
CONTAINER_NAME="contenedor-mysql"
ROOT_PASSWORD="PuraGenteDelCoachMoy"
MYSQL_VOLUME="mysql_data"
MYSQL_PORT="3306"
IMAGE_NAME="mysql:latest"
DATABASE_NAME="chatbotdb"

# SQL initialization script
SQL_INIT="
CREATE DATABASE IF NOT EXISTS ${DATABASE_NAME};
USE ${DATABASE_NAME};
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);"
# -------------------------------

echo "--- MySQL Docker Setup Script ---"

# 1. Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running or not installed."
    exit 1
fi

# 2. Check if a container with the same name already exists
if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    echo "Container '$CONTAINER_NAME' already exists."
    echo "To remove the existing container, run:"
    echo "  docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME"
    exit 1
fi

echo "Attempting to start MySQL container '$CONTAINER_NAME'..."

# 3. Run the docker command with the new environment variable
docker run --name $CONTAINER_NAME \
  -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD \
  -e MYSQL_DATABASE=$DATABASE_NAME \
  -p $MYSQL_PORT:3306 \
  -v $MYSQL_VOLUME:/var/lib/mysql \
  -d $IMAGE_NAME

# 4. Provide feedback to the user
if [ $? -eq 0 ]; then
    echo "----------------------------------------------------"
    echo "MySQL container started successfully!"
    echo "Container Name: $CONTAINER_NAME"
    echo "Host Port:      $MYSQL_PORT"
    echo "Root Password:  $ROOT_PASSWORD"
    echo "Database Name:  $DATABASE_NAME" # <-- Display the new database name
    echo "----------------------------------------------------"
    echo "To connect to the MySQL shell, run:"
    echo "  docker exec -it $CONTAINER_NAME mysql -u root -p $DATABASE_NAME"
else
    echo "--------------------      --------------------------------"
    echo "Error: Failed to start MySQL container."
    echo "----------------------------------------------------"
fi