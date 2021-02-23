'''
Subscripts:
    0 - Stagnation condition
    c - Chamber condition (should be the same as stagnation conditions)
    t - At the throat
    e - At the nozzle exit plane
    amb - Atmopsheric/ambient condition
'''

import example_config as ex
import bamboo as bam

molecular_weight = 21.627   #Molecular weight of the exhaust gas (kg/kmol) (only used to calculate R, and hence cp)

'''Create the engine object'''
perfect_gas = bam.PerfectGas(gamma = ex.gamma, molecular_weight = molecular_weight)
chamber = bam.ChamberConditions(ex.pc, ex.Tc, ex.mdot)
nozzle = bam.Nozzle.from_engine_components(perfect_gas, chamber, ex.p_amb, type = "rao", length_fraction = 0.8)
white_dwarf = bam.Engine(perfect_gas, chamber, nozzle)

print(nozzle)
nozzle.plot_nozzle()
print(f"Sea level thrust = {white_dwarf.thrust(1e5)/1000} kN")
print(f"Sea level Isp = {white_dwarf.isp(1e5)} s")

#Estimate apogee based on apprpoximate Martlet 4 vehicle mass and cross sectional area
apogee_estimate = bam.estimate_apogee(dry_mass = 60, 
                                      propellant_mass = 50, 
                                      engine = white_dwarf, 
                                      cross_sectional_area = 0.03, 
                                      show_plot = False)

print(f"Apogee estimate = {apogee_estimate/1000} km")

#Run an optimisation program to change the nozzle area ratio, to maximise the apogee obtained (I'm not sure if this is working correctly right now).
white_dwarf.optimise_for_apogee(dry_mass = 60, propellant_mass = 50, cross_sectional_area = 0.03)

print(white_dwarf.nozzle)
