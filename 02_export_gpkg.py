from io import BytesIO
from os.path import basename
from requests import get, post
from shutil import copyfileobj
from time import sleep
from zipfile import ZipFile

# Get an Italian Geopackage of forest reserves in the Canton of Jura.
# To do this, an account is needed, which you can be createt at https://geodienste.ch/register.
# Note also that some cantons require permission to download certain data. These permissions can
# only be requested via the website. Once permissions are granted, downloading using the API will
# be possbile.
auth=('user', 'pass')

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
    }
)
response.raise_for_status()
token = response.json()['token']

# Start the export
response = get(
    url=f'https://geodienste.ch/downloads/waldreservate/{token}/export.json',
    auth=auth
)
response.raise_for_status()

# Wait until completed
download_url = None
while not download_url:
    sleep(10)
    response = get(
        url=f'https://geodienste.ch/downloads/waldreservate/{token}/status.json',
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
