
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import io
import re
import nltk

text = ''
with open("emotions.txt") as mytxt:
    for line in mytxt:
        line = re.sub('\[.*?\]', '', line)
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
    bot_response = '' #Create an empty response for the bot
    similarity = CountVectorizer().fit_transform(sent_tokens) #Create the count matrix
    similarity_scores = cosine_similarity(similarity[-1], similarity) #Get the similarity scores to the users input
    flatten = similarity_scores.flatten() #Reduce the dimensionality of the similarity scores
    index = index_sort(flatten) #Sort the index from 
    index = index[1:] #Get all of the similarity scores except the first (the query itself)
    response_flag = 0 #Set a flag letting us know if the text contains a similarity score greater than 0.0
    #Loop the through the index list and get the 'n' number of sentences as the response

    sen_count = 1
    for i in range(0, len(index)):
      if (flatten[index[i]] > 0.0) and (flatten[index[i]] != flatten[index[i-1]]):
        bot_response = bot_response + ' ' + sent_tokens[index[i]]
        response_flag = 1
        sen_count = sen_count+1
      if sen_count > 3:
        break  
    #if no sentence contains a similarity score greater than 0.0 then print 'I apologize, I don't understand'
    if(response_flag==0):
        bot_response = bot_response+' '+"I apologize, I don't understand."
        sent_tokens.remove(user_input) #Remove the users response from the sentence tokens
       
    return bot_response

 
#response = bot_response('why am i stressed')

#response = re.sub('\[.*?\]', '', response)

#print(response)