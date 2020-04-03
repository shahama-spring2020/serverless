import json
import boto3, time
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    ## TODO implement


    message = event['Records'][0]['Sns']['Message']
    print(message)

    print(type(message))
    print("hello")

    message=eval(message)
    print(type(message))

    print(type(message))
    emailid=message['emailid']

    print(emailid)



    dynamo_table = 'Duedate'
    dynamodb = boto3.resource('dynamodb',region_name="us-east-1")

    table = dynamodb.Table(dynamo_table)


    dynamo_row = table.query(
        KeyConditionExpression=Key('email').eq(emailid)
    )


    for i in range(len(message)-1):
        index=str(i)
        link='http://prod.amanshah.xyz/v1/bill/'+message[index]
        link_array=[]
        link_array.append(link)



    csv = ',   '.join([str(elem) for elem in link_array])
    items = dynamo_row['Items']


    if not items:
        print("no similar items")

        ttl=time.time()+600
        print(ttl)
        response = table.put_item(
            Item={
                'email': emailid,
                'links':csv,
                'deleteTime':ttl

            }
        )


        print("New record inserted successfully")
        prepare_and_send_email(emailid,csv)
        print("New record email")
    else:
        print("record exists")
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }



def prepare_and_send_email(recipient, body):
    # Sender Email ID
    SENDER = "noreply@" + 'prod.amanshah.xyz'


    # The email body for recipients
    BODY_TEXT = ('bill links' + "\r\n" +body)


    SUBJECT = "link of bills"



    # print(AWS_REGION)

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',aws_region='us-east-1')
    # Try to send the email.
    CHARSET = "UTF-8"

    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
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
        print("Email sent!"),
        print(response['MessageId'])