import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.yaml')

#we can play with these
#fuel_ratio = 0.5  # 0 = 100% NH3, 1 = 100% CH4
gas_temp = 300

phis = [0.9, 1.0, 1.1]  # equivalence ratios
fuel_ratios = np.linspace(0, 1, 11)  # CH4 fraction from 0 to 1

temp = {phi: [] for phi in phis}
for phi in phis:
    for fr in fuel_ratios:
        fuel = f'CH4:{fr}, NH3:{1 - fr}' #round(1 - fuel_ratio,2)}'
        oxidizer = 'O2:1, N2:3.76'
            
        gas = ct.Solution('gri30.yaml')

        gas.set_equivalence_ratio(phi=phi, fuel=fuel, oxidizer=oxidizer)
        gas.equilibrate('HP')

        temp[phi].append(gas.T)

fig, axs = plt.subplots(figsize=(8, 10))

phi_styles = {
    0.9: {'marker': 'o', 'color': 'blue'},
    1.0: {'marker': 's', 'color': 'red'},
    1.1: {'marker': 'x', 'color': 'green'}
}


for phi, style in phi_styles.items():
    axs.plot(fuel_ratios, temp[phi], label=f'ϕ={phi}', **style)
    axs.legend()
    plt.xlabel('CH₄ Mole Fraction in Fuel')
    plt.ylabel('Adiabatic Flame Temperature [K]')
    plt.title(f'Adiabatic Flame Temperature vs Fuel Composition')
    plt.grid(True)
    plt.tight_layout()
plt.show()

