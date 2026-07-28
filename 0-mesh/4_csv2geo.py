import numpy as np 
import sys 
from shapely.geometry import LinearRing, Polygon

print(sys.executable)

output_file = 'test.geo'
lc = 100.0
min_hole_area = lc * lc * 4
simplify_tolerance = 50.0    # metres — removes staircase redundancy
smooth_iterations  = 5       # chaikin smoothing iterations

file = np.loadtxt('test.csv', delimiter=',')
xx = file[:,0].copy()
yy = file[:,1].copy()
id = file[:,2]

nTot = len(xx)

# ---- FIND SEGMENT BOUNDARIES ----
segments = []
seg_start = 0
for ii in range(1, nTot):
    if id[ii] != id[ii-1]:
        segments.append((seg_start, ii-1))
        seg_start = ii
segments.append((seg_start, nTot-1))

print('CONTOUR FACTSHEET -----------------------------------')
print('--> number of points     : \t\t'+str(nTot))    
print('--> number of contours   : \t\t'+str(len(segments)))

# ---- FIX ORIENTATION ----
for seg_idx, (s, e) in enumerate(segments):
    pts = list(zip(xx[s:e+1], yy[s:e+1]))
    ring = LinearRing(pts)
    if not ring.is_simple:
        print(f"WARNING: Contour {seg_idx} (id={id[s]:.0f}) is self-intersecting!")
    if seg_idx == 0:
        if not ring.is_ccw:
            print(f"Reversing outer boundary (contour {seg_idx})")
            xx[s:e+1] = xx[s:e+1][::-1]
            yy[s:e+1] = yy[s:e+1][::-1]
    else:
        if ring.is_ccw:
            print(f"Reversing hole (contour {seg_idx})")
            xx[s:e+1] = xx[s:e+1][::-1]
            yy[s:e+1] = yy[s:e+1][::-1]

# ---- REMOVE DUPLICATE CLOSING POINT ----
cleaned_segments = []
for seg_idx, (s, e) in enumerate(segments):
    dist = np.sqrt((xx[e]-xx[s])**2 + (yy[e]-yy[s])**2)
    cleaned_segments.append((s, e-1) if dist < 1e-6 else (s, e))
segments = cleaned_segments

# ---- CHAIKIN SMOOTHING FUNCTION ----
def chaikin(pts, iterations=5):
    """Chaikin corner cutting algorithm for smooth curves."""
    pts = np.array(pts)
    for _ in range(iterations):
        new_pts = []
        n = len(pts)
        for i in range(n):
            p0 = pts[i]
            p1 = pts[(i+1) % n]
            new_pts.append(0.75*p0 + 0.25*p1)
            new_pts.append(0.25*p0 + 0.75*p1)
        pts = np.array(new_pts)
    return pts

# ---- SMOOTH + SIMPLIFY CONTOURS, REBUILD ARRAYS ----
print("\n=== Smoothing contours ===")
new_xx   = []
new_yy   = []
new_id   = []
new_segs = []

for seg_idx, (s, e) in enumerate(segments):
    pts = list(zip(xx[s:e+1], yy[s:e+1]))
    orig_n = len(pts)
    
    # step 1: simplify to remove staircase redundancy
    ring = LinearRing(pts)
    simplified = ring.simplify(tolerance=simplify_tolerance, preserve_topology=True)
    simplified_pts = list(simplified.coords)[:-1]  # drop closing duplicate
    
    # step 2: chaikin smoothing (skip for very small contours)
    if len(simplified_pts) > 6:
        smoothed_pts = chaikin(simplified_pts, iterations=smooth_iterations)
    else:
        smoothed_pts = np.array(simplified_pts)
    
    print(f"Contour {seg_idx} (id={id[s]:.0f}): {orig_n} -> {len(simplified_pts)} -> {len(smoothed_pts)} pts")
    
    seg_start_new = len(new_xx)
    for px, py in smoothed_pts:
        new_xx.append(px)
        new_yy.append(py)
        new_id.append(id[s])
    seg_end_new = len(new_xx) - 1
    new_segs.append((seg_start_new, seg_end_new))

xx       = np.array(new_xx)
yy       = np.array(new_yy)
id       = np.array(new_id)
segments = new_segs
nTot     = len(xx)

print(f'\n--> total points after smoothing: {nTot}')

# ---- FILTER NUNATAKS ----
outer_pts = list(zip(xx[segments[0][0]:segments[0][1]+1],
                     yy[segments[0][0]:segments[0][1]+1]))
outer_poly = Polygon(outer_pts).buffer(-100)

valid_segments = [segments[0]]
n_total_holes = len(segments) - 1
n_dropped_outside = 0
n_dropped_toosmall = 0

