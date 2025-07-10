from io import BytesIO
from os.path import basename
from requests import get
from shutil import copyfileobj
from time import sleep
from zipfile import ZipFile

# Get data from staging as Geopackage.
auth = ('user', 'pass')

# Start the export
response = get(
    url='https://geodienste.ch/downloads/checkdb/waldreservate/export',
    auth=auth,
    params={
        'format': 'gpkg',
        'cantons': ','.join([
            'JU',
        ]),
        'locale': 'de'
    }
)
response.raise_for_status()
token = response.json()['token']

# Wait until completed
download_url = None
while not download_url:
    sleep(10)
    response = get(
        url=f'https://geodienste.ch/downloads/checkdb/waldreservate/{token}/status.json',
        auth=auth
    )
    response.raise_for_status()
    download_url = response.json()['download_url']

# Download the zip and extract the gpkg
response = get(
    download_url,
    auth=auth
)
response.raise_for_status()
with ZipFile(BytesIO(response.content)) as file:
    for info in file.infolist():
        if info.filename.lower().endswith('.gpkg'):
            with file.open(info) as source, open(basename(info.filename), 'wb') as target:
                copyfileobj(source, target)
