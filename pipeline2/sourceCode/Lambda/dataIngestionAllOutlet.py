import json
import requests
import boto3
def lambda_handler(event, context):
    # TODO implement

    url = "https://api.yelp.com/v3/businesses/search?location=singapore&term=jumboseafood&sort_by=best_match&limit=20"
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer ?"
    }
    
    response = requests.get(url, headers=headers)
    
    print(response.text)
    s3 = boto3.client('s3')
    filePut = json.dumps(response.text)
    bucket_name = 'assignment2-glenn'
    s3.put_object(Bucket=bucket_name, Key="input/allOutlet.json", Body=filePut)
    return {
        'statusCode': 200,
        'body': json.dumps(response.text)
    }
