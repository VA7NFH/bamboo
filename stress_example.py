import bamboo as bam
import example_config as ex
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
import numpy as np

'''Run the stress analysis, using cooling simulation data'''
cooling_data = ex.cooled_engine.run_heating_analysis(number_of_points = 1000, h_gas_model = "bartz 2")
stress_data = ex.cooled_engine.run_stress_analysis(cooling_data, ex.wall_material)

'''Get nozzle data'''
shape_x = np.linspace(ex.engine_geometry.x_min, ex.engine_geometry.x_max, 1000)
shape_y = np.zeros(len(shape_x))

for i in range(len(shape_x)):
    shape_y[i] = ex.engine_geometry.y(shape_x[i])

'''Plot results'''
fig2, ax_s = plt.subplots()
points = np.array([shape_x, stress_data["thermal_stress"]]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

if np.amax(stress_data["thermal_stress"]) < ex.wall_material.sigma_y:
    mid = 1.0
    red_max = 0
    norm_max = ex.wall_material.sigma_y
else:
    mid = wall_material.sigma_y/np.amax(stress_data["thermal_stress"])
    norm_max = np.amax(stress_data["thermal_stress"])
    red_max = 1
   
cdict = {"red":  [(0.0, 0.0, 0.0),
                  (mid, 0.0, 0.0),
                  (1.0, red_max, red_max)],  
    
        "green": [(0.0, 1.0, 1.0),
                  (mid/2, 0.0, 0.0),
                  (1.0, 0.0, 0.0)],
         
        "blue":  [(0.0, 0.0, 0.0),
                  (mid/2, 0.0, 0.0),
                  (mid, 1.0, 1.0),
                  (1.0, 0.0, 0.0)]
        }
colours = LinearSegmentedColormap("colours", cdict)

norm = plt.Normalize(np.amin(stress_data["thermal_stress"]), norm_max)
lc = LineCollection(segments, cmap=colours, norm=norm)
lc.set_array(stress_data["thermal_stress"])
lc.set_linewidth(2)
line = ax_s.add_collection(lc)
fig2.colorbar(line, ax=ax_s)

ax_s.set_xlim(shape_x.min(), shape_x.max())
ax_s.set_ylim(stress_data["thermal_stress"].min(), stress_data["thermal_stress"].max())
plt.show()