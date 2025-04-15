import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.yaml')

#we can play with these
gas_temp = 300
air_ratio = 1.0

NO = []
NO2 = []
N2O = []
NH3 = []

for fuel_ratio in range(0, 110, 10):
    fuel_ratio = fuel_ratio / 100.0  # Convert to a fraction
    fuel_ratio = round(fuel_ratio, 2)  # Round to 2 decimal places
    fuel = f'CH4:{fuel_ratio}, NH3:{1 - fuel_ratio}' #round(1 - fuel_ratio,2)}'    air = 'O2:1, N2:3.76'
    air = 'O2:1, N2:3.76'

    gas.set_equivalence_ratio(phi = air_ratio, fuel = fuel, oxidizer = air)
    gas.TP = gas_temp, ct.one_atm

    gas.equilibrate('HP')
    NO.append(gas.X[gas.species_index('NO')])
    NO2.append(gas.X[gas.species_index('NO2')])
    N2O.append(gas.X[gas.species_index('N2O')])
    NH3.append(gas.X[gas.species_index('NH3')])

NO = np.array(NO)
NO2 = np.array(NO2)
N2O = np.array(N2O)
NH3 = np.array(NH3)
fuel_ratio = np.linspace(0, 1, len(NO))


plt.figure(figsize=(8, 5))

plt.plot(fuel_ratio, NO,   marker='o', label='NO')
plt.plot(fuel_ratio, NO2,  marker='s', label='NO₂')
plt.plot(fuel_ratio, N2O,  marker='^', label='N₂O')
plt.plot(fuel_ratio, NH3,  marker='x', label='NH₃')

plt.xlabel('CH₄ Mole Fraction in Fuel')
plt.ylabel('Mole Fraction')
plt.title('Species vs CH₄ Fuel Fraction')
plt.yscale('log')  # optional, makes small NOₓ values easier to see
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

