from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
import pandas as pd


num_to_id = {
    "371": "08B7",
    "374": "E4B4",
    "364": "807A",
    "361": "6882",
    "351": "F089",
    "354": "28B5",
    "251": "AC7A",
    "353": "8880",
    "257": "34BA",
    "277": "9CBA",
    "271": "347A",
    "313": "9020",
    "341": "D8B9",
    "342": "BCB3",
    "345": "84EC",
    "311": "1CEE",
    "252": "A0C4",
    "274": "1CF8"
}

id_to_num = {
    "08B7": "371",
    "E4B4": "374",
    "807A": "364",
    "6882": "361",
    "F089": "351",
    "28B5": "354",
    "AC7A": "251",
    "8880": "353",
    "34BA": "257",
    "9CBA": "277",
    "347A": "271",
    "9020": "313",
    "D8B9": "341",
    "BCB3": "342",
    "84EC": "345",
    "1CEE": "311",
    "A0C4": "252",
    "1CF8": "274"
}


url = "http://10.205.101.24:8086"
org = "iput"
bucket = "m5kkiput"
token = "qiHps8hYrRmYi2xDvjY_J-9SITntEE8qPeZjP504eSfJwajREbIaqZZHGe1TZJo2jJUK4vbohz6h74mfh1AuiQ=="

infclient = InfluxDBClient(url=url, token=token, org=org, timeout=30000)
query_api = infclient.query_api()

# query = 'from(bucket:"m5kkiput") |> range(start:-8d, stop:-0m) |> filter(fn: (r) => r["_measurement"] =~ /' + '|'.join(num_to_id.values()) + '/) |> pivot(rowKey:["_time", "_measurement"], columnKey: ["_field"], valueColumn: "_value") |> keep(columns: ["_time", "_measurement", "co2", "humidity", "temperature"])'
# df = query_api.query_data_frame(query)
# for num, id in num_to_id.items():
#     df_id = df[df['_measurement'] == id]
#     df_id = df_id.drop(columns=['result', 'table'])
#     df_id.to_csv(f"{num}data.csv", encoding='utf-8-sig')
df = query_api.query_data_frame('''
    from(bucket:"m5kkiput")
        |> range(start:-3h, stop:-0m)
        |> filter(fn: (r) => r["_measurement"] == "08B7")
        |> pivot(rowKey:["_time", "_measurement"], columnKey: ["_field"], valueColumn: "_value")
        |> keep(columns: ["_time", "_measurement", "co2", "humidity", "temperature"])
    ''')

df2 = df.drop(columns=['result', 'table'])

print(df2.to_string())
df2.to_csv("2024-0110-371data.csv", encoding='utf-8-sig')
