FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y \
	curl \
	git \
	docker.io \
	python3 \
	python3-pip \
    && curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && apt-get remove -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -G docker -a root

WORKDIR /project


COPY requirements.txt .

ARG REFRESHED_REQS=5

RUN pip3 install -r requirements.txt && rm -rf /root/.cache

COPY  . .

RUN python3 setup.py develop --no-deps

RUN pip3 list
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONIOENCODING=utf8
RUN dt-challenges-evaluator --version

CMD ["dt-challenges-evaluator"]
