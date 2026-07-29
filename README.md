# Working Group on Continuity approaches for mass balance Intercomparsion eXercise (ContinuIX) (2025-2029)

This work is part of WP2 of the ContinuIX project. We use the finite-element ice-flow model ElmerIce to perform eleven transient simulations of Aletsch Glacier under different surface mass balance (SMB) forcings, spanning equilibrium line altitudes (ELAs) from 2900 to 3100 m a.s.l. in 20 m increments. The resulting output is used to evaluate model SMB uncertainty against available observations.

For more information, visit the project website: <https://cryosphericsciences.org/activities/continuity-approaches-for-mass-balance-intercomparison-exercise-continuix/>.

-------------------------------------------------------------------------------
## Requirements
-------------------------------------------------------------------------------

The following software was used in code development:

| Software | Version | Purpose |
|----------|---------|---------|
| Elmer/Ice | v9.0 | Ice-flow simulations |
| IGM | v2.2.2 | Glacier evolution model required to obtain Aletsch ice mask file via `OGGM_shop` |
| Python | v3.10.15 | Mesh generation, IGM dependencies |
| Gmsh | v4.8.4 | Mesh generation |
| MPI | v4.1.2 | Parallel Elmer/Ice simulations |

-------------------------------------------------------------------------------

## Project Workflow

Details for each step found in the corresponding directories.

-------------------------------------------------------------------------------
0-mesh — Mesh Generation
-------------------------------------------------------------------------------

Generate the computational mesh and convert the glacier geometry into an
Elmer-compatible mesh.

-------------------------------------------------------------------------------
1-dem — DEM Preprocessing
-------------------------------------------------------------------------------

Prepare the digital elevation model.

-------------------------------------------------------------------------------
2-steady — Steady-State Simulation
-------------------------------------------------------------------------------

Run the steady-state simulation used to initialise the subsequent
experiments.

-------------------------------------------------------------------------------
3-exp — ELA Experiments
-------------------------------------------------------------------------------

Run simulations for different ELA values (Here, eleven experiments with values between $2900$ and $3100$ in $20$ m increments.

-------------------------------------------------------------------------------
SRC
-------------------------------------------------------------------------------

Contains custom source code and plugins used during the simulations.

Contents:
- `SyntSMB.F90` - This solver generates an SMB forcing given ELA. Written by Olivier Gagliardini. 
- `SyntSMB_grad.F90` - This solver generates an SMB forcing given ELA and creates a horizontal gradient in the SMB field. Adapted from Olivier Gagliardini and updated by Nikola Jovanovic.
- `Compute2DNodalGradient.F90` - This solver computes the nodal gradient used to avoid accumulation on steep slopes. 

**Note**: Prior to running any simulations, one needs to compile the `.F90` files. For example:

```bash
elmerf90 SyntSMB.F90 -o SyntSMB.so
```

-------------------------------------------------------------------------------
Parameters
-------------------------------------------------------------------------------

Contains `Physical_Parameters.IN` file with appropriate values for Aletsch. Here, the user needs to specify the value for `ELA` for the appropriate experiment. 
