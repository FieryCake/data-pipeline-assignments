import boto3
import json

def lambda_handler(event, context):
    
    bucket_name = 'assignment1bucket-glenn'
    file_key = 'scrapedData/scaped.json'
  
    s3 = boto3.client('s3')

    try:
      
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        json_lines = response['Body'].read().decode('utf-8')
        data = json.loads(json_lines)
        li=[]
        for i in data:
            if i['comment'][:3].isnumeric():
                i['comment'] = int(i['comment'][:3])
                li.append(i)
            elif i['comment'][:2].isnumeric():
                i['comment'] = int(i['comment'][:2])
                li.append(i)
                
    
    
        # for line in json_lines:
        #     # Parse each line as a JSON object
        #     json_data = json.loads(line)
            
        #     ##[{label=POSITIVE, score=0.9998196959495544}]
        #     json_data['agSent'] = json_data['sentiment'][0]['label']
   
         
        #s3://assignment1bucket-glenn/scrapedData/scaped.json
         
            
        print(len(li))
        csv_file = "\n".join([json.dumps(obj) for obj in li])
        s3.put_object(Bucket=bucket_name, Key="scrapedClean/scaped.json", Body=csv_file)
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
