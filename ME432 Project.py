import cantera as ct

#Ace Burton, burtona25@up.edu
#Adin Sokol, sokol25@up.edu

gas = ct.Solution('gri30.cti')
#air = ct.Solution('gri30.cti')

#we can play with these
fuel_ratio = 0.5
gas_temp = 300
air_ratio = 1.0

ammonia_ratio = 1-fuel_ratio
fuel = 'CH4:fuel_ratio, NH3:ammonia_ratio'
air = 'O2:1, N2:3.76'
gas.TP = gas_temp, ct.one_atm

gas.set_equivalence_ratio(air_ratio, fuel, air)

gas.equilibrate('HP')

print(f"Adiabatic flame temperature: {gas.T:.1f} K")

#test commit from local repo