import numpy as np
import SimpleITK as sitk
from skimage import morphology, measure
from scipy.ndimage import binary_dilation


def segment_bone(volume, threshold_hu=300):
    """
    Segment femur + tibia in one binary mask.
    Args:
        volume: 3D numpy array in Hounsfield Units
        threshold_hu: HU threshold (default 300)
    Returns:
        combined: binary numpy mask
    """
    # Threshold
    mask = volume >= threshold_hu

    # Remove small objects and fill holes
    mask = morphology.remove_small_objects(mask, min_size=1000)
    mask = morphology.remove_small_holes(mask, area_threshold=1000)

    # Dilate to connect broken parts
    struct = morphology.ball(1)
    mask = binary_dilation(mask, structure=struct)

    # Label connected components
    labels = measure.label(mask)
    props = measure.regionprops(labels)
    # Keep two largest
    props = sorted(props, key=lambda p: p.area, reverse=True)[:2]
    out = np.zeros_like(mask, dtype=np.uint8)
    for p in props:
        out[labels == p.label] = 1
    return out