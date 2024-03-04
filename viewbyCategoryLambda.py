import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Blog')  # table name

    category = event['category']  #category is passed as input in the event

    response = table.scan(FilterExpression='category = :category', ExpressionAttributeValues={':category': category})

    items = response['Items']
    if len(items) == 0:
        return {
            'statusCode': 200,
            'body': f"No items found for category '{category}'."
        }
    
    categorized_items = {}
    for item in items:
        item_category = item['category']
        if item_category not in categorized_items:
            categorized_items[item_category] = []
        categorized_items[item_category].append(item)

    return {
        'statusCode': 200,
        'body': categorized_items
    }
