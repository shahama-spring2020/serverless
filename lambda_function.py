import json
import boto3
from boto3.dynamodb.conditions import Key,Attr

def lambda_handler(event, context):
    # TODO implement


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
    dynamodb = boto3.resource(region_name="us-east-1")

    table = dynamodb.Table(dynamo_table)


    dynamo_row = table.query(
        KeyConditionExpression=Key('email').eq(emailid)
    )


    for i in range(len(message)-1):
        index="'"+i+"'"
        bills=''
        bills=','+bills.append(message[index])



    items = dynamo_row['Items']


    if not items:
        print("no similar items")


        response = table.put_item(
            Item={
                'email': 'janedoe',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'age': 25,
                'account_type': 'standard_user',
            }
        )
        print("New record inserted successfully")




    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
