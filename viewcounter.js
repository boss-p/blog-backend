import { DynamoDBDocument, DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocument.from(client);
const tableName = "Blog";

export const handler = async (event) => {
  try {
    const headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    };

    const itemID = event.queryStringParameters.id;
    
    console.log(itemID);

    const params = {
      TableName: tableName,
      Key: { id: itemID },
      UpdateExpression: 'SET #attrName = if_not_exists(#attrName, :start) + :val',
      ExpressionAttributeNames: { '#attrName': 'views' },
      ExpressionAttributeValues: { ':start': 0, ':val': 1 },
      ReturnValues: 'ALL_NEW'
    };

    await docClient.update(params);

    const response = {
      statusCode: 200,
      body: JSON.stringify({ message: 'Views incremented successfully' }),
      headers: headers
    };

    return response;
  } catch (error) {
    console.error(error);

    const response = {
      statusCode: 500,
      body: JSON.stringify({ message: 'An error occurred while incrementing views' }),
      headers: headers
    };

    return response;
  }
};
