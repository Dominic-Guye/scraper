import requests
import bs4
import html5lib

#maybe I should make a function for requesting (+ maybe storing) and another for scraping
## Update: made a function for requesting, but storing will be hard bc of scope issues

# the requesting function
def get_page(url: str = None) -> requests.models.Response: #note: first ever type hint!
    #if no url is given, use example.org
    if url == None:
        inputted_url = input("What page do you want to request? Include the URL schema in your input. ")
        if inputted_url != None:
            url = inputted_url
        else:
            url = "http://example.org"
    #do the actual request
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        print("We couldn't recognize a URL schema. I TOLD you to include an URL schema! SMH.\nWe're just going to use 'https://'.")
        response = requests.get("https://" + url)
    #do not continue and just raise an exception if there is an HTTP error code
    response.raise_for_status()

    #return the response object as the function's output
    return response

# response1 = response # saving function output in the general scope # ugh, screwed this up, commenting out for now

def read_response(resp: requests.models.Response) -> str:
    '''Given a requests Response object, return the HTML source code'''
    text = resp.text
    # Code to deny responses that are null or too short
    if len(text) > 10:
        return text
    elif len(text) in (None, 0):
        raise ValueError("The response was null or zero.")
    elif text != None:
        raise requests.exceptions.RequestException(f"There was a response, but it was way too short. It consisted entirely of {print(example_read)}.")

def scrape(html: str):
    '''Scrape an HTML document. HTML should be in the form of a string'''
    soup = bs4.BeautifulSoup(html,'html5lib')
    while True: #  while = element_name != "NONE": # The commented-out code failed, the loop simply ignored it
        element_name = input("Which HTML element are you looking for?\n(Type 'none' (case-insensitive) to exit)\nElement choice: ")
        #If the user inputs 'none' (not case-sensitive), then exit loop
        if element_name.lower() == "none":
            print("Since you responded with 'none', we'll stop.\nThank you for scraping with us!")
            break
        found_elements = soup.find_all(element_name)
        if isinstance(found_elements, list):
            for e in found_elements:
                print(e)

#the main function
if __name__ == '__main__':
    #Note: I need to add exception handling
    try:
        page = get_page()
    except requests.exceptions.HTTPError as http:
        print(f"Ugh. There was an HTTP status code! Specifically, it was {http}.")
    except requests.exceptions.RetryError as gaveUp:
        print("We gave up. Too many tries, and they all failed.")
        print(gaveUp)
    except requests.Timeout as timed_out:
        print("Connection timed out. Sorry.")
        print(timed_out)
    except Exception as e_unexpected:
        print(f"There was an unexpected error: {e_unexpected}")
    assert  page != None # sick of that weird "'page' is not defined" error.
    pagetext = read_response(page)
    scrape(pagetext)
