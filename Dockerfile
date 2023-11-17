FROM mysql:8.0.23

ENV MYSQL_DATABASE=your_database
ENV MYSQL_USER=your_user
ENV MYSQL_PASSWORD=your_password
ENV MYSQL_ROOT_PASSWORD=your_root_password

EXPOSE 3306

VOLUME ["/var/lib/mysql", "/var/log/mysql", "/etc/mysql"] 

COPY my.cnf /etc/mysql/my.cnf
