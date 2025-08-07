from requests import get, post
from time import sleep

auth = ('user', 'pass')
filepath = '/path/to/lv95.zip'
server = 'https://geodienste.ch'

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
            'publish': False,  # Note: set to true to automatically publish after successful import
        },
        files={
            'lv95_file': file
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

# Print import logs
response = get(
    url=f'{server}/data_agg/import_tasks/{import_task_id}/logs'
)
response.raise_for_status()
print(response.text)
