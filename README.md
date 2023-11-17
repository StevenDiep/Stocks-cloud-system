# Stocks RESTful API
The project in this repo is a RESTful API system that uses stock time series data for fetching information and graphing. 
The system that does so will use the following framework:
![alt text](https://github.com/StevenDiep/Stocks-cloud-system/blob/main/readme/Framework.png?raw=true)
The three main components of the system are: the API, the database/queue, and the workers. First, requests from users will pour into the system where the API will process and potentially handle them. If the task is too time consuming for the API, like graphing, the API will send the task to the queue and record it in the database. Finally, the workers will pick up jobs from the queue and perform the tasksas needed.

## Dataset
The dataset used for the project will be stock data from the fortune 500 companies. To obtain this dataset, I used the yfinance library in python to pull real-time stock data from the yahoo website and saved this information inside of the redis database. Since pulling data from 500 companies over 5 years will naturally take long, I also used the concurrent.futures module in python to speed up the process of data collection through parallel processing.

## More information about system components
API: The API used for this project will be flask and it will take in requests from users and give updates on jobs.

Database: The database used for this project will be redis. Our data is large and doesn't have to be connected, which makes a noSQL database like redis perfect for the project. There are three main sections of the database. 
1. Jobs, this section of the database will contain all past jobs where users can look at with a UUID
2. Images, given that the user's request returns a graph, this section of the database will contain the graphs that are returned from the job.
3. Stocks, this section of the database will contain stock data from the fortune 500 companies.

Workers: The workers main job will be taking on graphing tasks. This involves taking jobs from the queue, identifying what kind of graphing job it is, executing it, and then saving the image to the database.

## Deployment
The project in this repo can be deployed on docker or, more preferably, on kubernetes cluster. 

0) Before you can deploy the project, make sure you have dockerhub installed and running on your computer. Also make sure that the k8s cluster is installed and working properly in settings of docker hub.
1) On your terminal, cd to the path you would like this repo to be under and use
```bash
git clone https://github.com/StevenDiep/Stocks-cloud-system
```
2a) To run on docker hub, run the command:
```bash
make build-all
make run-all
```
2b) To run on kubernetes, run the command:
```bash
make k-prod
```
## List of endpoints and expected responses

The following array represents the accepted periods for the end points: ['1d', '7d', '1m', '3m', '6m', '1y', '5y']
1. (/stock/<string:ticker>), e.x. (/stock/AAPL) should return all dates/values from the AAPL stock.
2. (/stock/diff/<string:ticker>/<string:period>), e.x. (/stock/diff/AAPL/1y) will return the percent difference of the stock's closing price between today and one year ago.
3. (/stock/add) will allow you to add datapoints into your stock data, thought not really recommended
4. (/stock/graph) will return a graph of your desired ticker
5. (/stock/compare) will return a graph comparing two tickers of your choice
6. (/stock/compare_sp500) will return a graph comparing the % difference between your stock of choice and the sp500
7. (/jobs/<uuid>) will return the status and information about your job
8. (/download/<uuid>) will allow you to download a picture of the graph you requested through the API

## Example curls
1. The following picture shows example curls for the first 3 routes:
![alt text](https://github.com/StevenDiep/Stocks-cloud-system/blob/main/readme/example_curl_1.png?raw=true)

2. The following picture shows example curls for the next 5 routes:
![alt text](https://github.com/StevenDiep/Stocks-cloud-system/blob/main/readme/example_curl_2.png?raw=true)

The results from all of these curls will be in the examples folder
## Kubernetes example curls
The process to get the same results on kubernetes is a bit more involved.
1) First you need to start up a python debug deployment if you haven't already using:
```bash
make k-debug-pod
```
2) Find the IP address of the API service you'll be pinging requests to using as well as the name of your debug pod:
```bash
kubectl get services
```

```bash
kubect get pods
```

3) Once you have the IP address, exec into the debug pod using:
```bash
kubectl exec -it <your pod> -- /bin/bash
```

4) Once inside, you can use curl requests as normal just replace 'localhost' with the IP address you got before
5) Last, once you download the images using download, we have to use kubectl cp to transfer the image from the pod to our local computer

## Kubernetes Example
The following picture shows how to start up the k8s pods and the python debug pod. Also shows how you need to copy the IP address of the API service for the curls and then shows an example of curling a route:
![alt text](https://github.com/StevenDiep/Stocks-cloud-system/blob/main/readme/example_k8s_1.png?raw=true)

This next picture shows how to use commands to request a graphing job and then takes that output graph from your pod to your local machine:
![alt text](https://github.com/StevenDiep/Stocks-cloud-system/blob/main/readme/example_k8s_2.png?raw=true)

## Future work

1) I would love to add some HTML and CSS to the project in the future to have some actual front-end
2) Some of the steps to grab a graph seemed involved, especially with kubernetes. Hopefully I can find a way in the future to make this process more smooth and fluent for users to obtain a graph.
3) Add more analysis jobs other than just graphing. Maybe use some machine learning algorithms or basic stock graph analysis to the project as well. 
