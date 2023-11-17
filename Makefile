.PHONY: build-image run version push-dist-image start stop clean

PWD := $(shell pwd)
VER := $(shell git describe --tags)
BUILD_IMG := gk-lv-mkt
CONTAINER_NAME := gk-lv-app
MYSQL_PATH := /var/lib/mysql-files

build-image:
	docker build -t ${BUILD_IMG}:${VER} .

run:
	docker run --name ${CONTAINER_NAME} --env-file ./.env -v ${PWD}${MYSQL_PATH}:/var/lib/mysql -d -p 3306:3306 ${BUILD_IMG}:${VER}

version:
	echo $(VER) > ./VERSION

push-dist-image:
	docker push ${BUILD_IMG}:${VER}

start:
	docker start ${CONTAINER_NAME}

stop:
	docker stop ${CONTAINER_NAME}

clean:
	docker stop ${CONTAINER_NAME}
	docker rm ${CONTAINER_NAME}
	docker rmi ${BUILD_IMG}:${VER}
