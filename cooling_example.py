import bamboo as bam
import bamboo.cooling as cool
import example_config as ex
import matplotlib.pyplot as plt
import numpy as np

'''Plots'''
# engine_geometry.plot_geometry()
ex.cooled_engine.show_gas_mach()

'''Run the cooling system simulation'''
cooling_data = ex.cooled_engine.run_heating_analysis(
    number_of_points=ex.points, h_gas_model="bartz 2")

'''Plot the results'''
# Nozzle shape
shape_x = np.linspace(ex.engine_geometry.x_min, ex.engine_geometry.x_max, ex.points)
shape_y = np.zeros(len(shape_x))

for i in range(len(shape_x)):
    shape_y[i] = ex.engine_geometry.y(shape_x[i])

# Temperatures
fig, ax_T = plt.subplots()
ax_T.plot(
    cooling_data["x"],
    cooling_data["T_wall_inner"] -
    273.15,
    label="Wall (Inner)")
ax_T.plot(
    cooling_data["x"],
    cooling_data["T_wall_outer"] -
    273.15,
    label="Wall (Outer)")
ax_T.plot(
    cooling_data["x"],
    cooling_data["T_coolant"] -
    273.15,
    label="Coolant")
#ax_T.plot(cooling_data["x"], cooling_data["T_gas"], label = "Exhaust gas")
if cooling_data["boil_off_position"] is not None:
    ax_T.axvline(
        cooling_data["boil_off_position"],
        color='red',
        linestyle='--',
        label="Coolant boil-off")

ax_T.grid()
ax_T.set_xlabel("Position ($m$)")
ax_T.set_ylabel("Temperature ($^\\circ C$)")
ax_T.legend()

#ax_shape = ax_T.twinx()
#ax_shape.plot(shape_x, shape_y, color="blue", label = "Engine contour")
#ax_shape.plot(shape_x, -shape_y, color="blue")
# ax_shape.set_aspect('equal')
#ax_shape.legend(loc = "lower left")

# Heat transfer coefficients and heat transfer rates
h_figs, h_axs = plt.subplots()
h_axs.plot(cooling_data["x"], cooling_data["h_gas"], label="h_gas")
h_axs.plot(cooling_data["x"], cooling_data["h_coolant"], label="h_coolant", )
h_axs.grid()
if cooling_data["boil_off_position"] is not None:
    h_axs.axvline(
        cooling_data["boil_off_position"],
        color='red',
        linestyle='--',
        label="Coolant boil-off")

h_axs.set_xlabel("Position ($m$)")
h_axs.set_ylabel("Heat transfer coefficicent ($W/m^2K$)")

h_axs.legend()
plt.show()
