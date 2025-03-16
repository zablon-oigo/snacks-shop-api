import json
import boto3
import uuid
import os 
from decimal import Decimal
dynamo_db = boto3.resource('dynamodb')
table_name = os.environ['SNACKS_ORDERS_TABLE']
table = dynamo_db.Table(table_name)

def lambda_handler(event, context):
    try:
        request_body = json.loads(event['body'])
        email=request_body.get('email')
        customer_name = request_body.get('customer_name')
        snack = request_body.get('snack')
        amount=Decimal(str(request_body['amount']))
        order_id = str(uuid.uuid4())
        params = {
            'TableName': table_name,
            'Item': {
                'OrderId': order_id,
                'Email':email,
                'CustomerName': customer_name,
                'Snack': snack,
                'OrderStatus': 'Pending',
                'Amount':amount
            }
        }
        table.put_item(Item=params['Item'])
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order created successfully!',
                'OrderId': order_id
            })
        }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Could not create order: {str(error)}'
            })
        }