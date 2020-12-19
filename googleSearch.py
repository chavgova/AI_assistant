

# https://python-googlesearch.readthedocs.io/en/latest/
# https://muddoo.com/tutorials/how-to-extract-data-from-a-website-using-python/


# TODO: command:'learn about X' => gets 3 articles and studies them and can answer questions 
#               https://randerson112358.medium.com/build-your-own-ai-chat-bot-using-python-machine-learning-682ddd8acc29 

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import io
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
                

gs = Gsearch_python("emotions")
link = gs.Gsearch()
    
# 

import urllib.request
from bs4 import BeautifulSoup
import nltk

content = urllib.request.urlopen(link)

read_content = content.read()
soup = BeautifulSoup(read_content,'html.parser')
pAll = soup.find_all('p')
h2All = soup.find_all('h2')


# text document 
learn_file = io.open('learn_emotions.txt', 'a+', encoding='utf8')
for i in pAll:
    learn_file.write(i.text)

text = ''
with open("learn_emotions.txt") as mytxt:
    for line in mytxt:
        text += line    

sent_tokens = nltk.sent_tokenize(text)# txt to a list of sentences 

#Return the indices of the values from an array in sorted order by the values
def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))
  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp
  return list_index


# Generate the response
def bot_response(user_input):
    user_input = user_input.lower() #Convert the users input to all lowercase letters
    sent_tokens.append(user_input) #Append the users response to the list of sentence tokens
    bot_response='' #Create an empty response for the bot
    cm = CountVectorizer().fit_transform(sent_tokens) #Create the count matrix
    similarity_scores = cosine_similarity(cm[-1], cm) #Get the similarity scores to the users input
    flatten = similarity_scores.flatten() #Reduce the dimensionality of the similarity scores
    index = index_sort(flatten) #Sort the index from 
    index = index[1:] #Get all of the similarity scores except the first (the query itself)
    response_flag=0 #Set a flag letting us know if the text contains a similarity score greater than 0.0
    #Loop the through the index list and get the 'n' number of sentences as the response
    j = 0
    for i in range(0, len(index)):
      if flatten[index[i]] > 0.0:
        bot_response = bot_response + ' ' + sent_tokens[index[i]]
        response_flag = 1
        j = j+1
      if j > 2:
        break  
    #if no sentence contains a similarity score greater than 0.0 then print 'I apologize, I don't understand'
    if(response_flag==0):
        bot_response = bot_response+' '+"I apologize, I don't understand."
        sent_tokens.remove(user_input) #Remove the users response from the sentence tokens
       
    return bot_response

 
response = bot_response('where do emotions come from')

index1 = response.find('[')

while(index1 != -1):
    response = response[:index1] + response[index1+4:]
    index1 = response.find('[')

print(response)