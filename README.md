# geodienste.ch API Examples

This repository contains Python examples for using the geodienste.ch API.

## Installation

The installation described here requires [pipenv](https://pipenv.pypa.io).

```bash
pipenv install
```

## Running Examples

```
pipenv run python 01_services_information.py
```

## Examples

### As User

|File|Description|
|---|---|
|01_services_information|How to get the latest update timestamps of forest-related services for Central Switzerland.|
|02_export_gpkg|How to get a Geopackage of forest reserves in the Canton of Jura.|

### As Provider/Delegate

|File|Description|
|---|---|
|03_import|How to upload and import data.|
|04_publish|How publish imported data.|
|05_import_uploaded|How to import datasets that have been uploaded by a delegate with only upload rights.|
|06_delete_dataset|How to delete datasets.|
|07_staging_export_gpkg|How to get a Geopackage from staging.|
|08_validation|How to validate data and how to see the result of a validation.|
