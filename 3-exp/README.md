# 3-exp

-------------------------------------------------------------------------------
## Purpose
-------------------------------------------------------------------------------

Runs eleven experiments with ELA values ranging from $2900$ to $3100$ in $20\,\mathrm{m}$ increments. All simulations last $10$ years.    

-------------------------------------------------------------------------------
## Contents
-------------------------------------------------------------------------------

| File | Description |
|------|-------------|
| `ela_exp_Stokes.sif` | `SIF` file used to run ELA experiments |
| `Extrusion.sif` | `SIF` file specifying extrusion details |
| `BCs` | A directory containing two options for basal sliding: `noslip.sif` for the no-slip BC or `slip_linear.sif` for a linear relationship between basal shear stress and basal velocity.
| `linsys` | A directory containing `SIF` files for different linear system solvers (here, `BiCGStab.sif`).

-------------------------------------------------------------------------------
## Workflow
-------------------------------------------------------------------------------

Run the steady state pipeline:

```bash
# Copy the mesh directory (here, we change the name of the working directory to the appropriate ELA experiment)
cp -r 2-steady/inv-shp 2900 
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

The most important files generated with this workflow will be located in the `2900` directory:

- `aletsch_2900.nc` file, containing the necessary outputs. 

-------------------------------------------------------------------------------
## Notes
-------------------------------------------------------------------------------

- Change `$namerun` variable in the `SIF` file to the appropriate ELA experiment (here, `2900`)  
- Change the `SMBELA` value in `../Parameters/Physical_Parameters.IN` to appropriate ELA value. 
