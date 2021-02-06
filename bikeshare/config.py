from os import environ
# Google BigQuery config
# gcp_project = environ.get(‘project_id’)
gcp_project = "bikeshare-303620"
bigquery_dataset = "TripsDataset"
bigquery_uri = f'bigquery://{gcp_project}/{bigquery_dataset}'