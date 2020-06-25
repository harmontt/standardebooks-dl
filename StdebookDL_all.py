# date: 06/24/20
# name: Harmon Turner
# version : 0.91
# description: Downloads given formats of ebooks from https://standardebooks.org/
import requests
from bs4 import BeautifulSoup
import feedparser
import os

#Options
    #True if books should be downloaded into the running directory
homedir = False
    #True for command line output
echo = True
    #Path to download to if homedir is set to False
destpath = "C:/test/"
    #ebook formats to download
formats = ['epub','amazon','kobo']
    #set True to download only new books
newbooks = False

baseurl = "https://standardebooks.org"
feed = feedparser.parse("https://standardebooks.org/rss/new-releases")

def getlinks(feed,echo = False):
    entries = feed.entries
    links = []
    for entry in entries:
        link = entry.link
        links.append(link)
        if echo:
            print(link)
    return links
    
#given a url and classtype, outputs url of book download link
def web(page,WebUrl,form,echo = False):
    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        for link in s.findAll('a', {'class':form}):
            tet = link.get('href')
            if echo:
                print(tet)
            return tet


#iterates through list of book page links and outputs the list of book download links
def createbooklist(links,formats,echo = False):
    booklist = []
    for link in links:
        for form in formats:
            booklist.append(web(1,link,form,echo))
    return booklist

#downloads a list of books in a given list of urls, and saves them to either the running directory or the given path
def dlebook(booklist,homedir,destpath = "C:/", echo = False):
    for book in booklist:
        site = baseurl + book
        site = site.rstrip()
        req = requests.get(site, allow_redirects=True)
        titles = book.split("/")
        title = titles[-1]
        title = title.rstrip()
        if echo:
            print(title)
        if not(homedir):
            title = destpath + title
        open(title, 'wb').write(req.content)
    return 0

#Puts it all together
def stdebookDL(feed,homedir=True,destpath='C:/books/',formats = ['epub'],newbooks = False,echo = True):
    links = getlinks(feed,echo)
    booklist = createbooklist(links,formats,echo)
    dlebook(booklist,homedir,destpath,echo)
    return 0


stdebookDL(feed,homedir,destpath,formats,echo)