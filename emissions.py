import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Settings
phis = [0.9, 1.0, 1.1]  # equivalence ratios
fuel_ratios = np.linspace(0, 1, 11)  # CH4 fraction from 0 to 1
NO = 'NO'
NO2 = 'NO2'
N2O = 'N2O'
NH3 = 'NH3'

# Store NO results for each phi
NO_results = {phi: [] for phi in phis}
NO2_results = {phi: [] for phi in phis}
N2O_results = {phi: [] for phi in phis}
NH3_results = {phi: [] for phi in phis}

for phi in phis:
    for fr in fuel_ratios:
        try:
            # Define fuel and oxidizer
            fuel = f'CH4:{fr}, NH3:{1 - fr}'
            oxidizer = 'O2:1, N2:3.76'
            
            # Set up gas and conditions
            gas = ct.Solution('gri30.yaml')
            gas.set_equivalence_ratio(phi=phi, fuel=fuel, oxidizer=oxidizer)
            gas.TP = 300, ct.one_atm
            
            # Equilibrate at constant pressure and enthalpy (adiabatic)
            gas.equilibrate('HP')

            # Get NO mole fraction
            if NO in gas.species_names:
                x_NO = gas.X[gas.species_index(NO)]
            else:
                x_NO = 0.0
            
            if NO2 in gas.species_names:
                x_NO2 = gas.X[gas.species_index(NO2)]
            else:
                x_NO2 = 0.0

            if N2O in gas.species_names:
                x_N2O = gas.X[gas.species_index(N2O)]
            else:
                x_N2O = 0.0

            if NH3 in gas.species_names:
                x_NH3 = gas.X[gas.species_index(NH3)]
            else:
                x_NH3 = 0.0

            NO_results[phi].append(x_NO)
            NO2_results[phi].append(x_NO2)
            N2O_results[phi].append(x_N2O)
            NH3_results[phi].append(x_NH3)

        except Exception as e:
            print(f"Failed at phi={phi}, CH4 fraction={fr:.2f}: {e}")
            NO_results[phi].append(np.nan)
            NO2_results[phi].append(np.nan)
            N2O_results[phi].append(np.nan)
            NH3_results[phi].append(np.nan)


# --- Plotting ---

fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)

phi_styles = {
    0.9: {'marker': 'o', 'color': 'blue'},
    1.0: {'marker': 's', 'color': 'red'},
    1.1: {'marker': 'x', 'color': 'green'}
}

species_results = [NO_results, NO2_results, N2O_results, NH3_results]
species_labels = ['NO', 'NO₂', 'N₂O', 'NH₃']

for ax, species, label in zip(axs, species_results, species_labels):
    for phi, style in phi_styles.items():
        ax.plot(fuel_ratios, species[phi], label=f'ϕ={phi}', **style)
    ax.set_ylabel(label)
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True)

axs[-1].set_xlabel('Fuel Ratio')
plt.tight_layout()
plt.show()