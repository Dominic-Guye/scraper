import requests
import bs4
import html5lib

examplepage = requests.get('https://example.org') # the actual request
example_headers = examplepage.headers # storing the headers in a variable
example_status = examplepage.status_code # storing the status code
example_read = examplepage.text # storing the actual content of the page

# Code to deny responses that are null or too short
if len(example_read) > 10:
    print(example_read)
elif len(example_read) in (None, 0):
    raise ValueError("The response was null or zero.")
elif example_read != None:
    raise urllib3.exceptions.ResponseError(f"There was a response, but it was way too short. It consisted entirely of {print(example_read)}.")

# The actual scraping occurs below
example_soup = bs4.BeautifulSoup(example_read,'html5lib')
print(example_soup)
print(example_soup.find('a')) # find hyperlinks
print(example_soup.find_all('p')) #Interesting, 'find_all' returns what seems like a list object

#maybe I should make a function for requesting (+ maybe storing) and another for scraping

# the requesting function
def get_page(url):
    #if no url is given, use example.org
    if url == None:
        url = "http://example.org"
    #do the actual request
    response = requests.get(url)
    #do not continue and just raise an exception if there is an HTTP error code
    response.raise_for_status()

    pass #I want more logic here, maybe for storing stuff or doing non-scraping analysis. IDK yet.

    #return the response object as the function's output
    return response

def scrape():
    # Need to do the scraping stuff here. Maybe later
    pass