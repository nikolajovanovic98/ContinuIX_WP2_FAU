# 2-steady

-------------------------------------------------------------------------------
## Purpose
-------------------------------------------------------------------------------

Runs the "steady state" simulation for Aletsch given SMB forcing (here, $\mathrm{ELA} = 2800$ m). $110$ years needed for the glacier to equilibrate $(\mathrm{dh}/\mathrm{dt} \approx 0$  $mathrm{m}\mathrm{y}^{-1})$.  

-------------------------------------------------------------------------------
## Contents
-------------------------------------------------------------------------------

| File | Description |
|------|-------------|
| `steady_climate_Stokes.sif` | `SIF` file used to run the steady state simulation|
| `Extrusion.sif` | `SIF` file specifying extrusion details |
| `BCs` | A directory containing two options for basal sliding: `noslip.sif` for the no-slip BC or `slip_linear.sif` for a linear relationship between basal shear stress and basal velocity.
| `linsys` | A directory containing `SIF` files for different linear system solvers (here, `BiCGStab.sif`).

-------------------------------------------------------------------------------
## Workflow
-------------------------------------------------------------------------------

Run the steady state pipeline:

```bash
# Copy the mesh directory
cp -r 1-dem/inv-shp . 
```
```
# Serial simulation
ElmerSolver steady_climate_Stokes.sif

# Parallel simulation
mpirun -np 16 ElmerSolver steady_climate_Stokes.sif
```
-------------------------------------------------------------------------------
## Outputs
-------------------------------------------------------------------------------

The most important files generated with this workflow will be located in the `inv-shp` directory, copied from `1-dem` directory earlier:

- `aletsch_steady_state.result*` files, used for restart in the next step. 

This directory needs to be copied further to run ELA experiments. 

-------------------------------------------------------------------------------
## Notes
-------------------------------------------------------------------------------

- Changing the `$namerun` variable will result in a different name for the `.result` file. Here, we use `aletsch_steady_state`. 
- Check the VTU output to make sure velocity and thickness fields look plausible.
