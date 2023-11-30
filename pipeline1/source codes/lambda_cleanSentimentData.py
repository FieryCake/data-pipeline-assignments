import boto3
import json

def lambda_handler(event, context):
    bucket_name = 'assignment1bucket-glenn'
    file_key = 'sentiment/sentiment.json'


    s3 = boto3.client('s3')

    try:
     
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        json_lines = response['Body'].read().decode('utf-8').splitlines()
        print(len(json_lines))
    
        li=[]
        for line in json_lines:
          
            json_data = json.loads(line)
            
            ##[{label=POSITIVE, score=0.9998196959495544}]
            json_data['agSent'] = json_data['sentiment'][0]['label']
   
            li.append(json_data)
            
         
            
        print(len(li))
        csv_file = "\n".join([json.dumps(obj) for obj in li])
        s3.put_object(Bucket=bucket_name, Key="sentimentClean/cleanedSentimentData.json", Body=csv_file)
        return {
            'statusCode': 200,
            'body': 'JSON data successfully processed.'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error processing JSON data.'
        }
