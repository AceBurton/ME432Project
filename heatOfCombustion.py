import cantera as ct
from cantera import FreeFlame
import matplotlib.pyplot as plt
from cantera import FreeFlame
import numpy as np

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.yaml')
gas_temp = 300

#we can play with these
phis = [0.9, 1.0, 1.1]  # equivalence ratios
fuel_ratios = np.linspace(0, 1, 11)  # CH4 fraction from 0 to 1

heat = {phi: [] for phi in phis}
for phi in phis:
    for fr in fuel_ratios:
        fuel = f'CH4:{fr}, NH3:{1 - fr}' #round(1 - fuel_ratio,2)}'
        air = 'O2:1, N2:3.76'
        gas.TP = gas_temp, ct.one_atm

        h_initial = gas.enthalpy_mass

        gas.set_equivalence_ratio(phi = phi, fuel = fuel, oxidizer = air)
        gas.equilibrate('TP')

        h_final = gas.enthalpy_mass
        delta_h = (h_final - h_initial)/1e6

        heat[phi].append(h_final)


fig, axs = plt.subplots(figsize=(8, 10))

phi_styles = {
    0.9: {'marker': 'o', 'color': 'blue'},
    1.0: {'marker': 's', 'color': 'red'},
    1.1: {'marker': 'x', 'color': 'green'}
}


for phi, style in phi_styles.items():
    axs.plot(fuel_ratios, heat[phi], label=f'ϕ={phi}', **style)
    axs.legend()
    plt.xlabel('CH₄ Mole Fraction in Fuel')
    plt.ylabel('Heat of Combustion [MJ/kg]')
    plt.title(f'Heat of Combustion vs Fuel Composition')
    plt.grid(True)
    plt.tight_layout()
    #axs.set_yscale('log')

plt.show()


