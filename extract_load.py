import os
import json
import requests
import pandas as pd
from google.oauth2 import service_account
def run_pipeline():
    #Fetch Weather Data
    print("Fetching data from Open-Meteo API.....")
    url="https://api.open-meteo.com/v1/forecast?latitude=22.57&longitude=88.36&current_weather=true"
    response=requests.get(url).json()
    current_wether = response["current_weather"]

    #Convert to DataFrame

    data={
        "fetched_at": [pd.Timestamp.now(tz='UTC')],
        "readings": [current_wether["time"]],
        "temperature": [float(current_wether["temperature"])],
        "windspeed": [float(current_wether["windspeed"])],
        "wethercode": [int(current_wether["weathercode"])],
    }
    df = pd.DataFrame(data)
    print ("Data fetched successfully.....")
    print(df)

    #Authenticate with Google Cloud
    print("Authenticating with Google Cloud.....")
    gcp_key_json= os.environ.get("GCP_SA_KEY")
    if not gcp_key_json:
        raise ValueError("GCP_SA_KEY environment variable not set.")
    info=json.loads(gcp_key_json)
    credentials=service_account.Credentials.from_service_account_info(info)

    #Load Data into BigQuery
    print("Loading data into BigQuery.....")
    df.to_gbq(  
                destination_table="weather_raw.current_conditions",
                project_id=info["project_id"],
                if_exists="append",
                credentials=credentials
            )

    print("Pipline executed successfully. Data loaded into BigQuery successfully.....")

if __name__ == "__main__":
    run_pipeline()