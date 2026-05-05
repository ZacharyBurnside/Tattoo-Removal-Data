import requests
import pandas as pd

records = []

for year in range(2010, 2024):
    # API used different NAICS param names depending on year
    if year >= 2017:
        naics_param = "NAICS2017"
    elif year >= 2012:
        naics_param = "NAICS2012"
    else:
        naics_param = "NAICS2007"

    url = f"https://api.census.gov/data/{year}/cbp"
    params = {
        "get": f"ESTAB,EMP,PAYANN,{naics_param}_LABEL",
        "for": "us:*",
        naics_param: "812199"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        row = data[1]
        records.append({
            "year":       year,
            "estab":      int(row[0]),
            "employment": int(row[1]),
            "payroll":    int(row[2]),
            "industry":   row[3]
        })
        print(f"  {year}: {row[0]} establishments")
    except Exception as e:
        print(f"  {year}: {e}")

df_cbp = pd.DataFrame(records)
df_cbp