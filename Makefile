PWD := $(shell pwd)
VER := $(shell git describe --tags)
BUILD_IMG := gk-lv-mkt
CONTAINER_NAME := gk-lv-app
RUN := docker run --rm -i
ID := 0bd98f01c32a
MYSQL_PATH := /var/lib/mysql-files

build-image:
	docker build -t ${BUILD_IMG} .

run:
	docker run --name ${CONTAINER_NAME} --env-file ./.env -d -p 3306:3306 ${BUILD_IMG}

version:
	echo $(VER) > ./VERSION

push-dist-image:
	docker push $(IMAGE)

start:
	docker start ${CONTAINER_NAME}

stop:
	docker stop ${CONTAINER_NAME}

clean:
	${RUN}${CONTAINER_NAME}
