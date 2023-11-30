import json
import boto3
import requests

def lambda_handler(event, context):
    # TODO implement
    bucket_name = 'assignment2-glenn'
    file_key = 'input/allOutlet.json'

    # Initialize the S3 client
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        json_content = json.loads(response['Body'].read().decode('utf-8'))
        json_content = json.loads(json_content.encode().decode('unicode-escape'))
        

        ##getting those only that are below average
        businesses = json_content['businesses']
        count = 0
        avg = 0
        total = 0
        bef = []
        
        for business in businesses:
          if business['alias'][0:5] == 'jumbo': ## only those jumbo
            bef.append(business)
            count+=1
            total+=business['rating']
            avg = total/count

        ###########################################
        
        ##Do API calls for those below avg
        final = []
        
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer ?"
        }
        test = []
        
        for business in bef:
          if business['rating']<=avg+0.1:
            url = "https://api.yelp.com/v3/businesses/"+business['id']+"/reviews?limit=200&sort_by=yelp_sort"
                
            response = requests.get(url, headers=headers)
        
            print(response.text)
            temp = json.loads(response.text)['reviews']
            test.append(len(temp))
            temp.append(business)
            final.append(temp)
        
        print(final)
        print("WHOO",test)
       
       
        filePut = json.dumps(final)
        bucket_name = 'assignment2-glenn'
        s3.put_object(Bucket=bucket_name, Key="output/outletReviews.json", Body=filePut)
        

        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
