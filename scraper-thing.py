import requests
import bs4
import html5lib


examplepage = requests.get('https://example.org')
example_headers = examplepage.headers
example_status = examplepage.status_code
example_read = examplepage.text
if len(example_read) > 10:
    print(example_read)
elif len(example_read) in (None, 0):
    raise ValueError("The response was null or zero.")
elif example_read != None:
    raise urllib3.exceptions.ResponseError(f"There was a response, but it was way too short. It consisted entirely of {print(example_read)}.")

example_soup = bs4.BeautifulSoup(example_read,'html5lib')
print(example_soup)
print(example_soup.find('a'))
print(example_soup.find_all('p')) #Interesting, 'find_all' returns what seems like a list object