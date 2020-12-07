import numpy as np
import pandas as pd

#TEXT EMO REC HERE 


filepath = r"C:\Users\ok\Documents\GABRIELA\ASSISTANT\NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t', keep_default_na=False)
#print(emolex_df.head(12))

# all emotions
# print(emolex_df.emotion.unique())  - all emos

#print(emolex_df.emotion.value_counts())
# How many words does each emotion have ------- We're only going to care about "is associated."
#print(emolex_df[emolex_df.association == 1].emotion.value_counts()) 

emolex_words = emolex_df.pivot(index='word', columns='emotion', values='association').reset_index()
emolex_words.head()

anger_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'anger')].word)
anticipation_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'anticipation')].word)
disgust_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'disgust')].word)
fear_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'fear')].word)
joy_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'joy')].word)
negative_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'negative')].word)
positive_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'positive')].word)
sadness_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'sadness')].word)
surprise_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'surprise')].word)
trust_words = str(emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'trust')].word)

def sentence_to_list(lst): 
    return (lst[0].split()) 

text = ['this place is an wrongful abandoned park']
#text = ['this place is a park']

#text = [recognized_text]

sentence_word_list = sentence_to_list(text)
text_emos_list = []

for word in sentence_word_list:
  current_word = ' ' + word

  if current_word in anger_words:
    text_emos_list.append('anger')
  if current_word in anticipation_words:
    text_emos_list.append('anticipation')
  if current_word in disgust_words:
    text_emos_list.append('disgust')
  if current_word in fear_words:
    text_emos_list.append('fear')
  if current_word in joy_words:
    text_emos_list.append('joy')
  if current_word in negative_words:
    text_emos_list.append('negative')
  if current_word in positive_words:
    text_emos_list.append('positive')
  if current_word in sadness_words:
    text_emos_list.append('sadness')
  if current_word in surprise_words:
    text_emos_list.append('surprise')
  if current_word in trust_words:
    text_emos_list.append('trust')

print(text_emos_list)
