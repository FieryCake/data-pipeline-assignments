import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # TODO implement
    bucket_name = 'assignment2-glenn'
    file_key = 'output/outletReviews.json'
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    json_content = json.loads(response['Body'].read().decode('utf-8'))
    print(type(json_content))
    display = []
    for i in json_content:
        a = {}
        restaurant = i[-1]

        print(restaurant)
        a['name'] = restaurant['alias']
        a['rating'] = restaurant['rating']
        a['review_count'] = restaurant['review_count']
   
        display.append(a)
        
    print(display)
    
    
    filePut = json.dumps(display)
    bucket_name = 'assignment2-glenn'
    s3.put_object(Bucket=bucket_name, Key="visualisation/ratingPerOutlet.json", Body=filePut)
    return {
        'statusCode': 200,
        'body': json.dumps(display)
    }

