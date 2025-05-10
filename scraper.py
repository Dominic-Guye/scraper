import requests
import bs4
import html5lib
from time import sleep # I need this to create artificial delays to allow users time to catch their breath

# the requesting function
def get_page(url: str = None) -> requests.models.Response: #note: first ever type hint!
    # Ask that the user input a URL if none was given
    if url == None:
        inputted_url = input("What page do you want to request? Include the URL schema (we only support 'http://' and 'https://' for now) in your input. ")
        if inputted_url != None and len(inputted_url) > 0:
            url = inputted_url
        else: #if no url is given, use example.org
            print("It doesn't seem like you provided any input. We'll use http://example.org instead.")
            url = "http://example.org"
    #do the actual request
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        print("We couldn't recognize a URL schema. I TOLD you to include an URL schema! SMH.\nWe're just going to use 'https://'.")
        response = requests.get("https://" + url)
    #do not continue and just raise an exception if there is an HTTP error code
    response.raise_for_status()
    print("Recieved content from the page!")
    #return the response object as the function's output
    return response

# response1 = response # saving function output in the general scope # ugh, screwed this up, commenting out for now

def read_response(resp: requests.models.Response) -> str:
    '''Given a requests Response object, return the HTML source code'''
    print("Reading the page's response...")
    text = resp.text
    # Code to deny responses that are null or too short
    if len(text) > 10:
        print("Response read! Length is not too short as to suggest an error.")
        return text
    elif len(text) in (None, 0):
        raise ValueError("The response was null or zero.")
    elif text != None:
        raise requests.exceptions.RequestException(f"There was a response, but it was way too short. It consisted entirely of {print(text)}.")

def save_page(html: str): #save the html to a file
    print("Attempting to save the page to a file...")
    from datetime import datetime
    title_tag = bs4.BeautifulSoup(html,"html5lib").find("title") # look for the page's title element
    title = title_tag.next
    title_v = title.replace("|","\u00a6") # replace pipes ('|') since they're common in titles and file systems hate them, and replace them with broken pipes ('¦')
    constructed_file_name = f"{title_v} \u2014 {datetime.now().timestamp()}.html"
    try: # I'm very concerned about IO errors, they are so common.
        with open(constructed_file_name, "wt") as file: #including date as part of the file name to ensure unique names
            file.write(html)
            file.close()
            print("File saved!")
    except IOError as save_error:
        print(f"There was an error when attempting to save the page to a file: {save_error}.\nOh well. Moving on to the rest of the program.")
    except UnicodeEncodeError as encode_err:
        print(f"There was an error when trying to encode page into Unicode: {encode_err}.\nOh well. Moving on to the rest of the program.")

def scrape(html: str):
    '''Scrape an HTML document. HTML should be in the form of a string'''
    print("Starting the true scraping process...")
    soup = bs4.BeautifulSoup(html,'html5lib')
    while True: #  while = tag_name != "NONE": # The commented-out code failed, the loop simply ignored it
        tag_name = input("Which HTML elements are you looking for?\nType the HTML tag name and we'll return all HTML elements in the page that match it.\n(Type 'none' (case-insensitive) to exit)\nTag name: ")
        #If the user inputs 'none' (not case-sensitive), then exit loop
        if tag_name.lower() == "none":
            print("Since you responded with 'none', we'll stop.\nThank you for scraping with us!") #farewell message
            break
        found_elements = soup.find_all(tag_name) # main scrape operation
        if len(found_elements) > 0: # only if elements were actually found.
            #print each found element on a new line
            print(f'Success! We found {len(found_elements)} element(s) that match {tag_name}!')
            if len(found_elements) > 10:
                print("Oh my. HERE THEY COME!")
                sleep(5)
            for e in found_elements:
                print(e)
        elif (len(found_elements) == 0) or (found_elements == None): # message if the element wasn't found
                print(Warning("The scraper was unable to find any elements of that tag name."))

#the main function
if __name__ == '__main__':
    try:
        page = get_page()
        pagetext = read_response(page)
        save_page(pagetext)
        scrape(pagetext)
    except requests.exceptions.HTTPError as http:
        print(f"Ugh. There was an HTTP status code! Specifically, it was {http}.")
    except requests.Timeout as timed_out:
        print("The connection timed out. Sorry.")
        print(timed_out)
    except requests.packages.urllib3.exceptions.NameResolutionError as failedToResolve:
        print("We were unable to resolve that name to a particular IP address.\nEither the DNS servers are not functioning properly, or the website you requested simple does not exist.")
        print(failedToResolve)
    except requests.exceptions.ConnectionError as e_connection:
        print(f"There was an unexpected connection-related error: {e_connection}")
        if isinstance(e_connection.args[0],requests.packages.urllib3.exceptions.MaxRetryError):
            print("The connection failed after multiple attempts.")
            print(f"The reason? {e_connection.args[0].reason}") #print actual error that caused the failure
    except Exception as e_unexpected:
        print(f"There was an unexpected error: {e_unexpected}")
        raise
