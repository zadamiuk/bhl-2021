# %%
import datetime

import numpy as np
import pandas as pd

# %%
DATE_FROM = datetime.date(2016, 3, 1)
DATE_TO = datetime.date(2016, 3, 31)
# %%
dates_range = pd.DataFrame({"date": pd.date_range(DATE_FROM, DATE_TO)})
dates_range["key"] = 1

hours_range = pd.DataFrame({"hour": [i for i in range(0, 24)]})
hours_range["key"] = 1

date_hour_grid = pd.merge(dates_range, hours_range, on="key").drop("key", 1)
date_hour_grid["month"] = date_hour_grid["date"].dt.month
date_hour_grid["weekday"] = date_hour_grid["date"].dt.weekday

map_weekday = {
    1: "Dni robocze",
    2: "Dni robocze",
    3: "Dni robocze",
    4: "Dni robocze",
    5: "Dni robocze",
    6: "Dni wolne od pracy",
    7: "Dni wolne od pracy",
}

date_hour_grid["weekday"] = date_hour_grid["weekday"].map(map_weekday)
# %%
heating_up_details = pd.read_csv("data/raw/e.csv", sep=";")
map_heating = {
    ">20°C": "20:100",
    "15°C-20°C": "15:20",
    "5°C-15°C": "5:15",
    "0°C-5°C": "0:5",
    "-5°C-0°C": "-5:0",
    "-10°C--5°C": "-10:-5",
    "-20°C--10°C": "-20:-5",
    "<-20°C": "-100:-20",
}
heating_up_details["Temperatura na zewnatrz"] = heating_up_details["Temperatura na zewnatrz"].map(
    map_heating
)
heating_up_details["low_temp"] = (
    heating_up_details["Temperatura na zewnatrz"].str.split(":").str[0].astype(int)
)
heating_up_details["upper_temp"] = (
    heating_up_details["Temperatura na zewnatrz"].str.split(":").str[1].astype(int)
)
# %%
expected_temperatures = pd.read_csv("data/raw/f.csv", sep=";").drop(5)
expected_temperatures["Oczekiwana temperatura"].iloc[4] = 12
hours = expected_temperatures["Godziny"].str.split(pat="-", expand=True)
hours["hour_from"] = hours[0].str.split(":").str[0].str.strip().astype(int)
hours["hour_to"] = hours[1].str.split(":").str[0].str.strip().astype(int)
expected_temperatures = pd.concat([expected_temperatures, hours], axis=1)
expected_temperatures["hour_range"] = expected_temperatures.apply(
    lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1
)
expected_temperatures = expected_temperatures.explode("hour_range")
expected_temperatures = expected_temperatures[["Dzien", "Oczekiwana temperatura", "hour_range"]]

expected_temperatures = expected_temperatures.drop_duplicates()

# %%
photovoltaics_details = pd.read_csv("data/raw/h.csv", sep=";").iloc[:, 0:4]
photovoltaics_details = photovoltaics_details[~photovoltaics_details["godziny"].isnull()]
photovoltaics_details["miesi<ice"] = photovoltaics_details["miesi<ice"].str.strip().str.split(",")
photovoltaics_details["godziny"] = photovoltaics_details["godziny"].str.strip().str.split(",")
photovoltaics_details = photovoltaics_details.explode("godziny")


hours = photovoltaics_details["godziny"].str.split("-", expand=True)

hours["midnight_0"] = "24:00"
hours["midnight_1"] = "00:00"

hours.loc[
    hours[0].str.split(":").str[0].astype(int) < hours[1].str.split(":").str[0].astype(int),
    "midnight_0",
] = hours[1][
    hours[0].str.split(":").str[0].astype(int) < hours[1].str.split(":").str[0].astype(int)
]

hours["first"] = hours[0] + "-" + hours["midnight_0"]
hours["second"] = hours["midnight_1"] + "-" + hours[1]
hours["godziny"] = hours["first"] + "," + hours["second"]

