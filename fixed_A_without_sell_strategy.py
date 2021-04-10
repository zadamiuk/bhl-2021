#%%
import pandas as pd

df = pd.read_csv('data/processed/energy_table.csv')
df = df.sort_values(by=['date','hour'])
df = df.reset_index().drop('index', axis=1)
df

# %%

# Parameters
COOLING_HOURS_AHEAD_THRESHOLD = 3
RECUPERATION_RATE = 0.8
SELL_ENERGY_PRICE_THRESHOLD = 2
BUY_ENERGY_PRICE_TRESHOLD = 1 
BUY_ENERGY_BARGAIN_PRICE_TRESHOLD = 0.5
# Accumulator
accumulator_level = 0
accumulator_capacity = 7
accumulator_charge_speed = 1
accumulator_supply_speed = 2

# House
house_temperature = 21
current_energy_strategy = "A"
hours_left_until_cooled = -1
next_house_temperature = house_temperature
total_income = 0
total_cost = 0

for index, row in df.iloc[:-3].iterrows():
    print(f'Hour: {index}')
    energy_supply = 0
    energy_demand = 0
    heat_demand = 0
    heat_supply = 0
    income = 0
    cost = 0
    #############   DEMAND  #############################
    # Woda
    if row.hour == 6 or row.hour == 18:
        energy_demand += 6

    energy_demand += row.other_devices_energy_out

    # Grzanie podlogi
    if row.outside_temperature <= 20:
        if df.iloc[[index + 1]].our_temperature_goal.values[0] > house_temperature: 
            heat_demand += row.energy_for_1_celsius_heatup
            next_house_temperature += 1
            print('Zwiekszamy temperature')
        elif df.iloc[[index + COOLING_HOURS_AHEAD_THRESHOLD]].our_temperature_goal.values[0] < house_temperature or hours_left_until_cooled != -1:
            if hours_left_until_cooled == -1:
                hours_left_until_cooled = row.time_for_1_celsius_drop - 1
                print(f'Zaczynamy chlodzic, pozostalo {hours_left_until_cooled} godzin chlodzenia')
            elif hours_left_until_cooled == 0:
                next_house_temperature -= 1
                hours_left_until_cooled = -1
                print('Dom zostal schlodzony. Zero potrzeb.')            
            else:
                hours_left_until_cooled -= 1
                print(f'Dalej chlodzic, pozostalo {hours_left_until_cooled} godzin chlodzenia')
        elif df.iloc[[index + 1]].our_temperature_goal.values[0] == house_temperature:
            heat_demand += row.energy_for_temperature_on_stable_level
            print('Utrzymujemy temperature')
    else:
        print("Otwieramy okna")
        next_house_temperature = row.outside_temperature
    
    energy_supply += RECUPERATION_RATE * heat_demand
    heat_demand -= row.other_devices_energy_in
    energy_demand += heat_demand
    
    ######## SUPPLY #################
    energy_supply += row.voltaic_energy_in

    # MAGIC TREE ALGORITHM
    overflow = energy_supply - energy_demand

    if overflow < 0:
        cost += abs(overflow) * row.buy_energy_cost
        
    house_temperature = next_house_temperature
    total_cost += cost
    print(f'Acc_level {accumulator_level}')
    print(f'Cost {cost}')
    print(f'Total cost {total_cost}')
df
# %%

# %%
