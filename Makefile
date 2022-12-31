BUILD_VERSION_PETEMOON?=v0.0
APP_NAME:=petemoon
SERVER_USER:=petemoon
PRODUCTION_SERVER_IP:=
DEVELOP_SERVER_IP:=
BACKUP_SERVER_IP:=


all: docker run log

docker: 
	@echo "---[building docker image]---"
	@DOCKER_BUILDKIT=1 docker build -t ${APP_NAME}:${BUILD_VERSION_PETEMOON} .

run: 
	@echo "---[building docker image]---"
	@BUILD_VERSION_PETEMOON=${BUILD_VERSION_PETEMOON} docker-compose up -d

down: 
	@echo "---[down docker instances]---"
	@BUILD_VERSION_PETEMOON=${BUILD_VERSION_PETEMOON} docker-compose down

log:
	@docker-compose logs -f app

migrations:
	@docker-compose exec app ./manage.py makemigrations
	@docker-compose exec app ./manage.py migrate

deploy-dev:
	@echo "---[deploy to dev server]---"
	@echo "---[pulling source code]---"
	@ssh ${SERVER_USER}@${BACKUP_SERVER_IP} "cd /opt/petemoon/project && git pull"
	@echo "---[build docker image]---"
	@ssh ${SERVER_USER}@${BACKUP_SERVER_IP} "cd /opt/petemoon/project && make docker"
	@echo "---[run docker instance]---"
	@ssh ${SERVER_USER}@${BACKUP_SERVER_IP} "cd /opt/petemoon/project && make run"

deploy-prod:
	@echo "---[deploy to prod server]---"
	@echo "---[pulling source code]---"
	@ssh -p 2588 ${SERVER_USER}@${PRODUCTION_SERVER_IP} "cd /opt/petemoon/project && git pull"
	@echo "---[build docker image]---"
	@ssh -p 2588 ${SERVER_USER}@${PRODUCTION_SERVER_IP} "cd /opt/petemoon/project && make docker"
	@echo "---[run docker instance]---"
	@ssh -p 2588 ${SERVER_USER}@${PRODUCTION_SERVER_IP} "cd /opt/petemoon/project && make run"