hours_1 = hours["first"].str.split(pat="-", expand=True)
hours_1["hour_from"] = hours_1[0].str.split(":").str[0].str.strip().astype(int)
hours_1["hour_to"] = hours_1[1].str.split(":").str[0].str.strip().astype(int) - 1
hours_1["hour_range_1"] = hours_1.apply(lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1)
hours_1 = hours_1["hour_range_1"]

hours_2 = hours["second"].str.split(pat="-", expand=True)
hours_2["hour_from"] = hours_2[0].str.split(":").str[0].str.strip().astype(int)
hours_2["hour_to"] = hours_2[1].str.split(":").str[0].str.strip().astype(int) - 1
hours_2["hour_range_2"] = hours_2.apply(lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1)
hours_2.loc[
    hours[0].str.split(":").str[0].astype(int) < hours[1].str.split(":").str[0].astype(int),
    "hour_range_2",
] = None
hours_2["hour_range_2"] = hours_2["hour_range_2"].apply(lambda d: d if isinstance(d, list) else [])
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
    "Ill": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
    "Xll": 12,
}

photovoltaics_details["miesi<ice"] = photovoltaics_details["miesi<ice"].str.strip()
photovoltaics_details["miesiace"] = photovoltaics_details["miesi<ice"].map(map_months)
photovoltaics_details = photovoltaics_details.drop("miesi<ice", axis=1)

map_clouds = {"90-100%": "90:100", "60-90%": "60:90", "<60%": "0:60"}

photovoltaics_details["%nieba bez chmur"] = photovoltaics_details["%nieba bez chmur"].map(
    map_clouds
)

photovoltaics_details["low_cloud"] = (
    photovoltaics_details["%nieba bez chmur"].str.split(":").str[0].astype(int)
)
photovoltaics_details["upper_cloud"] = (
    photovoltaics_details["%nieba bez chmur"].str.split(":").str[1].astype(int)
)

