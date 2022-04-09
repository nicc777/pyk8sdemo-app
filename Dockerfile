FROM ubuntu:21.04 AS flask-prod-base

LABEL Description="A container for the production hosting of a flask application" Vendor="none" Version="0.1"

# Prep Python
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libterm-readline-gnu-perl apt-utils -y
RUN apt-get install -y python3 python3-pip
RUN pip3 install Flask Flask-Cognito gunicorn cognitojwt

# Required for some debugging 
RUN apt-get install -y bind9-dnsutils telnet python3-boto3 curl wget unzip git openssh-client vim net-tools nmap
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sh ./aws/install




FROM flask-prod-base

LABEL Description="A demo container for the production hosting of a flask application" Vendor="none" Version="0.0.2"

# Envieonment
ENV DEMO_ENV_VAR_1 "VALUE_01"
ENV DEMO_ENV_VAR_2 "VALUE_02"
ENV DEMO_ENV_VAR_3 "VALUE_03"

# Install the app
WORKDIR /usr/src/app
RUN mkdir dist
COPY dist/*.tar.gz ./dist/
RUN pip3 install dist/*.tar.gz

# Operational Configuration
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "flask_demo_app.flask_demo_app:app"]



