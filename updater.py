import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print("Got IP", event["ip"])
    
    def update_route53_record(zone_id, record_name, new_ip):
    
        # Create a Route53 client
        client = boto3.client('route53')
    
        # Find the existing record
        response = client.list_resource_record_sets(
            HostedZoneId=zone_id,
            StartRecordName=record_name,
            EndRecordName=record_name
        )

        # Check if record exists
        if not response['ResourceRecordSets']:
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

    # Replace these with your specific values
    zone_id = "Z06020732IYL14L2ODTF5"
    record_name = "beacon.wyattmunson.com"

    update_route53_record(zone_id, record_name, event["ip"])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
