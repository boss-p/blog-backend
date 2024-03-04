import json
import boto3
import logging
from custom_encoder import CustomEncoder

# define the logger object
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# define global variables and objects
dynamodb = boto3.resource('dynamodb')
blogTable = dynamodb.Table('Blog')

# define the request methods
getMethod = 'GET'

# define api gateway paths
healthPath = '/health'
blogPath = '/blog'
blogsPath = '/blogs'


def lambda_handler(event, context):
    # log the event object to see how it looks
    logger.info(event)

    # extract the httpMethod from the event object
    httpMethod = event['httpMethod']

    # extract the path from the event object
    path = event['path']
    if httpMethod == getMethod and path == healthPath:  # check api gateway health
        response = buildResponse(200)
    elif httpMethod == getMethod and path == blogPath:  # get 1 blog
        response = getBlog(event['queryStringParameters']['id'])
    elif httpMethod == getMethod and path == blogsPath:  # get all blogs
        response = getBlogs()
    else:
        response = buildResponse(404, 'Not Found')

    return response


# get 1 blog method
def getBlog(blog_id):
    try:
        response = blogTable.get_item(
            Key={
                'id': blog_id,
            }
        )

        # check if blog exists
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'Blog %s not found' % blog_id})

    except:
        logger.exception('Error message')


# end of method

# get all blogs method
def getBlogs():
    try:
        response = blogTable.scan()
        result = response['Items']

        # if the table has many items, we may not be able to retrieve all of them at once because of the dynamodb
        # limits, we do a while statement to continue retrieving and add the results
        while 'LastEvaluatedKey' in response:
            response = blogTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'blogs': result
        }

        return buildResponse(200, body)

    except:
        logger.exception('Error message')


# end of method

# start the buildResponse method for the if statement
def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    # check if body is not none
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response
# end of the buildResponse method
