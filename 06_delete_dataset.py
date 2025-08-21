from requests import get, delete
from time import sleep

auth = ('user', 'pass')
server = 'https://geodienste.ch'
publish = False  # Note: set to true to automatically publish after successful deletion

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
        'publish': publish
    }
)
response.raise_for_status()
import_task_id = response.json()['import']['task_id']

# Wait delete until completed
while True:
    sleep(10)
    response = get(
        url=f'{server}/data_agg/import_tasks/{import_task_id}/status',
    )
    response.raise_for_status()
    if response.json()['import']['status'] != 'queued':
        break

# Print delete logs
response = get(
    url=f'{server}/data_agg/import_tasks/{import_task_id}/logs'
)
response.raise_for_status()
print(response.text)

# Wait until publish completed
if publish:
    publish_task_id = None
    while True:
        response = get(
            url=f'{server}/data_agg/import_tasks/{import_task_id}/status',
        )
        response.raise_for_status()
        response_json = response.json()
        publish_task_id = response_json['publish']['task_id']
        if publish_task_id and response_json['publish']['status'] != 'queued':
            break
        sleep(10)

    # Print publish logs
    response = get(
        url=f'{server}/data_agg/publish_tasks/{publish_task_id}/logs',
    )
    print(response.text)
