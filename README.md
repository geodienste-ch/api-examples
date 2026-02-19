# geodienste.ch API Examples

This repository contains Python examples for using the geodienste.ch API.

## Installation

The following software is required to run the examples:

- Python 3.10
- [pipenv](https://pipenv.pypa.io)

To install the required python packages, run:

```bash
pipenv install
```

## Running Examples

```bash
pipenv run python 01_services_information.py
```

## Examples

### As User

|File|Description|User Account Required|
|---|---|---|
|01_services_information|How to get the latest update timestamps of forest-related services for Central Switzerland.|No|
|02_export_gpkg|How to get a Geopackage of forest reserves in the Canton of Jura.|Yes|

### As Provider/Delegate

|File|Description|User Account Required|
|---|---|---|
|03_import|How to upload and import data.|Yes|
|04_publish|How publish imported data.|Yes|
|05_import_uploaded|How to import datasets that have been uploaded by a delegate with only upload rights.|Yes|
|06_delete_dataset|How to delete datasets.|Yes|
|07_staging_export_gpkg|How to get a Geopackage from staging.|Yes|
|08_validation|How to validate data and how to see the result of a validation.|Yes|

## Notes

### Credentials

The examples use hard-coded usernames and credentials for simplicity. This approach should never be
used in production environments. Storing sensitive information directly in source code creates
serious security risks.

Instead, use alternatives such as:

- Environment variables
- A dedicated secrets manager
- Encrypted configuration files
- Secure credential storage provided by your hosting platform

### Polling

For simplicity, the example scripts block and wait until each job has completed. This approach
should not be used in production environments. Depending on the size and complexity of the data,
some jobs may take a significant amount of time to finish.

Instead of waiting synchronously for completion, implement a polling strategy. Submit the job,
return control to the application, and periodically check the job status until the result is
available.
