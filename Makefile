
build-api:
	docker build -t stevendiep/stocks-test-flask:1.0 -f docker/Dockerfile.api .

run-api:
	docker run --name stevendiep-api \
                   -d \
                   -p 5000:5000 \
                   stevendiep/stocks-test-flask:1.0

build-worker:
	docker build -t stevendiep/stocks-test-worker:1.0 -f docker/Dockerfile.worker .

run-worker:
	docker run --name stevendiep-worker \
                   -d \
                   stevendiep/stocks-test-worker:1.0
build-retrieve:
	docker build -t stevendiep/stocks-test-retrieve:1.0 -f docker/Dockerfile.retrieve .

run-retrieve:
	docker run --name stevendiep-retrieve \
                   -d \
                    stevendiep/stocks-test-retrieve:1.0
run-redis:
	docker run --name stevendiep-db \
                   -d \
                   -p 6379:6379 \
                   -v datasets/:data \
                   redis:5.0.0


clean-db:
	docker stop stevendiep-db && docker rm -f stevendiep-db

clean-api:
	docker stop stevendiep-api && docker rm -f stevendiep-api

clean-worker:
	docker stop stevendiep-worker && docker rm -f stevendiep-worker


build-all: build-api build-worker

run-all: run-api run-worker run-db

clean-all: clean-api clean-db clean-worker


compose-up:
	docker-compose -f docker/docker-compose.yml -p stevendiep up -d 

compose-down:
	docker-compose -f docker/docker-compose.yml -p stevendiep down

test-api:
	python3 test/api_test.py

k-test:
	kubectl apply -f kubernetes/test/stocks-test-db-service.yml
	DBIP=$$(kubectl describe service stocks-test-db-service | grep 'IP:' | awk '{print $$2}') && \
	cat kubernetes/test/* | TAG="1.0" envsubst '$${TAG}' | RIP=$${DBIP} envsubst '$${RIP}' | kubectl apply -f -


k-test-del:
	cat kubernetes/test/*.yml | TAG="1.0" envsubst '$${TAG}' |  kubectl delete -f -	






