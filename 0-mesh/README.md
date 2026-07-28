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
| `1_get_mask_oggm.sh` | Script can be used to obtain Aletsch ice mask from `OGGM_shop` via `IGM` |
| `2_mask2shp.py` | Generate a .shp containing all geometries (nunataks, main outline, ...) |
| `3_shp2csv.py` | Convert `.shp` into `.csv` to generate a `.geo` file || `4_csv2geo.py` | Generate a `.geo` file from the `.csv` file (written by Claude) |
| `coords.csv` | Example `.csv` file |
| `icemask_lv95` | Aletsch ice mask used in this study |
| `params.json` | `.json` file generated for IGM | 

-------------------------------------------------------------------------------
## Workflow
-------------------------------------------------------------------------------

Run the mesh generation pipeline:

```bash
. 1_get_mask_oggm.sh
```
(specify ...)

In QGIS, run `2_mask2shp.py` via Python plug-in. Save the `.shp` file `0-mesh` directory. 

```bash
python 3_shp2csv.py test.shp test.csv
```

```bash
python 4_csv2geo
```

Then

```bash
gmsh -1 -2 "${MESH}.geo" -o "${MESH}.msh"

# Generate serial mesh and a VTU flie
ElmerGrid 14 2 "${MESH}.msh" -autoclean 
ElmerGrid 14 5 "${MESH}.msh" -autoclean

# Generate partitioned mesh 
ElmerGrid 2 2 "${MESH}" -metis 16 0 
```
-------------------------------------------------------------------------------
## Outputs
-------------------------------------------------------------------------------

The most important files generated with this workflow are located in the `inv-shp` directory:

- `mesh.boundary`, `mesh.elements`, `mesh.header`, and `mesh.nodes` if the user wishes to run simulations in serial
- `partitioning.16` directory, if run in parallel 

This directory needs to be copied further for mesh extrusion. 

-------------------------------------------------------------------------------
## Notes
-------------------------------------------------------------------------------

- Check mesh quality before moving to the next step (e.g., if nunataks are well represented). 
