FROM ubuntu:22.04
LABEL maintainer="DevOps Team <devops@example.com>"
RUN apt-get update && apt-get install -y nginx curl python3-pip
RUN mkdir -p /app
RUN chmod 755 /app
RUN pip install --upgrade pip
EXPOSE 80
EXPOSE 443
WORKDIR /app
USER appuser
VOLUME ["/app/data"]