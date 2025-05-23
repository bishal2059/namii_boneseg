import os
import matplotlib.pyplot as plt
import nibabel as nib


def save_original_slice(ct_path, output_dir, slice_index=None):
    """
    Save the original CT middle axial slice as an image.
    """
    ct_img = nib.load(ct_path)
    ct_vol = ct_img.get_fdata()

    if slice_index is None:
        slice_index = ct_vol.shape[2] // 2

    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(ct_vol[:, :, slice_index].T, cmap='gray', origin='lower')
    ax.set_title(f"Original CT Slice {slice_index}", fontsize=14)
    ax.axis('off')
    out_path = os.path.join(output_dir, f"original_slice_{slice_index}.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[Saved] {out_path}")


def overlay_each_mask(ct_path, mask_paths, output_dir, slice_index=None, alpha=0.4):
    """
    Overlay each mask separately and save with index and title.
    """
    ct_img = nib.load(ct_path)
    ct_vol = ct_img.get_fdata()

    if slice_index is None:
        slice_index = ct_vol.shape[2] // 2

    os.makedirs(output_dir, exist_ok=True)
    for idx, mask_path in enumerate(mask_paths, start=1):
        mask_vol = nib.load(mask_path).get_fdata().astype(bool)
        fig, ax = plt.subplots(figsize=(6,6))
        ax.imshow(ct_vol[:, :, slice_index].T, cmap='gray', origin='lower')
        ax.contour(
            mask_vol[:, :, slice_index].T,
            levels=[0.5], colors=['r'], linewidths=2, alpha=alpha
        )
        mask_name = os.path.basename(mask_path).split('.nii')[0]
        ax.set_title(f"{idx}. Overlay of {mask_name} on slice {slice_index}", fontsize=12)
        ax.axis('off')
        out_path = os.path.join(output_dir, f"overlay_{idx}_{mask_name}.png")
        plt.savefig(out_path, bbox_inches='tight')
        plt.close(fig)
        print(f"[Saved] {out_path}")


def overlay_comparison(ct_path, combined_path, exp2_path, exp4_path, output_dir, slice_index=None, alpha=0.4):
    """
    Create side-by-side comparison of combined, 2mm, and 4mm overlays on the CT slice.
    """
    ct_img = nib.load(ct_path)
    ct_vol = ct_img.get_fdata()
    masks = {
        'Combined': nib.load(combined_path).get_fdata().astype(bool),
        'Expanded 2mm': nib.load(exp2_path).get_fdata().astype(bool),
        'Expanded 4mm': nib.load(exp4_path).get_fdata().astype(bool)
    }

    if slice_index is None:
        slice_index = ct_vol.shape[2] // 2

    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for ax, (title, mask_vol) in zip(axes, masks.items()):
        ax.imshow(ct_vol[:, :, slice_index].T, cmap='gray', origin='lower')
        ax.contour(
            mask_vol[:, :, slice_index].T,
            levels=[0.5], colors=['r'], linewidths=2, alpha=alpha
        )
        ax.set_title(f"{title} on slice {slice_index}", fontsize=12)
        ax.axis('off')

    out_path = os.path.join(output_dir, f"side_by_side_comparison_{slice_index}.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[Saved] {out_path}")


if __name__ == '__main__':
    # Example usage
    ct_file = 'data/knee_ct.nii.gz'
    masks = [
        'results/masks/combined_mask.nii.gz',
        'results/masks/expanded_2mm.nii.gz',
        'results/masks/expanded_4mm.nii.gz',
        'results/masks/random1.nii.gz',
        'results/masks/random2.nii.gz'
        ]
    output_folder = 'sample_output_visualize'
    # Save original slice
    save_original_slice(ct_file, output_folder)
    # Save individual overlays
    overlay_each_mask(ct_file, masks, output_folder)
    # Save side-by-side comparison
    overlay_comparison(ct_file, masks[0], masks[1], masks[2], output_folder)