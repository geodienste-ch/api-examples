from io import BytesIO
from requests import get, post
from zipfile import ZipFile

# Validate staging data as a delegate with validation rights
auth = ('user', 'pass')

# Start the validation by setting the status to in_validation
response = post(
    url='https://geodienste.ch/data_agg/validation',
    auth=auth,
    params={
        'base_topic': 'planungszonen',
        'canton': 'SH',
        'status': 'in_validation',
        'message': 'starting valdiation now'
    }
)
response.raise_for_status()

# Validate the data, see for example 07_staging_export_gpkg how to get the data

# Document some errors, this can either be a zipped CSV and/or a Geopackage
zipped_csv = BytesIO()
with ZipFile(zipped_csv, 'w') as file:
    file.writestr(
        'errors.csv',
        (
            # Note: there is no predefined structure for the CSV
            'layer,error\n'
            'xy,some error\n'
        )
    )
zipped_csv.seek(0)

# Finish the validation by setting the status to completed or completed_with_errors
response = post(
    url='https://geodienste.ch/data_agg/validation',
    auth=auth,
    params={
        'base_topic': 'planungszonen',
        'canton': 'SH',
        'status': 'completed_with_errors',
        'message': 'there are some errors in the data'
    },
    files={
        'csv_file': zipped_csv
        # Note: you could also upload a zip with a Geopackage (gpkg_file)
    }
)
response.raise_for_status()

# Get the results of the validation as delegate with import rights or provider
auth = ('user', 'pass')

response = get(
    url='https://geodienste.ch/data_agg/validation/status',
    auth=auth,
    params={
        'base_topic': 'planungszonen',
        'canton': 'SH',
    }
)
response.raise_for_status()
print(response.json()['message'])

csv_url = response.json()['csv']
response = get(
    csv_url,
    auth=auth
)
response.raise_for_status()
with ZipFile(BytesIO(response.content)) as file:
    for info in file.infolist():
        with file.open(info, 'r') as file:
            print(file.read().decode())
