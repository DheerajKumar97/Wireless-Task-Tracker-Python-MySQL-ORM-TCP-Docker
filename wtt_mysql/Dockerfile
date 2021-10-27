FROM biarms/mysql:5.5.60

# Add a database in pi
ENV MYSQL_DATABASE wireless_tracker
ENV MYSQL_ROOT_HOST ' '
#ENV MYSQL_ROOT_PASSWORD root64

# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/