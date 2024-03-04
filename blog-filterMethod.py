import json
import boto3

def lambda_handler(event, context):
    try:
        # the JSON data is passed in the 'body' field of the event
        json_data = json.loads(event['body'])
        
        target_name = "Quinton"
        
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        
        table = dynamodb.Table('Blog')
        
        filtered_data = []
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Key('name').eq(target_name)
        )
        
        filtered_data.extend(response['Items'])
        
        # Paginate through remaining results
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Key('name').eq(target_name),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            filtered_data.extend(response['Items'])
        
        # Return the filtered data
        response = {
            'statusCode': 200,
            'body': json.dumps(filtered_data)
        }
        
        return response
        
    except Exception as e:
        # Handle any exceptions and return an error response
        response = {
            'statusCode': 500,
            'body': str(e)
        }
        return response
