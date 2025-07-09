from requests import get, post
from time import sleep

auth = ('user', 'pass')

# Find out which datasets have been uploaded by a delegate with only upload rights
response = get(
    url='https://geodienste.ch/data_agg/import_tasks/uploaded_datasets',
    auth=auth,
    params={
        'topic': 'leitungskataster_v2_0',
        'canton': 'OW',  # Note: only required for delegates
    }
)
response.raise_for_status()
datasets = [dataset['dataset'] for dataset in response.json()['uploaded_datasets']]
print('\n'.join(datasets))

# Import these datasets
response = post(
    url='https://geodienste.ch/data_agg/import_tasks/import_uploaded',
    auth=auth,
    params={
        'topic': 'leitungskataster_v2_0',
        'canton': 'OW',  # Note: only required for delegates,
        'datasets': ','.join(datasets),
        'publish': False,  # Note: set to true to automatically publish after successful import
    }
)
response.raise_for_status()
import_task_id = response.json()['import']['task_id']

# Wait until completed
while True:
    sleep(10)
    response = get(
        url=f'https://geodienste.ch/data_agg/import_tasks/{import_task_id}/status',
    )
    response.raise_for_status()
    if response.json()['import']['status'] != 'queued':
        break

# Print import logs
response = get(
    url=f'https://geodienste.ch/data_agg/import_tasks/{import_task_id}/logs'
)
response.raise_for_status()
print(response.text)
