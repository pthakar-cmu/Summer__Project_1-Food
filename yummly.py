import urllib.request
from bs4 import BeautifulSoup

#Specify which page to scrape
url = 'https://www.yummly.com/'

#adding header to mask the fact that we are a program
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}

#making a request with the the header that we created
req = urllib.request.Request(url, headers=headers)

#sending that request
resp = urllib.request.urlopen(req)

#reading the resulting html that browser would normally interpret 
html = resp.read()

#Passing html to BS for parsing
soup = BeautifulSoup(html, 'html.parser')

#Start playing from here
try_values = soup.find_all("div",{'class':'scroll-wrapper scrollbar'})
print(try_values)

