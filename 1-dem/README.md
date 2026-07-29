# 1-dem

-------------------------------------------------------------------------------
## Purpose
-------------------------------------------------------------------------------

Generates a Digital Elevation Model (DEM) for Aletsch given topography data.

-------------------------------------------------------------------------------
## Contents
-------------------------------------------------------------------------------

| File | Description |
|------|-------------|
| `initialise_DEM.sif` | `SIF` file used to generate the DEM |
| `Extrusion.sif` | `SIF` file specifying extrusion details |
| `aletsch_topography.nc` | `NetCDF` file containing surface and bedrock topography data (IGM inversion results from Marin Kneib) 

-------------------------------------------------------------------------------
## Workflow
-------------------------------------------------------------------------------

Run the extrusion pipeline:

```bash
# Copy the mesh directory
cp -r 0-mesh/inv-shp . 
```
```
# Serial simulation
ElmerSolver initialise_DEM.sif

# Parallel simulation
mpirun -np 16 ElmerSolver initialise_DEM.sif 
```
-------------------------------------------------------------------------------
## Outputs
-------------------------------------------------------------------------------

The most important files generated with this workflow will be located in the `inv-shp` directory:

- `.result*` files, used for restart in the next step. 

This directory needs to be copied further for mesh extrusion. 

-------------------------------------------------------------------------------
## Notes
-------------------------------------------------------------------------------

- Check that Aletsch ice mask and topography data projections align.
- Check that the mesh isn't faulty/corrupted.
