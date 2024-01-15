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

# InfluxDBサーバーのIPアドレスとポート
url = "http://10.205.101.24:8086"
# 対象organization
org = "iput"
# 対象bucket
bucket = "m5kkiput"
# 発行したToken
token = "qiHps8hYrRmYi2xDvjY_J-9SITntEE8qPeZjP504eSfJwajREbIaqZZHGe1TZJo2jJUK4vbohz6h74mfh1AuiQ=="

room = ['277','311','361','374','364']
###########################################
for  i in range(len(room)):
    infclient = InfluxDBClient(url=url, token=token, org=org,timeout=3000)

    query_api = infclient.query_api()

    # rangeで時刻範囲を指定する。サンプルでは過去10分間
    # start, endの時刻は、例えば 2023-04-01T09:00:00+09:00 みたいな形式でも指定可能
    # filterでセンサID(_measurement)を指定する。サンプルでは08B7 (371教室)
    # 時間平均をとる場合は、aggregateWindowの行を追加してください。サンプルでは1分毎の平均です。
    #   |> aggregateWindow(every: 1m, fn: mean)
    df = query_api.query_data_frame(f'''
        from(bucket:"m5kkiput")
            |> range(start:-90m, stop:-0m)
            |> filter(fn: (r) => r["_measurement"] == "08B7")
            |> pivot(rowKey:["_time", "_measurement"], columnKey: ["_field"], valueColumn: "_value")
            |> keep(columns: ["_time", "_measurement", "co2", "humidity", "temperature"])
        ''')

    df2 = df.drop(columns = ['result', 'table'])

    print(df2.to_string())

    # CSV出力の場合はこちら。
    print(df2.to_csv(f'20240110-371.csv'))
