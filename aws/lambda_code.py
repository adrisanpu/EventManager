import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Events')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to int or float
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):
    # Extract the HTTP method from the event object (Version 2.0)
    http_method = event['requestContext']['http']['method']
    
    if http_method == 'GET':
        params = event.get('queryStringParameters')
        if params and 'id' in params:
            # Retrieve a specific event by ID
            event_id = int(params['id'])
            try:
                response = table.get_item(Key={'id': event_id})
                if 'Item' in response:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(response['Item'], cls=DecimalEncoder)
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps('Event not found')
                    }
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps('Error retrieving event: ' + e.response['Error']['Message'])
                }
        else:
            # Retrieve all events
            try:
                response = table.scan()
                events = response.get('Items', [])
                return {
                    'statusCode': 200,
                    'body': json.dumps(events, cls=DecimalEncoder)
                }
            except ClientError as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps('Error scanning events: ' + e.response['Error']['Message'])
                }

    elif http_method == 'POST':
        try:
            event_data = json.loads(event['body'])
            
            # Validate that the required data is present
            required_fields = ['id', 'name', 'date', 'location', 'thumbnail_url']
            if not all(field in event_data for field in required_fields):
                return {
                    'statusCode': 400,
                    'body': json.dumps('Missing required event data fields.')
                }
            
            # Insert the event into DynamoDB
            response = table.put_item(Item=event_data)
            return {
                'statusCode': 200,
                'body': json.dumps('Event inserted successfully!')
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps('Error inserting event: ' + e.response['Error']['Message'])
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid input: ' + str(e))
            }

    elif http_method == 'DELETE':
        # Handle DELETE request
        try:
            params = event.get('queryStringParameters')
            if params and 'id' in params:
                event_id = int(params['id'])

                # Delete the event from DynamoDB
                response = table.delete_item(
                    Key={'id': event_id},
                    ConditionExpression="attribute_exists(id)"
                )

                return {
                    'statusCode': 200,
                    'body': json.dumps('Event deleted successfully!')
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps('Missing id parameter.')
                }
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return {
                    'statusCode': 404,
                    'body': json.dumps('Event not found.')
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps('Error deleting event: ' + e.response['Error']['Message'])
                }
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid input: ' + str(e))
            }

    elif http_method == 'PUT':
        try:
            # Parse and validate input
            event_data = json.loads(event['body'])
            if not event_data.get('id'):
                return {
                    'statusCode': 400,
                    'body': json.dumps('Missing required id field.')
                }

            event_id = int(event_data['id'])

            # Prepare update expression
            update_expression = 'SET '
            expression_attribute_values = {}
            expression_attribute_names = {}

            for key, value in event_data.items():
                if key != 'id':
                    update_expression += f"#{key} = :{key}, "
                    expression_attribute_names[f"#{key}"] = key
                    expression_attribute_values[f":{key}"] = value

            update_expression = update_expression.rstrip(', ')

            # Perform update
            response = table.update_item(
                Key={'id': event_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression="attribute_exists(id)",
                ReturnValues='ALL_NEW'
            )

            updated_attributes = response.get('Attributes')
            if not updated_attributes:
                return {
                    'statusCode': 500,
                    'body': json.dumps('Update failed. No attributes returned.')
                }

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Event updated successfully!',
                    'updatedAttributes': updated_attributes
                }, cls=DecimalEncoder)
            }

        except ClientError as e:
            error_message = e.response['Error']['Message']
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return {
                    'statusCode': 404,
                    'body': json.dumps('Event not found.')
                }
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error updating event: {error_message}')
            }

        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Invalid input: {str(e)}')
            }


    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method not allowed')
        }
