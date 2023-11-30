#!/usr/bin/python3
import json
import requests
import boto3
from textblob import TextBlob
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.chunk import RegexpParser
import pandas as pd
import nltk
from faker import Faker
import random
from datetime import datetime, timedelta


fake = Faker()


def generate_food_review():
    positive = True
    food_adjectives = []  

    random_number = random.random()
    if random_number < 0.3:
        positive = False

        food_adjectives = ["bland", "disappointing", "unappetizing", "mediocre", "tasteless","sucks","EWWWW","stare","fishy"]

    else:
        food_adjectives = ['amazing','wow']
 
    service_sentiment = random.choice(["good", "bad"])

    review = {
        "id": fake.uuid4(),
        "url": fake.url(),
        "text": f"The food was {random.choice(food_adjectives)}! The service was {service_sentiment}.",
        "rating": random.randint(1, 5),  
        "time_created": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d %H:%M:%S"),
        "user": {
            "id": fake.uuid4(),
            "profile_url": fake.url(),
            "image_url": fake.image_url(),
            "name": fake.name()
        }
    }

    return review



s3 = boto3.client('s3')
bucket_name = 'assignment2-glenn'
file_key = 'output/outletReviews.json'
response = s3.get_object(Bucket=bucket_name, Key=file_key)
json_content = json.loads(response['Body'].read().decode('utf-8'))

print (len(json_content))

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return ' '.join(words)

final = []
for i in json_content:
    reason_frequency = {}
    restaurant = i[-1]
    reviews = i[0:-1]
    negative_reviews = [generate_food_review() for _ in range(50)] ##generate reviews
    reviews+=negative_reviews ##add on 

    for review in reviews:
        review['Processed'] = preprocess_text(review['text'])
        review['Sentiment'] = TextBlob(review['Processed']).sentiment.polarity
        if review['Sentiment'] >0:
            review['Sentiment_Label'] = "Positive"
        elif review['Sentiment']<0:



            review['Sentiment_Label'] = "Negative"
           

            words = word_tokenize(review['text'])
            tagged_words = pos_tag(words)
            chunk_parser = RegexpParser(r'''Chunk: {<JJ>*<NN.*>+}''')
     
            chunks = chunk_parser.parse(tagged_words)
                   #  Chunks: (S
            # The/DT
            # (Chunk quick/JJ brown/NN)
            # (Chunk fox/NN)
            # jumped/VBD
            # over/IN
            # the/DT
            # (Chunk lazy/JJ dog/NN)
            # ./.)
            negative_phrases = [word for word, tag in chunks.leaves() if tag.startswith('JJ') or tag.startswith('NN')]
        
     
            for phrase in negative_phrases:
                reason_frequency[phrase] = reason_frequency.get(phrase, 0) + 1


        else:
            review['Sentiment_Label'] = "Neutral"

       
    reason_frequency['business'] = restaurant['alias']
    final.append(reason_frequency)
   

print(final)
filePut = json.dumps(final)
bucket_name = 'assignment2-glenn'
s3.put_object(Bucket=bucket_name, Key="visualisation/outletSentiment.json", Body=filePut)

region = 'us-east-1'
instances = ['i-0e7ef28df57c13e84']
ec2 = boto3.client('ec2', region_name=region)

ec2.stop_instances(InstanceIds=instances)

##sources 
# https://realpython.com/nltk-nlp-python/
# https://pypi.org/project/Faker/0.7.4/
# https://textblob.readthedocs.io/en/dev/quickstart.html
# https://www.nltk.org/howto/chunk.html
# https://stackoverflow.com/questions/58617920/how-print-only-the-string-result-of-the-chunking-with-nltk 