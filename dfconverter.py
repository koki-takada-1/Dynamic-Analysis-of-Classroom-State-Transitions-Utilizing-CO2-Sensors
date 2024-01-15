import numpy as np
import datetime
import pandas as pd

def converter(df):
    room = {
        "374": {
            "Monday": {"1": 0, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0},
            "Tuesday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Wednesday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Thursday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Friday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
        },
        "361": {
            "Monday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Tuesday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Wednesday": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
            "Thursday": {"1": 1, "2": 1, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
            "Friday": {"1": 1, "2": 1, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
        },
        "277": {
            "Monday": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
            "Tuesday": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
            "Wednesday": {"1": 0.3, "2": 0.3, "3": 0.3, "4": 0.3, "5": 0.3, "6": 0, "7": 0},
            "Thursday": {"1": 0, "2": 0, "3": 1, "4": 1, "5": 1, "6": 0, "7": 0},
            "Friday": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
        },
        "311": {
            "Monday": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
            "Tuesday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Wednesday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
            "Thursday": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0},
            "Friday": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 0, "6": 0, "7": 0},
        }
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
    classroom_seats = {
    "371": 56,
    "373": 52,
    "374": 56,
    "376": 52,
    "361": 56,
    "363": 56,
    "364": 50,
    "351": 102,
    "353": 46,
    "354": 53,
    "341": 55,
    "342": 55,
    "345": 55,
    "311": 183,
    "313": 80,
    "291": None,  # 座席数が提供されていない場合、Noneとしておきます
    "277": 80,
    "251": 3,
    "257": 80,
    }

    df["_measurement"] = df["_measurement"].astype(str)
    df = df.drop(columns=["Unnamed: 0"])
    df["_time"] = pd.to_datetime(df["_time"]).dt.tz_convert("Asia/Tokyo")
    df["day_name"] = df["_time"].dt.day_name()

    # df["seat_num"] = classroom_seats[id_to_num[df["_measurement"][0]]]
    df["y"] = None

    for i in range(len(df)):
        # 土日はいらない
        if df["day_name"][i] == "Saturday" or df["day_name"][i] == "Sunday":
            df["y"][i] = np.nan
            continue
        # オフセット情報を持たない日付時刻を作成する
        if df["_time"][i].tzinfo is not None:
            df["_time"][i] = df["_time"][i].replace(tzinfo=None)
        year = df["_time"][i].year
        month = df["_time"][i].month
        day = df["_time"][i].day
        if df["_time"][i] >= datetime.datetime(year, month, day, 9, 15) and df["_time"][
            i
        ] <= datetime.datetime(year, month, day, 10, 45):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "1"
            ]  # 1限
        # -----------------------------------------------休み時間-------------------------------------------------------
        elif df["_time"][i] > datetime.datetime(year, month, day, 10, 45) and df[
            "_time"
        ][i] < datetime.datetime(year, month, day, 10, 55):
            if i != 0 and (
                df["y"][i - 1] == 1
                or df["y"][i - 1] == 0.5
                or df["y"][i - 1] == 0.7
            ):
                df["y"][i] = 0.7
            else:
                df["y"][i] = 0
        # ------------------------------------------------------------------------------------------------------------

        elif df["_time"][i] >= datetime.datetime(year, month, day, 10, 55) and df[
            "_time"
        ][i] <= datetime.datetime(year, month, day, 12, 25):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "2"
            ]  # ２限

        # -----------------------------------------------休み時間-------------------------------------------------------

        elif df["_time"][i] > datetime.datetime(year, month, day, 12, 25) and df[
            "_time"
        ][i] < datetime.datetime(year, month, day, 13, 10):
            if i != 0 and (
                df["y"][i - 1] == 1
                or df["y"][i - 1] == 0.5
                or df["y"][i - 1] == 0.3
            ):  # 前の時間教室を使っていたとしたら
                df["y"][i] = 0.3
            else:
                df["y"][i] = 0
        # ------------------------------------------------------------------------------------------------------------
        elif df["_time"][i] >= datetime.datetime(year, month, day, 13, 10) and df[
            "_time"
        ][i] <= datetime.datetime(year, month, day, 14, 40):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "3"
            ]  # 3限
        # -----------------------------------------------休み時間-------------------------------------------------------
        elif df["_time"][i] > datetime.datetime(year, month, day, 14, 40) and df[
            "_time"
        ][i] < datetime.datetime(year, month, day, 14, 50):
            if i != 0 and (
                df["y"][i - 1] == 1
                or df["y"][i - 1] == 0.5
                or df["y"][i - 1] == 0.7
            ):
                df["y"][i] = 0.7
            else:
                df["y"][i] = 0
        # ------------------------------------------------------------------------------------------------------------
        elif df["_time"][i] >= datetime.datetime(year, month, day, 14, 50) and df[
            "_time"
        ][i] <= datetime.datetime(year, month, day, 16, 20):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "4"
            ]  # 4限
        # -----------------------------------------------休み時間-------------------------------------------------------
        elif df["_time"][i] > datetime.datetime(year, month, day, 16, 20) and df[
            "_time"
        ][i] < datetime.datetime(year, month, day, 16, 30):
            if i != 0 and (
                df["y"][i - 1] == 1
                or df["y"][i - 1] == 0.5
                or df["y"][i - 1] == 0.7
            ):
                df["y"][i] = 0.7
            else:
                df["y"][i] = 0
        # -------------------------------------------------------------------------------------------------------------
        elif df["_time"][i] >= datetime.datetime(year, month, day, 16, 30) and df[
            "_time"
        ][i] <= datetime.datetime(year, month, day, 18, 00):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "5"
            ]  # 5限
        # -----------------------------------------------休み時間-------------------------------------------------------
        elif df["_time"][i] > datetime.datetime(year, month, day, 18, 00) and df[
            "_time"
        ][i] < datetime.datetime(year, month, day, 18, 10):
            if i != 0 and (
                df["y"][i - 1] == 1
                or df["y"][i - 1] == 0.5
                or df["y"][i - 1] == 0.7
            ):
                df["y"][i] = 0.7
            else:
                df["y"][i] = 0
        # -------------------------------------------------------------------------------------------------------------
        elif df["_time"][i] >= datetime.datetime(year, month, day, 18, 10) and df[
            "_time"
        ][i] <= datetime.datetime(year, month, day, 19, 40):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "6"
            ]  # 6限
        # -----------------------------------------------休み時間-------------------------------------------------------
        elif df["_time"][i] > datetime.datetime(year, month, day, 19, 40) and df[
            "_time"
        ][i] < datetime.datetime(year, month, day, 19, 50):
            if i != 0 and (
                df["y"][i - 1] == 1
                or df["y"][i - 1] == 0.5
                or df["y"][i - 1] == 0.7
            ):
                df["y"][i] = 0.7
            else:
                df["y"][i] = 0
        # -------------------------------------------------------------------------------------------------------------
        elif df["_time"][i] >= datetime.datetime(year, month, day, 19, 50) and df[
            "_time"
        ][i] <= datetime.datetime(year, month, day, 21, 20):
            df["y"][i] = room[id_to_num[df["_measurement"][i]]][
                df["day_name"][i]
            ][
                "7"
            ]  # 7限

        else:
            df["y"][i] = np.nan

    df = df.dropna(subset=["y"])
    df = df.drop(columns=["_measurement"])
    return df
