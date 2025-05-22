import os
import matplotlib.pyplot as plt
from src.utils import load_nifti


def visualize_slices(mask_paths, output_dir, slice_index=None):
    vols = [load_nifti(p)[0] for p in mask_paths]
    if slice_index is None:
        slice_index = vols[0].shape[2] // 2
    n = len(vols)
    fig, axes = plt.subplots(1, n, figsize=(4*n, 4))
    for i, v in enumerate(vols):
        axes[i].imshow(v[:, :, slice_index].T, cmap='gray', origin='lower')
        axes[i].set_title(os.path.basename(mask_paths[i]).split('.nii')[0])
        axes[i].axis('off')
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f'compare_slice_{slice_index}.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)