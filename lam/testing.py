import json
import boto3
import requests

# Define the Splunk HEC endpoint URL and token
SPLUNK_HEC_URL = 'https://<your-splunk-host>/services/collector/event'
SPLUNK_HEC_TOKEN = '<your-splunk-hec-token>'

def lambda_handler(event, context):
    # Get the CloudWatch log stream name and log events from the Lambda event
    log_group = event['logGroup']
    log_stream = event['logStream']
    log_events = event['logEvents']

    # Create a boto3 client for CloudWatch Logs
    cw_logs = boto3.client('logs')

    # Get the sequence token for the CloudWatch log stream
    response = cw_logs.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=log_stream)
    sequence_token = response['logStreams'][0]['uploadSequenceToken']

    # Create a list of Splunk HEC event objects from the CloudWatch log events
    splunk_events = []
    for log_event in log_events:
        splunk_event = {
            'time': log_event['timestamp'],
            'event': json.loads(log_event['message'])
        }
        splunk_events.append(splunk_event)

    # Send the Splunk events to the HEC endpoint
    headers = {
        'Authorization': 'Splunk ' + SPLUNK_HEC_TOKEN
    }
    response = requests.post(SPLUNK_HEC_URL, json=splunk_events, headers=headers, verify=False)
    response.raise_for_status()

    # Update the sequence token for the CloudWatch log stream
    cw_logs.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=log_events,
        sequenceToken=sequence_token
    )
