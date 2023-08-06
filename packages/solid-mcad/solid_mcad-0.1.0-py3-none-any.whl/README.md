# `solid-mcad`: OpenSCAD's MCAD utility library in SolidPython

[OpenSCAD](https://www.openscad.org/) is 'The Programmers Solid 3D CAD Modeller'. 

[SolidPython](https://github.com/SolidCode/SolidPython) translates Python code into OpenSCAD so you can design 3D objects in your Python. 

[MCAD](https://github.com/OpenSCAD/MCAD) is a great general-purpose utility library written in OpenSCAD, with modules for [gears](FIXME: add), [motors](FIXME: add), [3D text](FIXME: add), and more. 

[SolidMCAD](https://github.com/etjones/SolidMCAD) bridges the gap and makes pythonic, namespaced imports of the MCAD libraries easy in SolidPython.

# Installation: On PyPI
`pip install solid-mcad`

# Usage:

* Show all SolidMCAD packages (Each corresponds to a .scad file in the MCAD library)
``` python
import solid_mcad
print(dir(solid_mcad))
```

* In an IPython REPL, show method signatures for imported MCAD code:

```python
In [1]: from solid_mcad import involute_gears      
In [2]: involute_gears.bevel_gear?                                                                            # Response:
# Init signature: involute_gears.bevel_gear(number_of_teeth=None, cone_distance=None, face_width=None, outside_circular_pitch=None, pressure_angle=None, clearance=None, bore_diameter=None, gear_thickness=None, backlash=None, involute_facets=None, finish=None, **kwargs)
# Docstring:      <no docstring>
# Type:           type
```                                                                      

* Import a particular package and use it in SolidPython
```python
import solid
from solid_mcad import involute_gears
gears = involute_gears.test_bevel_gear_pairs()
solid.scad_render_to_file(gears, './bevel_gears.scad')  
# Outputs scad file to ./bevel_gears.scad
```

