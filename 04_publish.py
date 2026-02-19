"""
Publish previously uploaded data
"""

from requests import get, post
from time import sleep

auth = ('user', 'pass')  # IMPORTANT: Replace this your actual account credentials.
server = 'https://geodienste.ch'

# Start publish task
response = post(
    f'{server}/data_agg/interlis/publish',
    auth=auth,
    params={
        'topic': 'leitungskataster_v2_0',
        'canton': 'OW',  # Note: only required for delegates
    },
    timeout=30
)
response.raise_for_status()
publish_task_id = response.json()['publish']['task_id']

# Wait until completed
download_url = None
while not download_url:
    sleep(10)
    response = get(
        url=f'{server}/data_agg/publish_tasks/{publish_task_id}/status',
        timeout=30
    )
    response.raise_for_status()
    if response.json()['publish']['status'] != 'queued':
        break

# Print publish logs
response = get(
    url=f'{server}/data_agg/publish_tasks/{publish_task_id}/logs',
    timeout=30
)
response.raise_for_status()
print(response.text)
