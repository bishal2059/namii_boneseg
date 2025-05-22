import numpy as np


def find_lowest_medial_lateral(mask, affine):
    zs, ys, xs = np.where(mask)
    if xs.size == 0:
        return None, None
    pts = np.vstack((xs, ys, zs, np.ones_like(xs)))
    world = (affine @ pts)[:3]
    X, Y, Z = world
    mid_x = np.median(X)
    med_idx = np.argmin(Z[X <= mid_x])
    lat_idx = np.argmin(Z[X > mid_x])
    med_pt = (X[X<=mid_x][med_idx], Y[X<=mid_x][med_idx], Z[X<=mid_x][med_idx])
    lat_pt = (X[X>mid_x][lat_idx], Y[X>mid_x][lat_idx], Z[X>mid_x][lat_idx])
    return med_pt, lat_pt