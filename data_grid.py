# %%
import datetime

import numpy as np
import pandas as pd

# %%
DATE_FROM = datetime.date(2020, 1, 1)
DATE_TO = datetime.date(2020, 3, 31)
# %%
dates_range = pd.DataFrame({"date": pd.date_range(DATE_FROM, DATE_TO)})
dates_range["key"] = 1

hours_range = pd.DataFrame({"hour": [i for i in range(0, 24)]})
hours_range["key"] = 1

date_hour_grid = pd.merge(dates_range, hours_range, on="key").drop("key", 1)
# %%
date_hour_grid["month"] = date_hour_grid["date"].dt.month
# %%
heating_up_details = pd.read_csv("e.csv", sep=";")

# %%
expected_temperatures = pd.read_csv("f.csv", sep=";").drop(5)
expected_temperatures["Oczekiwana temperatura"].iloc[4] = 12
hours = expected_temperatures["Godziny"].str.split(pat="-", expand=True)
hours["hour_from"] = hours[0].str.split(":").str[0].astype(int)
hours["hour_to"] = hours[1].str.split(":").str[0].astype(int)
expected_temperatures = pd.concat([expected_temperatures, hours], axis=1)
expected_temperatures["hour_range"] = expected_temperatures.apply(
    lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1
)
expected_temperatures = expected_temperatures.explode("hour_range")
expected_temperatures = expected_temperatures[["Dzien", "Oczekiwana temperatura", "hour_range"]]

# %%
photovoltaics_details = pd.read_csv("h.csv", sep=";").iloc[:, 0:4]
photovoltaics_details = photovoltaics_details[~photovoltaics_details["godziny"].isnull()]
photovoltaics_details["miesi<ice"] = photovoltaics_details["miesi<ice"].str.split(",")
photovoltaics_details["godziny"] = photovoltaics_details["godziny"].str.split(",")
photovoltaics_details = photovoltaics_details.explode("godziny")

hours = photovoltaics_details["godziny"].str.split("-", expand=True)
hours["midnight_0"] = "23:00"
hours["midnight_1"] = "00:00"

hours["first"] = hours[0] + "-" + hours["midnight_0"]
hours["second"] = hours["midnight_1"] + "-" + hours[1]
hours["godziny"] = hours["first"] + "," + hours["second"]

hours_1 = hours["first"].str.split(pat="-", expand=True)
hours_1["hour_from"] = hours_1[0].str.split(":").str[0].astype(int)
hours_1["hour_to"] = hours_1[1].str.split(":").str[0].astype(int)
hours_1["hour_range_1"] = hours_1.apply(lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1)
hours_1 = hours_1["hour_range_1"]

hours_2 = hours["first"].str.split(pat="-", expand=True)
hours_2["hour_from"] = hours_2[0].str.split(":").str[0].astype(int)
hours_2["hour_to"] = hours_2[1].str.split(":").str[0].astype(int)
hours_2["hour_range_2"] = hours_2.apply(lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1)
hours_2 = hours_2["hour_range_2"]


photovoltaics_details = pd.concat(
    [photovoltaics_details.drop("godziny", axis=1), hours_1, hours_2], axis=1
)
photovoltaics_details["hour_range"] = (
    photovoltaics_details["hour_range_1"] + photovoltaics_details["hour_range_2"]
)
photovoltaics_details = photovoltaics_details.explode("miesi<ice")
photovoltaics_details = photovoltaics_details.explode("hour_range").drop(
    ["hour_range_1", "hour_range_2"], axis=1
)

map_months = {
    "l": 1,
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
}

photovoltaics_details["miesiace"] = photovoltaics_details["miesi<ice"].map(map_months)
photovoltaics_details = photovoltaics_details.drop("miesi<ice", axis=1)

# %%
devices_power_details = pd.read_csv("j.csv", sep=";")[
    ["Dzien", "Godziny", "Srednia moc pobierana"]
]
hours = devices_power_details["Godziny"].str.split(pat="-", expand=True)
hours["hour_from"] = hours[0].str.split(":").str[0].astype(int)
hours["hour_to"] = hours[1].str.split(":").str[0].astype(int)
devices_power_details = pd.concat([devices_power_details, hours], axis=1)
devices_power_details["hour_range"] = devices_power_details.apply(
    lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1
)
devices_power_details = devices_power_details.explode("hour_range")
expected_temperatures = expected_temperatures[["Dzien", "hour_range", "Srednia moc pobierana"]]

# %%
pd.read_csv("k.csv", sep=";")
