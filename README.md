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


