import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re


def download_pngs(url, directory):
    # Send an HTTP request to the URL of the webpage you want to access.
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = requests.get(url)

    # Check if the response is valid.
    if response.status_code == 200:
        # Get the webpage's content and store it in a variable.
        html = response.text
    else:
        print("Invalid response.")
        return

    # Find all of the png image URLs on the webpage using a regular expression.
    png_urls = re.findall('https://.+?\.png', html)

    # Iterate over the list of png URLs.
    for url in png_urls:
        # Get the filename by splitting the URL and getting the last element.
        filename = url.split("/")[-1]

        # Create the full path by joining the directory and the filename.
        path = os.path.join(directory, filename)

        # Download the image data and save it to a file.
        with open(path, "wb") as f:
            f.write(requests.get(url).content)


# Extracts the page number from a url after the "=" sign
def getcurrentpage(url):
    url = url.split('=')
    return url[1]


# Extracts all text in a url before the "=" sign
def spliturl(url):
    url = url.split('=')
    return url[0] + "="


# enumerates each page by increasing the page number in the URL
def enumeratepage(url):
    urlname = spliturl(url)
    urlnum = int(getcurrentpage(url)) + 1
    return urlname + str(urlnum)

# iterates through every page and extracts the png files
def iteratepage(url):
    # Asks the user to specify the total number of pages that will be scanned
    totalpagenumber = int(input("Enter the total number of web pages to enumerate"))
    for i in range(totalpagenumber):
        download_pngs(url, "animal_heads")
        print(url)
        url = enumeratepage(url)


iteratepage("https://www.graaldepot.com/animalnon-human?nggpage=1")
