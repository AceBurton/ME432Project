import cantera as ct
from cantera import FreeFlame
import numpy as np
import matplotlib.pyplot as plt


# initial conditions
fuel_ratio = 0.5
phi = 1.0         
T0 = 300         
P0 = ct.one_atm  

oxidizer = 'O2:1, N2:3.76'

#Set up flame speed
flame_speeds = []

# Create gas object
gas = ct.Solution('gri30.yaml')
for fuel_ratio in range(0, 110, 10):
    fuel_ratio = fuel_ratio / 100.0  # Convert to a fraction
    fuel_ratio = round(fuel_ratio, 2)  # Round to 2 decimal places
    fuel = f'CH4:{fuel_ratio}, NH3:{1 - fuel_ratio}' #round(1 - fuel_ratio,2)}'
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
    flame_speeds.append(flame.velocity[0])

flame_speeds = np.array(flame_speeds)
fuel_ratio = np.linspace(0, 1, len(flame_speeds))
plt.figure(figsize=(8, 5))
plt.plot(fuel_ratio, flame_speeds, marker='o')
plt.xlabel('CH₄ Mole Fraction in Fuel')
plt.ylabel('Laminar Flame Speed [m/s]')
plt.title(f'Laminar Flame Speed vs Fuel Composition (ϕ = {phi})')
plt.grid(True)
plt.tight_layout()
plt.show()
