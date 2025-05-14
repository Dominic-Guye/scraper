# this was an initial concept, it should still be functional but is unnecessary and should be ignored or deleted

import requests
import bs4
import html5lib
from time import sleep
examplepage = requests.get('https://quotes.toscrape.com') # the actual request
example_headers = examplepage.headers # storing the headers in a variable
example_status = examplepage.status_code # storing the status code
example_read = examplepage.text # storing the actual content of the page

# Code to deny responses that are null or too short
if len(example_read) > 10:
    print("The page looks good so far! INCOMING!")
    sleep(3)
elif len(example_read) in (None, 0):
    raise ValueError("The response was null or zero.")
elif example_read != None:
    raise urllib3.exceptions.ResponseError(f"There was a response, but it was way too short. It consisted entirely of {print(example_read)}.")

# The actual scraping occurs below
example_soup = bs4.BeautifulSoup(example_read,'html5lib')
print('-------------START OF PAGE-------------\n')
print(example_soup)
print('\n-------------END OF PAGE-------------')
print(example_soup.find('a')) # find hyperlinks
found_elements = example_soup.find_all('p') #Interesting, 'find_all' returns what seems like a list object
if isinstance(found_elements,list):
    for i in found_elements:
        print(i)
