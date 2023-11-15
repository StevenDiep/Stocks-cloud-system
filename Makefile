
build-api:
	docker build -t stevendiep/stocks-test-flask:1.0 -f docker/Dockerfile.api .

run-api:
	docker run --name stevendiep-api \
                   --network stevendiep-network-test \
                   --env REDIS_IP=stevendiep-db \
                   -d \
                   -p 5000:5000 \
                   stevendiep/stocks-test-flask:1.0

build-worker:
	docker build -t stevendiep/stocks-test-worker:1.0 -f docker/Dockerfile.worker .

run-worker:
	docker run --name stevendiep-worker \
                   --network stevendiep-network-test \
                   --env REDIS_IP=stevendiep-db \
                   -d \
                   stevendiep/stocks-test-worker:1.0
build-retrieve:
	docker build -t stevendiep/stocks-test-retrieve:1.0 -f docker/Dockerfile.retrieve .

run-retrieve:
	docker run --name stevendiep-retrieve \
                   --network stevendiep-network-test \
                   --env REDIS_IP=stevendiep-db \
                   -d \
                    stevendiep/stocks-test-retrieve:1.0
run-redis:
	docker run --name stevendiep-db \
                   --network stevendiep-network-test \
                   -d \
                   -p 6379:6379 \
                   -v datasets:/data \
                   redis:5.0.0


clean-redis:
	docker stop stevendiep-db && docker rm -f stevendiep-db

clean-api:
	docker stop stevendiep-api && docker rm -f stevendiep-api

clean-worker:
	docker stop stevendiep-worker && docker rm -f stevendiep-worker

clean-retrieve:
	docker stop stevendiep-retrieve && docker rm -f stevendiep-retrieve


build-all: build-api build-worker build-retrieve

run-all: run-redis run-retrieve run-api run-worker 

clean-all: clean-redis clean-retrieve clean-api clean-worker


compose-up:
	docker-compose -f docker/docker-compose.yml -p stevendiep up -d --build

compose-down:
	docker-compose -f docker/docker-compose.yml -p stevendiep down

test-api:
	python3 test/api_test.py localhost

k-test:
	kubectl apply -f kubernetes/test/stocks-test-db-service.yml
	kubectl apply -f kubernetes/test/stocks-test-db-deployment.yml
	DBIP=$$(kubectl describe service stocks-test-db-service | grep 'IP:' | awk '{print $$2}') && \
	cat kubernetes/test/* | TAG="1.0" envsubst '$${TAG}' | RIP=$${DBIP} envsubst '$${RIP}' | kubectl apply -f -

k-test-del:
	cat kubernetes/test/*.yml | TAG="1.0" envsubst '$${TAG}' |  kubectl delete -f -	

k-prod:
	kubectl apply -f kubernetes/prod/stocks-prod-db-service.yml
	DBIP=$$(kubectl describe service stocks-prod-db-service | grep 'IP:' | awk '{print $$2}') && \
	cat kubernetes/prod/* | TAG="1.0" envsubst '$${TAG}' | RIP=$${DBIP} envsubst '$${RIP}' | kubectl apply -f -
k-prod-del:
	cat kubernetes/prod/*.yml | TAG="1.0" envsubst '$${TAG}' |  kubectl delete -f -