for seg_idx, (s, e) in enumerate(segments[1:], 1):
    pts = list(zip(xx[s:e+1], yy[s:e+1]))
    hole_poly = Polygon(pts)
    area = hole_poly.area
    if not outer_poly.contains(hole_poly):
        print(f"Dropping hole {seg_idx:3d} (id={id[s]:3.0f}) - outside boundary (area={area:.0f}m²)")
        n_dropped_outside += 1
    elif area < min_hole_area:
        print(f"Dropping hole {seg_idx:3d} (id={id[s]:3.0f}) - too small (area={area:.0f}m² < {min_hole_area:.0f}m²)")
        n_dropped_toosmall += 1
    else:
        valid_segments.append((s, e))
        print(f"Keeping  hole {seg_idx:3d} (id={id[s]:3.0f}) area={area:.0f}m²")

segments = valid_segments
print(f"\n--> kept    : {len(segments)-1} / {n_total_holes} holes")
print(f"--> dropped : {n_dropped_outside} outside boundary, {n_dropped_toosmall} too small")

# ---- PRINT FINAL PHYSICAL CURVE MAPPING ----
print("\n=== Final Physical Curve mapping ===")
for ci, (s, e) in enumerate(segments):
    print(f"Physical Curve {ci+1} -> original id={id[s]:.0f}, {e-s+1} pts")

# ---- BUILD POINT INDEX REMAPPING ----
kept_point_indices = []
for (s, e) in segments:
    kept_point_indices.extend(range(s, e+1))

old_to_new = {}
for new_idx, old_idx in enumerate(kept_point_indices):
    old_to_new[old_idx] = new_idx + 1  # 1-based

# ---- DIAGNOSTIC: check curve loop closure ----
print("\n=== Checking curve loop closure ===")
all_ok = True
for seg_idx, (s, e) in enumerate(segments):
    if old_to_new[s] == old_to_new[e]:
        print(f"WARNING: Contour {seg_idx} (id={id[s]:.0f}) has first==last point!")
        all_ok = False
if all_ok:
    print("All curve loops OK.")

# ---- OPEN OUTPUT FILE ----
geo = open(output_file, 'w')
geo.write('// Geo file created using contourtogeo_niki.py \n')
geo.write('Mesh.Algorithm = 5; \n')
geo.write(f'lc = {lc} ; \n')
geo.write('Mesh.ToleranceEdgeLength = 1e-3; \n')
geo.write('Mesh.CharacteristicLengthFromCurvature = 0; \n')
geo.write('Mesh.CharacteristicLengthFromPoints = 1; \n')
geo.write('Mesh.CharacteristicLengthExtendFromBoundary = 0; \n')
geo.write('Field[1] = MathEval; \n')
geo.write('Field[1].F = Sprintf("%g",lc); \n')
geo.write('Background Field = 1; \n\n')

# ---- POINTS ----
for new_idx, old_idx in enumerate(kept_point_indices):
    geo.write("Point(%i) = {%18.16e, %18.16e, 0.0, %9.4f}; \n"
              % (new_idx+1, xx[old_idx], yy[old_idx], lc))

geo.write('\n')

# ---- SPLINES (all contours, points already smoothed) ----
line_counter = 0
curve_loops  = []

for seg_idx, (s, e) in enumerate(segments):
    n_pts = e - s + 1
    loop_lines = []

    if n_pts > 4:
        # single spline per contour — points already smoothed so no overshoot
        pt_indices = [old_to_new[s + i] for i in range(n_pts)]
        pt_indices.append(old_to_new[s])  # close back to first point
        pts_str = ', '.join(map(str, pt_indices))
        line_counter += 1
        geo.write("Spline(%i) = {%s}; \n" % (line_counter, pts_str))
        loop_lines.append(line_counter)
    else:
        # tiny contours: straight lines
        for i in range(n_pts):
            p1 = old_to_new[s + i]
            p2 = old_to_new[s + (i+1) % n_pts]
            line_counter += 1
            geo.write("Line(%i) = {%i, %i}; \n" % (line_counter, p1, p2))
            loop_lines.append(line_counter)

    curve_loops.append(loop_lines)

geo.write('\n')

# ---- CURVE LOOPS ----
for ci, loop in enumerate(curve_loops):
    lines_str = ', '.join(map(str, loop))
    geo.write("Curve Loop(%i) = {%s}; \n" % (ci+1, lines_str))

geo.write('\n')

# ---- PLANE SURFACE ----
hole_ids = ', '.join(str(i+2) for i in range(len(curve_loops)-1))
if hole_ids:
    geo.write(f"Plane Surface(1) = {{1, {hole_ids}}}; \n\n")
else:
    geo.write("Plane Surface(1) = {1}; \n\n")

# ---- PHYSICAL GROUPS ----
for ci, loop in enumerate(curve_loops):
    lines_str = ', '.join(map(str, loop))
    geo.write("Physical Curve(%i) = {%s}; \n" % (ci+1, lines_str))

geo.write("Physical Surface(1) = {1}; \n")

geo.close()
print(f'\nDone: {output_file}')
