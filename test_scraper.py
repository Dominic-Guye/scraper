import unittest
import scraper
import requests
import bs4

class TestCorrectClasses(unittest.TestCase):
    def get_page_returns_response_object(self): #make sure the output of get_page is a requests Response object
        response = scraper.get_page("https://www.example.com")
        self.assertIsInstance(response, requests.models.Response)

if __name__ == '__main__':
    unittest.main()
