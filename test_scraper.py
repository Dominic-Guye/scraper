import unittest
import scraper
import requests
import bs4

class TestCorrectClasses(unittest.TestCase):
    def test_get_page_returns_response_object(self): #make sure the output of get_page is a requests Response object
        response = scraper.get_page("https://www.example.com")
        self.assertIsInstance(response, requests.models.Response)

    def test_read_response_returns_string(self): # make sure that the read response function returns a string
        this_should_be_a_string = scraper.read_response(requests.get("https://quotes.toscrape.com"))
        self.assertIsInstance(this_should_be_a_string, str)
if __name__ == '__main__':
    unittest.main()
