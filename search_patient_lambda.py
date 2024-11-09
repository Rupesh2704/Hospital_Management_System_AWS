import json
import boto3
from boto3.dynamodb.conditions import Attr
import decimal  # Import the decimal module

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PatientsTable')  # Replace with your actual table name

def decimal_default(obj):
    """Helper function to handle Decimal serialization."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        # Safely get queryStringParameters or return an empty dict if none are provided
        query_params = event.get('queryStringParameters', {}) or {}

        # Extract 'name' and 'illness' safely
        name = query_params.get('name', None)
        illness = query_params.get('illness', None)

        # Start with an empty list for filter conditions
        filter_conditions = []

        # Add conditions based on the parameters provided
        if name:
            filter_conditions.append(Attr('Name').eq(name))  # Exact match for Name
        if illness:
            filter_conditions.append(Attr('Illness').eq(illness))  # Exact match for Illness

        # Check if we have any filters to apply
        if filter_conditions:
            # Combine the conditions with AND logic if both name and illness are provided
            combined_filter = filter_conditions[0]
            for condition in filter_conditions[1:]:
                combined_filter = combined_filter & condition

            # Perform the scan with the combined filter expression
            response = table.scan(FilterExpression=combined_filter)
        else:
            # No filters provided, return all items (optional)
            response = table.scan()

        # Retrieve the patients
        patients = response.get('Items', [])
        print(f"Retrieved patients: {patients}")

        # Ensure response is always valid JSON, even if no patients are found
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Add CORS headers if needed
            },
            'body': json.dumps(patients, default=decimal_default) if patients else json.dumps([])
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Add CORS headers if needed
            },
            'body': json.dumps({"message": f"Error retrieving patients: {str(e)}"})
        }
