import cantera as ct
from cantera import FreeFlame
import matplotlib.pyplot as plt
from cantera import FreeFlame
import numpy as np

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.yaml')

#we can play with these
gas_temp = 300
air_ratio = 1.0

heat = []
for fuel_ratio in range(0, 110, 10):
    fuel_ratio = fuel_ratio / 100.0  # Convert to a fraction
    fuel_ratio = round(fuel_ratio, 2)  # Round to 2 decimal places
    fuel = f'CH4:{fuel_ratio}, NH3:{1 - fuel_ratio}' #round(1 - fuel_ratio,2)}'
    air = 'O2:1, N2:3.76'
    gas.TP = gas_temp, ct.one_atm

    h_initial = gas.enthalpy_mass

    gas.set_equivalence_ratio(phi = air_ratio, fuel = fuel, oxidizer = air)
    gas.equilibrate('TP')

    h_final = gas.enthalpy_mass
    delta_h = (h_final - h_initial)/1e6

    heat.append(h_final)

heat = np.array(heat)
print(heat)
fuel_ratio = np.linspace(0, 1, len(heat))
plt.figure(figsize=(8, 5))
plt.plot(fuel_ratio, heat, marker='o',color='green')
plt.xlabel('CH₄ Mole Fraction in Fuel')
plt.ylabel('Heat of Combustion [MJ/kg]')
plt.title(f'Heat of Combustion vs Fuel Composition (ϕ = {air_ratio})')
plt.grid(True)
plt.tight_layout()

plt.show()

