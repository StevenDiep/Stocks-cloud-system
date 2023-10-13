import unittestimport requestsimport jsonclass TestAPI(unittest.TestCase):        def test_flask(self):        response = requests.get('http://localhost:5000/')        self.assertEqual(response.status_code, 200)        #The following four tests tests the get point route    def test_stock_point(self):        response = requests.get('http://localhost:5000/stock/AAPL')        self.assertEqual(response.status_code, 200)        data = response.json()                self.assertEqual(len(data) > 100, True)        self.assertEqual(type(data), dict)        self.assertEqual(data["2022-09-22"], 151.84)            def test_stock_point_query(self):        response = requests.get('http://localhost:5000/stock/AAPL?date=2022-09-22')        self.assertEqual(response.status_code, 200)        data = response.json()        self.assertEqual(data, "2022-09-22: 151.84")            def test_invalid_stock_point(self):        response = requests.get('http://localhost:5000/stock/AA')        self.assertEqual(response.status_code, 404)            def test_invalid_stock_query(self):        response = requests.get('http://localhost:5000/stock/AAPL?date=2022-09-2')        self.assertEqual(response.status_code, 404)            #The following tests test the diff route    def test_stock_diff(self):        response = requests.get('http://localhost:5000/stock/diff/AAPL/1y')        self.assertEqual(response.status_code, 200)                data = response.json()        self.assertEqual(data, "The stock has increased by 14.55%")        def test_stock_diff_invalid_period(self):        response = requests.get('http://localhost:5000/stock/diff/AAPL/6y')        self.assertEqual(response.status_code, 404)            #The following tests will test the graph post route    def test_stock_graph(self):        url = 'http://localhost:5000/stock/graph'        job = {"ticker": "AAPL"}                response = requests.post(url, json=job)        self.assertEqual(response.status_code, 200)                data = response.json()        self.assertEqual(data['job_type'], 'graph' )        self.assertEqual(json.loads(data['input_values'])['ticker'], 'AAPL')                response2 = requests.get('http://localhost:5000/jobs/' + data['id'])        self.assertEqual(response2.status_code, 200)        data2 = response2.json()                response3 = requests.get('http://localhost:5000/download/' + data['id'])            def test_stock_compare(self):        url = 'http://localhost:5000/stock/compare'        job = {"ticker1": "AAPL", "ticker2": "ADBE"}                response = requests.post(url, json=job)        data = response.json()        self.assertEqual(response.status_code, 200)        self.assertEqual(data['job_type'], 'compare')        self.assertEqual(json.loads(data['input_values'])['ticker1'], 'AAPL')        self.assertEqual(json.loads(data['input_values'])['ticker2'], 'ADBE')                response2 = requests.get('http://localhost:5000/jobs/' + data['id'])        self.assertEqual(response2.status_code, 200)                response3 = requests.get('http://localhost:5000/download/' + data['id'])        if __name__ == '__main__':    unittest.main()