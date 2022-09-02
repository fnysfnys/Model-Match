FROM ubuntu:latest

# Copies the backend into app
RUN cd .. && rm -rf app
COPY ./src ./app
COPY requirements.txt ./app
RUN cd app

# Installs docker so we can build images
RUN apt-get update
RUN apt-get install \
    ca-certificates \
    curl \
    gnupg \
    build-essential \
    libpq-dev \
    lsb-release -y

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update

# Removes interactive mode for auto builds
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN yes | apt-get install docker-ce docker-ce-cli containerd.io

# Installs python3 and pip
RUN apt-get install python3-all python3-pip -y

# Installs postgres for database connections
RUN apt install postgresql postgresql-contrib -y

# Installs the requirements
RUN cd app && pip3 install -r requirements.txt

# Runs the server
CMD cd app && python3 -m uvicorn --host 0.0.0.0 api.main:app
