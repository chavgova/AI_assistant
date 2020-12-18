

# https://python-googlesearch.readthedocs.io/en/latest/
# https://muddoo.com/tutorials/how-to-extract-data-from-a-website-using-python/


# TODO: command:'learn about X' => gets 3 articles and studies them and can answer questions 
#               https://randerson112358.medium.com/build-your-own-ai-chat-bot-using-python-machine-learning-682ddd8acc29 

class Gsearch_python:
        def __init__(self,name_search):
            self.name = name_search

        def Gsearch(self):
            count = 0
            try :
                from googlesearch import search
            except ImportError:
                print("No Module named 'google' Found")
            for i in search(query=self.name, tld='co.in', num=5, lang='en', stop=1, pause=1):  
                count += 1
                print(count)
                print(i + '\n')
                return i
                

if __name__=='__main__':
   gs = Gsearch_python("emotions")
   link = gs.Gsearch()
    
# 

import urllib.request
from bs4 import BeautifulSoup

content = urllib.request.urlopen(link)

read_content = content.read()
soup = BeautifulSoup(read_content,'html.parser')
pAll = soup.find_all('p')
h2All = soup.find_all('h2')
print(pAll[4].text)
print(h2All[4].text)