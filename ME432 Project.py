import cantera as ct
import matplotlib.pyplot as plt

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.yaml')

#we can play with these
#fuel_ratio = 0.5  # 0 = 100% NH3, 1 = 100% CH4
gas_temp = 300
air_ratio = 1.0
fig, ax = plt.subplots()


for fuel_ratio in range(0, 100, 1):
    fuel_ratio = fuel_ratio / 100.0  # Convert to a fraction
    fuel = f'CH4:{fuel_ratio}, NH3:{1 - fuel_ratio}'
    air = 'O2:2, N2:7.52'
    gas.TP = gas_temp, ct.one_atm

    gas.set_equivalence_ratio(phi = air_ratio, fuel = fuel, oxidizer = air)

    gas.equilibrate('HP')


    #print(f"Fuel mixture: {fuel}")
    #print(f"Adiabatic flame temperature: {gas.T:.2f} K")
    ax.plot([fuel_ratio], [gas.T], 'ro')

plt.show()

