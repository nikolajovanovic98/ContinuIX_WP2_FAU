#!/opt/anaconda3/envs/igm/bin/python

# 17.07.2025 by Nikola Jovanovic

# --------------------------------------------#
#                                             #
#               IMPORT MODULES                # 
#                                             #
# --------------------------------------------#

import sys 
import numpy as np 
import shapefile

# python env
print(sys.executable)

# --------------------------------------------#
#                                             #
#               INPUT FIELDS                  # 
#                                             #
# --------------------------------------------#

input_name  = sys.argv[1]
output_name = sys.argv[2]

# --------------------------------------------#
#                                             #
#                MAIN PROGRAM                 # 
#                                             #
# --------------------------------------------#

# load shapefile
sf = shapefile.Reader(f"{input_name}")

# check shape type

if not sf.shapeType == shapefile.POLYGON:
    sys.exit("Shapefile not a polygon!")
else:
    print("Length of shapefile: ", len(sf))

# attributes + geometries (fid + DN)
shapeRecs = sf.shapeRecords()

# group collections of points into shapes
print("Shapefile parts: ", shapeRecs[-2].shape.parts)
parts_len = len(shapeRecs[-2].shape.parts)

# exit if no holes
if parts_len == 1: 
    sys.exit("No holes!")

# get the total number of points
[ni, nj] = np.shape(shapeRecs[-2].shape.points)

# init coord and id fields 
xx = np.zeros(ni)
yy = np.zeros(ni)
tags = np.zeros(ni)

for ii in range(ni):

    xx[ii] = shapeRecs[-2].shape.points[ii][0]
    yy[ii] = shapeRecs[-2].shape.points[ii][1]

# init id
id = 1

# fill id for holes
for part in range(parts_len):

    # get current index
    curr_idx = shapeRecs[-2].shape.parts[part]

    # get next index
    # for the last one index out of range
    if not part == parts_len - 1:
        next_idx = shapeRecs[-2].shape.parts[part+1]

    # last loop
    if part == parts_len-1:
        #print(shapeRecs[-2].shape.points[curr_idx:])
        for jj in range(curr_idx, ni):
            tags[jj] = int(id)

    # other loops
    else:
        #print(shapeRecs[-2].shape.points[curr_idx:next_idx])
        for jj in range(curr_idx, next_idx):
            tags[jj] = int(id)

    id += 1

full_array = np.column_stack((xx, yy, tags))

np.savetxt(f"{output_name}.csv", X=full_array, delimiter=',')