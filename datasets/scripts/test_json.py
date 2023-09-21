import json
import unittest

class TestJsonEx(unittest.TestCase):
    
    def test_check_json(self):
        with open("stocks.json", 'r') as f:
            stocks = json.load(f)
        
        self.assertEqual(len(stocks), 504)
        self.assertEqual("AAPL" in stocks, True)
        self.assertEqual(stocks["AAPL"]["2023-09-19"], 179)
        self.assertEqual("GOOGL" in stocks, True)
        

if __name__ == '__main__':
    unittest.main()
