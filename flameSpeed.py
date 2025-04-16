import cantera as ct
from cantera import FreeFlame
import numpy as np
import matplotlib.pyplot as plt


# initial conditions
phi = 1.0         
T0 = 300         
P0 = ct.one_atm  

oxidizer = 'O2:1, N2:3.76'

#Set up flame speed

# Create gas object
gas = ct.Solution('gri30.yaml')

phis = [0.9, 1.0, 1.1]  # equivalence ratios
fuel_ratios = np.linspace(0, 1, 11)  # CH4 fraction from 0 to 1
flame_speeds = {phi: [] for phi in phis}

for phi in phis:
    for fr in fuel_ratios:
        
        fuel = f'CH4:{fr}, NH3:{1 - fr}' #round(1 - fuel_ratio,2)}'
        #air = 'O2:1, N2:3.76'
        gas.set_equivalence_ratio(phi, fuel=fuel, oxidizer=oxidizer)
        gas.TP = T0, P0

    # Set up the flame object (domain width in meters)
        width = 0.08  # 8 cm
        flame = FreeFlame(gas, width=width)

    # Set refinement criteria (can be adjusted)
        flame.set_refine_criteria(ratio=3.0, slope=0.06, curve=0.12)

    # Solve flame
        flame.solve(loglevel=0, auto=True)

    # Output laminar flame speed
        print(f"Laminar flame speed: {flame.velocity[0]:.3f} m/s")
        flame_speeds[phi].append(flame.velocity[0])

fig, axs = plt.subplots(figsize=(8, 10))

phi_styles = {
    0.9: {'marker': 'o', 'color': 'blue'},
    1.0: {'marker': 's', 'color': 'red'},
    1.1: {'marker': 'x', 'color': 'green'}
}


for phi, style in phi_styles.items():
    axs.plot(fuel_ratios, flame_speeds[phi], label=f'ϕ={phi}', **style)
    axs.legend()
    plt.xlabel('CH₄ Mole Fraction in Fuel')
    plt.ylabel('Laminar Flame Speed [m/s]')
    plt.title(f'Laminar Flame Speed vs Fuel Composition')
    plt.grid(True)
    plt.tight_layout()
    #axs.set_yscale('log')

plt.show()
