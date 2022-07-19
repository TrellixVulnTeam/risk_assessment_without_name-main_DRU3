"""Food Data Central API"""

import requests
import pandas as pd

API_KEY = "ng2xHA4cj15ZfKlpDDHiGkZFeX9L56AlaM59Z7Oz"
PAYLOAD = {}
HEADERS = {'Cookie': 'ApplicationGatewayAffinity=4469cb314e6a2b22e48fcf12d9ef45ba; ApplicationGatewayAffinityCORS=4469cb314e6a2b22e48fcf12d9ef45ba'}


def call_api(company_name):
    URL = f"https://api.nal.usda.gov/fdc/v1/foods/search?brandOwner={company_name}&api_key={API_KEY}"

    response = requests.request("GET", URL , headers= HEADERS, data= PAYLOAD)

    return pd.DataFrame(response.json()["foods"])
    
