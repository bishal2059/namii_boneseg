# 3D Bone Segmentation & Landmark Detection Pipeline

## Overview

This repository provides a robust, modular pipeline to segment femur and tibia from 3D knee CT scans, perform controlled mask expansions, randomize contours within defined limits, detect key tibial anatomical landmarks, and visualize results. 

## Features

* **Bone Segmentation**: Threshold-based extraction (HU ≥ 300) with morphological cleanup and connected-component filtering.
* **Mask Expansion**: Uniform outward dilation by configurable millimeter radii (e.g., 2 mm, 4 mm).
* **Contour Randomization**: Generate randomized masks constrained between original and expanded contours.
* **Landmark Detection**: Identify medial and lateral lowest points on the tibial surface in physical (mm) coordinates.
* **Visualization**: Side-by-side and overlay figures for qualitative assessment.
* **Logging**: Detailed console output of voxel counts and processing steps.

## Repository Layout

```plaintext
├── README.md
├── requirements.txt          # Python dependencies
├── data/                     # Place your input .nii or .nii.gz here
│   └── knee_ct.nii.gz
├── results/                  # Generated outputs
│   ├── masks/                # All segmentation masks (.nii.gz)
│   ├── visualize/            # Comparison & overlay figures (.png)
│   └── landmarks.txt         # Medial/lateral coordinates per mask
└── src/                      # Source code modules
    ├── utils.py              # I/O, spacing, mm-to-voxel conversion
    ├── segmentation.py       # Bone threshold + cleanup
    ├── expansion.py          # mm-based dilation
    ├── randomization.py      # Controlled random contour
    ├── landmarks.py          # Landmark extraction
    ├── visualize.py          # Slice visualizations
    └── main.py               # CLI entrypoint with logging
```

## Setup & Installation

1. **Clone repository**:

   ```bash
   git clone https://github.com/bishal2059/namii_boneseg.git
   cd namii_boneseg
   ```
2. **Create Python environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Create a data folder and place the original nii.gz file:
```
mkdir data
```
Now, copy the original nii.gz file and rename it to: **knee_ct.nii.gz**

### Run the full pipeline via the `main.py` script:

```bash
python -m src.main \
  --input data/knee_ct.nii \
  --output_dir results \
  --threshold 300    # HU threshold for bone segmentation (default: 300)
  --expand1 2.0      # First expansion radius in mm (default: 2.0)
  --expand2 4.0      # Second expansion radius in mm (default: 4.0)
```

## Arguments

* `--input`      : Path to the input CT volume (.nii or .nii.gz).
* `--output_dir` : Directory where all results (masks, figures, landmarks) will be saved.
* `--threshold`  : Hounsfield Unit (HU) threshold for initial bone segmentation.
* `--expand1`    : First mask expansion radius in millimeters.
* `--expand2`    : Second mask expansion radius in millimeters.

## Result Locations

* **`results/masks/`**: Contains binary NIfTI masks for:

  * `original_mask.nii.gz`
  * `expanded_2mm.nii.gz`
  * `expanded_4mm.nii.gz`
  * `randomized_mask1.nii.gz`, `randomized_mask2.nii.gz`

* **`results/landmarks.txt`**: Lists medial and lateral lowest point coordinates for each mask.

* **`results/visualize/`**: Store the visualization of each masks. For futher visualization refer below.


### Direct Visualization

You can also visualize masks by using **`overlay_visualize.py`**:

```bash
python src/overlay_visualize.py
```

By default, it reads:

* CT: `data/knee_ct.nii`
* Masks: `results/masks/combined_mask.nii.gz`, `expanded_2mm.nii.gz`, `expanded_4mm.nii.gz`, `random1.nii.gz`, `random2.nii.gz`
* Outputs to `results/visualize/`:

  1. `original_slice_<idx>.png` (CT)
  2. `overlay_1_combined_mask.png`, ..., `overlay_5_random2.png` (mask overlays)
  3. `side_by_side_comparison_<idx>.png` (Combined vs 2mm vs 4mm)

## Extensibility

* **Thresholding**: Adjust HU threshold in `segmentation.py` or via `--threshold` flag.
* **Mask Radii**: Modify `--expand1` and `--expand2` for different dilation scales.
* **Randomization**: Tweak behavior in `randomization.py` to control spatial variation.
* **Visualization**: Extend `visualize.py` or `overlay_visualize.py` for multi-slice or volume rendering.


## Contact

For questions or issues, please open a GitHub issue or contact `bishal.sap21@gmail.com`.
