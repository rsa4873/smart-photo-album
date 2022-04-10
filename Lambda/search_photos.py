import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
import requests

def lambda_handler(event, context):
    # TODO implement
    
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    client = boto3.client('lex-runtime')
    
    response_lex = client.post_text(
    botName='GetPhotos',
    botAlias="Dev",
    userId="test",
    inputText=  event["queryStringParameters"]['q'])
    
    print('Lex Response ')
    print(response_lex)
    keys = []
    if 'slots' in response_lex:
        keys = [response_lex['slots']['slotOne'],response_lex['slots']['slotTwo']]
    print(keys)
    
    url2 = 'https://search-photos1-fuctzox4kk4n3vwy44xpfthlde.us-east-1.es.amazonaws.com/search/_search?q='
    
    responses = []
    for key in keys:
        if key is not None and key != '' :
            r = requests.get(url = url2+key, auth=('root','Zensar11!')).json()
            responses.append(r)
            
    print(responses)
    
    photoUrls = []
    for response in responses:
        if 'hits' in response:
            for val in response['hits']['hits']:
                picture = val["_source"]["objectKey"]
                bucket =  val["_source"]["bucket"]
                photoURL = "https://{0}.s3.amazonaws.com/{1}".format(bucket,picture)
                if photoURL not in photoUrls:
                 photoUrls.append(photoURL)
                
    print(photoUrls)
                
    if(photoUrls != []) :
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(photoUrls),
            "isBase64Encoded": False
        }
    
    return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": "",
            "isBase64Encoded": False}
    
    

