# 0-mesh

-------------------------------------------------------------------------------
## Purpose
-------------------------------------------------------------------------------

Generate the computational mesh used for the simulations.

This directory contains scripts for converting glacier geometry data into a
computational mesh suitable for Elmer/Ice simulations.


-------------------------------------------------------------------------------
## Contents
-------------------------------------------------------------------------------

| File | Description |
|------|-------------|
| `3-get_mesh.sh` | Main mesh generation script |
| `Claude_splines.py` | Generate spline-based geometries |
| `Contour2geo.py` | Convert contour data into geometry format |


-------------------------------------------------------------------------------
## Inputs
-------------------------------------------------------------------------------

Required input files:

- Glacier outlines / contour data
- Surface and bed geometry information
- Configuration parameters


-------------------------------------------------------------------------------
## Workflow
-------------------------------------------------------------------------------

Run the mesh generation pipeline:

```bash
./3-get_mesh.sh
```


-------------------------------------------------------------------------------
## Outputs
-------------------------------------------------------------------------------

Generated files include:

- Computational mesh
- Geometry files
- Mesh conversion files


-------------------------------------------------------------------------------
## Notes
-------------------------------------------------------------------------------

- Check mesh quality before running simulations.
- Generated mesh files may be excluded from version control.
