import os
import argparse
from src.utils import load_nifti, save_nifti, get_spacing
from src.segmentation import segment_bone
from src.expansion import expand_mask
from src.randomization import randomize_mask
from src.landmarks import find_lowest_medial_lateral
from src.visualize import visualize_slices


def parse_args():
    parser = argparse.ArgumentParser(
        description="3D Bone Segmentation & Landmark Detection Pipeline"
    )
    parser.add_argument('--input', required=True, help='Path to input CT NIfTI file')
    parser.add_argument('--output_dir', required=True, help='Directory for saving results')
    parser.add_argument('--threshold', type=int, default=300, help='HU threshold for segmentation')
    parser.add_argument('--expand1', type=float, default=2.0, help='First expansion radius mm')
    parser.add_argument('--expand2', type=float, default=4.0, help='Second expansion radius mm')
    return parser.parse_args()


def main():
    args = parse_args()
    print("\n=== 3D Bone Segmentation & Landmark Detection ===")
    print(f"Input CT: {args.input}")
    print(f"Output folder: {args.output_dir}\n")

    mask_dir = os.path.join(args.output_dir, 'masks')
    vis_dir = os.path.join(args.output_dir, 'visualize')
    os.makedirs(mask_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)

    print("[Step 1] Loading CT volume...")
    vol, affine, hdr = load_nifti(args.input)
    spacing = get_spacing(hdr)
    print(f"  - Volume shape: {vol.shape}, spacing: {spacing}\n")

    print(f"[Step 2] Segmenting bone (threshold >= {args.threshold} HU)...")
    combined = segment_bone(vol, threshold_hu=args.threshold)
    print(f"  - Voxels in combined mask: {combined.sum()}")
    combined_path = os.path.join(mask_dir, 'combined_mask.nii.gz')
    save_nifti(combined, affine, hdr, combined_path)
    print(f"  - Saved combined mask: {combined_path}\n")

    print(f"[Step 3] Expanding mask by {args.expand1} mm...")
    exp2 = expand_mask(combined, spacing, args.expand1)
    print(f"  - Voxels after expansion: {exp2.sum()}")
    exp2_path = os.path.join(mask_dir, 'expanded_2mm.nii.gz')
    save_nifti(exp2, affine, hdr, exp2_path)
    print(f"  - Saved expanded mask: {exp2_path}\n")

    print(f"[Step 4] Expanding mask by {args.expand2} mm...")
    exp4 = expand_mask(combined, spacing, args.expand2)
    print(f"  - Voxels after expansion: {exp4.sum()}")
    exp4_path = os.path.join(mask_dir, 'expanded_4mm.nii.gz')
    save_nifti(exp4, affine, hdr, exp4_path)
    print(f"  - Saved expanded mask: {exp4_path}\n")

    print(f"[Step 5] Randomizing mask within {args.expand1} mm...")
    rnd1 = randomize_mask(combined, exp2, spacing, args.expand1)
    print(f"  - Voxels in randomized mask: {rnd1.sum()}")
    rnd1_path = os.path.join(mask_dir, 'random1.nii.gz')
    save_nifti(rnd1, affine, hdr, rnd1_path)
    print(f"  - Saved randomized mask: {rnd1_path}\n")

    print(f"[Step 6] Randomizing mask within {args.expand2} mm...")
    rnd2 = randomize_mask(combined, exp4, spacing, args.expand2)
    print(f"  - Voxels in randomized mask: {rnd2.sum()}")
    rnd2_path = os.path.join(mask_dir, 'random2.nii.gz')
    save_nifti(rnd2, affine, hdr, rnd2_path)
    print(f"  - Saved randomized mask: {rnd2_path}\n")

    print("[Step 7] Detecting landmarks...")
    landmarks_file = os.path.join(args.output_dir, 'landmarks.txt')
    masks = ['combined_mask','expanded_2mm','expanded_4mm','random1','random2']
    with open(os.path.join(args.output_dir,'landmarks.txt'),'w') as f:
        for name in masks:
            m, _, _ = load_nifti(os.path.join(args.output_dir,'masks',f"{name}.nii.gz"))
            med, lat = find_lowest_medial_lateral(m, affine)
            f.write(f"{name} \n, medial: {med},\n lateral: {lat}\n")
    print(f"  - Saved landmarks: {landmarks_file}\n")

    print("[Step 8] Visualizing comparisons...")
    visualize_slices([combined_path, exp2_path, exp4_path, rnd1_path, rnd2_path], vis_dir)
    print(f"  - Saved comparison figure to {vis_dir}\n")

    print("=== Pipeline complete! ===\n")

if __name__ == '__main__':
    main()  