from requests import get
from tabulate import tabulate

# Get information about forest-related services for Central Switzerland
response = get(
    url='https://geodienste.ch/info/services.json',
    params={
        'base_topics': ','.join([
            'waldreservate',
            'npl_waldgrenzen',
            'npl_waldabstandslinien',
            'wildruhezonen',
            'holznutzungsbewilligung',
            'rodungen_und_rodungsersatz',
            'waldreservate'
        ]),
        'cantons': ','.join([
            'LU',
            'UR',
            'SZ',
            'OW',
            'NW',
            'ZG'
        ]),
        'language': 'de'
    }
)
response.raise_for_status()

# Print publication state and update date, sorted by topic and canton
services = response.json()['services']
services.sort(key=lambda service: (service['base_topic'], service['canton']))
table = [
    [service['canton'], service['publication_data'], service['updated_at'], service['topic']]
    for service in services
]
print(tabulate(table, headers=["Canton", "Publication Date", "Updated At", "Topic"], tablefmt="github"))
