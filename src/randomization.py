import numpy as np
from scipy.ndimage import distance_transform_edt


def randomize_mask(original, expanded, spacing, max_radius_mm):
    """
    Randomly shrink-expanded mask between original and expanded limits.
    """
    # Compute Euclidean distance (in mm) from each voxel to original mask
    inv = 1 - original
    dist_mm = distance_transform_edt(inv, sampling=spacing)
    # Clamp to max_radius_mm
    dist_mm = np.minimum(dist_mm, max_radius_mm)
    # Sample per-voxel threshold
    rnd = np.random.rand(*dist_mm.shape) * max_radius_mm
    mask = dist_mm >= rnd
    mask = np.logical_and(mask, expanded)
    mask = np.logical_or(mask, original)
    return mask.astype(np.uint8)