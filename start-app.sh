#!/bin/bash

echo "Waiting for MySQL to wake up..."
while ! mysqladmin ping -h"localhost" --silent; do
    sleep 1
done
echo "MySQL is now awake! Good Morning! - executing command"

exec python3 main.py
