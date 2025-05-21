import numpy as np
from scipy.ndimage import binary_dilation
from src.utils import mm_to_voxel


def expand_mask(mask, spacing, radius_mm):
    """
    Expands binary mask outward by radius_mm using voxel-based dilation.
    """
    # Convert mm to voxel structuring element radius
    rx, ry, rz = mm_to_voxel(spacing, radius_mm)
    # Create spherical structuring element
    grid = np.ogrid[-rx:rx+1, -ry:ry+1, -rz:rz+1]
    se = (grid[0]**2/rx**2 + grid[1]**2/ry**2 + grid[2]**2/rz**2) <= 1
    expanded = binary_dilation(mask, structure=se)
    return expanded.astype(np.uint8)