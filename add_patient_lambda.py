import json
import boto3
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PatientsTable')  # Replace 'Patients' with your actual table name

def lambda_handler(event, context):
    try:
        # Parse the request body for patient details
        name = event['Name']
        age = event['Age']
        gender = event['Gender']
        illness = event['Illness']
        
        # Put the item into DynamoDB table
        table.put_item(
            Item={
                'Name': name,
                'Age': int(age),
                'Gender': gender,
                'Illness': illness
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Patient added successfully!')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding patient: {e.response['Error']['Message']}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
