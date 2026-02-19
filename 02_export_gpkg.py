"""
Get an Italian Geopackage of forest reserves in the Canton of Jura.

To access this data, you need to create an account at https://geodienste.ch/register.

Note: Some cantons require special permission to download certain datasets. These permissions must
be requested through the website. Once granted, the data can be downloaded using the API.
"""

from io import BytesIO
from os.path import basename
from requests import get, post
from shutil import copyfileobj
from time import sleep
from zipfile import ZipFile

auth = ('user', 'pass')  # IMPORTANT: Replace this your actual account credentials.

# Obtain a download token.
response = post(
    url='https://geodienste.ch/downloads/waldreservate/export',
    auth=auth,
    params={
        'format': 'gpkg',
        'cantons': ','.join([
            'JU',
        ]),
        'locale': 'it'
    },
    timeout=30
)
response.raise_for_status()
token = response.json()['token']

# Start the export
response = post(
    url=f'https://geodienste.ch/downloads/waldreservate/{token}/export',
    auth=auth,
    timeout=30
)
response.raise_for_status()

# Wait until completed
download_url = None
while not download_url:
    sleep(10)
    response = get(
        url=f'https://geodienste.ch/downloads/waldreservate/{token}/status.json',
        auth=auth,
        timeout=30
    )
    response.raise_for_status()
    download_url = response.json()['download_url']

# Download the zip and extract the gpkg
response = get(
    download_url,
    auth=auth,
    timeout=30
)
response.raise_for_status()
with ZipFile(BytesIO(response.content)) as file:
    for info in file.infolist():
        if info.filename.lower().endswith('.gpkg'):
            with file.open(info) as source, open(basename(info.filename), 'wb') as target:
                copyfileobj(source, target)
