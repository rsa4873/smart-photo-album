import json
import boto3
import time
import requests
from requests.auth import HTTPBasicAuth

#My Changes

def lambda_handler(event, context):
    # TODO implement
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    #print(bucket_name)
    
    client = boto3.client('rekognition')
    s3 = boto3.client('s3')
    head = s3.head_object(Bucket=bucket_name, Key=key_name)
    print("Attention: ")
    print(head)
    
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    resp = client.detect_labels(Image=pass_object)
    #print('<---------Now response object---------->')
    #print(json.dumps(resp, indent=4, sort_keys=True))
    timestamp =time.time()
    #timestamp = event['Records'][0]['eventTime']
    #timestamp = timestamp[:-5]
    labels = []
    #temp = resp['Labels'][0]['Name']
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)
    
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    
    url = 'https://search-photos1-fuctzox4kk4n3vwy44xpfthlde.us-east-1.es.amazonaws.com/search/_doc'
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, auth = ("root","Zensar11!"), data=json.dumps(format).encode("utf-8"), headers=headers)
    print(r.text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
