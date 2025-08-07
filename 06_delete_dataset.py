from requests import get, delete
from time import sleep

auth = ('user', 'pass')
server = 'https://geodienste.ch'

# Find out which datasets have been imported
response = get(
    url=f'{server}/data_agg/import_tasks/imported_datasets',
    auth=auth,
    params={
        'topic': 'leitungskataster_v2_0',
        'canton': 'OW',  # Note: only required for delegates
    }
)
response.raise_for_status()
datasets = [dataset['dataset'] for dataset in response.json()['imported_datasets']]
print('\n'.join(datasets))

# Delete these datasets
response = delete(
    url=f'{server}/data_agg/interlis/delete',
    auth=auth,
    params={
        'topic': 'leitungskataster_v2_0',
        'canton': 'OW',  # Note: only required for delegates,
        'datasets': ','.join(datasets),
        'publish': False,  # Note: set to true to automatically publish after successful deletion
    }
)
response.raise_for_status()
import_task_id = response.json()['import']['task_id']

# Wait until completed
while True:
    sleep(10)
    response = get(
        url=f'{server}/data_agg/import_tasks/{import_task_id}/status',
    )
    response.raise_for_status()
    if response.json()['import']['status'] != 'queued':
        break

# Print logs
response = get(
    url=f'{server}/data_agg/import_tasks/{import_task_id}/logs'
)
response.raise_for_status()
print(response.text)