photovoltaics_details = photovoltaics_details.drop_duplicates().drop("%nieba bez chmur", axis=1)
# %%
devices_power_details = pd.read_csv("data/raw/j.csv", sep=";")[
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
devices_power_details = devices_power_details[["Dzien", "hour_range", "Srednia moc pobierana"]]

devices_power_details = devices_power_details.drop_duplicates()

# %%
energy_prices = pd.read_csv("data/raw/k.csv", sep=";")
energy_prices["miesiace"] = energy_prices["miesiace"].str.split(",")

hours = energy_prices["Godziny"].str.split(pat="-", expand=True)
hours["hour_from"] = hours[0].str.split(":").str[0].astype(int)
hours["hour_to"] = hours[1].str.split(":").str[0].astype(int)
energy_prices = pd.concat([energy_prices, hours], axis=1)
energy_prices["hour_range"] = energy_prices.apply(
    lambda x: list(range(x["hour_from"], x["hour_to"] + 1)), 1
)
energy_prices = energy_prices.explode("hour_range")
energy_prices = energy_prices.explode("miesiace")
energy_prices = energy_prices[["miesiace", "dzien", "koszt", "przychod", "hour_range"]]

energy_prices = energy_prices.drop_duplicates()
energy_prices["miesiace"] = energy_prices["miesiace"].astype(int)
energy_prices["hour_range"] = energy_prices["hour_range"].astype(int)

# %%
weather = pd.read_csv("data/raw/hour-by-hour-weather-data.csv", sep=";")
weather["date"] = weather["datetime"].str[0:10]
weather["date"] = pd.to_datetime(weather["date"], format="%d.%m.%Y")
weather["hour"] = pd.to_datetime(weather["datetime"]).dt.hour

cloud_map = {
    "haze": 0,
    "light snow": 0,
}
weather = weather.replace({"%nieba bez chmur": cloud_map})
weather = weather.drop(["datetime"], axis=1)


# %%
extremely_powerful_table = date_hour_grid.merge(
    expected_temperatures,
    left_on=["weekday", "hour"],
    right_on=["Dzien", "hour_range"],
    how="inner",
).drop(["weekday", "hour_range"], axis=1)

extremely_powerful_table = extremely_powerful_table.merge(
    photovoltaics_details,
    left_on=["month", "hour"],
    right_on=["miesiace", "hour_range"],
    how="inner",
).drop(["miesiace", "hour_range"], axis=1)

extremely_powerful_table = extremely_powerful_table.merge(
    devices_power_details, left_on=["Dzien", "hour"], right_on=["Dzien", "hour_range"], how="inner"
).drop(["hour_range"], axis=1)

extremely_powerful_table = extremely_powerful_table.merge(
    weather, on=["hour", "date"], how="inner"
)

extremely_powerful_table = extremely_powerful_table.merge(
    energy_prices,
    left_on=["month", "Dzien", "hour"],
    right_on=["miesiace", "dzien", "hour_range"],
    how="inner",
).drop(["miesiace", "dzien", "hour_range"], axis=1)

# %%
# Zachmurzenie
extremely_powerful_table["clouds_actual"] = extremely_powerful_table["%nieba bez chmur"].astype(
    int
)
extremely_powerful_table["low_cloud"] = extremely_powerful_table["low_cloud"].astype(int)
extremely_powerful_table["upper_cloud"] = extremely_powerful_table["upper_cloud"].astype(int)
extremely_powerful_table = extremely_powerful_table.replace(
    {"low_cloud": {0: -1}, "upper_cloud": {100: 101},}
)


extremely_powerful_table = extremely_powerful_table.drop("%nieba bez chmur", axis=1)

extremely_powerful_table = extremely_powerful_table[
    (extremely_powerful_table["clouds_actual"] > extremely_powerful_table["low_cloud"])
    & (extremely_powerful_table["clouds_actual"] <= extremely_powerful_table["upper_cloud"])
]

# %%

extremely_powerful_table["key"] = 1
heating_up_details["key"] = 1

extremely_powerful_table = extremely_powerful_table.merge(heating_up_details, on="key").drop(
    "key", 1
)

# Temperatura
extremely_powerful_table["temperatura"] = extremely_powerful_table["temperatura"].astype(int)
extremely_powerful_table["low_temp"] = extremely_powerful_table["low_temp"].astype(int)
extremely_powerful_table["upper_temp"] = extremely_powerful_table["upper_temp"].astype(int)

extremely_powerful_table = extremely_powerful_table[
    (extremely_powerful_table["temperatura"] > extremely_powerful_table["low_temp"])
    & (extremely_powerful_table["temperatura"] <= extremely_powerful_table["upper_temp"])
]

# %%
extremely_powerful_table = extremely_powerful_table.drop(
    [
        "Temperatura na zewnatrz",
        "low_cloud",
        "upper_cloud",
        "clouds_actual",
        "low_temp",
        "upper_temp",
    ],
    axis=1,
)


extremely_powerful_table = extremely_powerful_table.rename(
    {
        "Dzien": "day_type",
        "Oczekiwana temperatura": "temperature_goal",
        "Moc wytwarzana": "voltaic_energy_in",
        "Srednia moc pobierana": "other_devices_energy_out",
        "temperatura": "outside_temperature",
        "Moc srednia na podtrzymanie (wszystkie Éródla)": "energy_for_temperature_on_stable_level",
        "Podtrzymanie + podniesienie temp. o 1°C w ciagu 1h": "energy_for_1_celsius_heatup",
        "Czas spadku temp o 1°C bez ogrzewania": "time_for_1_celsius_drop",
        "koszt": "buy_energy_cost",
        "przychod": "sell_energy_value",
    },
    axis=1,
)

extremely_powerful_table["other_devices_energy_in"] = (
    extremely_powerful_table["other_devices_energy_out"] * 0.7
)
extremely_powerful_table["temperature_goal"] = extremely_powerful_table["temperature_goal"].astype(
    int
)
extremely_powerful_table["outside_temperature"] = extremely_powerful_table[
    "outside_temperature"
].astype(int)
extremely_powerful_table["hour"] = extremely_powerful_table["hour"].astype(int)
extremely_powerful_table = extremely_powerful_table.reset_index().drop("index", axis=1)
extremely_powerful_table["our_temperature_goal"] = extremely_powerful_table[
    "temperature_goal"
].map({23: 22, 20: 21})
# %%
extremely_powerful_table.to_csv("data/processed/energy_table.csv")

# %%
