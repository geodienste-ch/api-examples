"""
Upload and import local data to geodienste.
"""

from requests import get, post
from time import sleep

auth = ('user', 'pass')  # IMPORTANT: Replace this your actual account credentials.
filepath = '/path/to/lv95.zip'
server = 'https://geodienste.ch'
publish = False  # Note: set to true to automatically publish after successful import

# Upload data and start import task
with open(filepath, 'rb') as file:
    response = post(
        f'{server}/data_agg/interlis/import',
        auth=auth,
        params={
            'topic': 'leitungskataster_v2_0',
            'canton': 'OW',  # Note: only required for delegates
            'replace_all': False,
            'force_import': False,
            'extract': False,  # Note: only for leitungskataster_v2_0
            'publish': publish,
        },
        files={
            'lv95_file': file
        },
        timeout=30
    )
response.raise_for_status()
import_task_id = response.json()['import']['task_id']

# Wait until import completed
while True:
    sleep(10)
    response = get(
        url=f'{server}/data_agg/import_tasks/{import_task_id}/status',
        timeout=30
    )
    response.raise_for_status()
    if response.json()['import']['status'] != 'queued':
        break

# Print import logs
response = get(
    url=f'{server}/data_agg/import_tasks/{import_task_id}/logs',
    timeout=30
)
response.raise_for_status()
print(response.text)

# Wait until publish completed
if publish:
    publish_task_id = None
    while True:
        response = get(
            url=f'{server}/data_agg/import_tasks/{import_task_id}/status',
            timeout=30
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
        timeout=30
    )
    print(response.text)
