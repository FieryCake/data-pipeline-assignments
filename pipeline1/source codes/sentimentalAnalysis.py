##Source
##https://huggingface.co/blog/sentiment-analysis-python
import nltk
import boto3
import json
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

nlp = pipeline("sentiment-analysis")
bucket_name = 'assignment1bucket-glenn'
file_key = 'output/cleanedData.json'
count=0
def analyze_sentiment(line):
    global count
    try:
        json_data = json.loads(line)
        result = nlp(json_data['short_description'])
        print(result)

        json_data['sentiment'] = result 
        count+=1
        print(count)
        return json_data
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None

# Initialize the S3 client
s3 = boto3.client('s3')
response = s3.get_object(Bucket=bucket_name, Key=file_key)
json_lines = response['Body'].read().decode('utf-8').splitlines()
print(len(json_lines))
  
li = []
with ThreadPoolExecutor(max_workers=40) as executor:
    results = list(executor.map(analyze_sentiment, json_lines))
    li = [data for data in results if data is not None]

json_file = "\n".join([json.dumps(obj) for obj in li])


s3.put_object(Bucket=bucket_name, Key="sentiment/sentiment.json", Body=json_file)

print("Success")
    
