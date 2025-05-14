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
            print("\tIt doesn't seem like you provided any input. We'll use https://example.org instead.")
            url = "https://example.org"
    #do the actual request
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        print("\tWe couldn't recognize a URL schema. I TOLD you to include an URL schema! SMH.\n\tWe're just going to use 'https://'.")
        response = requests.get("https://" + url)
    #do not continue and just raise an exception if there is an HTTP error code
    response.raise_for_status()
    print("\tReceived content from the page!")
    #return the response object as the function's output
    return response

# response1 = response # saving function output in the general scope # ugh, screwed this up, commenting out for now

def read_response(resp: requests.models.Response) -> str:
    '''Given a requests Response object, return the HTML source code'''
    print("Reading the page's response...")
    text = resp.text
    # Code to deny responses that are null or too short
    if len(text) > 10:
        print("\tResponse read! Length is not too short as to suggest an error.")
        return text
    elif len(text) in (None, 0):
        raise ValueError("\tThe response was null or zero.")
    elif text != None:
        raise requests.exceptions.RequestException(f"\tThere was a response, but it was way too short. It consisted entirely of {print(text)}.")

def save_page(html: str): #save the html to a file
    print("Attempting to save the page to a file...")
    from datetime import datetime
    title_tag = bs4.BeautifulSoup(html,"html5lib").find("title") # look for the page's title element
    title = title_tag.next
    title_v = title.replace("|","\u00a6") # replace pipes ('|') since they're common in titles and file systems hate them, and replace them with broken pipes ('¦')
    constructed_file_name = f"{title_v} \u2014 {datetime.now().timestamp()}.html"
    try: # I'm very concerned about IO errors, they are so common.
        with open(constructed_file_name, "wt") as file: # I'm including the date as part of the file name to ensure unique file names
            file.write(html) # the actual write operation
            file.close()
            print("\tFile saved!")
    except IOError as save_error:
        print(f"\tThere was an error when attempting to save the page to a file: {save_error}.\n\t\tOh well. Moving on to the rest of the program.")
    except UnicodeEncodeError as encode_err:
        print(f"\tThere was an error when trying to encode page into Unicode: {encode_err}.\n\t\tOh well. Moving on to the rest of the program.")

def scrape(html: str):
    '''Scrape an HTML document. HTML should be in the form of a string'''
    print("Starting the true scraping process...")
    soup = bs4.BeautifulSoup(html,'html5lib')
    while True: #  while = tag_name != "NONE": # The commented-out code failed, the loop simply ignored it
        tag_name = input("Which HTML elements are you looking for?\nType the HTML tag name and we'll return all HTML elements in the page that match it.\n(Type 'none' (case-insensitive) to exit)\nTag name: ")
        #If the user inputs 'none' (not case-sensitive), then exit loop
        if tag_name.lower() in ("none", "none "): # allowing a space for exit requests so users more easily avoid PyCharm's autocomplete feature from interfering. Sadly, IDK how to do this for the tag names
            print("\t\tSince you responded with 'none', we'll stop.\n\nThank you for scraping with us! Goodbye!") #farewell message
            break
        found_elements = soup.find_all(tag_name) # main scrape operation
        if len(found_elements) > 0: # only if elements were actually found.
            #print each found element on a new line
            print(f"\t\tSuccess! We found {len(found_elements)} element(s) that match \"{tag_name}\"!") # the escaped double-quotes were PyCharm's idea, not mine
            if len(found_elements) > 10:
                print("\t\t\tOh my. That's a lot. HERE THEY COME!")
                sleep(5)
            for e in found_elements:
                print(e)
                print(" ---- END OF ELEMENT LIST ----" + ("\n" * 3))
        elif (len(found_elements) == 0) or (found_elements == None): # message if the element wasn't found
                print(Warning(f"\t\tThe scraper was unable to find any elements of that tag name '{tag_name}'."))

#the main function
def main(URL : str = None):
    '''The main function of the scraper. URL parameter is optional;
    it will interactively ask for a URL as input if you don't provide one as an argument.'''
    try:
        print("Hi, this is my little web scraper!\n") # Greeting
        page = get_page(URL) # request the page and save the response into "page"
        pagetext = read_response(page) # extract the source code from the response object "page" and save it as a string into "pagetext"
        save_page(pagetext) # attempt to save the string object "pagetext" into a file. Failure here does not terminate the program.
        scrape(pagetext) # extract requested HTML elements from the source code string "pagetext"
    except requests.exceptions.HTTPError as http_err:
        print(f"\tUgh. There was an HTTP status code! Specifically, it was {http_err}.")
    except requests.Timeout as timed_out:
        print("\tThe connection timed out. Sorry.")
        print(timed_out)
    except requests.packages.urllib3.exceptions.NameResolutionError as failedToResolve:
        print("\tWe were unable to resolve that name to a particular IP address.\nEither the DNS servers are not functioning properly, or the website you requested simply does not exist.")
        print(failedToResolve)
    except requests.exceptions.ConnectionError as e_connection:
        print(f"\tThere was an unexpected connection-related error: {e_connection}")
        if isinstance(e_connection.args[0],requests.packages.urllib3.exceptions.MaxRetryError):
            print("\t\tThe connection failed after multiple attempts.")
            print(f"\t\tThe reason?\n\t\t\t{e_connection.args[0].reason}") #print actual underlying error that caused the repeated attempts to fail
    except Exception as e_unexpected:
        print(f"\tThere was an unexpected error: {e_unexpected}")
        raise

if __name__ == '__main__':
    main(URL)