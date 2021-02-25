import bamboo as bam
import example_config as ex
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
import numpy as np

'''Run the stress analysis, using cooling simulation data'''
cooling_data = ex.cooled_engine.run_heating_analysis(number_of_points = 4000, h_gas_model = "bartz 2")
stress_data = ex.cooled_engine.run_stress_analysis(cooling_data, ex.wall_material)
max_stress = np.amax(stress_data["thermal_stress"])

'''Get nozzle data'''
shape_x = np.linspace(ex.engine_geometry.x_min, ex.engine_geometry.x_max, 4000)
shape_y = np.zeros(len(shape_x))

for i in range(len(shape_x)):
    shape_y[i] = ex.engine_geometry.y(shape_x[i])

'''Plot results'''
fig2, ax_s = plt.subplots()

points1 = np.array([shape_x, shape_y]).T.reshape(-1, 1, 2)
points2 = np.array([shape_x, -shape_y]).T.reshape(-1, 1, 2)
segments1 = np.concatenate([points1[:-1], points1[1:]], axis=1)
segments2 = np.concatenate([points2[:-1], points2[1:]], axis=1)
# Each element in segments represents a point definining a coloured line segment

if max_stress < ex.wall_material.sigma_y:
    mid = 1.0
    red_max = 0.0
    norm_max = ex.wall_material.sigma_y
else:
    mid = ex.wall_material.sigma_y/max_stress
    norm_max = max_stress
    red_max = 1.0
# Check if yield is reached to adjust colour mapping, normalisation
   
cdict = {"red":  [(0.0, 0.0, 0.0),
                  (mid, 0.0, 0.0),
                  (1.0, red_max, red_max)],  
    
        "green": [(0.0, 1.0, 1.0),
                  (mid/2, 0.0, 0.0),
                  (1.0, 0.0, 0.0)],
         
        "blue":  [(0.0, 0.0, 0.0),
                  (mid/2, 0.0, 0.0),
                  (mid, 1.0, 1.0),
                  (1.0, 0.0, 0.0)]}
colours = LinearSegmentedColormap("colours", cdict)
# Set up colour map for stress values

norm = plt.Normalize(np.amin(stress_data["thermal_stress"]), norm_max)
# Normalise the stress data so it can be mapped

lc1 = LineCollection(segments1, cmap=colours, norm=norm)
lc1.set_array(stress_data["thermal_stress"])
lc1.set_linewidth(20)
lc2 = LineCollection(segments2, cmap=colours, norm=norm)
lc2.set_array(stress_data["thermal_stress"])
lc2.set_linewidth(20)
# Create line collections defined by segments arrays, map colours

line1 = ax_s.add_collection(lc1)
line2 = ax_s.add_collection(lc2)

cbar = fig2.colorbar(line1, ax=ax_s)
#cbar = fig2.colorbar(line1, ax=ax_s, ticks=[int(ex.wall_material.sigma_y)])
#cbar.set_ticklabels(["$\sigma_y$"])

ax_s.set_xlim(shape_x.min(), shape_x.max())
ax_s.set_ylim(-shape_y.max(), shape_y.max())

max_stress_index = np.where(stress_data["thermal_stress"] == max_stress)
ax_s.axvline(shape_x[max_stress_index], color = 'red', linestyle = '--',
             label = "Max stress {:.1f} MPa, {:.1f}% of $\sigma_y$ ({:.1f} MPa)".format(
             max_stress/10**6, 100*max_stress/ex.wall_material.sigma_y,
             ex.wall_material.sigma_y/10**6))
# Show where the maximum stress in the liner is

plt.gca().set_aspect('equal', adjustable='box')
# Equal axes scales for a true view of the engine
ax_s.legend()
plt.show()