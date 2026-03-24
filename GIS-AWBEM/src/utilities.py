import numpy as np
from sympy import Plane, Polygon , Point3D, Point2D

def distance(p1,p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    d = np.sqrt(dx**2 + dy**2 + dz**2)
    return d

def P2A(point):
    # Point3D to numpy array
    return np.array(point).astype(float)

def Centroid(points):
    CPx = np.mean(points[:,0])
    CPy = np.mean(points[:,1])
    CPz = np.mean(points[:,2])
    CP = np.array([CPx, CPy, CPz])
    return CP


def get_polygon_orientaion(vertices: np.ndarray) -> str:
    """
    Determines polygon winding order from an (N,2) NumPy array.

    Returns:
        'CCW'        Counter-clockwise
        'CW'         Clockwise
        'DEGENERATE' Collinear / zero area
    """
    vertices = np.asarray(vertices, dtype=np.float64)

    if vertices.ndim != 2 or vertices.shape[1] != 2:
        raise ValueError("Input must be an (N,2) array.")

    if len(vertices) < 3:
        raise ValueError("At least three vertices are required.")

    x = vertices[:, 0]
    y = vertices[:, 1]

    # Roll arrays to compute next-vertex pairs
    x_next = np.roll(x, -1)
    y_next = np.roll(y, -1)

    # Shoelace signed area (vectorized)
    area2 = np.sum((x_next - x) * (y_next + y))

    if area2 < 0:
        return "CCW"
    elif area2 > 0:
        return "CW"
    else:
        return "DEGENERATE"


# wall_vertices = wall_dict['Wall_1']
def generate_window_vertices(wall_vertices, WWR):
    
    # assumptions:
    #     aspect ratio of wall and window are equal
    #     center points of wall and window are the same
    #     vertices are already sorted
    

    if wall_vertices[0,2] == wall_vertices[1,2]:
        L_hor = distance(wall_vertices[0], wall_vertices[1])
        L_ver = distance(wall_vertices[0], wall_vertices[-1])
    else:
        L_ver = distance(wall_vertices[0], wall_vertices[1])
        L_hor = distance(wall_vertices[0], wall_vertices[-1])

    
    # angle between the wall and the xz plane
    xz_plane = Plane(Point3D(0,0,0), Point3D(1,0,0), Point3D(0,0,1))
    pp1 = Plane(Point3D(wall_vertices[0]), Point3D(wall_vertices[1]), Point3D(wall_vertices[2]))
    theta = float(pp1.angle_between(xz_plane)) # radian
    pi_rad = np.pi 
    if theta > pi_rad/2: theta = pi_rad - theta
    
    
    # Center vertice
    CP = Centroid(wall_vertices)
    
    # Move the points: relative (to the origin) vertices
    ver_rel = wall_vertices - CP
    
    
    # rotation around z axis. x-axis will be coplanar. y-axis will be normal vector
    r = np.sqrt(ver_rel[:,0]**2 + ver_rel[:,1]**2)
    X_vert_rotated = r * np.sign(ver_rel[:,0])
    Y_vert_rotated = np.zeros((ver_rel[:,1].shape[0]))
    Z_vert_rotated = ver_rel[:,-1]
    Vert_rotated = np.array((X_vert_rotated, Y_vert_rotated, Z_vert_rotated)).T

    # assumption: length to width (aspec) ratio of wall and window are equal
    window_Z = L_ver * np.sqrt(WWR)
    window_X = window_Z * L_hor/L_ver
    
    # window vertices
    verts = np.array((window_X/2, 0, window_Z/2)) * np.ones(Vert_rotated.shape)
    window_vertices_rotated = np.sign(Vert_rotated) * verts

    # rotate back (around z axis)   
    rw = np.sqrt(window_vertices_rotated[:,0]**2 + window_vertices_rotated[:,1]**2)
    window_vertices_X = rw * np.cos(theta)
    window_vertices_Y = rw * np.sin(theta)
    window_vertices_Z = window_vertices_rotated[:,-1]
    window_vertices_rotated_back = np.array([np.sign(ver_rel[:,0])*window_vertices_X, np.sign(ver_rel[:,1])*window_vertices_Y, window_vertices_Z]).T
    
    # Move the vertices back
    window_vertices = window_vertices_rotated_back + CP

    return window_vertices



def sort_CCW_wall(points, floor):
    """
    Sort a vertical wall polygon counter-clockwise (CCW) such that its normal
    points outward of the building footprint defined by `floor`.

    Parameters
    ----------
    points : (N,3) array-like
        Coplanar convex wall vertices (usually 4 for LOD1).
    floor : (M,3) array-like
        Building footprint polygon.

    Returns
    -------
    (N,3) ndarray
        CCW-ordered wall vertices with outward facing normal.
    """

    # Convert to numpy arrays
    P = np.asarray(points, dtype=float)
    F = np.asarray(floor, dtype=float)

    # Find the wall centroid
    CP = P.mean(axis=0)

    # Find two non-collinear points
    v1 = P[1] - P[0]
    for i in range(2, len(P)):
        v2 = P[i] - P[0]
        if np.linalg.norm(np.cross(v1, v2)) > 1e-8:
            break

    wall_plane = Plane(Point3D(CP), Point3D(P[0]), Point3D(P[i]))
    n = np.array(wall_plane.normal_vector, dtype=float)
    n /= np.linalg.norm(n)

    # ---- Build local 2D coordinate frame ----
    # Choose u axis inside the wall plane
    u = P[0] - CP
    u -= u.dot(n) * n
    u /= np.linalg.norm(u)

    # v axis orthogonal in plane
    v = np.cross(n, u)

    # Project vertices into wall local coordinates
    rel = P - CP
    x = rel @ u
    y = rel @ v

    # Angular sort
    angles = np.arctan2(y, x)
    order = np.argsort(angles)
    sorted_P = P[order]

    # Determine outward direction using floor footprint
    floor_poly = Polygon(*[Point2D(pt[0], pt[1]) for pt in F])

    # Artificial point slightly in wall normal direction
    eps = 0.01
    probe = CP + eps * n

    # Project probe onto floor plane (XY)
    probe_xy = Point2D(probe[0], probe[1])

    # If probe is inside footprint, normal is inward → reverse
    if floor_poly.encloses_point(probe_xy):
        sorted_P = sorted_P[::-1]

    return sorted_P

