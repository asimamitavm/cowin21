import json
from botocore.vendored import requests
import logging
import boto3
from botocore.exceptions import ClientError
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

age = 18
a = 585402
b = 585401
SENDER = ""
RECIPIENT = ""
CONFIGURATION_SET = "ConfigSet"
AWS_REGION = "ap-south-1"
client = boto3.client('ses',region_name=AWS_REGION)
CHARSET = "UTF-8"

def lambda_handler(event, context):
    response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=272&date=19-05-2021', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'})
    posts = response.json()
    for i in posts["centers"]:
        #print(i["name"],'\t',i["pincode"])
        if i["pincode"] == a or i["pincode"] == b:
            for j in i["sessions"]:
                if j["min_age_limit"] == age and j["available_capacity"] > 0:
                    print(i["name"],'\t',i["pincode"],'\t',j["min_age_limit"],'\t',j["vaccine"])
                    SUBJECT = "Vaccine Alert"
                    #print (BODY_TEXT)
                    BODY_TEXT = str(j["date"])+' '+str(i["name"])+' '+str(i["pincode"])+' '+str(j["min_age_limit"])+' '+str(j["vaccine"])+' '+str(j["available_capacity"])
                    print (BODY_TEXT)
                    try:
                        response = client.send_email(
                            Destination={
                                'ToAddresses': [
                                    RECIPIENT,
                                    ],
                            },
                            Message={
                                'Body': {
                                    'Text': {
                                        'Charset': CHARSET,
                                        'Data': BODY_TEXT,
                                    },
                                },
                                'Subject': {
                                    'Charset': CHARSET,
                                    'Data': SUBJECT,
                                },
                            },
                            Source=SENDER,
                        )
                # Display an error if something goes wrong.       
                    except ClientError as e:
                        print(e.response['Error']['Message'])
                    else:
                        print("Email sent! Message ID:"),
                        print(response['MessageId'])
        print("\n")

