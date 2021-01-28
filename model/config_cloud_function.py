
from google.oauth2 import service_account
import os
import pandas_gbq
from google.cloud import secretmanager


WEBSCRAPE_DATA_PATH = os.path.abspath(os.path.join(os.getcwd(), 'data')) 

INGESTED_DATA = "gw_raw"
FEATURE_DATA = "features_df"
PREDICTIONS = "predictions"
PROJECT_ID = os.environ.get("PROJECT_ID")

secrets_client = secretmanager.SecretManagerServiceClient()
request = {"name": f"projects/{PROJECT_ID}/secrets/service-account-key-compute-engine-user2/versions/latest"}
response = secrets_client.access_secret_version(request)
secret_string = response.payload.data.decode("UTF-8")

# Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
pandas_gbq.context.credentials = secret_string

pandas_gbq.context.project = PROJECT_ID

          