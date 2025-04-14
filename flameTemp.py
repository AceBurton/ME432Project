import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.yaml')
gas1 = ct.Solution('gri30.yaml')

#we can play with these
#fuel_ratio = 0.5  # 0 = 100% NH3, 1 = 100% CH4
gas_temp = 300
air_ratio = 1.0

temp = []
for fuel_ratio in range(0, 110, 10):
    fuel_ratio = fuel_ratio / 100.0  # Convert to a fraction
    fuel_ratio = round(fuel_ratio, 2)  # Round to 2 decimal places
    fuel = f'CH4:{fuel_ratio}, NH3:{1 - fuel_ratio}' #round(1 - fuel_ratio,2)}'
    air = 'O2:1, N2:3.76'
    gas.TP = gas_temp, ct.one_atm

    gas.set_equivalence_ratio(phi = air_ratio, fuel = fuel, oxidizer = air)
    gas.equilibrate('HP')

    print(f"Adiabatic flame temperature: {gas.T:.2f} K")
    temp.append(gas.T)

temp = np.array(temp)
fuel_ratio = np.linspace(0, 1, len(temp))
plt.figure(figsize=(8, 5))
plt.plot(fuel_ratio, temp, marker='o',color='red')
plt.xlabel('CH₄ Mole Fraction in Fuel')
plt.ylabel('Adiabatice Flame Temperature [K]')
plt.title(f'Adiabatic Flame Temperature vs Fuel Composition (ϕ = {air_ratio})')
plt.grid(True)
plt.tight_layout()

plt.show()

