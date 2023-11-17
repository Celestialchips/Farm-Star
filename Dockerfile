FROM mysql:8.0.23

ENV MYSQL_DATABASE=your_database
ENV MYSQL_USER=your_user
ENV MYSQL_PASSWORD=your_password
ENV MYSQL_ROOT_PASSWORD=your_root_password

EXPOSE 3306

VOLUME ["/var/lib/mysql", "/var/log/mysql", "/etc/mysql"]

COPY my.cnf /etc/mysql/my.cnf

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/ /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY start-app.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-app.sh

CMD ["start-app.sh"]
