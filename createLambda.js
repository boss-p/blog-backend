import {DynamoDBDocument, DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';
import {DynamoDBClient} from '@aws-sdk/client-dynamodb';

const client = new DynamoDBClient({});

const docClient = DynamoDBDocument.from(client);

const tableName = "Blogs";

export const handler = async (event, context) => {
    let body;
    let statusCode = 200;
    const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    };

    let requestJSON = JSON.parse(event.body);
        await docClient.put({
            TableName: tableName,
                Item: {
                    id: requestJSON.id,
                    title: requestJSON.title,
                    description: requestJSON.description,
                }
                })
        body = "Added/Updated Product ${requestJSON.id}";

        return {
            statusCode,
            body,
            headers
        };
};