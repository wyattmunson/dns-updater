import boto3

def update_route53_record(zone_id, record_name, new_ip):
    print("[INFO] Updating Route53 record...")
    # Create a Route53 client
    client = boto3.client('route53')

    # Find the existing record
    response = client.list_resource_record_sets(
        HostedZoneId=zone_id,
        StartRecordName=record_name,
        StartRecordType="A"
    )

    # Check if record exists
    if not response['ResourceRecordSets']:
        print("[ERR] Failed to get ResourceRecordSets")
        raise Exception(f"Record '{record_name}' not found in zone '{zone_id}'")

    # Extract existing record details
    record_set = response['ResourceRecordSets'][0]
    current_ip = record_set['ResourceRecords'][0]['Value']

    # Check if update is necessary
    if current_ip == new_ip:
        print(f"Record '{record_name}' already points to {new_ip}. No update needed.")
        return

    # Prepare the change record
    change_batch = {
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'A',
                    'TTL': record_set['TTL'],
                    'ResourceRecords': [{'Value': new_ip}]
                }
            }
        ]
    }

    # Update the record
    client.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
    print(f"Record '{record_name}' successfully updated to point to {new_ip}.")

def lambda_handler(event, context):
    """
    Lambda handler function to update a Route53 A record with a new IP address.

    Args:
        event: The event passed to the Lambda function.
        context: The context of the Lambda function.

    Returns:
        A dictionary containing status code and message.
    """
    
    zone_id = "Z06020732IYL14L2ODTF5"
    record_name = "beacon.wyattmunson.com"

    try:
        # Get values from environment variables or event payload
        new_ip = event.get('ip')  # Assuming new IP is passed in the event payload
        print("[INFO] Updating IP address to:", new_ip)

        if not all([zone_id, record_name, new_ip]):
            raise ValueError("Missing required parameters for Route53 update.")

        update_route53_record(zone_id, record_name, new_ip)
        return {
            'statusCode': 200,
            'body': f"Record '{record_name}' updated successfully."
        }

    except Exception as e:
        print("[ERR] Error caught. See below:")
        print(e)
        return {
            'statusCode': 500,
            'body': f"Error updating Route53 record: {str(e)}"
        }

# lambda_handler({'ip':'10.0.0.1'}, None)